# Version 0.0.3 Docs

## Quick Diagnostic Read

`v0.0.3` moves Cardiff from a contract-only pre-alpha into the first reusable render baseline.
The repository now contains a manifest-driven template package, a shared render pipeline, deterministic PDF generation, normalized evidence output, and render-focused automated tests.

## One-Sentence Objective

Document exactly what changed in `v0.0.3` beyond the short changelog so reviewers can see the render surface, evidence model, verification results, and the gaps that still remain.

## Why This Version Matters

This version is the first point where Cardiff can do more than validate input.
It now turns an accepted `RenderRequest` into a classified render result and a reviewable PDF artifact through one shared pipeline that future CLI, batch, and API entry points can all reuse.

## Plan A / Plan B

Plan A: start with `README.md`, then read `cardiff/docs/render-pipeline.md`, then inspect `cardiff/src/cardiff/rendering/`.

Plan B: start with the rendering tests in `cardiff/tests/rendering/`, then inspect the approved template package under `cardiff/src/cardiff/templates/business-card/`, then read the ADR and traceability artifact for `BOLT-001B`.

## Artifact Map

- `cardiff/src/cardiff/rendering/__init__.py`
- `cardiff/src/cardiff/rendering/models.py`
- `cardiff/src/cardiff/rendering/templates.py`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/src/cardiff/rendering/tex.py`
- `cardiff/src/cardiff/templates/business-card/manifest.json`
- `cardiff/src/cardiff/templates/business-card/card.tex`
- `cardiff/tests/rendering/test_template_resolution.py`
- `cardiff/tests/rendering/test_pipeline.py`
- `cardiff/tests/rendering/test_determinism.py`
- `cardiff/tests/fixtures/approved-assets/brand/logo.png`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-output.pdf`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`
- `cardiff/tests/fixtures/approved-samples/business-card/determinism-output.pdf`
- `cardiff/docs/render-pipeline.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/domain-design.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/logical-design.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/adr/bolt-001b-adr.md`
- `cardiff/ai-dlc-docs/traceability/UNIT-001/bolt-001b-traceability.md`
- `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md`

## What Changed In This Version

### 1. Shared Render Pipeline Added

The repository now includes `cardiff/src/cardiff/rendering/`, which owns the renderer-facing public API.
This package introduces stable render result models, manifest resolution, asset resolution, pipeline orchestration, and adapter boundaries.

### 2. First Approved Template Package Added

The `business-card` template is now packaged under `cardiff/src/cardiff/templates/business-card/`.
The template is resolved through a manifest-backed symbolic template ID instead of an ad hoc file path.

### 3. Deterministic Evidence Model Added

The render pipeline now emits normalized evidence with these fingerprints and runtime details:

- manifest fingerprint
- canonical request fingerprint
- rendered TeX fingerprint
- PDF fingerprint
- runtime name and version
- business-card geometry in points

This is the proof model for the current determinism check.

### 4. Two Adapter Paths Now Exist

The current version supports:

- `DeterministicTeXAdapter` for local deterministic output and environments that do not have `xelatex`
- `XeLaTeXAdapter` for real compiler-backed runs when `xelatex` is available on `PATH`

This keeps the pipeline reusable now while preserving a clear boundary for later reference-runtime parity work.

### 5. Rendering Tests And Review Artifacts Added

This version adds rendering-focused tests under `cardiff/tests/rendering/`.
These tests verify:

- approved template resolution
- missing-template failure classification
- missing-asset failure classification
- PDF output generation to the requested path
- repeated-run normalized evidence parity across 3 runs

The version also stores review artifacts under `cardiff/tests/fixtures/approved-samples/business-card/`.

### 6. Root Docs Realigned Again

The root `README.md` now reflects that the render pipeline has landed.
`CONTRIBUTING.md` now points contributors at the actual requirements source of truth under `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md` instead of the missing root-level path that earlier docs implied.

## Behavior Available Now

Cardiff can now:

- validate and sanitize a single-record request
- resolve the approved `business-card` template from a symbolic template ID
- check required asset availability against approved asset roots
- produce a PDF artifact through the shared render pipeline
- emit stable failure classes when resolution or rendering fails
- emit normalized render evidence for repeated-run comparison

## Verification

Recorded evidence for this implementation slice:

```powershell
cd cardiff
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests -q -p no:cacheprovider
```

Expected result:

- 5 rendering tests pass
- 13 total tests pass

Stored review artifacts:

- `cardiff/tests/fixtures/approved-samples/business-card/reference-output.pdf`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`
- `cardiff/tests/fixtures/approved-samples/business-card/determinism-output.pdf`

## Known Gaps

This version still does not deliver:

- CLI `validate` and `render` commands
- CSV batch processing
- FastAPI service mode
- richer template customization and approval workflows beyond the first template package
- pinned reference-runtime parity with a real `xelatex` environment
- CI wiring, deployment packaging, and ops instrumentation surfaces

The current workspace also still contains generated runtime artifacts that should be removed before a clean commit:

- `cardiff/src/cardiff.egg-info/`
- `cardiff/**/__pycache__/`
- `cardiff/**/*.pyc`

## Practice Task

Open `cardiff/tests/rendering/test_pipeline.py` and explain which assertions prove output-path behavior versus which assertions prove artifact content or geometry expectations.
If you can map those assertions to `TEST-007` and `DEP-001`, you understand the current render slice.

## Next Steps

The next approved construction targets are:

1. `BOLT-001C` for the CLI operator flow
2. UNIT-002 for template polish and controlled customization
3. reference-runtime parity work for the real `xelatex` execution path

That is the path from the current render baseline to the first polished operator-facing MVP.
