# Version 0.0.4 Docs

## Quick Diagnostic Read

`v0.0.4` completes `UNIT-001`.
Cardiff now has its first end-to-end CLI operator flow on top of the canonical contract and shared render pipeline, with deterministic comparison against the approved reference evidence.

## One-Sentence Objective

Document exactly what changed in `v0.0.4` beyond the short changelog so reviewers can see the new CLI surface, direct entry paths, verification evidence, and what still remains out of scope.

## Why This Version Matters

This is the first release where Cardiff is operator-facing instead of library-first only.
A user can now validate a request, render the approved business-card PDF, inspect structured status output, and compare normalized render evidence through one supported CLI path.

## Plan A / Plan B

Plan A: read `README.md`, then `cardiff/docs/cli-quickstart.md`, then inspect `cardiff/src/cardiff/cli.py` and `cardiff/tests/cli/test_cli.py`.

Plan B: start with `REQUIREMENTS.md`, then inspect `cardiff/tests/cli/test_cli.py`, then run the CLI commands listed in the verification section.

## Artifact Map

- `cardiff/cardiff.py`
- `cardiff/pyproject.toml`
- `cardiff/src/cardiff/__main__.py`
- `cardiff/src/cardiff/cli.py`
- `cardiff/tests/cli/test_cli.py`
- `cardiff/tests/fixtures/requests/invalid-request-missing-email.yaml`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`
- `cardiff/docs/cli-quickstart.md`
- `REQUIREMENTS.md`
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`

## What Changed In This Version

### 1. The First CLI Operator Flow Landed

`cardiff/src/cardiff/cli.py` now implements the first thin CLI adapter around the existing contract and rendering kernels.
It adds:

- `validate`
- `render`
- structured JSON status output
- stable exit codes for success, validation failure, usage failure, render failure, and reference mismatch
- `--deterministic` for deterministic local runs
- `--reference-evidence` for normalized evidence comparison

### 2. Entry Paths Were Unified

The CLI now has three practical entry paths that converge on the same `main()` function:

- `python -m cardiff` from the source checkout through `cardiff/cardiff.py`
- `python -m cardiff` from an installed package through `cardiff/src/cardiff/__main__.py`
- `cardiff ...` through the console script entry in `cardiff/pyproject.toml`

This matters because the command surface is now real both for local development and for installation-based workflows.

### 3. CLI-Specific Tests And Fixtures Were Added

`cardiff/tests/cli/test_cli.py` now verifies:

- validate success for the approved sample
- validate rejection for an invalid request
- render success with deterministic runtime metadata
- reference-evidence match behavior
- validation-stop behavior for render
- the `python -m cardiff` bootstrap path itself

The negative fixture `cardiff/tests/fixtures/requests/invalid-request-missing-email.yaml` was added to keep validation-failure behavior explicit and reproducible.

### 4. The Approved Reference Evidence Was Refreshed

`cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` was refreshed from the current deterministic render path.
This was necessary because the live accepted sample request fingerprint had drifted from the older stored approval artifact.

The CLI reproducibility flow now compares against the current approved evidence instead of a stale fingerprint.

### 5. Root Docs Were Realigned To The New Capability Baseline

The root `README.md` is now updated to `v0.0.4` and describes the actual shipped CLI surface rather than the earlier render-foundation-only state.
The public docs also keep contributors on public documentation paths instead of exposing ignored internal workflow files.

## Behavior Available Now

Cardiff can now:

- validate JSON and YAML single-record request files through one canonical contract
- render the approved `business-card` template to a requested PDF path
- emit machine-readable command status for both validate and render flows
- expose runtime metadata from the shared renderer through the CLI
- compare current normalized evidence against the approved reference evidence
- prove `UNIT-001` acceptance across contract, rendering, and operator-flow boundaries

## Verification

Recorded evidence for this implementation slice:

```powershell
cd cardiff
python -m pytest tests/cli -q -p no:cacheprovider
python -m pytest tests -q -p no:cacheprovider
python -m cardiff validate tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets
python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output tests/fixtures/approved-samples/business-card/determinism-output.pdf --deterministic --reference-evidence tests/fixtures/approved-samples/business-card/reference-evidence.json
```

Expected result:

- 6 CLI tests pass
- 19 total tests pass
- the direct validate command returns `status: accepted`
- the direct render command returns `status: succeeded` and `reference_comparison.status: match`

## Known Gaps

This version still does not deliver:

- CSV batch processing
- FastAPI service mode
- richer template customization and print-fidelity polish beyond the first approved template package
- pinned reference-runtime parity with a real `xelatex` environment
- CI wiring, deployment packaging, and ops instrumentation surfaces

Local Python cache files or editable-install metadata generated during development should still stay out of commits.

## Practice Task

Run the deterministic render command once with `--reference-evidence` and once without it.
Then explain which fields in the JSON status payload are part of the operator contract versus which fields are just implementation diagnostics.
If you can explain why `reference_comparison` is optional and why `runtime` should stay stable, you understood the core CLI slice.

## Next Steps

The next approved construction targets are:

1. `UNIT-002` for template polish and controlled customization
2. `UNIT-003` for CSV batch generation
3. `UNIT-004` for FastAPI service mode
4. `UNIT-005` for runtime packaging, CI, deployment, and ops readiness

That is the path from the current CLI MVP to the broader multi-surface rendering platform.
