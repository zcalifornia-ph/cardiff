# [BUG] [rev] load_request_document raises OSError on Linux with Python 3.12 when given request text as a string

## Summary

`load_request_document` and `load_and_validate_request` accept "a path, stream, or raw string". For a `str` input without `source_name`, the loader first calls `Path(source).exists()` to decide whether the string is a file path. On Linux with Python 3.12, which this project supports, that probe raises `OSError: [Errno 36] File name too long` for ordinary request text. Passing the bundled sample request's text is enough to trigger it, so the documented raw-string form crashes instead of being parsed. The desired outcome is that request text passed as a string is always parsed, on every supported Python version and platform.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The crash was reproduced on Ubuntu 24.04 with Python 3.12.3 using the bundled fixture text. The same call returned normally on Windows with Python 3.14.0. The probe is directly observed in one line. The existing raw-string test is identified, along with why it does not catch the problem: it passes `source_name`, which skips the probe. The CI matrix already has an Ubuntu Python 3.12 leg that a new test would run on.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/contract/loaders.py`. Supporting reads:
- `cardiff/tests/contract/test_validation.py`: `test_stream_and_raw_string_inputs_are_unchanged`.
- `cardiff/tests/fixtures/requests/valid-request.yaml`: the trigger input.
- `cardiff/pyproject.toml`: `requires-python = ">=3.12"`.
- `.github/workflows/ci.yml`: the Python 3.12 and 3.13 matrix on Ubuntu and Windows.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-contract-loaders--2.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Making the path probe in `load_request_document` unable to raise for raw request text, so that text which is not an existing file is parsed as request content.
- A regression test that passes request text without `source_name`.

Out of scope:
- Removing support for string file paths.
- Changing stream handling.
- BOM handling for in-memory strings and streams.
- CLI behavior. The CLI always passes a resolved `Path`.

## Current / Observed Behavior

Observed in the code (`cardiff/src/cardiff/contract/loaders.py` lines 243-267):

```python
candidate_path = Path(source)
if source_name is None and candidate_path.exists():
    return _load_request_file(candidate_path)
```

The `exists()` call has no error handling.

`cardiff/tests/contract/test_validation.py` lines 499-508 (`test_stream_and_raw_string_inputs_are_unchanged`) call `load_request_document(text, source_name="inline.yaml")`. Because `source_name` is set, the probe is skipped.

Observed at runtime:
- Ubuntu 24.04 (WSL), Python 3.12.3, with the text of `tests/fixtures/requests/valid-request.yaml` (315 bytes; the longest run without `/` is 305 bytes):
  - `Path(text).exists()` raises `OSError` with errno `36` (`File name too long`);
  - `load_and_validate_request(text)` raises the same `OSError`.
- Windows 11, Python 3.14.0, same text: `load_and_validate_request(text)` returns a `ValidationResult`. It is rejected only because no approved asset root was given.

Inferred, not verified: Python 3.12's `Path.exists()` re-raises `OSError` values other than "not found"-style errors, and later versions route through `os.path.exists`, which returns `False`. That would make the crash specific to Python 3.12 on platforms with a 255-byte file-name limit. It is reachable whenever a path component (text between `/` characters) exceeds that limit, which is typical for request documents.

## Expected / Target Behavior

`load_request_document(text)` and `load_and_validate_request(text)`, called with request JSON or YAML text and no `source_name`, never raise from the path probe. They parse the text as request content on Linux, macOS, and Windows with Python 3.12 and 3.13. A string naming an existing request file is still loaded from that file, as today.

## Reproduction Steps or Validation Steps

1. On Linux with Python 3.12, from `cardiff/` with dependencies installed, run:

   ```python
   from pathlib import Path
   from cardiff.contract import load_and_validate_request

   text = Path("tests/fixtures/requests/valid-request.yaml").read_text(encoding="utf-8")
   load_and_validate_request(text, approved_asset_roots=(Path("tests/fixtures/approved-assets"),))
   ```

2. Failing observation: `OSError: [Errno 36] File name too long`. After the fix, the call returns a result with outcome `accepted`.

## Environment and Evidence

- **Runtimes:**
  - reproduced on Ubuntu 24.04 (WSL) with Python 3.12.3;
  - not reproduced on Windows 11 with Python 3.14.0.
  - Commit `5caba1e`.
- **Exception:** `OSError` errno `36`, strerror `File name too long`.
- **Python 3.13 on Linux:** not tested.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/contract/loaders.py`: `load_request_document` (lines 243-267), `load_and_validate_request` (lines 310-319). Directly observed.
- `cardiff/tests/contract/test_validation.py`: `test_stream_and_raw_string_inputs_are_unchanged` (lines 499-508). Directly observed.
- `cardiff/tests/contract/test_models.py`: lines 260-264 call `load_and_validate_request` with an inline YAML string and `source_name="request.yaml"`, which also skips the probe. Directly observed.
- `.github/workflows/ci.yml` lines 18-20: the OS and Python matrix. Directly observed.

## Agent Handoff Notes

- The change surface is the three lines around `candidate_path.exists()`.
- Hypothesis to verify, not an instruction: treat `OSError` and `ValueError` from the probe as "not a path", or skip the probe when the string contains a newline, which no file path argument realistically does. Either keeps string-path support.
- Search terms: `candidate_path`, `load_request_document`, `source_name is None`.
- Constraint: callers that pass `str(path)` for an existing file must keep loading from disk, including UTF-8 BOM stripping and decode-error reporting.
- Assumption to avoid: do not assume Windows CI covers this. The Windows probe returns `False` for this input.

## Acceptance Criteria

- [ ] On the Ubuntu Python 3.12 CI leg, `load_and_validate_request(<text of valid-request.yaml>, approved_asset_roots=(<approved-assets>,))` returns outcome `accepted`.
- [ ] `load_request_document(<text>)` without `source_name` returns a document whose `content` equals the input text.
- [ ] `load_request_document(str(<path to valid-request.yaml>))` still returns a document whose `source_name` is that path.
- [ ] A new test covering the first criterion exists in `cardiff/tests/contract/`.
- [ ] `python -m pytest tests/contract -q -p no:cacheprovider` passes on all four CI legs.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): `python -m pytest tests/contract -q -p no:cacheprovider`, then `tests/rendering` and `tests/cli`.
- **New tests likely needed:** a contract test that passes the fixture text without `source_name`, and one that passes a long single-line JSON string (more than 255 bytes, no `/`).
- **Manual check:** the reproduction steps on Linux with Python 3.12.
- **Regression checks:** loading by `Path`, by `str` path, and by stream still works; the BOM and decode-error tests still pass.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no API removal;
  - no new parameters.
- **Forbidden shortcuts:**
  - Do not catch `OSError` around the whole function. A real I/O error on an existing file must still surface as today.
- **Compatibility:** Python 3.12 and 3.13 on Linux and Windows.
- **Conventions:** the module's existing `RawRequestDocument` construction.

## Risks and Review Focus

- **Correctness:** check that a string naming an existing file still loads from disk.
- **Regression:** check that `_guess_source_format` still sees the raw text when no `source_name` is given.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/contract/loaders.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** should raw strings be probed as paths at all? A string that happens to equal an existing file name is read from disk today. Separate `load_request_text` and `load_request_file` entry points would remove the ambiguity, but they change the public API and belong in a separate issue.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
