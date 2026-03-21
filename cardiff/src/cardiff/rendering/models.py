"""Rendering models for Cardiff."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class RenderStatus(StrEnum):
    """Stable top-level render outcome."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


class RenderFailureClass(StrEnum):
    """Stable failure classes for renderer callers."""

    TEMPLATE_NOT_FOUND = "template_not_found"
    TEMPLATE_MANIFEST_INVALID = "template_manifest_invalid"
    TEMPLATE_ASSET_MISSING = "template_asset_missing"
    UNSUPPORTED_TEMPLATE_OPTION = "unsupported_template_option"
    TEX_COMPILE_FAILED = "tex_compile_failed"
    RENDER_OUTPUT_INVALID = "render_output_invalid"


class RenderingError(RuntimeError):
    """Internal exception that carries a stable failure class."""

    def __init__(self, failure_class: RenderFailureClass, message: str):
        super().__init__(message)
        self.failure_class = failure_class
        self.diagnostics = (message,)


@dataclass(frozen=True, slots=True)
class TemplateDescriptor:
    """Manifest-backed description of an approved template."""

    template_id: str
    manifest_version: int
    display_name: str
    entrypoint: str
    output_format: str
    page_width_in: float
    page_height_in: float
    supported_variants: tuple[str, ...] = ()
    required_asset_slots: tuple[str, ...] = ()
    optional_asset_slots: tuple[str, ...] = ()
    required_identity_fields: tuple[str, ...] = ("full_name", "role", "email")
    sample_request: str | None = None

    @property
    def page_width_pt(self) -> float:
        return round(self.page_width_in * 72.0, 2)

    @property
    def page_height_pt(self) -> float:
        return round(self.page_height_in * 72.0, 2)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "template_id": self.template_id,
            "manifest_version": self.manifest_version,
            "display_name": self.display_name,
            "entrypoint": self.entrypoint,
            "output_format": self.output_format,
            "page_width_in": self.page_width_in,
            "page_height_in": self.page_height_in,
            "supported_variants": list(self.supported_variants),
            "required_asset_slots": list(self.required_asset_slots),
            "optional_asset_slots": list(self.optional_asset_slots),
            "required_identity_fields": list(self.required_identity_fields),
        }
        if self.sample_request is not None:
            payload["sample_request"] = self.sample_request
        return payload


@dataclass(frozen=True, slots=True)
class ResolvedTemplate:
    """Filesystem-backed approved template ready for use by the pipeline."""

    descriptor: TemplateDescriptor
    template_root: Path
    manifest_path: Path
    entrypoint_path: Path


@dataclass(frozen=True, slots=True)
class NormalizedRenderEvidence:
    """Deterministic comparison surface for render outputs."""

    template_id: str
    manifest_fingerprint: str
    request_fingerprint: str
    tex_fingerprint: str
    pdf_fingerprint: str
    runtime_name: str
    runtime_version: str
    page_width_pt: float
    page_height_pt: float

    def to_dict(self) -> dict[str, object]:
        return {
            "template_id": self.template_id,
            "manifest_fingerprint": self.manifest_fingerprint,
            "request_fingerprint": self.request_fingerprint,
            "tex_fingerprint": self.tex_fingerprint,
            "pdf_fingerprint": self.pdf_fingerprint,
            "runtime_name": self.runtime_name,
            "runtime_version": self.runtime_version,
            "page_width_pt": self.page_width_pt,
            "page_height_pt": self.page_height_pt,
        }


@dataclass(frozen=True, slots=True)
class RenderResult:
    """Stable renderer response returned to callers."""

    status: RenderStatus
    template_id: str
    output_path: str | None = None
    failure_class: RenderFailureClass | None = None
    diagnostics: tuple[str, ...] = ()
    evidence: NormalizedRenderEvidence | None = None
    rendered_tex: str | None = None
    preview_lines: tuple[str, ...] = field(default_factory=tuple)

    @property
    def succeeded(self) -> bool:
        return self.status == RenderStatus.SUCCEEDED

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "status": self.status.value,
            "template_id": self.template_id,
            "diagnostics": list(self.diagnostics),
            "preview_lines": list(self.preview_lines),
        }
        if self.output_path is not None:
            payload["output_path"] = self.output_path
        if self.failure_class is not None:
            payload["failure_class"] = self.failure_class.value
        if self.evidence is not None:
            payload["evidence"] = self.evidence.to_dict()
        if self.rendered_tex is not None:
            payload["rendered_tex"] = self.rendered_tex
        return payload
