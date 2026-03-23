# Version 0.1.4 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.4
- **Release Date:** 2026-03-23
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 (complete), normalized evidence portability

---

## Executive Summary

Version 0.1.4 is a focused reproducibility and public-doc alignment release.
The main behavior change is that approved reference-evidence comparison is now stable across equivalent checkouts instead of drifting on path-only or line-ending-only differences.

This release does five things:

1. normalizes manifest fingerprints from parsed manifest JSON instead of raw checked-out bytes,
2. normalizes request fingerprints from the canonical request payload without source metadata,
3. adds regression coverage that fails if checkout path or line-ending details leak back into approved evidence,
4. refreshes the approved reference-evidence record and restores the CLI comparison path to exit code `0`,
5. advances the root public docs to `v0.1.4`, including a generic `venv` quickstart example and an updated requirements snapshot.

---

## What Changed from v0.1.3

### Root Release Markers And Public Doc Alignment

Files involved:

- `README.md`
- `CHANGELOG.md`
- `REQUIREMENTS.md`
- `docs/version-0-1-4-docs.md`

The root public docs now describe the current repo state as `v0.1.4`.
This release keeps the existing `v0.1.3` record intact and adds a new versioned note for the normalized-evidence change set.

The root quickstart in `README.md` also now uses a generic `venv` example instead of an ignored local-environment path name.
That keeps the public documentation aligned with the repo rule against surfacing ignored local workflow paths in the published root docs.

### Reference Evidence Is Now Portable Across Equivalent Checkouts

Files involved:

- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`

The render pipeline now normalizes evidence inputs before hashing them:

- the manifest fingerprint is derived from canonicalized parsed JSON instead of raw manifest file bytes,
- the request fingerprint is derived from `render_request.to_dict()` instead of a payload that includes source-path metadata.

This matters because the prior behavior could report a false reference mismatch when:

- the same manifest was checked out with different line endings,
- the same request was loaded from a different absolute path,
- the approved evidence file was refreshed on one machine and compared on another.

The approved `reference-evidence.json` fixture was refreshed to the normalized manifest and request fingerprints produced by the new behavior.

### Regression Coverage For Future Regressions

Files involved:

- `cardiff/tests/rendering/test_determinism.py`

Two determinism regressions now protect this behavior:

1. `test_request_fingerprint_ignores_source_metadata()` verifies that changing `source_name` and `source_format` does not change normalized evidence.
2. `test_manifest_fingerprint_ignores_line_ending_differences()` verifies that equivalent manifest JSON with different line endings produces the same evidence payload.

These tests make the original failure mode much harder to reintroduce without an explicit test failure.

### Public Docs And Contributor Guidance

Files involved:

- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `CONTRIBUTING.md`

The supporting docs now explain the normalized evidence contract directly:

- `cardiff/docs/render-pipeline.md` explains what the manifest and request fingerprints are actually derived from,
- `cardiff/docs/cli-quickstart.md` now states that the approved comparison is portable across checkout path and line-ending differences,
- `CONTRIBUTING.md` now tells contributors not to refresh approved evidence for path-only or line-ending-only checkout differences.

That contributor note is important because it turns the bug fix into a maintained workflow rule instead of leaving it as an implementation detail buried in the pipeline.

### Current Verification Snapshot

Commands run for this release:

```powershell
cd d:\Programming\Repositories\cardiff\cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

Observed results:

- `tests/contract`: `9 passed`
- `tests/rendering`: `23 passed`
- `tests/cli`: `14 passed`

The optional CLI reference-comparison path now succeeds again when run against the approved request, approved asset root, deterministic adapter, and refreshed `reference-evidence.json`.

### Cleanup Candidates Carried Forward

These directories still exist in the workspace and should be removed manually by the user when appropriate:

- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/`
- `cardiff/pytest-cache-files-*/`
- `tmphk9u2kf5/`

### Other Markdown Files

No changes were required in:

- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

Reason:

This release changes render evidence behavior, contributor workflow guidance, and public documentation, but it does not alter vulnerability disclosure policy or community conduct rules.

---

## Files Touched in This Release

- `README.md`
- `CHANGELOG.md`
- `REQUIREMENTS.md`
- `docs/version-0-1-4-docs.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/docs/cli-quickstart.md`
- `CONTRIBUTING.md`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/tests/rendering/test_determinism.py`
- `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json`

---

## Next Steps

1. Decide whether deterministic mode should remain strictly ASCII-only or gain a separate transliteration or escaping strategy for developer previews.
2. Clean the lingering temporary QR and pytest-cache directories before relying on broad test collection.
