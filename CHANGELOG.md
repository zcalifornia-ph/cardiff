# Changelog

Status: pre-alpha; `UNIT-001` is complete and the repository currently contains QR-directive rendering plus deterministic/Unicode rendering clarification work.

## v0.1.3

### Added or Changed
- Reconciled the root release markers by normalizing the previous top `CHANGELOG.md` block into `v0.1.2` and advancing the public `README.md` version/docs references to `v0.1.3`.
- Clarified in `README.md` that `xelatex` is recommended for Unicode-safe local rendering and that the deterministic fallback is only suitable for ASCII-only preview/title text.
- Expanded `cardiff/tests/rendering/test_pipeline.py` coverage so deterministic mode fails clearly for non-ASCII `full_name`, `role`, `organization`, `address_lines`, and template-title inputs.
- Updated `cardiff/docs/render-pipeline.md` to document the ASCII-only limit of `DeterministicTeXAdapter` and to direct Unicode-safe local rendering to `XeLaTeXAdapter`.
- Refreshed `cardiff/tests/fixtures/approved-samples/business-card/qr-evidence-stability.pdf` in the approved sample set alongside the rendering test changes.
- Verified the targeted suite baseline for the current repo state: `tests/contract` passes (`8`), `tests/rendering` passes (`21`), and `tests/cli` currently has one failing reference-comparison test (`11` passed, `1` failed) because `reference-evidence.json` fingerprints are stale.
- Added `docs/version-0-1-3-docs.md` with the detailed release notes for this deterministic-rendering clarification update.

### For Deletion
- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/` generated QR work directory from non-deterministic rendering runs.
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/` generated QR directive test work directory.
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/` inaccessible temporary QR directories left behind by earlier runs.
- `cardiff/pytest-cache-files-*/` temporary pytest cache directories that are currently permission-denied in this workspace.
- `tmphk9u2kf5/` orphaned temporary root directory.

## v0.1.2

### Added or Changed
- Reconciled the root public docs with the current repo state, including the checked-in QR directive/rendering additions and the latest verification caveats.
- Updated `README.md` so it now documents `segno`-backed QR preprocessing, the expanded rendering test surface, and a Windows-friendly virtual-environment activation flow.
- Updated `CONTRIBUTING.md` so contributors refresh directive coverage and reference evidence when template, approved-request, or deterministic-output behavior changes.
- Recorded the current verification reality of the checked-in tree: `tests/contract` passes (`8` tests), `tests/rendering` passes (`16` tests), and `tests/cli` currently has one failing reference-comparison test because `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` is stale relative to the current manifest and request fingerprints.
- Documented that broad `python -m pytest tests -q -p no:cacheprovider` collection can fail until temporary QR work directories under `cardiff/tests/fixtures/approved-samples/business-card/` are cleaned.

### For Deletion
- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/` generated QR work directory from non-deterministic rendering runs.
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/` generated QR directive test work directory.
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/` inaccessible temporary QR directories left behind by earlier runs.
- `cardiff/pytest-cache-files-*/` temporary pytest cache directories that are currently permission-denied in this workspace.
- `tmphk9u2kf5/` orphaned temporary root directory.

## v0.1.1

### Added or Changed
- Refreshed `README.md` so its public structure aligns more closely with the repository's standard project-doc layout while preserving the existing Cardiff-specific product, roadmap, and contact content.
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
