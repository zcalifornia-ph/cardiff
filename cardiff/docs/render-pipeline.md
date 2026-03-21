# Cardiff Render Pipeline

## Scope

`BOLT-001B` introduces the first shared render pipeline for Cardiff. It resolves one approved symbolic template, renders TeX from the canonical contract, and produces a PDF artifact plus normalized evidence for deterministic review.

## Template Directory Contract

Approved templates live under `cardiff/src/cardiff/templates/<template-id>/`.

Each template package must currently provide:

- `manifest.json`: template metadata, page geometry, supported variants, and required asset slots
- `card.tex`: the entry TeX template consumed by the pipeline

## Render Lifecycle

1. Load and validate a JSON or YAML request through `cardiff.contract`.
2. Resolve `template.id` through the manifest-driven template registry.
3. Resolve required asset paths against the caller-provided approved asset roots.
4. Materialize TeX by applying the canonical request data to the approved template.
5. Compile through a TeX adapter.
6. Return `RenderResult` plus normalized evidence fingerprints.

## Adapter Modes

- `DeterministicTeXAdapter`: local deterministic fallback used by tests and by environments that do not have `xelatex` installed.
- `XeLaTeXAdapter`: subprocess-backed adapter for real compiler execution when `xelatex` is available.

`render_request_to_pdf()` will pick `XeLaTeXAdapter` automatically when `xelatex` is on `PATH`; otherwise it falls back to `DeterministicTeXAdapter`.

## Sample Usage

```python
from pathlib import Path

from cardiff.contract import load_and_validate_request
from cardiff.rendering import DeterministicTeXAdapter, render_request_to_pdf

assets_root = Path("tests/fixtures/approved-assets")
request_result = load_and_validate_request(
    Path("tests/fixtures/requests/valid-request.yaml"),
    approved_asset_roots=(assets_root,),
)
request = request_result.request
assert request is not None

render_result = render_request_to_pdf(
    request,
    Path("tests/fixtures/approved-samples/business-card/reference-output.pdf"),
    approved_asset_roots=(assets_root,),
    tex_adapter=DeterministicTeXAdapter(),
)
assert render_result.succeeded
```

## Evidence And Review

`BOLT-001B` review evidence is stored under `cardiff/tests/fixtures/approved-samples/business-card/`.

The normalized evidence record captures:

- manifest fingerprint
- canonical request fingerprint
- rendered TeX fingerprint
- PDF fingerprint
- adapter runtime name and version
- business-card page dimensions in points
