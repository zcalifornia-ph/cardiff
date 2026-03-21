from __future__ import annotations

from pathlib import Path

from cardiff.contract import load_and_validate_request
from cardiff.contract.errors import ValidationOutcome
from cardiff.rendering import DeterministicTeXAdapter, RenderStatus, render_request_to_pdf

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


def test_repeated_runs_produce_matching_normalized_evidence():
    request = _load_request()
    output_path = APPROVED_SAMPLES / "determinism-output.pdf"
    adapter = DeterministicTeXAdapter()
    evidence_payloads = []

    for _ in range(3):
        result = render_request_to_pdf(
            request,
            output_path,
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=adapter,
        )
        assert result.status == RenderStatus.SUCCEEDED
        assert result.evidence is not None
        evidence_payloads.append(result.evidence.to_dict())

    assert evidence_payloads[0] == evidence_payloads[1] == evidence_payloads[2]
