# [BUG] [rev] Validation accepts control characters in identity text that XeLaTeX then rejects

## Summary

The request contract rejects newlines, backslashes, and template delimiters in business text. It accepts other ASCII control characters, such as NUL, BEL, ESC, and DEL. `cardiff validate` reports such a request as accepted. The XeLaTeX render of the same request then fails with `! Text line contains an invalid character.` and exit code `3`. The same characters also flow unchanged into the QR vCard payload. The desired outcome is that validation rejects control characters with `unsafe_content`, so a request that validates does not fail compilation because of its text.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

Four control characters were each reproduced as "validation accepted, XeLaTeX render failed" with the real CLI and the real compiler. The validation path and the unsafe-pattern list are directly observed. The fix uses an existing issue code. Whether to also reject invisible formatting characters is recorded as a non-blocking open question.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/contract/sanitization.py`. Supporting reads:
- `cardiff/src/cardiff/contract/validation.py`: `_validate_text_field`, `sanitize_render_fields`.
- `cardiff/src/cardiff/rendering/directives.py`: `build_vcard` uses the unescaped canonical text.
- `cardiff/docs/validation-contract.md`: the documented unsafe-content rule.
- `cardiff/tests/rendering/test_pipeline.py`: the constructed-request unsafe-text test.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-contract-sanitization.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Rejecting characters in Unicode category `Cc` (control) that remain in identity text after whitespace normalization, with issue code `unsafe_content` on the field path. In practice this means U+0000-U+0008, U+000E-U+001B, U+007F, and U+0080-U+009F. Tab, form feed, vertical tab, U+001C-U+001F, and U+0085 are already collapsed to spaces by `normalize_text`. CR and LF are already rejected as multi-line input.
- Applying the same rule in `sanitize_render_fields`, so constructed requests that bypass validation are also rejected before compilation.
- Updating the contract rule in `cardiff/docs/validation-contract.md`.

Out of scope:
- Asset path, template ID, and template option validation, which already use strict patterns.
- Unicode format characters (category `Cf`); see Open Questions.
- Length limits or layout fit.

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/contract/validation.py` lines 766-774 reject `\n` and `\r` in single-line fields.
- `validation.py` line 776 normalizes whitespace through `normalize_text` (`sanitization.py` lines 248-254, `re.sub(r"\s+", " ", ...)`).
- `validation.py` lines 798-808 call `reject_unsafe_text`.
- `sanitization.py` lines 236-241: `UNSAFE_TEXT_PATTERNS` contains only a backslash, `{{`, `{%`, and `%}`. No other character class is checked.
- `cardiff/src/cardiff/rendering/directives.py` lines 231-255: `build_vcard` copies identity text verbatim into the QR payload.
- `cardiff/docs/validation-contract.md` line 44 documents only backslashes, `{{`, `{%`, and `%}` as unsafe fragments.

Observed at runtime (Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16), with `identity.role` set to `Computing<CHAR>Pioneer`:

| Character | `validate_render_request` | XeLaTeX render |
| --- | --- | --- |
| U+0000 NUL | accepted | failed, `tex_compile_failed`, `! Text line contains an invalid character.` |
| U+0007 BEL | accepted | failed, same error |
| U+001B ESC | accepted | failed, same error |
| U+007F DEL | accepted | failed, same error |

The CLI shows the same split for DEL: `cardiff validate` exits `0` with `status` `accepted`, and `cardiff render` exits `3` with the TeX log line `l.10 Computing^^?`.

Also observed: U+202E (right-to-left override) and U+200B (zero-width space) are accepted by validation. Their render behavior was not tested.

## Expected / Target Behavior

`validate_render_request` rejects any identity text field (including each `address_lines` entry) that still contains a category `Cc` character after whitespace normalization. The issue has code `unsafe_content` and the field path, for example `identity.role`. `cardiff validate` then exits `1`. `sanitize_render_fields` raises `UnsafeContentError` for the same input, so `render_request_to_pdf` fails before compilation for constructed requests. Requests without control characters behave exactly as today.

## Reproduction Steps or Validation Steps

1. From `cardiff/`, write `<tmp>/ctrl.json` with `{"identity": {"full_name": "Ada Lovelace", "role": "Computing\u007fPioneer", "email": "ada@example.com"}, "template": {"id": "business-card"}, "assets": {"logo": "brand/logo.png"}}`. The `\u007f` is a JSON escape, so the file stays plain ASCII.
2. Run `python -m cardiff validate <tmp>/ctrl.json --approved-asset-root tests/fixtures/approved-assets` and observe exit `0` and `"status": "accepted"`.
3. With `xelatex` on `PATH`, run `python -m cardiff render <tmp>/ctrl.json --approved-asset-root tests/fixtures/approved-assets --output <tmp>/ctrl.pdf`.
4. Failing observation: exit `3`, `"failure_class": "tex_compile_failed"`, and a diagnostic containing `! Text line contains an invalid character.` After the fix, step 2 exits `1` with an `unsafe_content` issue on `identity.role`, and step 3 is skipped at validation.

## Environment and Evidence

- **Operating system and runtime:** Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16 (MiKTeX 25.12), at commit `5caba1e`. The TeX behavior is engine-level and not Windows-specific (inferred).
- **Commands:** adapted from `cardiff/docs/cli-quickstart.md`.
- **Error messages:** `! Text line contains an invalid character.` and `l.10 Computing^^?`, from the XeLaTeX transcript returned in the CLI diagnostics.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/contract/sanitization.py`: `UNSAFE_TEXT_PATTERNS`, `normalize_text`, `reject_unsafe_text`, `sanitize_text`. Directly observed.
- `cardiff/src/cardiff/contract/validation.py`: `_validate_text_field` (lines 736-810), `_validate_address_lines` (lines 701-733), `sanitize_render_fields` (lines 328-374). Directly observed.
- `cardiff/src/cardiff/rendering/directives.py`: `build_vcard`. Directly observed.
- `cardiff/docs/validation-contract.md`: line 44. Directly observed.
- `cardiff/tests/contract/test_security.py`: the existing unsafe-content tests are likely here. Inferred from naming; not read in full.
- `cardiff/tests/rendering/test_pipeline.py`: `test_unsafe_text_on_a_constructed_request_fails_before_compilation` (line 723). Directly observed by name.

## Agent Handoff Notes

- Start at `reject_unsafe_text` in `sanitization.py`. Both `_validate_text_field` and `sanitize_text` call it, so a check there covers validation and constructed requests.
- Search terms: `UNSAFE_TEXT_PATTERNS`, `reject_unsafe_text`, `unicodedata.category`.
- Order matters: the check must run after `normalize_text`. Otherwise tabs and other whitespace controls that are legitimately collapsed today would start being rejected.
- Constraint: reusing the existing `UnsafeContentError` message shape (`"<field> contains unsafe template or LaTeX control content"`, `sanitization.py` lines 263-265) keeps CLI issue output consistent. No existing test asserts that exact string.
- Assumption to avoid: this is not only a TeX concern. The vCard payload receives unescaped canonical text, so control characters also reach the QR code.

## Acceptance Criteria

- [ ] `validate_render_request` rejects `identity.full_name` containing U+0000 with code `unsafe_content`.
- [ ] `validate_render_request` rejects `identity.role` containing U+0007 with code `unsafe_content`.
- [ ] `validate_render_request` rejects `identity.organization` containing U+001B with code `unsafe_content`.
- [ ] `validate_render_request` rejects an `identity.address_lines` entry containing U+007F with code `unsafe_content` on `identity.address_lines[<index>]`.
- [ ] `validate_render_request` rejects `identity.email` containing U+009B with code `unsafe_content`.
- [ ] `validate_render_request` still accepts a field containing a tab, and the stored value has the tab collapsed to a space.
- [ ] `sanitize_render_fields` raises `UnsafeContentError` for a constructed `RenderRequest` whose `role` contains U+007F.
- [ ] `cardiff/docs/validation-contract.md` lists control characters among the rejected unsafe content.
- [ ] `python -m pytest tests/contract tests/rendering tests/cli -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites.
- **New tests likely needed:**
  - parametrized contract tests over the control characters in the acceptance criteria;
  - one tab-collapse regression test;
  - one constructed-request test in `cardiff/tests/rendering/test_pipeline.py` next to line 723.
- **Manual check:** the reproduction steps above, before and after.
- **Regression checks:** the fixtures in `cardiff/tests/fixtures/requests/` still validate, and non-ASCII letters such as `é` and `Á` are still accepted.
- **Security checks:** confirm that no rejected character reaches `build_vcard` through the validated path.
- **Performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no new issue code;
  - no length limits;
  - no change to asset path validation.
- **Forbidden shortcuts:**
  - Do not strip control characters silently. The contract rejects unsafe input instead of rewriting it.
  - Do not restrict text to ASCII.
- **Compatibility:**
  - Python 3.12 and 3.13.
  - Existing accepted fixtures stay accepted.
- **Conventions:** the stable issue codes in `cardiff/src/cardiff/contract/errors.py`; deterministic issue ordering through `_finalize_issues`.

## Risks and Review Focus

- **Correctness:** check that whitespace characters Python treats as `\s` are still collapsed, not rejected.
- **Regression:** check non-Latin scripts and combining marks (category `Mn`) remain accepted.
- **Documentation drift:** `cardiff/docs/validation-contract.md` must describe the new rule.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/contract/sanitization.py`, `cardiff/src/cardiff/contract/validation.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer/security:** should Unicode format characters (category `Cf`) also be rejected? Examples are the bidirectional overrides U+202A-U+202E and U+2066-U+2069, and zero-width characters such as U+200B. They are accepted today and can make printed or scanned contact details read differently from the stored text. Some of them, such as U+200D (zero-width joiner) and U+00AD (soft hyphen), have legitimate uses, so this needs a policy decision. It can be a follow-up issue.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
