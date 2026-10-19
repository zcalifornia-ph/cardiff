# [BUG] [rev] Asset resolution accepts a directory as an asset file

## Summary

When a request asset path resolves to a directory, render-time asset resolution accepts it as the asset. An example is a directory named `logo.png` inside an approved asset root. `_resolve_asset_reference` checks only `exists()`, not that the path is a regular file. Validation accepts the path because its extension is allowed, and the deterministic render then reports success with a "logo" that is a directory. The bundled template does not place the logo yet, so nothing visibly breaks today. Any template that uses `{{ logo_path }}` would get a directory path and fail inside TeX instead of failing early. The desired outcome is that a non-file asset path fails resolution with `template_asset_missing`.

## Issue Type

Primary type: bug

Labels:
- `bug` (pre-existing)
- `good first issue` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The behavior was reproduced with a temporary approved root and the deterministic adapter. Both resolution branches (absolute and relative) are directly observed, and both use `exists()`. The change is two conditions in one function, with an existing failure class and no blocking question.

## Source Context

Path-scoped context in the current repository: `cardiff/src/cardiff/rendering/templates.py`. Supporting reads:
- `cardiff/src/cardiff/contract/validation.py`: `validate_asset_reference`.
- `cardiff/src/cardiff/rendering/pipeline.py`: the `logo_path` placeholder.
- `cardiff/src/cardiff/templates/business-card/card.tex`: the bundled template does not use `{{ logo_path }}`.
- `cardiff/docs/template-authoring.md`: `{{ logo_path }}` is a supported placeholder.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-bug-cardiff-src-cardiff-rendering-templates--3.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- Requiring that a resolved asset path is a regular file, in both the absolute and relative branches of `_resolve_asset_reference`.
- Tests for both branches.

Out of scope:
- Validating image content or format.
- Changing validation-time checks in `validate_asset_reference`, which deliberately do not touch the filesystem for relative paths.
- Placing the logo in the bundled template.

## Current / Observed Behavior

Observed in the code (`cardiff/src/cardiff/rendering/templates.py`):
- line 431 (absolute paths): `if not resolved.exists(): raise RenderingError(TEMPLATE_ASSET_MISSING, ...)`.
- line 440 (relative paths): `if asset_path.exists() and asset_path.is_relative_to(root): return asset_path`.

Neither branch checks `is_file()`.

`cardiff/src/cardiff/rendering/pipeline.py` line 415 passes the resolved path as the `logo_path` placeholder value. `cardiff/src/cardiff/templates/business-card/card.tex` does not reference `{{ logo_path }}`. `cardiff/docs/template-authoring.md` lists `{{ logo_path }}` among the supported placeholders.

Observed at runtime (Windows 11, Python 3.14.0): with an approved root containing a directory named `logo.png`, and a request with `assets.logo: logo.png`:
- `validate_render_request` returns `accepted`;
- `render_request_to_pdf` with `DeterministicTeXAdapter` returns `status` `succeeded`.

## Expected / Target Behavior

When the resolved asset path exists but is not a regular file, `render_request_to_pdf` returns `status` `failed` with `failure_class` `template_asset_missing`, and the diagnostic names the slot (for example `asset 'logo' ...`). This holds for both relative and absolute request paths and for every adapter. Regular-file assets behave exactly as today.

## Reproduction Steps or Validation Steps

1. Create a temporary approved root `<tmp>/assets` containing a directory named `logo.png`.
2. From `cardiff/`, write `<tmp>/req.json`: `{"identity": {"full_name": "Ada", "role": "x", "email": "a@b.c"}, "template": {"id": "business-card"}, "assets": {"logo": "logo.png"}}`.
3. Run `python -m cardiff render <tmp>/req.json --approved-asset-root <tmp>/assets --output <tmp>/out.pdf --deterministic`.
4. Failing observation: exit `0`, `"status": "succeeded"`. After the fix: exit `3`, `"failure_class": "template_asset_missing"`.

## Environment and Evidence

- **Runtime:** Windows 11, Python 3.14.0, at commit `5caba1e`. Platform-independent logic.
- **Commands:** adapted from `cardiff/docs/cli-quickstart.md`.
- **Logs:** not applicable.

## Relevant Files, Symbols, and Tests

- `cardiff/src/cardiff/rendering/templates.py`: `resolve_asset_paths` (lines 298-321) and `_resolve_asset_reference` (lines 422-446). Directly observed.
- `cardiff/src/cardiff/contract/validation.py`: `validate_asset_reference` (lines 377-460). Directly observed.
- `cardiff/src/cardiff/rendering/pipeline.py`: `_build_placeholder_values`, `logo_path` (line 415). Directly observed.
- `cardiff/src/cardiff/templates/business-card/card.tex`. Directly observed.
- `cardiff/tests/rendering/test_template_resolution.py`: the asset-resolution tests likely live here. Inferred from naming; not read in full.
- `cardiff/tests/rendering/test_pipeline.py`: `test_missing_asset_is_classified_before_pdf_generation` (line 330). Directly observed by name.

## Agent Handoff Notes

- Replace or extend the two `exists()` checks in `_resolve_asset_reference` with `is_file()`.
- In the relative branch, a directory under the first root should not block a regular file at the same relative path under a later root. Keep the loop semantics: skip and keep searching.
- Search terms: `_resolve_asset_reference`, `TEMPLATE_ASSET_MISSING`, `exists()`.
- Constraints: keep the existing diagnostics wording for the "outside the approved asset roots" and "could not be resolved" cases.
- Assumption to avoid: the fix does not belong in contract validation. Validation stays filesystem-independent for relative paths.

## Acceptance Criteria

- [ ] A relative asset path that resolves to a directory yields `failure_class` `template_asset_missing`.
- [ ] An absolute asset path inside an approved root that points to a directory yields `failure_class` `template_asset_missing`.
- [ ] With two approved roots, where the first contains a directory `logo.png` and the second contains a file `logo.png`, the render succeeds using the file from the second root.
- [ ] `tests/fixtures/requests/valid-request.yaml` with `tests/fixtures/approved-assets` still renders successfully.
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes from `cardiff/`.

## Test / Verification Plan

- **Existing tests to run** (from `CONTRIBUTING.md`, run from `cardiff/`): the three suites.
- **New tests likely needed:** three cases matching the first three acceptance criteria, using `tmp_path` roots and `DeterministicTeXAdapter`.
- **Manual check:** the reproduction steps above.
- **Regression checks:**
  - the missing-asset test at `test_pipeline.py` line 330;
  - the Windows absolute-path behavior from #37.
- **Security checks:** confirm the root-containment checks (`is_relative_to`) still run after `resolve()`.
- **Performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:**
  - no image validation;
  - no change to allowed extensions;
  - no template change.
- **Forbidden shortcuts:** do not skip the containment check when the path is a file.
- **Compatibility:**
  - Python 3.12 and 3.13;
  - Windows and Linux.
- **Conventions:** `RenderingError` with `RenderFailureClass.TEMPLATE_ASSET_MISSING`.

## Risks and Review Focus

- **Security:** the root-containment logic must be unchanged; review the diff of both branches.
- **Regression:** check the multi-root search order.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `cardiff/src/cardiff/rendering/templates.py` -> acceptance criteria above -> verification plan above.

## Open Questions

No open questions identified from the loaded evidence.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
