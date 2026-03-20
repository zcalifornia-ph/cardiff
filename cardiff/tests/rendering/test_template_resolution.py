from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from cardiff.contract import load_and_validate_request
from cardiff.contract.errors import ValidationOutcome
from cardiff.contract.models import TemplateSelection
from cardiff.rendering import (
    DeterministicTeXAdapter,
    RenderFailureClass,
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


def test_approved_business_card_template_resolves():
    request = _load_request()

    resolved = resolve_template(request.template)

    assert resolved.descriptor.template_id == "business-card"
    assert resolved.descriptor.page_width_pt == 252.0
    assert resolved.descriptor.page_height_pt == 144.0
    assert resolved.entrypoint_path.name == "card.tex"


def test_missing_template_is_classified_before_compilation():
    request = _load_request()
    missing_request = replace(
        request,
        template=TemplateSelection(
            template_id="missing-card",
            options=dict(request.template.options),
        ),
    )

    result = render_request_to_pdf(
        missing_request,
        APPROVED_SAMPLES / "missing-template.pdf",
        approved_asset_roots=(APPROVED_ASSETS,),
        tex_adapter=DeterministicTeXAdapter(),
    )

    assert result.status == RenderStatus.FAILED
    assert result.failure_class == RenderFailureClass.TEMPLATE_NOT_FOUND
