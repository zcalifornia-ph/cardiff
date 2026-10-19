# [BUG] [rev] XeLaTeX renders produce a new pdf_fingerprint on every run, so --reference-evidence always reports a mismatch

## Summary

Two XeLaTeX renders of the same request on the same machine produce PDFs with different bytes. The normalized evidence therefore differs in `pdf_fingerprint` every time. `cardiff render --reference-evidence` accepts XeLaTeX renders, and the documentation does not limit the flag to the deterministic adapter. Comparing a XeLaTeX render against evidence recorded from an identical earlier XeLaTeX render still exits `4` (reference mismatch). Setting `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE=1` for the compiler made two renders byte-identical in a local test. The desired outcome is that same-runtime XeLaTeX renders of the same request produce identical evidence, so reference comparison is meaningful for real PDFs.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `for experienced devs` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The mismatch was reproduced through the CLI with two consecutive XeLaTeX renders. The candidate mechanism was verified locally on MiKTeX: with the two environment variables set, two renders produced the same `pdf_fingerprint`. TeX Live behavior is not verified, so the verification plan requires it on the Linux CI leg. Restricting the flag to deterministic renders is recorded as a non-blocking alternative in Open Questions.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/tex.py`. Supporting reads:
- `cardiff/src/cardiff/rendering/pipeline.py`: how evidence is built.
- `cardiff/src/cardiff/cli.py`: `--reference-evidence` handling.
- `cardiff/README.md` and `cardiff/docs/cli-quickstart.md`: the flag's documentation.
- `REQUIREMENTS.md`: the acceptance baseline for reference comparison.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-tex--3.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Making `XeLaTeXAdapter` output reproducible for identical input on the same TeX runtime, for example by passing `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE=1` in the compiler subprocess environment.
- An XeLaTeX-gated test that renders twice and compares `pdf_fingerprint`.
- A one-line documentation note on what XeLaTeX reference comparison guarantees.

Out of scope:
- Cross-machine or cross-version reproducibility. `runtime_version` is part of the evidence by design, and different TeX versions produce different bytes.
- Changing the deterministic adapter or the evidence fields.
- QR image determinism. segno output is already deterministic for the same payload (inferred; not separately verified).

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/rendering/tex.py` lines 325-336 run `xelatex` without an `env` argument, so it inherits the caller's environment.
- `cardiff/src/cardiff/rendering/pipeline.py` lines 362-364 set `pdf_fingerprint` to the SHA-256 of the output PDF bytes.
- `cardiff/src/cardiff/cli.py`:
  - lines 401-423 load reference evidence for any adapter;
  - lines 496-519 compare it and return `EXIT_REFERENCE_MISMATCH` (`4`) on any difference.
- `cardiff/README.md` line 46 documents `--reference-evidence` without restricting it to `--deterministic`.
- `cardiff/docs/cli-quickstart.md` line 37 shows the flag together with `--deterministic`.
- `REQUIREMENTS.md` line 30 states that deterministic runs can compare normalized evidence.

Observed at runtime (Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16), with `tests/fixtures/requests/valid-request.yaml`:
- Two consecutive renders with `XeLaTeXAdapter` match in every evidence field except `pdf_fingerprint`.
- `cardiff render ... --reference-evidence <evidence from the first render>` without `--deterministic` exits `4`, with `"reference_comparison": {"status": "mismatch", ...}` listing only `pdf_fingerprint`.
- The PDFs contain an `/ID` array. Inference: the ID and the document dates come from the current time.
- With `SOURCE_DATE_EPOCH=1700000000` and `FORCE_SOURCE_DATE=1` set in the environment, two consecutive renders produce identical `pdf_fingerprint` values.

## Expected / Target Behavior

On a given machine and TeX runtime, rendering the same request twice with `XeLaTeXAdapter` produces the same `pdf_fingerprint`, with no environment setup by the caller. `cardiff render --reference-evidence <evidence from an earlier XeLaTeX render on the same runtime>` then exits `0` with `"status": "match"`. The caller's own environment and `os.environ` are not modified.

## Reproduction Steps or Validation Steps

1. From `cardiff/`, with `xelatex` on `PATH`, render once and capture evidence through the Python API:

   ```python
   import json
   from pathlib import Path
   from cardiff.contract import load_and_validate_request
   from cardiff.rendering import XeLaTeXAdapter, render_request_to_pdf

   assets = Path("tests/fixtures/approved-assets")
   request = load_and_validate_request(Path("tests/fixtures/requests/valid-request.yaml"),
                                       approved_asset_roots=(assets,)).request
   result = render_request_to_pdf(request, Path("<tmp>/first.pdf"),
                                  approved_asset_roots=(assets,), tex_adapter=XeLaTeXAdapter())
   Path("<tmp>/ref.json").write_text(json.dumps(result.evidence.to_dict()), encoding="utf-8")
   ```

2. Wait at least one second.
3. Run `python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output <tmp>/second.pdf --reference-evidence <tmp>/ref.json`.
4. Failing observation: exit `4`, and `reference_comparison.mismatches` lists only `pdf_fingerprint`. After the fix: exit `0` and `"status": "match"`.

## Environment and Evidence

- **Runtime:** Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16 (MiKTeX 25.12), at commit `5caba1e`.
- **Not verified:** TeX Live's handling of `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE` in the CI image. The Linux CI leg installs `texlive-xetex` (`.github/workflows/ci.yml` lines 40-44).
- **Logs:** the CLI JSON `reference_comparison` payload described above.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/tex.py`: `XeLaTeXAdapter.compile` (lines 298-363). Directly observed.
- `cardiff/src/cardiff/rendering/pipeline.py`: `NormalizedRenderEvidence` construction (lines 353-369). Directly observed.
- `cardiff/src/cardiff/cli.py`: `run_render` reference handling (lines 399-423, 496-519) and `compare_reference_evidence` (lines 555-607). Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`:
  - `test_non_deterministic_qr_renders_keep_normalized_evidence_stable` (line 365) covers TeX-source stability with a fake adapter, not PDF bytes. Directly observed by name.
  - The XeLaTeX-gated tests (lines 611-660) are where a new test fits. Directly observed.
- `cardiff/tests/rendering/test_determinism.py`: determinism tests for the deterministic adapter. Inferred from naming; not read in full.

## Agent Handoff Notes

- Inspect the `subprocess.run` call in `XeLaTeXAdapter.compile` first.
- Hypothesis to verify, not an instruction: `env={**os.environ, "SOURCE_DATE_EPOCH": "<constant>", "FORCE_SOURCE_DATE": "1"}` makes XeTeX and `xdvipdfmx` write fixed dates and a fixed `/ID`. This was verified on MiKTeX only.
- Constraint: if the caller already set `SOURCE_DATE_EPOCH`, decide deliberately whether to honor it; see Open Questions.
- Search terms: `pdf_fingerprint`, `SOURCE_DATE_EPOCH`, `reference_evidence`.
- Assumption to avoid: do not "fix" this by removing `pdf_fingerprint` from the evidence. The fingerprint is the only evidence field that reflects the actual PDF bytes.

## Acceptance Criteria

- [ ] Two consecutive `XeLaTeXAdapter` renders of `tests/fixtures/requests/valid-request.yaml` on the same machine produce equal `pdf_fingerprint` values on the Windows (MiKTeX) CI leg.
- [ ] The same holds on the Linux (TeX Live) CI leg.
- [ ] `os.environ` in the calling process is unchanged after a render.
- [ ] The reproduction steps exit `0` with `"status": "match"`.
- [ ] Deterministic-adapter evidence and `tests/fixtures/approved-samples/business-card/reference-evidence.json` are unchanged.
- [ ] `cardiff/docs/cli-quickstart.md` states that XeLaTeX reference evidence is only comparable on the same TeX runtime version.
- [ ] `python -m pytest tests/rendering tests/cli -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites.
- **New tests likely needed:** an XeLaTeX-gated test in `cardiff/tests/rendering/test_pipeline.py` that renders twice into `tmp_path` and compares `pdf_fingerprint`, plus an `os.environ` unchanged assertion.
- **Manual check:** the reproduction steps above.
- **Regression checks:** XeLaTeX renders still compile; deterministic reference evidence still matches.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no cross-version reproducibility;
  - no change to evidence fields;
  - no change to the deterministic adapter.
- **Forbidden shortcuts:**
  - Do not set the variables in `os.environ` globally.
  - Do not drop `pdf_fingerprint` from the comparison for XeLaTeX renders.
- **Compatibility:**
  - Python 3.12 and 3.13;
  - TeX Live and MiKTeX.
- **Conventions:** the subprocess call shape in `tex.py` (bare file name, `cwd=temp_root`) stays as is.

## Risks and Review Focus

- **Correctness:** confirm on TeX Live that both dates and `/ID` become stable, not only the dates.
- **Documentation drift:** the docs should say what XeLaTeX evidence comparison does and does not guarantee.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/tex.py`, `cardiff/src/cardiff/cli.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** which epoch value should be used? A fixed constant is enough for reproducibility. Honoring a caller-provided `SOURCE_DATE_EPOCH` gives the caller control over the embedded date.
- **Non-blocking, maintainer:** if TeX Live cannot be made reproducible this way, should `--reference-evidence` without `--deterministic` be rejected or warned about instead? That alternative would replace the reproducibility criteria above with a CLI usage check.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
