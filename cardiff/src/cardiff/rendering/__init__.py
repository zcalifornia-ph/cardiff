"""Public rendering surface for Cardiff."""

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
    "get_default_template_root",
    "get_default_tex_adapter",
    "render_request_to_pdf",
    "resolve_asset_paths",
    "resolve_template",
]
