# Changelog

Status: pre-alpha; canonical contract and validation foundation landed, while rendering, CLI, batch, and API delivery work remain in progress.

## v0.0.2

### Added or Changed
- Added the nested Python project under `cardiff/` with package metadata in `cardiff/pyproject.toml`.
- Added the public package surface in `cardiff/src/cardiff/` and the first completed implementation slice for `UNIT-001 / BOLT-001A`.
- Implemented the canonical contract kernel in `cardiff/src/cardiff/contract/`, including JSON and YAML loading, required-field validation, stable failure taxonomy, asset-path guardrails, and sanitization hooks.
- Added contract fixtures and automated tests under `cardiff/tests/` for happy-path parity, malformed input rejection, unknown-field rejection, unsafe-content rejection, and invalid asset-path handling.
- Added detailed implementation artifacts for the new slice, including `cardiff/docs/validation-contract.md` and the associated AI-DLC requirements, design, ADR, and traceability records under `cardiff/ai-dlc-docs/`.
- Updated `README.md`, `CONTRIBUTING.md`, and `REQUIREMENTS.md` so the root docs reflect the current pre-alpha implementation baseline instead of the earlier bootstrap-only state.
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
