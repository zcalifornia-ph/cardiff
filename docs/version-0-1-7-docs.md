# Version 0.1.7 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.7
- **Release Date:** 2026-03-24
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 maintenance and release-alignment update

---

## Executive Summary

Version 0.1.7 is a source-attribution normalization and release-documentation alignment update.
The main goal of this release is to make the maintained Cardiff Python source surface carry the required in-file attribution and Apache-2.0 text consistently while keeping the public release markers, contribution guidance, and package metadata aligned to the same version line.

This release does five things:

1. normalizes the required attribution/license header across the tracked Python files that were still missing it,
2. advances the public release markers from `v0.1.6` to `v0.1.7`,
3. keeps `cardiff/pyproject.toml` aligned with the new release line so tag-gated publish validation still matches package metadata,
4. documents the attribution-header expectation for future Python-source contributions,
5. records a fresh targeted verification snapshot and the current cleanup candidates.

---

## What Changed from v0.1.6

### Missing Attribution Headers Were Normalized Across The Remaining Tracked Python Files

Files involved:

- `cardiff/src/cardiff/paths.py`
- `cardiff/src/cardiff/rendering/__init__.py`
- `cardiff/src/cardiff/rendering/directives.py`
- `cardiff/src/cardiff/rendering/models.py`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/src/cardiff/rendering/templates.py`
- `cardiff/src/cardiff/rendering/tex.py`
- `cardiff/tests/rendering/test_determinism.py`
- `cardiff/tests/rendering/test_directives.py`
- `cardiff/tests/rendering/test_pipeline.py`
- `cardiff/tests/rendering/test_template_resolution.py`

Earlier Cardiff Python files already carried the repository attribution block and embedded Apache license text, but these 11 tracked files still did not.
This release normalizes them to the same format already used elsewhere in the project:

- repository attribution text first,
- full Apache-2.0 license text in comment form,
- file-specific `[path]` and description block,
- original module body preserved below the header.

This is a maintenance/compliance update, not a behavior change.
No render, validation, CLI, or workflow semantics were intentionally modified by this normalization pass.

### Public Release Markers And Package Metadata Were Advanced Together

Files involved:

- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `cardiff/pyproject.toml`
- `docs/version-0-1-7-docs.md`

The repo now consistently points to `v0.1.7` as the current public release line.

Specific alignment work:

- `README.md` now advertises `v0.1.7` and explicitly mentions the tracked-source attribution normalization,
- `REQUIREMENTS.md` now labels the public requirements snapshot as `v0.1.7`,
- `CHANGELOG.md` now records this release as the latest version entry,
- `cardiff/pyproject.toml` now uses package version `0.1.7` so release tags and metadata stay consistent.

This matters because the checked-in release workflow rejects mismatched tags before publishing.
Allowing docs and package metadata to drift again would recreate the exact class of release confusion that `v0.1.6` was intended to reduce.

### Contribution Guidance Now Explicitly Protects Source Attribution Consistency

Files involved:

- `CONTRIBUTING.md`

This release adds one contributor-facing rule that was previously implicit:

- when contributors add or modify tracked Python source files, they must preserve the required attribution header and embedded Apache-2.0 text.

The release-tag example in `CONTRIBUTING.md` was also advanced to `v0.1.7 -> 0.1.7` so the documented example matches the live package metadata again.

### README Versioned-Docs References Were Refreshed

Files involved:

- `README.md`

The root README already described Cardiff accurately, so this release does not replace its overall structure.
Instead, it updates the release-facing parts that would otherwise become stale:

- version marker,
- status summary,
- repository layout list,
- latest versioned-doc reference under the documentation section.

That keeps the README useful as the fastest public orientation document instead of letting it lag one release behind the real repo state.

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

These targeted suites remain the current high-signal verification baseline for Cardiff's public CLI, contract, and rendering surface.

### Cleanup Candidates Carried Forward

These directories still exist in the workspace and should be removed manually by the user when appropriate:

- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-uxq_h5e2/`
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-xymbgoy7/`
- `cardiff/tests/fixtures/tmp5jdz_7bl/`
- `cardiff/tests/fixtures/tmpr9v8b8nh/`
- `cardiff/pytest-cache-files-6m2fab6s/`
- `cardiff/pytest-cache-files-73ljzvxn/`
- `cardiff/pytest-cache-files-a6saqzj0/`
- `cardiff/pytest-cache-files-cucgfg1_/`
- `cardiff/pytest-cache-files-itctf5rq/`
- `cardiff/pytest-cache-files-iusr931u/`
- `cardiff/pytest-cache-files-qyz2mto6/`
- `cardiff/pytest-cache-files-r82e4azx/`
- `cardiff/tmpgremi45_/`
- `cardiff/tmpn4v7ks5z/`
- `tmphk9u2kf5/`

### Other Markdown Files

No changes were required in:

- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

Reason:

This release changes source attribution consistency, release markers, and contributor/process documentation.
It does not change vulnerability disclosure flow or community-conduct policy.

---

## Files Touched in This Release

- `cardiff/src/cardiff/paths.py`
- `cardiff/src/cardiff/rendering/__init__.py`
- `cardiff/src/cardiff/rendering/directives.py`
- `cardiff/src/cardiff/rendering/models.py`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/src/cardiff/rendering/templates.py`
- `cardiff/src/cardiff/rendering/tex.py`
- `cardiff/tests/rendering/test_determinism.py`
- `cardiff/tests/rendering/test_directives.py`
- `cardiff/tests/rendering/test_pipeline.py`
- `cardiff/tests/rendering/test_template_resolution.py`
- `cardiff/pyproject.toml`
- `README.md`
- `CHANGELOG.md`
- `REQUIREMENTS.md`
- `CONTRIBUTING.md`
- `docs/version-0-1-7-docs.md`

---

## Next Steps

1. Decide whether attribution normalization should be enforced automatically through a repo script or lint-style check instead of relying on manual review.
2. Remove the carried-forward transient directories listed above so broad test collection and repository scans stop tripping over stale permission-denied artifacts.
3. Continue `UNIT-002` planning with the source-attribution baseline and release markers now back in sync.
