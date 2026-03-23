"""Public rendering surface for Cardiff."""

from .directives import (
    build_vcard,
    generate_qr_png,
    resolve_qr_directives,
    resolve_qr_directives_deterministic,
)
from .models import (
    NormalizedRenderEvidence,
    RenderFailureClass,
    RenderResult,
    RenderStatus,
    ResolvedTemplate,
    TemplateDescriptor,
)
from .pipeline import render_request_to_pdf
from .templates import get_default_template_root, resolve_asset_paths, resolve_template
from .tex import DeterministicTeXAdapter, XeLaTeXAdapter, get_default_tex_adapter

__all__ = [
    "DeterministicTeXAdapter",
    "NormalizedRenderEvidence",
    "RenderFailureClass",
    "RenderResult",
    "RenderStatus",
    "ResolvedTemplate",
    "TemplateDescriptor",
    "XeLaTeXAdapter",
    "build_vcard",
    "generate_qr_png",
    "get_default_template_root",
    "get_default_tex_adapter",
    "render_request_to_pdf",
    "resolve_asset_paths",
    "resolve_qr_directives",
    "resolve_qr_directives_deterministic",
    "resolve_template",
]
