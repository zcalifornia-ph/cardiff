"""Template discovery and asset resolution for Cardiff."""

from __future__ import annotations

import json
from pathlib import Path

from cardiff.contract.models import RenderRequest, TemplateSelection

from .models import (
    RenderFailureClass,
    RenderingError,
    ResolvedTemplate,
    TemplateDescriptor,
)


def get_default_template_root() -> Path:
    """Return the package-local template root."""

    return Path(__file__).resolve().parents[1] / "templates"


def resolve_template(
    template_selection: TemplateSelection,
    *,
    template_root: str | Path | None = None,
) -> ResolvedTemplate:
    """Resolve one approved template selection to its manifest and entrypoint."""

    root = Path(template_root) if template_root is not None else get_default_template_root()
    resolved_root = root.resolve()
    template_dir = (resolved_root / template_selection.template_id).resolve()

    if not template_dir.exists() or not template_dir.is_dir() or not template_dir.is_relative_to(resolved_root):
        raise RenderingError(
            RenderFailureClass.TEMPLATE_NOT_FOUND,
            f"template '{template_selection.template_id}' is not available under '{resolved_root.as_posix()}'",
        )

    manifest_path = template_dir / "manifest.json"
    if not manifest_path.exists():
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            f"template '{template_selection.template_id}' is missing manifest.json",
        )

    descriptor = _load_descriptor(manifest_path)
    if descriptor.template_id != template_selection.template_id:
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            "manifest template_id does not match the requested template id",
        )

    variant = template_selection.options.get("variant", "default")
    if descriptor.supported_variants and variant not in descriptor.supported_variants:
        raise RenderingError(
            RenderFailureClass.UNSUPPORTED_TEMPLATE_OPTION,
            f"template '{descriptor.template_id}' does not support variant '{variant}'",
        )

    entrypoint_path = (template_dir / descriptor.entrypoint).resolve()
    if not entrypoint_path.exists() or not entrypoint_path.is_file() or not entrypoint_path.is_relative_to(template_dir):
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            f"template '{descriptor.template_id}' entrypoint '{descriptor.entrypoint}' is invalid",
        )

    return ResolvedTemplate(
        descriptor=descriptor,
        template_root=template_dir,
        manifest_path=manifest_path,
        entrypoint_path=entrypoint_path,
    )


def resolve_asset_paths(
    render_request: RenderRequest,
    resolved_template: ResolvedTemplate,
    *,
    approved_asset_roots: tuple[str | Path, ...] | None = None,
) -> dict[str, Path]:
    """Resolve request asset references against approved roots and template rules."""

    approved_roots = tuple(Path(root).resolve() for root in (approved_asset_roots or ()))
    resolved_assets: dict[str, Path] = {}

    expected_slots = tuple(dict.fromkeys((*resolved_template.descriptor.required_asset_slots, *resolved_template.descriptor.optional_asset_slots)))
    for slot in expected_slots:
        asset_reference = render_request.assets.get(slot)
        if asset_reference is None:
            if slot in resolved_template.descriptor.required_asset_slots:
                raise RenderingError(
                    RenderFailureClass.TEMPLATE_ASSET_MISSING,
                    f"required asset slot '{slot}' is missing for template '{resolved_template.descriptor.template_id}'",
                )
            continue
        resolved_assets[slot] = _resolve_asset_reference(slot, asset_reference.path, approved_roots)

    return resolved_assets


def _load_descriptor(manifest_path: Path) -> TemplateDescriptor:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            f"failed to load template manifest '{manifest_path.as_posix()}': {error}",
        ) from error

    required_fields = {
        "template_id": str,
        "manifest_version": int,
        "display_name": str,
        "entrypoint": str,
        "output_format": str,
        "page_width_in": (int, float),
        "page_height_in": (int, float),
    }
    for field_name, expected_type in required_fields.items():
        value = payload.get(field_name)
        if not isinstance(value, expected_type):
            raise RenderingError(
                RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
                f"manifest field '{field_name}' is missing or has the wrong type",
            )

    if payload["output_format"] != "pdf":
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            "template manifests must currently declare output_format 'pdf'",
        )

    supported_variants = _validate_string_list(payload.get("supported_variants", []), "supported_variants")
    required_asset_slots = _validate_string_list(payload.get("required_asset_slots", []), "required_asset_slots")
    optional_asset_slots = _validate_string_list(payload.get("optional_asset_slots", []), "optional_asset_slots")
    required_identity_fields = _validate_string_list(payload.get("required_identity_fields", ["full_name", "role", "email"]), "required_identity_fields")

    return TemplateDescriptor(
        template_id=payload["template_id"],
        manifest_version=payload["manifest_version"],
        display_name=payload["display_name"],
        entrypoint=payload["entrypoint"],
        output_format=payload["output_format"],
        page_width_in=float(payload["page_width_in"]),
        page_height_in=float(payload["page_height_in"]),
        supported_variants=supported_variants,
        required_asset_slots=required_asset_slots,
        optional_asset_slots=optional_asset_slots,
        required_identity_fields=required_identity_fields,
        sample_request=payload.get("sample_request"),
    )


def _validate_string_list(payload: object, field_name: str) -> tuple[str, ...]:
    if not isinstance(payload, list) or any(not isinstance(item, str) for item in payload):
        raise RenderingError(
            RenderFailureClass.TEMPLATE_MANIFEST_INVALID,
            f"manifest field '{field_name}' must be a list of strings",
        )
    return tuple(payload)


def _resolve_asset_reference(slot: str, raw_path: str, approved_roots: tuple[Path, ...]) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        resolved = candidate.resolve()
        if not any(resolved.is_relative_to(root) for root in approved_roots):
            raise RenderingError(
                RenderFailureClass.TEMPLATE_ASSET_MISSING,
                f"asset '{slot}' is outside the approved asset roots",
            )
        if not resolved.exists():
            raise RenderingError(
                RenderFailureClass.TEMPLATE_ASSET_MISSING,
                f"asset '{slot}' does not exist at '{resolved.as_posix()}'",
            )
        return resolved

    for root in approved_roots:
        asset_path = (root / candidate).resolve()
        if asset_path.exists() and asset_path.is_relative_to(root):
            return asset_path

    raise RenderingError(
        RenderFailureClass.TEMPLATE_ASSET_MISSING,
        f"asset '{slot}' could not be resolved under the approved asset roots",
    )
