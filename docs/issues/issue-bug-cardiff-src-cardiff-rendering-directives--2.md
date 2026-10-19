# [BUG] [rev] QR vCard payload does not escape commas and semicolons and omits the required N property

## Summary

`build_vcard` copies identity text into vCard 3.0 properties without the backslash escaping that RFC 2426 requires. A semicolon in an organization or address line therefore changes the structure of the scanned contact. For example, the organization `Smith; Jones LLC` becomes the organization `Smith` with organizational units ` Jones LLC` and the department. The payload also has no `N` property, which RFC 2426 says "MUST be present". Validation accepts both characters, so ordinary business text triggers this. The desired outcome is a QR payload that is a well-formed vCard 3.0 object and that round-trips the identity text exactly.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `for experienced devs` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The malformed payload was reproduced from a validated request with a direct `build_vcard` call. The escaping and presence rules are quoted from RFC 2426. The existing tests that pin today's output are identified, including one assertion that conflicts with correct escaping. The content of the new `N` property needs a maintainer choice, recorded as a non-blocking open question, because the acceptance criteria hold for any of the listed options.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/directives.py`. Supporting reads:
- `cardiff/tests/rendering/test_directives.py`: `TestBuildVcard`.
- `cardiff/tests/rendering/test_pipeline.py`: `test_qr_payload_uses_original_text_while_tex_stays_escaped`.
- `cardiff/src/cardiff/contract/validation.py`: which characters validation accepts.
- External specification: RFC 2426 (vCard MIME Directory Profile, vCard 3.0), https://www.rfc-editor.org/rfc/rfc2426.txt.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-directives--2.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Escaping text values in `build_vcard`: backslash, semicolon, comma, and newline, as RFC 2426 section 4 defines `ESCAPED-CHAR`.
- Keeping the structural separators unescaped: `;` between `ORG` organization and unit, and `;` between `ADR` components.
- Emitting exactly one `N` property.
- Updating the tests that pin today's unescaped output.

Out of scope:
- vCard 4.0 or other formats.
- Line folding at 75 octets.
- Splitting `full_name` into family and given names beyond what the chosen `N` strategy needs.
- QR image size or error-correction level.
- Rejecting `;` or `,` at validation. They are legitimate business text.

## Current / Observed Behavior

Observed in the code (`cardiff/src/cardiff/rendering/directives.py` lines 231-255):
- The properties are built as `f"FN:{identity.full_name}"`, `f"TITLE:{identity.role}"`, `f"EMAIL:{identity.email}"`, `f"ORG:{identity.organization};{identity.department}"`, `f"TEL:..."`, `f"URL:..."`, `f"ADR:;;{street};;;;"` (where `street = ", ".join(identity.address_lines)`), and `f"NOTE:Pronouns: {identity.pronouns}"`.
- No value is escaped, and there is no `N:` line.
- When only `department` is set, without `organization`, no `ORG` line is emitted (lines 241-244).

Observed at runtime (Python 3.14.0). A request accepted by `validate_render_request`, with `full_name` `Doe, Jane`, `role` `Lead; Platform`, `organization` `Smith; Jones LLC`, `department` `R&D`, and `address_lines` `["Suite 5; Bldg 2", "Davao City"]`, produces this payload (CRLF shown as ` | `):

```text
BEGIN:VCARD | VERSION:3.0 | FN:Doe, Jane | TITLE:Lead; Platform | EMAIL:jane@example.com | ORG:Smith; Jones LLC;R&D | ADR:;;Suite 5; Bldg 2, Davao City;;;; | END:VCARD
```

Under RFC 2426, the `ORG` value has three components (`Smith`, ` Jones LLC`, `R&D`). The `ADR` street component ends at `Suite 5`, and ` Bldg 2, Davao City` lands in the locality component.

Specification, quoted from RFC 2426:
- section 3.1.1 (FN) and section 3.1.2 (N): "The property MUST be present in the vCard object."
- section 4, text value grammar: `ESCAPED-CHAR = "\\" / "\;" / "\," / "\n" / "\N"`.
- section 3.5.5 (ORG) example: `ORG:ABC\, Inc.;North American Division;Marketing`.

Tests that pin today's output:
- `cardiff/tests/rendering/test_directives.py` lines 262-275 assert `ORG:Analytical Engine Lab;Mathematics` and `ADR:;;123 Logic St., London;;;;`. Both stay valid with correct escaping, because those values contain no special characters.
- `test_directives.py` lines 283-306 (`test_uses_original_text_from_a_validated_request`) uses the organization `Analytical Engine Lab, Inc.` and asserts `"\\" not in vcard`. Correct escaping produces `Analytical Engine Lab\, Inc.`, so this assertion conflicts with the fix. Its purpose, per #35, is that no LaTeX escape sequences leak into the payload.

## Expected / Target Behavior

For any identity accepted by validation, the payload from `build_vcard` meets three conditions:
- Every text value has `\`, `;`, `,`, and newline escaped per RFC 2426 section 4.
- `ORG` and `ADR` use unescaped `;` only as component separators.
- Exactly one `N:` line is present.

A vCard parser reading the payload recovers `FN`, `TITLE`, `EMAIL`, the organization name, the organizational unit, and each address line exactly as written in the request. No LaTeX escape sequences appear in the payload (the #35 guarantee is preserved).

## Reproduction Steps or Validation Steps

1. From `cardiff/`, run:

   ```python
   from cardiff.contract import validate_render_request
   from cardiff.rendering import build_vcard

   result = validate_render_request({
       "identity": {"full_name": "Doe, Jane", "role": "Lead; Platform", "email": "jane@example.com",
                    "organization": "Smith; Jones LLC", "department": "R&D",
                    "address_lines": ["Suite 5; Bldg 2", "Davao City"]},
       "template": {"id": "business-card", "options": {"include_qr": True}},
   })
   print(result.accepted)
   print(build_vcard(result.request.identity))
   ```

   Run it as `python -c` or a script with `src` on `PYTHONPATH`.
2. Observe `True`, then the payload above.
3. Failing observation: `ORG:Smith; Jones LLC;R&D` contains an unescaped `;` inside the organization name, and no line starts with `N:`. After the fix, the line reads `ORG:Smith\; Jones LLC;R&D` and an `N:` line exists.

## Environment and Evidence

- **Runtime:** Python 3.14.0 on Windows 11, at commit `5caba1e`. Pure string logic, platform-independent.
- **Specification:** RFC 2426 text as quoted above.
- **Logs and stack traces:** not applicable.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/directives.py`: `build_vcard` (lines 231-255), `resolve_qr_directives` (lines 288-311). Directly observed.
- `cardiff/tests/rendering/test_directives.py`: `TestBuildVcard` (lines 253-306). Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`: `test_qr_payload_uses_original_text_while_tex_stays_escaped` (lines 676-704). It asserts `TITLE:R&D Lead`, `EMAIL:ada_lovelace@example.com`, and `URL:https://example.com/~ada`, which remain valid after escaping. Directly observed.
- `cardiff/src/cardiff/contract/validation.py`: `_validate_text_field` does not restrict `;` or `,`. Directly observed.

## Agent Handoff Notes

- The change surface is `build_vcard` plus the tests listed above.
- Search terms: `build_vcard`, `ORG:`, `ADR:`, `BEGIN:VCARD`.
- Hypothesis to verify, not an instruction: a small helper that escapes one text value, applied per component before the components are joined, keeps structural separators intact.
- Address lines: today they are joined with `", "` into the single street component. Under RFC 2426, an unescaped comma inside a component separates multiple values, so the join comma can stay as a value separator, but commas inside each line must be escaped.
- Constraints:
  - The payload must keep using the original, unescaped canonical text (#35).
  - Do not run identity text through `sanitize_text` for the vCard.
- Assumption to avoid: do not escape `:` or `@`. RFC 2426 does not require it, and doing so breaks `EMAIL` and `URL` values.

## Acceptance Criteria

- [ ] For the reproduction identity, the payload contains `ORG:Smith\; Jones LLC;R&D`.
- [ ] For the reproduction identity, the payload contains `TITLE:Lead\; Platform`.
- [ ] For the reproduction identity, the payload contains `FN:Doe\, Jane`.
- [ ] For the reproduction identity, the `ADR` street component contains `Suite 5\; Bldg 2`.
- [ ] Every payload from `build_vcard` contains exactly one line that starts with `N:`.
- [ ] For an identity whose text has no `\`, `;`, `,`, or newline, every property except the new `N` line is byte-identical to today's output.
- [ ] `test_uses_original_text_from_a_validated_request` still asserts that no LaTeX escape sequences (for example `textasciitilde`, `\&`, `\#`, `\_`) appear in the payload.
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): `python -m pytest tests/rendering -q -p no:cacheprovider`, then `tests/contract` and `tests/cli`.
- **New tests likely needed:** escaping tests in `TestBuildVcard` for `;`, `,`, and newline in each property, and an `N` presence test.
- **Manual check:** generate a QR with a semicolon in the organization (XeLaTeX render with `include_qr: true`), scan it with a phone, and confirm the organization field shows `Smith; Jones LLC`.
- **Regression checks:** the #35 guarantee (no LaTeX sequences in the payload); deterministic evidence is unaffected, because the deterministic adapter does not generate QR images.
- **Security checks:** confirm a value cannot inject an extra vCard property line. Newlines are already rejected by validation for single-line fields; the escaping also covers constructed requests.
- **Performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no vCard 4.0;
  - no line folding;
  - no new identity fields.
- **Forbidden shortcuts:**
  - Do not strip `;` or `,` from values.
  - Do not reject them at validation.
- **Compatibility:**
  - The normalized evidence `tex_fingerprint` uses a constant QR file name, so it is unaffected (inferred from `pipeline.py` lines 304-308).
  - XeLaTeX `pdf_fingerprint` changes, but it is not stable today anyway.
- **Conventions:** CRLF line endings; vCard 3.0 property order as today, with `N` placed next to `FN`.

## Risks and Review Focus

- **Correctness:** escaping must apply to values only, never to the structural `;` separators. Review `ORG` and `ADR` closely.
- **Regression:** the #35 test purpose must survive the assertion change.
- **UX:** scan a generated QR on at least one iOS and one Android device before closing.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/directives.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** what should the `N` property contain? Options:
  - all components empty (`N:;;;;`), leaving `FN` as the only name source;
  - the full name in the family-name component;
  - a heuristic split of `full_name`.

  Names vary by culture, so a split is risky. Any option satisfies the acceptance criteria.
- **Non-blocking, maintainer:** should a `department` without an `organization` produce `ORG:;<department>` instead of being dropped, as it is today?

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
