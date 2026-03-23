"""Render pipeline entry points for Cardiff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from cardiff.contract.models import RenderRequest

from .directives import (
    CARDIFF_QR_FILENAME,
    resolve_qr_directives,
    resolve_qr_directives_deterministic,
    substitute_qr_directives,
)
from .models import (
    NormalizedRenderEvidence,
    RenderFailureClass,
    RenderResult,
    RenderStatus,
    RenderingError,
)
from .templates import resolve_asset_paths, resolve_template
from .tex import BaseTeXAdapter, get_default_tex_adapter

PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")


def render_request_to_pdf(
    render_request: RenderRequest,
    output_path: str | Path,
    *,
    template_root: str | Path | None = None,
    approved_asset_roots: tuple[str | Path, ...] | None = None,
    tex_adapter: BaseTeXAdapter | None = None,
) -> RenderResult:
    """Render one accepted request to a PDF artifact."""

    adapter = tex_adapter or get_default_tex_adapter()
    output = Path(output_path)
    template_id = render_request.template.template_id
    try:
        resolved_template = resolve_template(
            render_request.template,
            template_root=template_root,
        )
        resolved_assets = resolve_asset_paths(
            render_request,
            resolved_template,
            approved_asset_roots=approved_asset_roots,
        )
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise RenderingError(
                RenderFailureClass.RENDER_OUTPUT_INVALID,
                f"failed to prepare output directory '{output.parent.as_posix()}': {error}",
            ) from error

        placeholder_values = _build_placeholder_values(render_request, resolved_assets)
        template_source = resolved_template.entrypoint_path.read_text(encoding="utf-8")
        tex_source = _render_template_source(template_source, placeholder_values)

        include_qr = bool(render_request.template.options.get("include_qr", False))
        rendered_tex = tex_source
        evidence_tex = tex_source

        if adapter.deterministic:
            rendered_tex = resolve_qr_directives_deterministic(
                tex_source,
                include_qr=include_qr,
            )
            evidence_tex = rendered_tex
        else:
            evidence_tex = substitute_qr_directives(
                tex_source,
                include_qr=include_qr,
                qr_tex_path=CARDIFF_QR_FILENAME,
            )
            if include_qr:
                qr_work_dir = output.parent / ".cardiff-qr"
                qr_filename = f"{output.stem}-cardiff-qr.png"
                try:
                    qr_work_dir.mkdir(parents=True, exist_ok=True)
                    rendered_tex = resolve_qr_directives(
                        tex_source,
                        render_request.identity,
                        include_qr=True,
                        work_dir=qr_work_dir,
                        qr_filename=qr_filename,
                    )
                except Exception as error:
                    raise RenderingError(
                        RenderFailureClass.TEX_COMPILE_FAILED,
                        f"failed to prepare QR directive assets: {error}",
                    ) from error
            else:
                rendered_tex = evidence_tex

        preview_lines = _build_preview_lines(render_request, resolved_assets)
        compile_artifact = adapter.compile(
            rendered_tex,
            output,
            page_size_pt=(
                resolved_template.descriptor.page_width_pt,
                resolved_template.descriptor.page_height_pt,
            ),
            preview_lines=preview_lines,
            title=resolved_template.descriptor.display_name,
        )
        if (
            not compile_artifact.output_path.exists()
            or compile_artifact.output_path.stat().st_size == 0
        ):
            raise RenderingError(
                RenderFailureClass.RENDER_OUTPUT_INVALID,
                "adapter reported success but did not produce a non-empty PDF artifact",
            )

        # Keep evidence stable across equivalent checkouts and input transport details.
        evidence = NormalizedRenderEvidence(
            template_id=template_id,
            manifest_fingerprint=_sha256_text(
                _canonical_json_file_text(resolved_template.manifest_path)
            ),
            request_fingerprint=_sha256_text(
                _canonical_json_text(render_request.to_dict())
            ),
            tex_fingerprint=_sha256_text(evidence_tex),
            pdf_fingerprint=_sha256_bytes(
                compile_artifact.output_path.read_bytes()
            ),
            runtime_name=compile_artifact.runtime_name,
            runtime_version=compile_artifact.runtime_version,
            page_width_pt=resolved_template.descriptor.page_width_pt,
            page_height_pt=resolved_template.descriptor.page_height_pt,
        )
        return RenderResult(
            status=RenderStatus.SUCCEEDED,
            template_id=template_id,
            output_path=compile_artifact.output_path.as_posix(),
            diagnostics=compile_artifact.diagnostics,
            evidence=evidence,
            rendered_tex=rendered_tex,
            preview_lines=preview_lines,
        )
    except RenderingError as error:
        return RenderResult(
            status=RenderStatus.FAILED,
            template_id=template_id,
            failure_class=error.failure_class,
            diagnostics=error.diagnostics,
        )


def _build_placeholder_values(
    render_request: RenderRequest,
    resolved_assets: dict[str, Path],
) -> dict[str, str]:
    identity = render_request.identity
    options = render_request.template.options
    address_lines = tuple(identity.address_lines)
    logo_path = resolved_assets.get("logo")
    return {
        "full_name": identity.full_name,
        "role": identity.role,
        "email": identity.email,
        "organization": identity.organization or "",
        "department": identity.department or "",
        "phone": identity.phone or "",
        "website": identity.website or "",
        "pronouns": identity.pronouns or "",
        "address_block": r" \\ ".join(address_lines),
        "variant": str(options.get("variant", "default")),
        "accent_hex": str(options.get("accent_hex", "#000000")),
        "logo_path": logo_path.as_posix() if logo_path is not None else "",
    }


def _render_template_source(template_source: str, values: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        return values.get(match.group(1), "")

    return PLACEHOLDER_PATTERN.sub(replace, template_source)


def _build_preview_lines(
    render_request: RenderRequest,
    resolved_assets: dict[str, Path],
) -> tuple[str, ...]:
    identity = render_request.identity
    options = render_request.template.options
    lines = [
        f"Name: {identity.full_name}",
        f"Role: {identity.role}",
    ]
    if identity.organization:
        lines.append(f"Org: {identity.organization}")
    lines.append(f"Email: {identity.email}")
    lines.extend(f"Address: {line}" for line in identity.address_lines)
    lines.append(f"Variant: {options.get('variant', 'default')}")
    lines.append(f"Accent: {options.get('accent_hex', '#000000')}")
    lines.append(
        f"QR: {'enabled' if bool(options.get('include_qr', False)) else 'disabled'}"
    )
    if "logo" in resolved_assets:
        lines.append(f"Logo: {resolved_assets['logo'].name}")
    return tuple(lines)


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _canonical_json_file_text(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            f"failed to normalize template manifest '{path.as_posix()}': {error}",
        ) from error
    return _canonical_json_text(payload)


def _canonical_json_text(payload: object) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
