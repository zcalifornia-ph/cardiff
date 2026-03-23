"""Cardiff custom directives resolved before TeX compilation."""

from __future__ import annotations

import re
from pathlib import Path

from cardiff.contract.models import IdentityProfile

CARDIFF_QR_FILENAME = "cardiff-qr.png"
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    qr = segno.make(data, error="M")
    with output_path.open("wb") as handle:
        qr.save(handle, kind="png", scale=scale, border=1)
    return output_path


def substitute_qr_directives(
    tex_source: str,
    *,
    include_qr: bool,
    qr_tex_path: str,
) -> str:
    """Replace \\cardiffqr[...] directives with a chosen TeX include path."""

    if not include_qr:
        return CARDIFF_QR_PATTERN.sub("", tex_source)

    def _replace(match: re.Match[str]) -> str:
        options = match.group(1)
        return f"\\includegraphics[{options}]{{{qr_tex_path}}}"

    return CARDIFF_QR_PATTERN.sub(_replace, tex_source)


def resolve_qr_directives(
    tex_source: str,
    identity: IdentityProfile,
    *,
    include_qr: bool,
    work_dir: Path,
    qr_filename: str = CARDIFF_QR_FILENAME,
) -> str:
    """Resolve \\cardiffqr[...] directives by generating a QR PNG."""

    if not include_qr:
        return substitute_qr_directives(
            tex_source,
            include_qr=False,
            qr_tex_path="",
        )

    vcard = build_vcard(identity)
    qr_path = generate_qr_png(vcard, work_dir / qr_filename)
    return substitute_qr_directives(
        tex_source,
        include_qr=True,
        qr_tex_path=qr_path.as_posix(),
    )


def resolve_qr_directives_deterministic(
    tex_source: str,
    *,
    include_qr: bool,
) -> str:
    """Resolve \\cardiffqr[...] for deterministic adapter (no image I/O)."""

    if not include_qr:
        return CARDIFF_QR_PATTERN.sub("", tex_source)

    return CARDIFF_QR_PATTERN.sub("% cardiffqr: enabled (deterministic)", tex_source)
