# Requirements

Status: pre-alpha public requirements snapshot for `v0.1.0`.

## Objective

Build Cardiff as a shared rendering platform that turns validated structured identity data into print-ready PDF outputs through one reusable core exposed by a CLI first, then by batch and API surfaces.

## Current Milestone

`UNIT-001` is complete.
The current public MVP includes:

- a canonical request contract and validation kernel
- an approved `business-card` template package
- a shared render pipeline with deterministic evidence output
- CLI `validate` and `render` commands
- structured JSON status output and optional reference-evidence comparison

## Acceptance Baseline

- JSON and YAML single-record inputs validate against one canonical request model before rendering.
- The approved `business-card` template renders to a requested PDF path.
- CLI `validate` and `render` return actionable structured results with non-zero exits on failure.
- Deterministic runs can compare normalized evidence against the approved reference record.

## Recorded Verification

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
python -m pytest tests -q -p no:cacheprovider
```

Expected result:

- 8 contract tests pass
- 5 rendering tests pass
- 6 CLI tests pass
- 19 total tests pass

## Public Source Files

- `cardiff/docs/validation-contract.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `docs/version-0-1-0-docs.md`
- `learn/unit-001-bolt-001a-study-guide.md`

## Next Units

- `UNIT-002`: template quality and controlled customization
- `UNIT-003`: CSV batch generation
- `UNIT-004`: FastAPI service mode
- `UNIT-005`: runtime packaging, CI, deployment, and ops readiness

This public snapshot intentionally keeps hidden planning and traceability files out of the root documentation surface.
