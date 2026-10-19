# [BUG] [rev] Render crashes with a traceback and exit code 1 when the output PDF cannot be written

## Summary

When the PDF output path cannot be written, `cardiff render` crashes with an uncaught `OSError` traceback. This happens, for example, when `--output` names an existing directory. The CLI prints nothing to standard output and exits with status `1`, which the documented exit-code contract reserves for "validation rejected the request". Both TeX adapters write the output file outside any error handling, and `render_request_to_pdf` only catches `RenderingError`. The desired outcome is that an unwritable output path becomes an ordinary render failure: the JSON status object on stdout, failure class `render_output_invalid`, and exit code `3`.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The crash was reproduced through the real CLI with both the deterministic adapter and the XeLaTeX adapter (see Reproduction Steps). The unguarded write calls and the narrow `except RenderingError` clause are directly observed in the cited lines. `render_output_invalid` already exists and is already used for the neighboring output-directory failure, so no taxonomy decision is needed. The acceptance checks can be automated with `tmp_path` and the deterministic adapter.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/pipeline.py`. Supporting reads:
- `cardiff/src/cardiff/rendering/tex.py`: the adapter write paths.
- `cardiff/src/cardiff/rendering/models.py`: `RenderFailureClass`, `RenderingError`.
- `cardiff/src/cardiff/cli.py`: exit codes and `main`.
- `cardiff/README.md` and `cardiff/docs/cli-quickstart.md`: the documented output and exit-code contract.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-pipeline--3.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Turning `OSError` raised while the adapter writes or copies the output PDF into a failed `RenderResult` with `failure_class` `render_output_invalid`.
- Covering both `DeterministicTeXAdapter` and `XeLaTeXAdapter`.
- Tests that lock in the behavior.

Out of scope:
- Guarding against `--output` pointing at the request file or at a non-`.pdf` name.
- Changing any other failure class or exit code.
- Catching exceptions unrelated to writing the output (for example XeLaTeX output decoding, tracked separately).

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/rendering/pipeline.py` lines 280-286 wrap only `output.parent.mkdir(...)` and convert its `OSError` into `RenderingError(RENDER_OUTPUT_INVALID, ...)`.
- `pipeline.py` lines 333-342 call `adapter.compile(...)`, and the only handler is `except RenderingError` at line 379.
- `cardiff/src/cardiff/rendering/tex.py` line 280: `DeterministicTeXAdapter.compile` calls `output.write_bytes(pdf_bytes)` with no handling.
- `tex.py` line 353: `XeLaTeXAdapter.compile` calls `shutil.copyfile(compiled_pdf, output)` with no handling.
- `cardiff/src/cardiff/cli.py` lines 309-314: `main` calls the handler directly. An uncaught exception therefore ends the process with Python's default status `1`, which equals `EXIT_VALIDATION_FAILED` (line 238).

Observed at runtime (Windows 11, Python 3.14.0) with `--output` pointing at an existing directory named `out.pdf`:
- `--deterministic`: exit status `1`, empty stdout, stderr ends with `PermissionError: [Errno 13] Permission denied: '<tmp>\\out.pdf'`.
- XeLaTeX adapter (MiKTeX-XeTeX 4.16): same result.

Inferred, not reproduced: on Linux the same case raises `IsADirectoryError`. On Windows, a PDF that is currently open in a viewer that locks the file is likely to fail the same way, which makes the crash easy to hit when re-rendering.

Documented contract: `cardiff/README.md` line 48 says "Each command prints one JSON status object to standard output". Lines 53 and 55 define exit code `1` as validation rejected and exit code `3` as render failed after validation succeeded.

## Expected / Target Behavior

When the output PDF cannot be written, `render_request_to_pdf` returns a `RenderResult` with `status` `failed`, `failure_class` `render_output_invalid`, and a diagnostic that names the output path and the operating-system error. It does not raise. `cardiff render` then prints its normal JSON failure object (`status` `failed`, `failure_stage` `render`) to stdout and exits with code `3`.

## Reproduction Steps or Validation Steps

1. From `cardiff/` in a checkout with dependencies installed (`pip install -e ".[dev]"`), create a directory to act as the output path: `mkdir -p "$TMPDIR/out.pdf"` (any temporary location works).
2. Run `python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output "$TMPDIR/out.pdf" --deterministic`.
3. Print the exit status (`echo $?`).
4. Failing observation: stdout is empty, stderr shows a Python traceback ending in `PermissionError` (Windows) or `IsADirectoryError` (Linux, expected), and the exit status is `1`. After the fix, stdout holds one JSON object with `"failure_class": "render_output_invalid"` and the exit status is `3`.

## Environment and Evidence

- **Operating system and runtime:** reproduced on Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16 (MiKTeX 25.12), at commit `5caba1e`. Linux behavior is inferred from the code, not reproduced.
- **Commands:** the CLI invocation in the steps above, adapted from `cardiff/docs/cli-quickstart.md`.
- **Logs:** last stderr line `PermissionError: [Errno 13] Permission denied: '<tmp>\\out.pdf'`. The local path is replaced with `<tmp>`.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/pipeline.py`: `render_request_to_pdf`, lines 280-286, 333-342, and 379-385. Directly observed.
- `cardiff/src/cardiff/rendering/tex.py`: `DeterministicTeXAdapter.compile` (line 280) and `XeLaTeXAdapter.compile` (line 353). Directly observed.
- `cardiff/src/cardiff/rendering/models.py`: `RenderFailureClass.RENDER_OUTPUT_INVALID`, `RenderingError`. Directly observed.
- `cardiff/src/cardiff/cli.py`: `main` (lines 309-314), exit constants (lines 237-241), and `run_render` failure payload (lines 473-494). Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`: `FakeNonDeterministicAdapter` (line 264) is a pattern for an adapter-level test double. Directly observed.
- `cardiff/tests/cli/test_cli.py`: CLI test module where an exit-code test would live. Inferred from naming; not read in full.

## Agent Handoff Notes

- Start with `pipeline.py` lines 280-286. That is the existing pattern for converting an output `OSError` into `RENDER_OUTPUT_INVALID`.
- Search terms: `write_bytes`, `copyfile`, `RENDER_OUTPUT_INVALID`, `except RenderingError`.
- Data flow: `cli.run_render` -> `render_request_to_pdf` -> `adapter.compile` -> file write. The failure must be converted before it leaves `render_request_to_pdf`, because CLI callers and library callers both rely on `RenderResult`.
- Hypothesis to verify, not an instruction: wrapping the write in each adapter keeps the failure classification exact. Catching every `OSError` around `adapter.compile` in the pipeline would also mislabel unrelated adapter failures as output failures.
- Constraints: keep the public failure classes and exit codes unchanged; keep the Apache attribution header in edited modules.
- Assumptions to avoid: do not assume the directory case is the only trigger. Any write failure, such as permissions or a locked file, should take the same path.

## Acceptance Criteria

- [ ] `render_request_to_pdf` with `DeterministicTeXAdapter` and an output path that is an existing directory returns a `RenderResult` instead of raising.
- [ ] That `RenderResult` has `status` `failed`.
- [ ] That `RenderResult` has `failure_class` `render_output_invalid`.
- [ ] Its diagnostics contain the output path.
- [ ] An adapter whose output write raises `OSError` also yields `failure_class` `render_output_invalid` from `render_request_to_pdf`.
- [ ] `python -m cardiff render ... --output <existing-directory> --deterministic` exits with code `3`.
- [ ] In that case stdout is exactly one JSON object with `"status": "failed"` and `"failure_stage": "render"`.
- [ ] `python -m pytest tests/contract tests/rendering tests/cli -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md` Verification Notes, run from `cardiff/`): `python -m pytest tests/contract -q -p no:cacheprovider`, `python -m pytest tests/rendering -q -p no:cacheprovider`, `python -m pytest tests/cli -q -p no:cacheprovider`.
- **New tests likely needed:**
  - a pipeline test in `cardiff/tests/rendering/test_pipeline.py` that renders to `tmp_path / "out.pdf"` after creating it as a directory;
  - a CLI test in `cardiff/tests/cli/test_cli.py` asserting exit code `3` and the JSON payload for the same case.
- **Manual check:** the reproduction steps above, plus re-rendering while the output PDF is open in a viewer that locks files on Windows.
- **Regression checks:** normal renders still exit `0`; the existing output-directory `mkdir` failure still reports `render_output_invalid`.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:** no new CLI flags, no output-path policy (such as refusing to overwrite the request file), no changes to evidence.
- **Forbidden shortcuts:**
  - Do not add a blanket `except Exception` in `cli.main` to hide the traceback while keeping exit status `1`.
  - Do not change `EXIT_VALIDATION_FAILED` or `EXIT_RENDER_FAILED`.
- **Compatibility:**
  - Python 3.12 and 3.13.
  - Windows and Linux CI legs.
- **Conventions:** stable `RenderFailureClass` values; diagnostics as plain strings; existing test styles in each module.

## Risks and Review Focus

- **Correctness:** an over-broad handler could relabel compile or QR failures as `render_output_invalid`. Review which exceptions are caught and where.
- **Regression:** check that the partially written output file, if any, does not report success.
- **Documentation drift:** if diagnostics wording is documented anywhere, keep it aligned. No doc change is expected.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/pipeline.py`, `cardiff/src/cardiff/rendering/tex.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** should a failed write remove a partially written output file, or leave whatever the adapter managed to write? The acceptance criteria hold either way.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
