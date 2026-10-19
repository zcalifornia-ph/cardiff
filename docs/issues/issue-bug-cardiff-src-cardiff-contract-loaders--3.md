# [BUG] [rev] Duplicate keys in JSON and YAML requests are silently resolved to the last value

## Summary

A request document that repeats a key, such as two `email` entries under `identity`, is accepted. Only the last value is kept, and no validation issue is reported. This applies to both JSON and YAML, because `json.loads` and `yaml.safe_load` keep the last duplicate. The validation contract rejects unknown fields "so downstream CLI, batch, and API consumers cannot drift silently", but a duplicated field drops data just as silently. The desired outcome is that duplicate mapping keys at any level are rejected with a validation issue that names the duplicated field.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `for experienced devs` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

Both formats were reproduced with a direct call to the public loader. The parsing calls are directly observed. The fix needs a duplicate-detecting JSON hook and YAML constructor, which is why it is labeled for experienced contributors. The issue-code choice is recorded as a non-blocking open question with a default that keeps the existing taxonomy.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/contract/loaders.py`. Supporting reads:
- `cardiff/src/cardiff/contract/validation.py`: the strict unknown-field checks.
- `cardiff/src/cardiff/contract/errors.py`: the stable issue codes.
- `cardiff/docs/validation-contract.md`: the strictness rationale.
- `cardiff/src/cardiff/cli.py`: `_extract_template_id` parses the document a second time.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-contract-loaders--3.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Detecting duplicate keys while decoding JSON and YAML request documents, at every mapping level.
- Returning a rejected `ValidationResult` whose issue names the duplicated key path.
- Documenting the rule in `cardiff/docs/validation-contract.md`.

Out of scope:
- YAML anchors and aliases, which are not duplicates.
- Template manifest parsing.
- `_extract_template_id` in the CLI, which only reads `template.id` for status output.

## Current / Observed Behavior

Observed in the code: `cardiff/src/cardiff/contract/loaders.py` lines 348-356 (`_decode_mapping`) call `json.loads(raw_document.content)` or `yaml.safe_load(raw_document.content)` with default options. Both keep the last value for a repeated key. Nothing after decoding can detect the repeat, because the decoded `dict` holds only one entry.

Observed at runtime (Python 3.14.0, PyYAML 6.0.3), using `parse_render_request(load_request_document(src, source_name=...))`:

| Format | Input | Result |
| --- | --- | --- |
| YAML | `identity:` with `email: first@example.com` then `email: second@example.com` | `accepted`; `identity.email == "second@example.com"` |
| JSON | `"identity": {..., "email": "first@example.com", "email": "second@example.com"}` | `accepted`; `identity.email == "second@example.com"` |

Documented contract: `cardiff/docs/validation-contract.md` line 70: "Unknown fields are rejected instead of ignored so downstream CLI, batch, and API consumers cannot drift silently."

## Expected / Target Behavior

A request document that contains the same key twice in any mapping (top level, `identity`, `template`, `template.options`, or `assets`) is rejected. The `ValidationResult` has outcome `rejected` and one issue per duplicated key. The issue `field` is the key's path (for example `identity.email`), and the message says the key is duplicated. `cardiff validate` exits `1`. Documents without duplicates produce exactly the same results as today.

## Reproduction Steps or Validation Steps

1. From `cardiff/`, run:

   ```python
   from cardiff.contract import load_request_document, parse_render_request

   src = ("identity:\n  full_name: Ada\n  role: x\n  email: first@example.com\n"
          "  email: second@example.com\ntemplate:\n  id: business-card\n")
   result = parse_render_request(load_request_document(src, source_name="dup.yaml"))
   print(result.outcome, result.request.identity.email if result.request else result.issues)
   ```

2. Observe `accepted second@example.com`.
3. Repeat with the JSON equivalent and `source_name="dup.json"` and observe the same.
4. Failing observation: a document with a duplicated key is accepted and the first value is lost. After the fix, the outcome is `rejected` with an issue on `identity.email`.

## Environment and Evidence

- **Runtime:** Python 3.14.0 and PyYAML 6.0.3 on Windows 11, at commit `5caba1e`. The decoders behave the same on every platform (inferred).
- **Logs:** not applicable.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/contract/loaders.py`: `_decode_mapping` (lines 348-356), `parse_render_request` (lines 270-307). Directly observed.
- `cardiff/src/cardiff/contract/errors.py`: `ValidationCode` (lines 223-232). Directly observed.
- `cardiff/src/cardiff/contract/validation.py`: `_unknown_keys` and `_key_label` (lines 813-832) show how non-string keys are labeled. Directly observed.
- `cardiff/docs/validation-contract.md`: line 70 and the Behavior Notes section. Directly observed.
- `cardiff/tests/contract/test_validation.py`: contract tests; new tests belong here. Directly observed in part.

## Agent Handoff Notes

- Start in `_decode_mapping`.
- Hypotheses to verify, not instructions:
  - for JSON, `json.loads(..., object_pairs_hook=...)` sees every key pair in order;
  - for YAML, a `yaml.SafeLoader` subclass with an overridden `construct_mapping` can detect repeated keys before the `dict` is built.
- The parse step today raises exceptions that `parse_render_request` turns into one `contract_error` on `$` (lines 285-300). Duplicate detection needs to report the key path, so it may need to return issues rather than raise.
- YAML merge keys (`<<`): PyYAML's safe loader supports them. Decide whether a key supplied both by a merge and explicitly counts as a duplicate; see Open Questions.
- Non-string YAML keys such as `1`, `on`, or `null` are already labeled by `_key_label`; reuse it for field paths.
- Search terms: `_decode_mapping`, `safe_load`, `json.loads`, `contract_error`.

## Acceptance Criteria

- [ ] A YAML request with `identity.email` repeated is rejected.
- [ ] A JSON request with `identity.email` repeated is rejected.
- [ ] Each rejection includes an issue whose `field` is `identity.email`.
- [ ] A JSON request with the top-level key `template` repeated is rejected with an issue whose `field` is `template`.
- [ ] A YAML request with `template.options.include_qr` repeated is rejected with an issue whose `field` is `template.options.include_qr`.
- [ ] `tests/fixtures/requests/valid-request.yaml` and `valid-request.json` are still accepted.
- [ ] `cardiff/docs/validation-contract.md` states that duplicate keys are rejected.
- [ ] `python -m pytest tests/contract tests/rendering tests/cli -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites.
- **New tests likely needed:** parametrized contract tests for duplicates at each mapping level in both formats, plus a CLI test asserting exit `1` for a duplicate-key file.
- **Manual check:** `python -m cardiff validate <file with duplicate email>` exits `1` and names `identity.email`.
- **Regression checks:**
  - the BOM, non-UTF-8, and non-string-key tests (#40, #41) still pass;
  - the issue ordering from `_finalize_issues` is unchanged.
- **Security checks:** confirm that a duplicate key cannot bypass the unknown-field check, for example a supported name repeated with an unsupported value type.
- **Performance checks:** not applicable at current document sizes.

## Implementation Boundaries

- **Non-goals:**
  - no change to which fields are supported;
  - no switch away from PyYAML.
- **Forbidden shortcuts:**
  - Do not keep the first value instead of the last. Either choice drops data silently.
  - Do not use `yaml.load` with a non-safe loader.
- **Compatibility:**
  - Python 3.12 and 3.13;
  - PyYAML `>=6,<7` (`cardiff/pyproject.toml`).
- **Conventions:**
  - the stable codes in `errors.py`;
  - deterministic ordering through `_finalize_issues`.

## Risks and Review Focus

- **Security:** the YAML loader must stay a safe loader subclass.
- **Data compatibility:** existing request files that relied on last-wins become invalid. That is intended, but it should go in the changelog.
- **Documentation drift:** the contract doc must describe the new rule.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/contract/loaders.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** which issue code should be used? The existing `contract_error` keeps the public taxonomy unchanged and is the default assumed here. A new code such as `duplicate_field` would be more specific, but it changes the documented failure taxonomy.
- **Non-blocking, maintainer:** should a key supplied both through a YAML merge key (`<<`) and explicitly in the same mapping count as a duplicate?

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
