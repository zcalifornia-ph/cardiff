# [BUG] [rev] Malformed template manifests and entrypoints crash the render instead of failing with template_manifest_invalid

## Summary

Template packages loaded through `--template-root` (or `render_request_to_pdf(template_root=...)`) are validated only partly. A `manifest.json` whose top level is not a JSON object crashes the render with `AttributeError`. An entrypoint `.tex` file that is not UTF-8 crashes it with `UnicodeDecodeError`. Both escape `render_request_to_pdf`, so the CLI exits with status `1` and prints no JSON. Separately, `manifest_version: true` and zero or negative page sizes are accepted, and the deterministic adapter writes a PDF with an empty, inverted MediaBox. The desired outcome is that every malformed manifest or entrypoint fails with `template_manifest_invalid`.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `good first issue` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

All three cases were reproduced with throwaway template roots and the deterministic adapter (see Reproduction Steps). The type checks and the unguarded reads are directly observed in two functions. `template_manifest_invalid` already exists for exactly this purpose. The tests can follow the existing patterns in `cardiff/tests/rendering/test_template_resolution.py`, and no TeX installation is needed.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/templates.py`. Supporting reads:
- `cardiff/src/cardiff/rendering/pipeline.py`: where the entrypoint is read.
- `cardiff/src/cardiff/rendering/models.py`: `TemplateDescriptor`, `RenderFailureClass`.
- `cardiff/src/cardiff/rendering/tex.py`: `_build_minimal_pdf` writes the page size.
- `cardiff/docs/render-pipeline.md`: the template directory contract.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-templates--2.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- In `_load_descriptor`:
  - reject a manifest whose top-level JSON value is not an object;
  - reject `bool` values for the integer and number fields;
  - require `page_width_in` and `page_height_in` to be finite and greater than zero.
- In the pipeline, convert a non-UTF-8 (or unreadable) entrypoint into `template_manifest_invalid`.
- Tests for each case.

Out of scope:
- New manifest fields or a schema library.
- Validating `sample_request`.
- Changing the bundled `business-card` manifest.
- Template content checks beyond placeholders (already covered by `template_placeholder_unknown`).

## Current / Observed Behavior

Observed in the code:
- `cardiff/src/cardiff/rendering/templates.py` lines 354-360 catch `OSError` and `json.JSONDecodeError` when loading the manifest.
- Lines 371-377 then call `payload.get(field_name)`, which assumes `payload` is a `dict`.
- Lines 362-370 type-check with `isinstance(value, int)` and `isinstance(value, (int, float))`. In Python, `bool` is a subclass of `int`, so `true` passes.
- No range check exists for `page_width_in` or `page_height_in`.
- `cardiff/src/cardiff/rendering/pipeline.py` line 289: `resolved_template.entrypoint_path.read_text(encoding="utf-8")` with no error handling. The handler at line 379 catches only `RenderingError`.

Observed at runtime (Windows 11, Python 3.14.0), using a template root with one template `custom`, the deterministic adapter, and a request selecting `custom`:

| Template package | Result |
| --- | --- |
| `manifest.json` is `[]` | uncaught `AttributeError: 'list' object has no attribute 'get'` |
| `manifest_version: true`, `page_width_in: 0`, `page_height_in: -2`, otherwise valid | `status` `succeeded`; the PDF has `/MediaBox [0 0 0.00 -144.00]` |
| valid manifest, `card.tex` starts with bytes `FF FE` | uncaught `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0` |

## Expected / Target Behavior

For each package in the table, `render_request_to_pdf` returns a `RenderResult` with `status` `failed` and `failure_class` `template_manifest_invalid`, and the diagnostic names the problem. It never raises. `cardiff render --template-root ...` exits `3` with its JSON failure object. A valid manifest, including the bundled `business-card` manifest, behaves exactly as today.

## Reproduction Steps or Validation Steps

1. Create `<tmp>/root/custom/manifest.json` containing `[]` and `<tmp>/root/custom/card.tex` containing `{{ full_name }}`.
2. From `cardiff/`, write `<tmp>/custom.json`: `{"identity": {"full_name": "Ada", "role": "x", "email": "a@b.c"}, "template": {"id": "custom"}}`.
3. Run `python -m cardiff render <tmp>/custom.json --template-root <tmp>/root --output <tmp>/out.pdf --deterministic` and observe exit status `1`, empty stdout, and a traceback ending in `AttributeError`.
4. Replace `manifest.json` with `{"template_id": "custom", "manifest_version": true, "display_name": "d", "entrypoint": "card.tex", "output_format": "pdf", "page_width_in": 0, "page_height_in": -2}`, rerun step 3, and observe exit `0`.
5. Set `page_width_in` to `3.5`, `page_height_in` to `2`, and `manifest_version` to `1`. Write `card.tex` as the bytes `FF FE` followed by `{{ full_name }}`. Rerun step 3 and observe exit `1` with a `UnicodeDecodeError` traceback.
6. Failing observation: steps 3 and 5 crash, and step 4 succeeds. After the fix, all three exit `3` with `"failure_class": "template_manifest_invalid"`.

## Environment and Evidence

- **Runtime:** Windows 11, Python 3.14.0, at commit `5caba1e`. Platform-independent logic.
- **Commands:** adapted from `cardiff/README.md` (`--template-root`) and `cardiff/docs/cli-quickstart.md`.
- **Error messages:** quoted above. Temporary paths are omitted.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/templates.py`: `resolve_template` (lines 245-295), `_load_descriptor` (lines 353-410), `_validate_string_list` (lines 413-419). Directly observed.
- `cardiff/src/cardiff/rendering/pipeline.py`: entrypoint read at line 289; handler at line 379. Directly observed.
- `cardiff/src/cardiff/rendering/models.py`: `TemplateDescriptor.page_width_pt` and `page_height_pt`; `RenderFailureClass.TEMPLATE_MANIFEST_INVALID`. Directly observed.
- `cardiff/src/cardiff/rendering/tex.py`: `_build_minimal_pdf` writes `/MediaBox [0 0 {width_pt:.2f} {height_pt:.2f}]`. Directly observed.
- `cardiff/tests/rendering/test_template_resolution.py`: existing template-resolution tests; new tests belong here. Inferred from naming; not read in full.

## Agent Handoff Notes

- Start with `_load_descriptor`. Add an `isinstance(payload, dict)` check before the field loop.
- Exclude `bool` explicitly (`isinstance(value, bool)`) for `manifest_version`, `page_width_in`, and `page_height_in`.
- For page sizes, `math.isfinite` together with `> 0` covers `NaN` and `Infinity`, which Python's `json.loads` accepts.
- For the entrypoint read at `pipeline.py` line 289, catching `UnicodeDecodeError` and `OSError` and raising `RenderingError(TEMPLATE_MANIFEST_INVALID, ...)` matches the manifest-loading pattern. Moving the read into `resolve_template` is an alternative, but it is not required.
- Search terms: `_load_descriptor`, `required_fields`, `read_text(encoding="utf-8")`, `TEMPLATE_MANIFEST_INVALID`.
- Constraint: keep the existing diagnostic texts for the cases that already fail, because tests may assert them.

## Acceptance Criteria

- [ ] A template whose `manifest.json` is `[]` yields `failure_class` `template_manifest_invalid` from `render_request_to_pdf`.
- [ ] A manifest with `manifest_version: true` yields `template_manifest_invalid`.
- [ ] A manifest with `page_width_in: 0` yields `template_manifest_invalid`.
- [ ] A manifest with `page_height_in: -2` yields `template_manifest_invalid`.
- [ ] A manifest with `page_width_in: NaN` yields `template_manifest_invalid`.
- [ ] A template whose entrypoint is not valid UTF-8 yields `template_manifest_invalid`.
- [ ] In none of these cases does `render_request_to_pdf` raise an exception.
- [ ] The bundled `business-card` template still renders with `tests/fixtures/requests/valid-request.yaml`.
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites.
- **New tests likely needed:** parametrized cases in `cardiff/tests/rendering/test_template_resolution.py` that write each malformed package under `tmp_path`.
- **Manual check:** the reproduction steps above.
- **Regression checks:**
  - the bundled template and the deterministic reference evidence (`tests/fixtures/approved-samples/business-card/reference-evidence.json`) still match;
  - `manifest_fingerprint` is unchanged, because the bundled manifest is unchanged.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no new manifest fields;
  - no JSON Schema dependency;
  - no change to the bundled manifest.
- **Forbidden shortcuts:**
  - Do not coerce `bool` to `int`.
  - Do not clamp invalid page sizes to defaults.
- **Compatibility:** integer page sizes (for example `2`) stay accepted, because the bundled manifest uses `2.0` and other packages may use `2`.
- **Conventions:** raise `RenderingError` with `RenderFailureClass.TEMPLATE_MANIFEST_INVALID`, as the rest of `_load_descriptor` does.

## Risks and Review Focus

- **Regression:** check that `isinstance(value, (int, float))` still accepts integer page sizes after `bool` is excluded.
- **Correctness:** check that the entrypoint read failure is not reported as `template_not_found`.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/templates.py`, `cardiff/src/cardiff/rendering/pipeline.py` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** should there also be an upper bound on page sizes? The acceptance criteria only require finite positive values.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
