# Version 0.1.0 Docs

## Quick Diagnostic Read

`v0.1.0` is the first milestone release after completing `UNIT-001`.
Cardiff now ships one coherent operator-facing slice: validated JSON/YAML input, the approved `business-card` template, a shared render pipeline, and CLI `validate` / `render` commands with deterministic evidence comparison.

## One-Sentence Objective

Document why Cardiff moved from `0.0.x` to `0.1.0` and what the completed `UNIT-001` baseline now includes.

## Why This Version Matters

`UNIT-001` is the first complete product slice rather than an isolated bolt.
The repository now has one reusable path from request validation to PDF generation that future batch and API surfaces can reuse without redefining the contract.

## Plan A / Plan B

Plan A: read `README.md`, then `REQUIREMENTS.md`, then `cardiff/docs/cli-quickstart.md`, then inspect `cardiff/src/cardiff/cli.py` and `cardiff/tests/cli/test_cli.py`.

Plan B: start with `cardiff/docs/validation-contract.md` and `cardiff/docs/render-pipeline.md`, then run the verification commands listed below, then compare the result against `REQUIREMENTS.md`.

## Artifact Map

- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `cardiff/pyproject.toml`
- `cardiff/cardiff.py`
- `cardiff/src/cardiff/__main__.py`
- `cardiff/src/cardiff/cli.py`
- `cardiff/src/cardiff/contract/`
- `cardiff/src/cardiff/rendering/`
- `cardiff/src/cardiff/templates/business-card/`
- `cardiff/tests/cli/test_cli.py`
- `cardiff/tests/contract/`
- `cardiff/tests/rendering/`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`
- `cardiff/docs/validation-contract.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `learn/unit-001-bolt-001a-study-guide.md`

## What Changed In This Version

### 1. The Release Line Moved To `v0.1.0`

The public version now reflects a completed `UNIT-001` milestone instead of staying on patch-style `0.0.x` numbering.
This is a milestone bump, not a claim that the project is feature-complete.

### 2. `UNIT-001` Is Now The Public MVP Baseline

The first finished slice now includes:

- canonical contract validation for JSON and YAML inputs
- manifest-driven template resolution for the approved `business-card` template
- deterministic render evidence generation
- CLI `validate` and `render` commands
- structured status output with stable failure classes

### 3. A Public Requirements Snapshot Now Exists

Root `REQUIREMENTS.md` now acts as the public requirements baseline for the shipped MVP surface.
It summarizes the current acceptance scope, verification commands, and the next Units without pointing readers at ignored internal workflow files.

### 4. Public Docs And Package Metadata Were Realigned

The root docs now point readers at public documentation only, and the nested Python package metadata in `cardiff/pyproject.toml` is aligned to `0.1.0` so the package and repo no longer advertise different release lines.

## Behavior Available Now

Cardiff can now:

- load JSON and YAML single-record request files into one canonical request model
- validate required identity fields, template options, and approved asset paths before rendering
- render the approved `business-card` template to a requested PDF path
- emit structured JSON status payloads for `validate` and `render`
- compare deterministic render evidence against the approved reference record
- reuse the same contract and render core across future CLI, batch, and API surfaces

## Verification

Recorded acceptance evidence for the completed `UNIT-001` milestone:

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
python -m pytest tests -q -p no:cacheprovider
python -m cardiff validate tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets
python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output tests/fixtures/approved-samples/business-card/determinism-output.pdf --deterministic --reference-evidence tests/fixtures/approved-samples/business-card/reference-evidence.json
```

Expected result:

- 8 contract tests pass
- 5 rendering tests pass
- 6 CLI tests pass
- 19 total tests pass
- the direct `validate` command returns `status: accepted`
- the direct `render` command returns `status: succeeded` and `reference_comparison.status: match`

## Known Gaps

This milestone still does not deliver:

- CSV batch processing
- FastAPI service mode
- richer template customization and print-fidelity polish beyond the first approved template package
- pinned reference-runtime parity with a real `xelatex` environment
- CI wiring, deployment packaging, and ops instrumentation surfaces

## Practice Task

Compare `REQUIREMENTS.md`, `cardiff/docs/cli-quickstart.md`, and `cardiff/tests/cli/test_cli.py`.
Then explain how the public acceptance baseline maps to the actual CLI commands and test assertions.

## Next Steps

The next approved construction targets are:

1. `UNIT-002` for template polish and controlled customization
2. `UNIT-003` for CSV batch generation
3. `UNIT-004` for FastAPI service mode
4. `UNIT-005` for runtime packaging, CI, deployment, and ops readiness

That is the path from the current CLI MVP to the broader multi-surface rendering platform.
