# Changelog

Status: pre-alpha; canonical contract and render pipeline foundations landed, while CLI, batch, API, and deployment work remain in progress.

## v0.0.3

### Added or Changed
- Completed `UNIT-001 / BOLT-001B` and added the shared render pipeline in `cardiff/src/cardiff/rendering/`.
- Added the first approved manifest-backed template package under `cardiff/src/cardiff/templates/business-card/`.
- Added deterministic and compiler-backed adapter boundaries through `DeterministicTeXAdapter` and `XeLaTeXAdapter`.
- Added rendering-focused automated coverage under `cardiff/tests/rendering/` for template resolution, classified failure handling, and normalized determinism checks.
- Added approval artifacts under `cardiff/tests/fixtures/approved-samples/business-card/`, including a reference PDF and normalized render-evidence JSON.
- Added `cardiff/docs/render-pipeline.md` to document the template directory contract, pipeline lifecycle, adapter behavior, and sample usage.
- Updated `README.md` and `CONTRIBUTING.md` so the root docs reflect the implemented render pipeline and the actual requirements source of truth at `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md`.
- Added `docs/version-0-0-3-docs.md` with the full version narrative beyond this changelog summary.

### For Deletion
- `cardiff/src/cardiff.egg-info/`
- `cardiff/**/__pycache__/`
- `cardiff/**/*.pyc`

## v0.0.2

### Added or Changed
- Added the nested Python project under `cardiff/` with package metadata in `cardiff/pyproject.toml`.
- Added the public package surface in `cardiff/src/cardiff/` and the first completed implementation slice for `UNIT-001 / BOLT-001A`.
- Implemented the canonical contract kernel in `cardiff/src/cardiff/contract/`, including JSON and YAML loading, required-field validation, stable failure taxonomy, asset-path guardrails, and sanitization hooks.
- Added contract fixtures and automated tests under `cardiff/tests/` for happy-path parity, malformed input rejection, unknown-field rejection, unsafe-content rejection, and invalid asset-path handling.
- Added detailed implementation artifacts for the new slice, including `cardiff/docs/validation-contract.md` and the associated AI-DLC requirements, design, ADR, and traceability records under `cardiff/ai-dlc-docs/`.
- Updated `README.md`, `CONTRIBUTING.md`, and `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md` so the public docs reflect the current pre-alpha implementation baseline instead of the earlier bootstrap-only state.
- Added `docs/version-0-0-2-docs.md` with the full version narrative beyond this changelog summary.

### For Deletion
- `cardiff/src/cardiff/__pycache__/`
- `cardiff/src/cardiff/contract/__pycache__/`
- `cardiff/tests/__pycache__/`
- `cardiff/tests/contract/__pycache__/`
- `cardiff/**/*.pyc`

## v0.0.1

### Added or Changed
- Initialized the root public documentation for Cardiff.
- Replaced template placeholders in `README.md` with the project identity, product direction, contact information, and current bootstrap status.
- Added project-specific `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SECURITY.md` content.
- Preserved Apache 2.0 licensing in `LICENSE.txt` and filled the placeholder copyright notice.
- Added an initialization `.gitignore` to ignore `.gitignore` itself and hide internal workflow files from future commits.
- Referenced the existing project screenshot asset at `repo/images/project_screen.png`.

### For Deletion
- None from this task context.

