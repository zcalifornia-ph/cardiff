# Requirements

Status: pre-alpha public requirements snapshot for `v0.1.7`.

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
- normalized manifest/request evidence that stays stable across checkout path and line-ending differences
- fail-fast rejection of unknown template placeholders before PDF generation starts
- initial GitHub Actions validation for pushes and pull requests plus tag-gated release verification before distribution publishing
- package metadata aligned to the `cardiff-cli` distribution while preserving the `cardiff` console command
- normalized Apache attribution/license headers across the tracked Python source files that make up the current package and rendering-test surface

## Acceptance Baseline

- JSON and YAML single-record inputs validate against one canonical request model before rendering.
- The approved `business-card` template renders to a requested PDF path.
- CLI `validate` and `render` return actionable structured results with non-zero exits on failure.
- Deterministic runs can compare normalized evidence against the approved reference record.
- Reference-evidence comparison remains stable across equivalent checkout paths and line-ending differences.
- Templates with unknown placeholders fail before PDF generation with a stable render failure class.
- Tagged releases validate package-version metadata and rerun the targeted suites before building distributions or publishing.

## Recorded Verification

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

Expected result:

- 9 contract tests pass
- 25 rendering tests pass
- 14 CLI tests pass

## Public Source Files

- `cardiff/docs/validation-contract.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `cardiff/docs/template-authoring.md`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `cardiff/pyproject.toml`
- `docs/version-0-1-7-docs.md`
- `learn/unit-001-bolt-001a-study-guide.md`

## Next Units

- `UNIT-002`: template quality and controlled customization
- `UNIT-003`: CSV batch generation
- `UNIT-004`: FastAPI service mode
- `UNIT-005`: runtime packaging, broader CI, deployment, and ops readiness

This public snapshot intentionally keeps hidden planning and traceability files out of the root documentation surface.
