from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock, patch

from cardiff.contract import load_and_validate_request
from cardiff.contract.errors import ValidationOutcome
from cardiff.rendering import (
    DeterministicTeXAdapter,
    RenderStatus,
    render_request_to_pdf,
    resolve_template,
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


def test_request_fingerprint_ignores_source_metadata():
    request = _load_request()
    output_path = APPROVED_SAMPLES / "determinism-output.pdf"
    adapter = DeterministicTeXAdapter()
    alternate_source_request = replace(
        request,
        source_name="C:/elsewhere/valid-request.json",
        source_format="json",
    )

    baseline = render_request_to_pdf(
        request,
        output_path,
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=adapter,
    )
    variant = render_request_to_pdf(
        alternate_source_request,
        output_path,
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=adapter,
    )

    assert baseline.status == RenderStatus.SUCCEEDED
    assert variant.status == RenderStatus.SUCCEEDED
    assert baseline.evidence is not None
    assert variant.evidence is not None
    assert baseline.evidence.to_dict() == variant.evidence.to_dict()


def test_manifest_fingerprint_ignores_line_ending_differences():
    request = _load_request()
    output_path = APPROVED_SAMPLES / "determinism-output.pdf"
    adapter = DeterministicTeXAdapter()
    resolved_template = resolve_template(request.template)
    original_bytes = resolved_template.manifest_path.read_bytes()
    newline = "\r\n" if b"\r\n" not in original_bytes else "\n"
    manifest_text = original_bytes.decode("utf-8").replace("\r\n", "\n")
    alternate_manifest_text = manifest_text.replace("\n", newline)
    alternate_manifest_bytes = alternate_manifest_text.encode("utf-8")
    assert alternate_manifest_bytes != original_bytes
    alternate_manifest_path = Mock()
    alternate_manifest_path.read_text.return_value = alternate_manifest_text
    alternate_manifest_path.read_bytes.return_value = alternate_manifest_bytes
    alternate_manifest_path.as_posix.return_value = "virtual/manifest.json"

    baseline = render_request_to_pdf(
        request,
        output_path,
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=adapter,
    )
    with patch(
        "cardiff.rendering.pipeline.resolve_template",
        return_value=replace(
            resolved_template,
            manifest_path=alternate_manifest_path,
        ),
    ):
        variant = render_request_to_pdf(
            request,
            output_path,
            approved_asset_roots=(APPROVED_ASSETS,),
            tex_adapter=adapter,
        )

    assert baseline.status == RenderStatus.SUCCEEDED
    assert variant.status == RenderStatus.SUCCEEDED
    assert baseline.evidence is not None
    assert variant.evidence is not None
    assert baseline.evidence.to_dict() == variant.evidence.to_dict()
