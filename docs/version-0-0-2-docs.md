# Version 0.0.2 Docs

## Quick Diagnostic Read

`v0.0.2` moves Cardiff from a repository bootstrap into a real pre-alpha implementation baseline.
The repository now contains a Python package, a completed `UNIT-001 / BOLT-001A` contract kernel, contract tests, fixtures, and supporting design and traceability artifacts.

## One-Sentence Objective

Document exactly what changed in `v0.0.2` beyond the short changelog so reviewers can see the code surface, validation behavior, evidence, and remaining gaps.

## Why This Version Matters

This version establishes the first reusable core that later CLI, batch, and API entry points can all share.
Without this contract kernel, every future interface would risk schema drift, inconsistent validation, and weak asset or content safety.

## Plan A / Plan B

Plan A: start with `README.md`, then read `cardiff/docs/validation-contract.md`, then inspect `cardiff/src/cardiff/contract/`.

Plan B: start with the tests in `cardiff/tests/contract/`, then read the validation contract doc, then inspect the implementation modules.

## Artifact Map

- `cardiff/pyproject.toml`
- `cardiff/src/cardiff/__init__.py`
- `cardiff/src/cardiff/contract/__init__.py`
- `cardiff/src/cardiff/contract/errors.py`
- `cardiff/src/cardiff/contract/loaders.py`
- `cardiff/src/cardiff/contract/models.py`
- `cardiff/src/cardiff/contract/sanitization.py`
- `cardiff/src/cardiff/contract/validation.py`
- `cardiff/tests/conftest.py`
- `cardiff/tests/contract/test_models.py`
- `cardiff/tests/contract/test_validation.py`
- `cardiff/tests/contract/test_security.py`
- `cardiff/tests/fixtures/requests/valid-request.json`
- `cardiff/tests/fixtures/requests/valid-request.yaml`
- `cardiff/tests/fixtures/approved-assets/README.md`
- `cardiff/docs/validation-contract.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/domain-design.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/logical-design.md`
- `cardiff/ai-dlc-docs/design-artifacts/UNIT-001/adr/bolt-001a-adr.md`
- `cardiff/ai-dlc-docs/traceability/UNIT-001/bolt-001a-traceability.md`

## What Changed In This Version

### 1. Nested Python Project Added

The repository now includes a real Python project under `cardiff/` instead of only root-level planning docs.
`cardiff/pyproject.toml` defines the package metadata, Python requirement, and minimal dependencies for the current stage.

### 2. Canonical Contract Kernel Implemented

The `cardiff/src/cardiff/contract/` package now provides the first reusable domain surface for single-record rendering requests.
This surface is intentionally framework-agnostic so later Typer and FastAPI adapters can call it without owning their own schema logic.

### 3. Validation And Safety Rules Added

The current implementation supports:

- JSON and YAML parity into one canonical request structure
- required identity-field enforcement
- unknown top-level and template-option rejection
- template ID validation
- approved-root and approved-extension checks for asset references
- sanitization hooks for business text that later enters LaTeX rendering

### 4. Tests And Fixtures Added

The version now contains contract-focused tests and deterministic fixtures under `cardiff/tests/`.
These tests cover happy-path parsing, malformed input handling, unsupported-field rejection, invalid asset paths, and seeded unsafe-content rejection.

### 5. AI-DLC Construction Artifacts Added

This version also includes the supporting design and execution trail for `UNIT-001 / BOLT-001A`:

- domain design
- logical design
- accepted ADR
- traceability record
- updated requirements evidence

### 6. Root Docs Realigned

The root `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `REQUIREMENTS.md` now describe the actual pre-alpha implementation baseline instead of the older bootstrap-only state.

## Behavior Available Now

Cardiff can now accept a structured single-record request with:

- `identity`
- `template`
- optional `assets`

The current implementation enforces required identity fields:

- `full_name`
- `role`
- `email`

The current implementation also recognizes these stable issue classes:

- `contract_error`
- `unknown_field`
- `missing_required`
- `invalid_type`
- `invalid_template`
- `invalid_asset_path`
- `unsafe_content`

## Verification

Recorded evidence for this implementation slice:

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
```

Expected result:

- 8 contract tests pass

## Known Gaps

This version does not yet deliver:

- PDF rendering
- template resolution
- CLI commands
- CSV batch processing
- FastAPI service mode
- deployment packaging and CI wiring

The current workspace also contains generated Python cache artifacts that should be removed before a clean commit:

- `cardiff/src/cardiff/__pycache__/`
- `cardiff/src/cardiff/contract/__pycache__/`
- `cardiff/tests/__pycache__/`
- `cardiff/tests/contract/__pycache__/`
- `cardiff/**/*.pyc`

## Practice Task

Review `cardiff/tests/contract/test_security.py` and explain which assertions protect against unsafe content versus unsafe file access.
If you can map each assertion to a stable validation code, you understand the current contract slice.

## Next Steps

The next approved construction targets are:

1. `BOLT-001B` for render pipeline and template resolution
2. `BOLT-001C` for the CLI operator flow

That is the path from this contract baseline to the first real end-to-end render.
