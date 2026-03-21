# Changelog

Status: pre-alpha; `UNIT-001` is complete and the first CLI operator flow is now implemented.

## v0.1.1

### Added or Changed
- Refreshed `README.md` so its public structure aligns more closely with `agent/reference/sample-readme.md` while preserving the existing Cardiff-specific product, roadmap, and contact content.
- Added root README badges, action links, a table of contents, `Built With` badges, back-to-top anchors, and contributor-facing footer sections.
- Updated the current public documentation line from `v0.1.0` to `v0.1.1` in `README.md`, `REQUIREMENTS.md`, and `cardiff/pyproject.toml` for version coherence.
- Added `docs/version-0-1-1-docs.md` with the full documentation-release notes for this README refresh.

### For Deletion
- `cardiff/__pycache__/` generated Python bytecode cache directory.
- `cardiff/src/cardiff.egg-info/` editable-install metadata directory.
- `cardiff/src/cardiff/**/__pycache__/` generated package bytecode cache directories.
- `cardiff/tests/**/__pycache__/` generated test bytecode cache directories.
- `cardiff/**/*.pyc` generated Python bytecode files currently present in the source and test trees.

## v0.1.0

### Added or Changed
- Promoted the public release line from `v0.0.4` to `v0.1.0` now that `UNIT-001` is complete and the CLI MVP is in place.
- Added root `REQUIREMENTS.md` as the public requirements snapshot for the current implementation scope, acceptance baseline, and post-`UNIT-001` roadmap.
- Added `docs/version-0-1-0-docs.md` with milestone-level release notes for the completed `UNIT-001` baseline.
- Updated `README.md`, `CONTRIBUTING.md`, and `SECURITY.md` to align with `v0.1.0` and remove public references to ignored internal workflow paths.

### For Deletion
- None from this task context (documentation and package-metadata alignment only).

## v0.0.4

### Added or Changed
- Completed `UNIT-001 / BOLT-001C` and marked `UNIT-001` complete in the project requirements baseline.
- Added the first CLI operator flow in `cardiff/src/cardiff/cli.py` with `validate` and `render` commands, structured JSON status output, stable exit codes, deterministic-mode support, and optional reference-evidence comparison.
- Added shared entry paths for the CLI through `cardiff/src/cardiff/__main__.py`, the `cardiff` console script in `cardiff/pyproject.toml`, and the source-checkout bootstrap file `cardiff/cardiff.py`.
- Added command-level CLI coverage in `cardiff/tests/cli/test_cli.py` plus the negative fixture `cardiff/tests/fixtures/requests/invalid-request-missing-email.yaml`.
- Added operator documentation in `cardiff/docs/cli-quickstart.md`.
- Refreshed `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` so deterministic CLI comparison now matches the approved request fingerprint.
- Updated `README.md` from `v0.0.3` to `v0.0.4` and realigned the root project summary, current capability list, getting-started flow, and roadmap to the landed CLI surface.
- Updated `CONTRIBUTING.md` so contributors now maintain CLI docs/tests when they change command behavior.
- Added `docs/version-0-0-4-docs.md` with the full version-level implementation notes beyond this changelog.

### For Deletion
- Local Python cache files and editable-install metadata generated during validation runs.

## v0.0.3

### Added or Changed
- Implemented `UNIT-001 / BOLT-001B`, adding the shared render pipeline, manifest-driven template resolution, and deterministic evidence generation.
- Added the approved `business-card` template package under `cardiff/src/cardiff/templates/business-card/`.
- Added rendering tests, approved sample fixtures, and `cardiff/docs/render-pipeline.md`.
- Updated `README.md` from `v0.0.2` to `v0.0.3` to reflect the landed render baseline.

### For Deletion
- Local Python cache files or editable-install metadata generated during development should stay out of commits.

## v0.0.2

### Added or Changed
- Added the nested Python project under `cardiff/` with package metadata, a public package surface, and the first reusable implementation baseline.
- Implemented `UNIT-001 / BOLT-001A`, covering the canonical render contract, validation rules, sanitization hooks, and stable validation issue classes.
- Added contract-focused tests and fixtures under `cardiff/tests/contract/` and `cardiff/tests/fixtures/`.
- Added `cardiff/docs/validation-contract.md` and realigned the root docs to the actual Cardiff implementation baseline.

### For Deletion
- Local Python cache files generated during development should stay out of commits.

## v0.0.1

### Added or Changed
- Established the initial Cardiff repository bootstrap and public documentation baseline.
- Defined the project direction around standardized, print-ready business-card rendering from structured input.
- Prepared the repo for the nested Python implementation that landed in `v0.0.2`.

### For Deletion
- None from this task context (bootstrap-only baseline).
