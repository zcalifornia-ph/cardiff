from __future__ import annotations

from pathlib import Path

from cardiff.contract.models import IdentityProfile
from cardiff.rendering.directives import (
    build_vcard,
    generate_qr_png,
    resolve_qr_directives,
    resolve_qr_directives_deterministic,
)

FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
APPROVED_SAMPLES = FIXTURES_ROOT / "approved-samples" / "business-card"


def _make_identity(**overrides) -> IdentityProfile:
    defaults = {
        "full_name": "Ada Lovelace",
        "role": "Computing Pioneer",
        "email": "ada@example.com",
        "organization": "Analytical Engine Lab",
    }
    defaults.update(overrides)
    return IdentityProfile(**defaults)


def _work_dir(name: str) -> Path:
    path = APPROVED_SAMPLES / "_directive-work" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


class TestBuildVcard:
    def test_includes_required_fields(self):
        vcard = build_vcard(_make_identity())
        assert "FN:Ada Lovelace" in vcard
        assert "TITLE:Computing Pioneer" in vcard
        assert "EMAIL:ada@example.com" in vcard
        assert vcard.startswith("BEGIN:VCARD")
        assert vcard.endswith("END:VCARD")

    def test_includes_optional_fields(self):
        identity = _make_identity(
            phone="+1-555-0100",
            website="https://ada.example.com",
            department="Mathematics",
            address_lines=("123 Logic St.", "London"),
            pronouns="she/her",
        )
        vcard = build_vcard(identity)
        assert "TEL:+1-555-0100" in vcard
        assert "URL:https://ada.example.com" in vcard
        assert "ORG:Analytical Engine Lab;Mathematics" in vcard
        assert "ADR:;;123 Logic St., London;;;;" in vcard
        assert "NOTE:Pronouns: she/her" in vcard

    def test_omits_absent_optional_fields(self):
        identity = _make_identity(organization=None)
        vcard = build_vcard(identity)
        assert "ORG:" not in vcard
        assert "TEL:" not in vcard
        assert "URL:" not in vcard
        assert "ADR:" not in vcard


class TestGenerateQrPng:
    def test_creates_valid_png(self):
        path = generate_qr_png("hello", _work_dir("png") / "test.png")
        assert path.exists()
        assert path.read_bytes()[:4] == b"\x89PNG"


class TestResolveQrDirectives:
    def test_enabled_replaces_with_includegraphics(self):
        tex = r"before \cardiffqr[width=0.6in] after"
        result = resolve_qr_directives(
            tex,
            _make_identity(),
            include_qr=True,
            work_dir=_work_dir("enabled"),
        )
        assert r"\includegraphics[width=0.6in]" in result
        assert "before" in result
        assert "after" in result
        assert r"\cardiffqr" not in result

    def test_disabled_emits_nothing(self):
        tex = r"before \cardiffqr[width=0.6in] after"
        result = resolve_qr_directives(
            tex,
            _make_identity(),
            include_qr=False,
            work_dir=_work_dir("disabled"),
        )
        assert r"\includegraphics" not in result
        assert r"\cardiffqr" not in result
        assert "before  after" in result

    def test_options_pass_through(self):
        tex = r"\cardiffqr[height=1in,keepaspectratio]"
        result = resolve_qr_directives(
            tex,
            _make_identity(),
            include_qr=True,
            work_dir=_work_dir("options"),
        )
        assert r"\includegraphics[height=1in,keepaspectratio]" in result


class TestResolveQrDirectivesDeterministic:
    def test_enabled_emits_comment(self):
        tex = r"before \cardiffqr[width=0.6in] after"
        result = resolve_qr_directives_deterministic(tex, include_qr=True)
        assert "% cardiffqr: enabled (deterministic)" in result
        assert r"\cardiffqr" not in result

    def test_disabled_emits_nothing(self):
        tex = r"before \cardiffqr[width=0.6in] after"
        result = resolve_qr_directives_deterministic(tex, include_qr=False)
        assert r"\cardiffqr" not in result
        assert "cardiffqr" not in result
        assert "before  after" in result
