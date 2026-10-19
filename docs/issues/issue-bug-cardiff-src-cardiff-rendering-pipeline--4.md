# [BUG] [rev] QR renders fail in XeLaTeX when the output filename contains # or %

## Summary

With `include_qr: true` and the XeLaTeX adapter, the pipeline names the QR image after the output file (`<output-stem>-cardiff-qr.png`) and inserts its path, unescaped, into `\includegraphics{...}`. If the output filename contains a TeX-special character, compilation fails and `cardiff render` exits with code `3`. Examples are `card #1.pdf` and `card 100%.pdf`. The same names render fine with QR disabled or with the deterministic adapter. The desired outcome is that the output filename never affects the TeX source, so any filename the operating system accepts renders with QR enabled.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

Both failures were reproduced with the real CLI, the bundled sample request, and a real XeLaTeX compile. A control run without QR succeeded with the same `#` filename. The filename construction and the unescaped substitution are directly observed. The existing `QrInspectingNonDeterministicAdapter` test double can check the generated TeX without a TeX installation.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/pipeline.py`. Supporting reads:
- `cardiff/src/cardiff/rendering/directives.py`: `resolve_qr_directives`, `substitute_qr_directives`.
- `cardiff/tests/rendering/test_pipeline.py`: the QR cleanup tests and the `~` temp-directory test.
- `cardiff/tests/fixtures/requests/valid-request.yaml`: the request used for the reproduction.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-pipeline--4.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

Related, text-only: #38 (closed) moved the QR image into a render-scoped temporary directory. That change is why the output-stem prefix is no longer needed to keep QR file names unique.

## Scope

In scope:
- Removing characters derived from the output filename from the QR image path that is written into the TeX source.
- A regression test that uses an output filename containing `#` and `%`.

Out of scope:
- Escaping arbitrary absolute paths for TeX in general.
- The deterministic adapter, which does not generate QR images.
- QR image placement or size, which is controlled by the template's `\cardiffqr[...]` options.

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/rendering/pipeline.py` line 310: `qr_filename = f"{output.stem}-cardiff-qr.png"`.
- `pipeline.py` lines 311-323: a `tempfile.TemporaryDirectory(prefix="cardiff-qr-")` is created per render, and `resolve_qr_directives(..., work_dir=qr_work_dir, qr_filename=qr_filename)` is called.
- `cardiff/src/cardiff/rendering/directives.py` lines 306-311 write the PNG to `work_dir / qr_filename` and pass `qr_path.as_posix()` to `substitute_qr_directives`.
- `directives.py` lines 281-285 emit `\includegraphics[<options>]{<path>}` with the path unescaped.
- Evidence uses a constant name: `pipeline.py` lines 304-308 build `evidence_tex` with `CARDIFF_QR_FILENAME` (`cardiff-qr.png`), so `tex_fingerprint` does not depend on the output filename today.

Observed at runtime (Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16), rendering `tests/fixtures/requests/valid-request.yaml` (which sets `include_qr: true`):

| `--output` filename | Result |
| --- | --- |
| `card #1.pdf` | exit `3`, `tex_compile_failed`, transcript: `Illegal parameter number in definition of \@tempb` at `l.16 ...ardiff-qr-<random>/card #1-cardiff-qr.png}` |
| `card 100%.pdf` | exit `3`, `tex_compile_failed`, transcript: `! File ended while scanning use of \Gin@ii.` |
| `card #1-noqr.pdf`, request with QR disabled | exit `0` |
| `card #1.pdf` with `--deterministic` | exit `0` |

## Expected / Target Behavior

With `include_qr: true` and the XeLaTeX adapter, rendering to an output filename containing `#` or `%` succeeds. The `\includegraphics` path in the rendered TeX contains no part of the output filename. The QR temporary directory is still removed after both successful and failed renders. `tex_fingerprint` in the normalized evidence is unchanged for the bundled sample request.

## Reproduction Steps or Validation Steps

1. From `cardiff/`, with `xelatex` on `PATH`, run `python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output "<tmp>/card #1.pdf"`.
2. Observe exit `3` and `"failure_class": "tex_compile_failed"`.
3. Repeat with `--output "<tmp>/card 100%.pdf"` and observe the same result.
4. Control: repeat step 1 with `--deterministic` and observe exit `0`.
5. Failing observation: steps 1 and 3 fail only because of the output filename. After the fix, both exit `0` and write the PDF.

## Environment and Evidence

- **Operating system and runtime:** Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16 (MiKTeX 25.12), at commit `5caba1e`. The TeX parsing behavior is engine-level, so Linux is expected to behave the same (inferred).
- **Commands:** adapted from `cardiff/docs/cli-quickstart.md`.
- **Logs:** quoted from the XeLaTeX transcript in the CLI diagnostics; the random temporary directory suffix is elided.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/pipeline.py`: `render_request_to_pdf`, lines 296-331. Directly observed.
- `cardiff/src/cardiff/rendering/directives.py`: `CARDIFF_QR_FILENAME`, `resolve_qr_directives`, `substitute_qr_directives`. Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`:
  - `QrInspectingNonDeterministicAdapter` (line 750), `test_non_deterministic_qr_render_cleans_up_qr_image_after_success` (line 795), and `test_non_deterministic_qr_render_cleans_up_qr_image_after_compile_failure` (line 820). Directly observed by name and line.
  - `test_xelatex_compiles_when_the_temp_directory_contains_a_tilde` (line 637): shows that a `~` in the temporary directory path already works. Directly observed.
  - `test_non_deterministic_qr_renders_keep_normalized_evidence_stable` (line 365). Directly observed by name.

## Agent Handoff Notes

- Inspect `pipeline.py` line 310 first.
- Hypothesis to verify, not an instruction: because each render gets its own temporary directory, `CARDIFF_QR_FILENAME` can be used as the file name, and the output stem is no longer needed.
- Remaining exposure: the temporary directory path itself comes from `TMP`/`TEMP`/`TMPDIR`, which a user could set to a path containing `#` or `%`. Decide whether to cover that here or in a follow-up; see Open Questions.
- Search terms: `qr_filename`, `cardiff-qr`, `includegraphics`.
- Constraints:
  - keep the QR image out of the output directory (#38);
  - keep `tex_fingerprint` stable;
  - keep the `~` temp-directory test passing.
- Assumption to avoid: the problem is not in `\includegraphics` options. The options come from the template, not from the user.

## Acceptance Criteria

- [ ] With the XeLaTeX adapter and `include_qr: true`, rendering the sample request to `card #1.pdf` returns `status` `succeeded`.
- [ ] With the XeLaTeX adapter and `include_qr: true`, rendering the sample request to `card 100%.pdf` returns `status` `succeeded`.
- [ ] With a non-deterministic test adapter, the rendered TeX for output `card #1.pdf` contains no `#` inside the `\includegraphics{...}` path.
- [ ] The QR cleanup tests at `test_pipeline.py` lines 795 and 820 still pass.
- [ ] `tex_fingerprint` for `valid-request.yaml` with a non-deterministic adapter is unchanged from before the fix.
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes from `cardiff/` on the Windows and Linux CI legs.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites, especially `tests/rendering`.
- **New tests likely needed:**
  - a TeX-free test using `QrInspectingNonDeterministicAdapter` with output name `card #1.pdf`;
  - an XeLaTeX-gated test that compiles to `card #1.pdf` and `card 100%.pdf`.
- **Manual check:** the reproduction steps above.
- **Regression checks:** QR cleanup after success and failure; evidence stability.
- **Security checks:** confirm the QR image still never lands beside the output (#38).
- **Performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no change to the vCard content;
  - no change to the deterministic adapter;
  - no change to template syntax.
- **Forbidden shortcuts:**
  - Do not reject output filenames containing `#` or `%` at the CLI. The operating system allows them.
  - Do not write the QR image beside the output again.
- **Compatibility:**
  - Python 3.12 and 3.13;
  - TeX Live and MiKTeX.
- **Conventions:** existing test-double patterns in `test_pipeline.py`.

## Risks and Review Focus

- **Regression:** the evidence fingerprint and QR cleanup behavior from #38.
- **Correctness:** check whether any other user-controlled string reaches the TeX source unescaped on this path.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/pipeline.py`, `cardiff/src/cardiff/rendering/directives.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** should this issue also make the QR path safe when the system temporary directory itself contains `#` or `%`? One option is to write the QR image next to the `.tex` file inside the adapter's working directory and reference it by a bare name. The acceptance criteria above only cover characters coming from the output filename.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
