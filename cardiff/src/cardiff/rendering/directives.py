"""Cardiff custom directives resolved before TeX compilation."""

from __future__ import annotations

import re
from pathlib import Path

from cardiff.contract.models import IdentityProfile

CARDIFF_QR_PATTERN = re.compile(r"\\cardiffqr\[([^\]]*)\]")


def build_vcard(identity: IdentityProfile) -> str:
    """Build a vCard 3.0 payload from identity fields."""

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{identity.full_name}",
        f"TITLE:{identity.role}",
        f"EMAIL:{identity.email}",
    ]
    if identity.organization and identity.department:
        lines.append(f"ORG:{identity.organization};{identity.department}")
    elif identity.organization:
        lines.append(f"ORG:{identity.organization}")
    if identity.phone:
        lines.append(f"TEL:{identity.phone}")
    if identity.website:
        lines.append(f"URL:{identity.website}")
    if identity.address_lines:
        street = ", ".join(identity.address_lines)
        lines.append(f"ADR:;;{street};;;;")
    if identity.pronouns:
        lines.append(f"NOTE:Pronouns: {identity.pronouns}")
    lines.append("END:VCARD")
    return "\r\n".join(lines)


def generate_qr_png(data: str, output_path: Path, *, scale: int = 4) -> Path:
    """Generate a QR code PNG using segno."""

    import segno

    qr = segno.make(data, error="M")
    qr.save(str(output_path), kind="png", scale=scale, border=1)
    return output_path


def resolve_qr_directives(
    tex_source: str,
    identity: IdentityProfile,
    *,
    include_qr: bool,
    work_dir: Path,
) -> str:
    """Resolve \\cardiffqr[...] directives by generating a QR PNG."""

    if not include_qr:
        return CARDIFF_QR_PATTERN.sub("", tex_source)

    vcard = build_vcard(identity)
    qr_path = generate_qr_png(vcard, work_dir / "cardiff-qr.png")

    def _replace(match: re.Match[str]) -> str:
        options = match.group(1)
        return f"\\includegraphics[{options}]{{{qr_path.as_posix()}}}"

    return CARDIFF_QR_PATTERN.sub(_replace, tex_source)


def resolve_qr_directives_deterministic(
    tex_source: str,
    *,
    include_qr: bool,
) -> str:
    """Resolve \\cardiffqr[...] for deterministic adapter (no image I/O)."""

    if not include_qr:
        return CARDIFF_QR_PATTERN.sub("", tex_source)

    return CARDIFF_QR_PATTERN.sub("% cardiffqr: enabled (deterministic)", tex_source)
