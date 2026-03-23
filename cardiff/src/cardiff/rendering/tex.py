"""TeX adapter implementations for Cardiff."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import tempfile

from .models import RenderFailureClass, RenderingError


@dataclass(frozen=True, slots=True)
class TeXCompileArtifact:
    """Output returned by a TeX adapter."""

    output_path: Path
    runtime_name: str
    runtime_version: str
    compiler_path: str | None = None
    diagnostics: tuple[str, ...] = ()


class BaseTeXAdapter:
    """Small adapter contract used by the render pipeline."""

    runtime_name = "base-tex-adapter"
    runtime_version = "0"
    deterministic = False

    def compile(
        self,
        tex_source: str,
        output_path: str | Path,
        *,
        page_size_pt: tuple[float, float],
        preview_lines: tuple[str, ...],
        title: str,
    ) -> TeXCompileArtifact:
        raise NotImplementedError


class DeterministicTeXAdapter(BaseTeXAdapter):
    """Deterministic adapter used for tests and local fallback execution."""

    runtime_name = "deterministic-tex-adapter"
    runtime_version = "1"
    deterministic = True

    def compile(
        self,
        tex_source: str,
        output_path: str | Path,
        *,
        page_size_pt: tuple[float, float],
        preview_lines: tuple[str, ...],
        title: str,
    ) -> TeXCompileArtifact:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        pdf_bytes = _build_minimal_pdf(preview_lines, page_size_pt=page_size_pt, title=title)
        output.write_bytes(pdf_bytes)
        return TeXCompileArtifact(
            output_path=output,
            runtime_name=self.runtime_name,
            runtime_version=self.runtime_version,
            diagnostics=(f"deterministic adapter wrote '{output.as_posix()}'",),
        )


class XeLaTeXAdapter(BaseTeXAdapter):
    """Subprocess-backed XeLaTeX adapter for real compiler runs."""

    runtime_name = "xelatex"

    def __init__(self, command: str = "xelatex"):
        self.command = command
        self.runtime_version = self._detect_version()

    def compile(
        self,
        tex_source: str,
        output_path: str | Path,
        *,
        page_size_pt: tuple[float, float],
        preview_lines: tuple[str, ...],
        title: str,
    ) -> TeXCompileArtifact:
        compiler_path = shutil.which(self.command)
        if compiler_path is None:
            raise RenderingError(
                RenderFailureClass.TEX_COMPILE_FAILED,
                f"'{self.command}' is not available in PATH",
            )

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            tex_path = temp_root / "cardiff-render.tex"
            tex_path.write_text(tex_source, encoding="utf-8")

            completed = subprocess.run(
                [
                    compiler_path,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={temp_root.as_posix()}",
                    tex_path.as_posix(),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                diagnostics = tuple(
                    line for line in (completed.stdout, completed.stderr) if line.strip()
                )
                raise RenderingError(
                    RenderFailureClass.TEX_COMPILE_FAILED,
                    diagnostics[-1] if diagnostics else "xelatex compilation failed",
                )

            compiled_pdf = temp_root / "cardiff-render.pdf"
            if not compiled_pdf.exists():
                raise RenderingError(
                    RenderFailureClass.RENDER_OUTPUT_INVALID,
                    "xelatex completed without producing a PDF artifact",
                )

            shutil.copyfile(compiled_pdf, output)
            diagnostics = tuple(
                line for line in (completed.stdout, completed.stderr) if line.strip()
            )
            return TeXCompileArtifact(
                output_path=output,
                runtime_name=self.runtime_name,
                runtime_version=self.runtime_version,
                compiler_path=compiler_path,
                diagnostics=diagnostics,
            )

    def _detect_version(self) -> str:
        compiler_path = shutil.which(self.command)
        if compiler_path is None:
            return "unavailable"
        completed = subprocess.run(
            [compiler_path, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0 or not completed.stdout.strip():
            return "unknown"
        return completed.stdout.splitlines()[0].strip()


def get_default_tex_adapter() -> BaseTeXAdapter:
    """Return the best available local adapter."""

    return XeLaTeXAdapter() if shutil.which("xelatex") else DeterministicTeXAdapter()


def _build_minimal_pdf(
    preview_lines: tuple[str, ...],
    *,
    page_size_pt: tuple[float, float],
    title: str,
) -> bytes:
    _ensure_ascii_preview_text(title, field_name="title")
    for index, line in enumerate(preview_lines):
        _ensure_ascii_preview_text(line, field_name=f"preview_lines[{index}]")

    width_pt, height_pt = page_size_pt
    y = height_pt - 18.0
    commands = ["BT", "/F1 9 Tf"]
    for line in preview_lines:
        commands.append(f"1 0 0 1 12 {y:.2f} Tm ({_escape_pdf_text(line)}) Tj")
        y -= 10.0
    commands.append("ET")
    stream = "\n".join(commands).encode("ascii", errors="replace")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n",
        (
            f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width_pt:.2f} {height_pt:.2f}] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
        ).encode("ascii"),
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        f"5 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"\nendstream\nendobj\n",
        (
            f"6 0 obj\n<< /Title ({_escape_pdf_text(title)}) /Producer (Cardiff deterministic adapter) >>\nendobj\n"
        ).encode("ascii"),
    ]

    buffer = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(buffer))
        buffer.extend(obj)

    xref_start = len(buffer)
    buffer.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    buffer.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        buffer.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    buffer.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 6 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(buffer)


def _escape_pdf_text(value: str) -> str:
    escaped = value.encode("ascii").decode("ascii")
    escaped = escaped.replace("\\", r"\\")
    escaped = escaped.replace("(", r"\(")
    escaped = escaped.replace(")", r"\)")
    return escaped


def _ensure_ascii_preview_text(value: str, *, field_name: str) -> None:
    try:
        value.encode("ascii")
    except UnicodeEncodeError as error:
        raise RenderingError(
            RenderFailureClass.TEX_COMPILE_FAILED,
            (
                "deterministic adapter cannot render non-ASCII text in "
                f"{field_name}; install xelatex for Unicode-safe rendering"
            ),
        ) from error
