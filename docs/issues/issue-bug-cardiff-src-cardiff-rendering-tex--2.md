# [BUG] [rev] XeLaTeX adapter crashes on Windows when compiler output contains bytes the ANSI code page cannot decode

## Summary

`XeLaTeXAdapter.compile` runs `xelatex` with `text=True` and no explicit encoding, so Python decodes the compiler's UTF-8 output with the locale code page. On Windows this is usually `cp1252`. XeTeX echoes typeset text in overfull and underfull box warnings. When that text contains a character whose UTF-8 bytes are undefined in `cp1252`, decoding fails, `completed.stdout` comes back as `None`, and the adapter crashes with `AttributeError`. For example, `Á` is the bytes `C3 81`, and `0x81` is undefined in `cp1252`. A valid request with such a name or organization makes `cardiff render` exit with status `1` and print no JSON. The desired outcome is that compiler output decoding never crashes a render, on any platform or code page.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The crash was reproduced end to end through the CLI with a real XeLaTeX run on Windows. A direct `xelatex` run confirmed that the compiler writes UTF-8 bytes that `cp1252` cannot decode. The decoding call and the crashing line are directly observed. The repair surface is two `subprocess.run` calls in one module. The only open point is how to build a cross-platform regression test, and the verification plan lists workable options.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/tex.py`. Supporting reads:
- `cardiff/src/cardiff/rendering/pipeline.py`: only `RenderingError` is caught around `adapter.compile`.
- `cardiff/src/cardiff/cli.py`: the render command and its exit codes.
- `cardiff/tests/rendering/test_pipeline.py`: the XeLaTeX-gated tests.
- `.github/workflows/ci.yml`: the Windows leg with MiKTeX.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-tex--2.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

Related, text-only: #56 changes which XeLaTeX output becomes the failure diagnostic, in the same lines (`tex.py` lines 337-344 and 354-356). The two issues are independent, but whichever lands second will need a rebase.

## Scope

In scope:
- Decoding XeLaTeX stdout and stderr deterministically (for example as UTF-8 with replacement of invalid bytes) in `XeLaTeXAdapter.compile`. Applying the same change to `XeLaTeXAdapter._detect_version` is optional; see Open Questions.
- A regression test.

Out of scope:
- Choosing which output lines become the failure diagnostic (#56).
- Changing font setup or glyph coverage for non-Latin text.
- Changing the deterministic adapter.

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/rendering/tex.py` lines 325-336: `subprocess.run([...], cwd=temp_root, capture_output=True, text=True, check=False)`, with no `encoding` or `errors` argument.
- `tex.py` lines 354-356 (success path) and 338-340 (failure path) both evaluate `line.strip()` for `line in (completed.stdout, completed.stderr)`.
- `tex.py` lines 369-374: `_detect_version` also uses `text=True`. `xelatex --version` output is ASCII in practice, so this call is lower risk.
- `pipeline.py` line 379 catches only `RenderingError`, so the `AttributeError` reaches the CLI.

Observed at runtime (Windows 11, Python 3.14.0, `locale.getpreferredencoding(False)` = `cp1252`, MiKTeX-XeTeX 4.16):
- A request accepted by validation, with `identity.organization` set to 60 copies of `Á`, rendered without `--deterministic`, exits with status `1` and empty stdout.
- stderr shows `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 1357: character maps to <undefined>`, followed by a traceback ending at `tex.py` line 355: `AttributeError: 'NoneType' object has no attribute 'strip'`.
- A standalone `xelatex` run of a document with an overfull `\hbox` containing `Á` exits `0`. Its raw stdout contains the bytes `C3 81`, and decoding that stdout as `cp1252` raises `UnicodeDecodeError`.

Inferred, not reproduced:
- Other characters whose UTF-8 encoding contains `0x81`, `0x8D`, `0x8F`, `0x90`, or `0x9D` trigger the same crash when echoed. Examples are `Í`, `Ï`, `Ð`, `Ý`, and `ā`.
- When decoding does not fail, non-ASCII text in diagnostics is mojibake, because UTF-8 bytes are read as `cp1252`.
- Linux runners with a UTF-8 locale do not reproduce the crash, which is why the Linux CI legs pass.

## Expected / Target Behavior

`XeLaTeXAdapter.compile` never raises `UnicodeDecodeError` or `AttributeError` because of compiler output encoding. A request that compiles successfully renders successfully on Windows with a `cp1252` code page, even when XeLaTeX echoes non-ASCII identity text. Diagnostics contain the compiler output decoded as UTF-8, with any invalid bytes replaced rather than raising.

## Reproduction Steps or Validation Steps

Preconditions: Windows with a non-UTF-8 ANSI code page (for example `cp1252`), Python not in UTF-8 mode, and `xelatex` on `PATH`.

1. From `cardiff/`, write `accent.json` in a temporary directory with this content: `{"identity": {"full_name": "Ada Lovelace", "role": "Computing Pioneer", "email": "ada@example.com", "organization": "<the character Á repeated 60 times>"}, "template": {"id": "business-card"}, "assets": {"logo": "brand/logo.png"}}`, saved as UTF-8.
2. Run `python -m cardiff validate <tmp>/accent.json --approved-asset-root tests/fixtures/approved-assets` and observe exit `0`.
3. Run `python -m cardiff render <tmp>/accent.json --approved-asset-root tests/fixtures/approved-assets --output <tmp>/accent.pdf`.
4. Failing observation: exit status `1`, empty stdout, and stderr ending in `AttributeError: 'NoneType' object has no attribute 'strip'` preceded by a `UnicodeDecodeError` for byte `0x81`. After the fix: exit `0` and a JSON success object.

## Environment and Evidence

- **Operating system and runtime:** Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16 (MiKTeX 25.12), at commit `5caba1e`. Locale encoding `cp1252`, `sys.flags.utf8_mode` `0`.
- **Commands:** the CLI invocations above, taken from `cardiff/docs/cli-quickstart.md`.
- **Error messages:** quoted above. Absolute paths are omitted.
- **CI context:** `.github/workflows/ci.yml` runs the XeLaTeX tests on `windows-latest` with MiKTeX. The existing XeLaTeX tests use ASCII-only identity text, so they do not exercise this path.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/tex.py`: `XeLaTeXAdapter.compile` (lines 298-363) and `XeLaTeXAdapter._detect_version` (lines 365-377). Directly observed.
- `cardiff/src/cardiff/rendering/pipeline.py`: `render_request_to_pdf`, handler at line 379. Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`: `test_bundled_template_compiles_with_xelatex` (line 616) and `test_xelatex_compiles_when_the_temp_directory_contains_a_tilde` (line 637), both gated by `skipif(shutil.which("xelatex") is None)`. Directly observed.
- `.github/workflows/ci.yml`: Windows MiKTeX install (lines 46-57). Directly observed.

## Agent Handoff Notes

- Inspect the two `subprocess.run` calls in `tex.py` first; that is the whole change surface.
- Search terms: `text=True`, `capture_output`, `completed.stdout`.
- Hypothesis to verify, not an instruction: passing `encoding="utf-8", errors="replace"` instead of relying on `text=True` alone matches what XeTeX writes. Verify with TeX Live on Linux as well as MiKTeX on Windows.
- Constraints: keep the existing working-directory approach in `compile` (bare file name, `cwd=temp_root`), which exists to avoid the `~` problem documented at lines 322-324.
- Assumptions to avoid:
  - Do not assume `completed.stdout` is always a string. It was `None` in the observed crash.
  - Do not assume the Linux CI legs will catch a regression; they run with a UTF-8 locale.

## Acceptance Criteria

- [ ] On Windows with a `cp1252` locale, rendering the reproduction request with the XeLaTeX adapter returns `status` `succeeded`.
- [ ] `XeLaTeXAdapter.compile` does not raise when compiler stdout contains bytes that are invalid in the locale encoding.
- [ ] `XeLaTeXAdapter.compile` does not raise when compiler stdout contains bytes that are invalid UTF-8.
- [ ] The success-path diagnostics contain the echoed `Á` characters as `Á`, not as mojibake.
- [ ] A regression test exists that fails on the current code on the Windows CI leg.
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes on the Windows and Linux CI legs.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): `python -m pytest tests/rendering -q -p no:cacheprovider`, then `tests/contract` and `tests/cli` as a regression sweep.
- **New tests likely needed** (recommended, not yet confirmed):
  - an XeLaTeX-gated test in `cardiff/tests/rendering/test_pipeline.py` that renders an identity with a long run of `Á`. It fails before the fix on the Windows CI leg.
  - optionally, a platform-independent test using `XeLaTeXAdapter(command=...)` pointed at a stub compiler that prints the byte `0x81` and writes `cardiff-render.pdf`.
- **Manual check:** the reproduction steps on a Windows machine with `xelatex`.
- **Regression checks:** `test_xelatex_compiles_when_the_temp_directory_contains_a_tilde` still passes; failed compiles still report a TeX error diagnostic.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no change to diagnostic selection (#56);
  - no font or `fontspec` changes;
  - no change to the deterministic adapter.
- **Forbidden shortcuts:**
  - Do not set `PYTHONUTF8` or change the process-wide locale to hide the problem.
  - Do not catch `AttributeError` around the generator expressions.
- **Compatibility:**
  - Python 3.12 and 3.13;
  - TeX Live on Linux and MiKTeX on Windows.
- **Conventions:** keep the existing `RenderingError` and `TeXCompileArtifact` shapes.

## Risks and Review Focus

- **Correctness:** check that both the success and the failure branch read decoded strings.
- **Regression:** a merge with #56 could reintroduce a `None`-unsafe expression. Check both branches after rebasing.
- **Observability:** replacement characters in diagnostics are acceptable, but check that the TeX error line itself is still readable.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/tex.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** should `_detect_version` get the same decoding change for consistency, even though `xelatex --version` output is ASCII in practice? The acceptance criteria do not depend on it.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
