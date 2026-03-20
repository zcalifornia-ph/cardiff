from __future__ import annotations

from pathlib import Path

from cardiff.contract import load_and_validate_request
from cardiff.contract.errors import ValidationOutcome
from cardiff.rendering import (
    DeterministicTeXAdapter,
    RenderFailureClass,
    RenderStatus,
    render_request_to_pdf,
)

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
