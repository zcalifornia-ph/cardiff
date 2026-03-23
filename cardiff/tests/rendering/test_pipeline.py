from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import pytest

from cardiff.contract import load_and_validate_request
from cardiff.contract.errors import ValidationOutcome
from cardiff.rendering import (
    DeterministicTeXAdapter,
    RenderFailureClass,
    RenderStatus,
    render_request_to_pdf,
    resolve_template,
)
from cardiff.rendering.tex import BaseTeXAdapter, TeXCompileArtifact

FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
APPROVED_ASSETS = FIXTURES_ROOT / "approved-assets"
APPROVED_SAMPLES = FIXTURES_ROOT / "approved-samples" / "business-card"
REQUEST_PATH = FIXTURES_ROOT / "requests" / "valid-request.yaml"


def _load_request():
    result = load_and_validate_request(
        REQUEST_PATH,
        approved_asset_roots=(APPROVED_ASSETS,),
    )
    assert result.outcome == ValidationOutcome.ACCEPTED
    assert result.request is not None
    return result.request


def _fake_qr_path(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class FakeNonDeterministicAdapter(BaseTeXAdapter):
    runtime_name = "fake-nondeterministic-adapter"
    runtime_version = "1"
    deterministic = False

    def compile(
        self,
        tex_source: str,
        output_path: str | Path,
        *,
        page_size_pt: tuple[float, float],
        preview_lines: tuple[str, ...],
        title: str,
    ) -> TeXCompileArtifact:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"%PDF-1.4\n%%EOF\n")
        return TeXCompileArtifact(
            output_path=output,
            runtime_name=self.runtime_name,
            runtime_version=self.runtime_version,
        )


def test_pipeline_writes_pdf_to_the_requested_output_path():
    request = _load_request()
    output_path = APPROVED_SAMPLES / "reference-output.pdf"

    result = render_request_to_pdf(
        request,
        output_path,
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=DeterministicTeXAdapter(),
    )

    assert result.status == RenderStatus.SUCCEEDED
    assert result.output_path == output_path.as_posix()
    assert result.evidence is not None
    assert result.evidence.runtime_name == "deterministic-tex-adapter"
    pdf_bytes = output_path.read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"Ada Lovelace" in pdf_bytes
    assert b"252.00 144.00" in pdf_bytes


def test_missing_asset_is_classified_before_pdf_generation():
    request = _load_request()

    result = render_request_to_pdf(
        request,
        APPROVED_SAMPLES / "missing-asset.pdf",
        approved_asset_roots=(FIXTURES_ROOT / "requests",),
        tex_adapter=DeterministicTeXAdapter(),
    )

    assert result.status == RenderStatus.FAILED
    assert result.failure_class == RenderFailureClass.TEMPLATE_ASSET_MISSING


def test_qr_preprocessing_failure_is_classified_before_compilation():
    request = _load_request()

    with patch(
        "cardiff.rendering.pipeline.resolve_qr_directives",
        side_effect=PermissionError("access denied"),
    ):
        result = render_request_to_pdf(
            request,
            APPROVED_SAMPLES / "qr-preprocess-failure.pdf",
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=FakeNonDeterministicAdapter(),
        )

    assert result.status == RenderStatus.FAILED
    assert result.failure_class == RenderFailureClass.TEX_COMPILE_FAILED
    assert result.diagnostics == (
        "failed to prepare QR directive assets: access denied",
    )


def test_non_deterministic_qr_renders_keep_normalized_evidence_stable():
    request = _load_request()
    output_path = APPROVED_SAMPLES / "qr-evidence-stability.pdf"
    adapter = FakeNonDeterministicAdapter()

    with patch(
        "cardiff.rendering.directives.generate_qr_png",
        side_effect=lambda data, output_path, scale=4: _fake_qr_path(output_path),
    ):
        first = render_request_to_pdf(
            request,
            output_path,
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=adapter,
        )
        second = render_request_to_pdf(
            request,
            output_path,
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=adapter,
        )

    assert first.status == RenderStatus.SUCCEEDED
    assert second.status == RenderStatus.SUCCEEDED
    assert first.evidence is not None
    assert second.evidence is not None
    assert first.rendered_tex is not None
    assert ".cardiff-qr/qr-evidence-stability-cardiff-qr.png" in first.rendered_tex
    assert first.evidence.to_dict() == second.evidence.to_dict()


@pytest.mark.parametrize(
    ("identity_updates", "expected_fragment", "output_name"),
    [
        ({"full_name": "José Álvarez"}, "preview_lines[0]", "unicode-name.pdf"),
        ({"role": "Diseñadora Sénior"}, "preview_lines[1]", "unicode-role.pdf"),
        ({"organization": "Niño Labs"}, "preview_lines[2]", "unicode-organization.pdf"),
        (
            {"address_lines": ("123 Rue de l'Église", "London")},
            "preview_lines[4]",
            "unicode-address.pdf",
        ),
    ],
)
def test_deterministic_adapter_fails_clearly_on_non_ascii_identity_text(
    identity_updates,
    expected_fragment,
    output_name,
):
    request = _load_request()
    unicode_request = replace(
        request,
        identity=replace(request.identity, **identity_updates),
    )
    output_path = APPROVED_SAMPLES / output_name

    result = render_request_to_pdf(
        unicode_request,
        output_path,
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=DeterministicTeXAdapter(),
    )

    assert result.status == RenderStatus.FAILED
    assert result.failure_class == RenderFailureClass.TEX_COMPILE_FAILED
    assert result.output_path is None
    assert any("non-ASCII" in message for message in result.diagnostics)
    assert any(expected_fragment in message for message in result.diagnostics)


def test_deterministic_adapter_fails_clearly_on_non_ascii_template_title():
    request = _load_request()
    resolved_template = resolve_template(request.template)
    unicode_title_template = replace(
        resolved_template,
        descriptor=replace(
            resolved_template.descriptor,
            display_name="Tarjeta José",
        ),
    )

    with patch(
        "cardiff.rendering.pipeline.resolve_template",
        return_value=unicode_title_template,
    ):
        result = render_request_to_pdf(
            request,
            APPROVED_SAMPLES / "unicode-title.pdf",
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=DeterministicTeXAdapter(),
        )

    assert result.status == RenderStatus.FAILED
    assert result.failure_class == RenderFailureClass.TEX_COMPILE_FAILED
    assert result.output_path is None
    assert any("non-ASCII" in message for message in result.diagnostics)
    assert any("title" in message for message in result.diagnostics)
