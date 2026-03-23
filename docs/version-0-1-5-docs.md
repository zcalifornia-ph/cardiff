# Version 0.1.5 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.5
- **Release Date:** 2026-03-24
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 (complete), template placeholder validation hardening

---

## Executive Summary

Version 0.1.5 is a small but important rendering-correctness release.
The main behavior change is that templates with unknown placeholders now fail before PDF generation instead of silently erasing missing fields and reporting success.

This release does five things:

1. adds stable render failure classification for unknown template placeholders,
2. rejects unresolved placeholders before TeX compilation starts,
3. strengthens regression coverage so placeholder tests use isolated temporary template files,
4. updates the public docs and requirements snapshot to the current repo state,
5. records the latest targeted verification baseline and current cleanup candidates.

---

## What Changed from v0.1.4

### Unknown Template Placeholders Now Fail Fast

Files involved:

- `cardiff/src/cardiff/rendering/models.py`
- `cardiff/src/cardiff/rendering/pipeline.py`

Cardiff previously substituted unknown placeholders with empty strings.
That meant a typo in a TeX template could remove content while still producing a successful render result.

This release changes that behavior:

- `RenderFailureClass` now includes `template_placeholder_unknown`,
- `_render_template_source()` now detects placeholders present in the template source but absent from the supported placeholder-value map,
- the render pipeline now returns a failed render result before any compile step starts when such placeholders are found.

The failure diagnostic reports the unresolved placeholder names directly so contributors and operators can fix the template source instead of debugging a partially blank PDF.

### Regression Tests Now Prove Compilation Never Starts

Files involved:

- `cardiff/tests/rendering/test_pipeline.py`

The placeholder regression coverage was tightened in two ways:

1. template-mutation tests now use isolated temporary `.tex` files instead of writing a fixed helper filename into the real approved template directory,
2. the tests now prove the acceptance condition from the bug report directly by asserting that:
   - the render fails with `TEMPLATE_PLACEHOLDER_UNKNOWN`,
   - `result.output_path` is `None`,
   - no output PDF is created,
   - adapter compilation is never called.

This matters because the original issue was not only about classification.
It was specifically about preventing silent degradation from reaching the PDF-generation phase.

### Public Docs And Contributor Guidance Were Realigned

Files involved:

- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `cardiff/docs/template-authoring.md`
- `docs/version-0-1-5-docs.md`

The root docs now describe the current repo state as `v0.1.5`.
They also now document the placeholder-validation contract consistently across operator, contributor, and requirements-facing surfaces.

Specific alignment updates include:

- `README.md` now points to `v0.1.5` and the latest versioned documentation note,
- `REQUIREMENTS.md` now records fail-fast placeholder rejection in the public MVP and acceptance baseline,
- `CONTRIBUTING.md` now tells contributors to use isolated temporary files when template-mutation tests need custom TeX source,
- `cardiff/docs/render-pipeline.md` now states that placeholder validation happens before compile,
- `cardiff/docs/cli-quickstart.md` now explains that render failures such as unknown placeholders stop before PDF generation,
- `cardiff/docs/template-authoring.md` now documents the approved placeholder boundary and the fail-fast rule for unsupported placeholders.

### Current Verification Snapshot

Commands run for the current repo state:

```powershell
cd d:\Programming\Repositories\cardiff\cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

Observed results:

- `tests/contract`: `9 passed`
- `tests/rendering`: `25 passed`
- `tests/cli`: `14 passed`

The rendering count is now higher than the `v0.1.4` snapshot because the placeholder regression work added two more rendering tests.

### Cleanup Candidates Carried Forward

These directories still exist in the workspace and should be removed manually by the user when appropriate:

- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/`
- `cardiff/tests/fixtures/tmp5jdz_7bl/`
- `cardiff/tests/fixtures/tmpr9v8b8nh/`
- `cardiff/pytest-cache-files-*/`
- `cardiff/tmpgremi45_/`
- `cardiff/tmpn4v7ks5z/`
- `tmphk9u2kf5/`

### Other Markdown Files

No changes were required in:

- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

Reason:

This release changes renderer correctness, contributor test guidance, and public documentation alignment, but it does not alter vulnerability disclosure policy or community conduct rules.

---

## Files Touched in This Release

- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `docs/version-0-1-5-docs.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `cardiff/docs/template-authoring.md`
- `cardiff/src/cardiff/rendering/models.py`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/tests/rendering/test_pipeline.py`

---

## Next Steps

1. Decide whether template placeholder support should eventually move to an explicit manifest-declared contract instead of staying implicit in the render pipeline helper.
2. Clean the lingering QR, pytest-cache, and orphaned temp directories before relying on broad test collection.
