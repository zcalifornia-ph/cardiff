# Version 0.1.3 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.3
- **Release Date:** 2026-03-23
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 (complete), deterministic rendering clarification

---

## Executive Summary

Version 0.1.3 is a focused rendering-quality and documentation-reconciliation release.
The main behavior change is not a new feature; it is a clearer contract around when the deterministic fallback is appropriate and when real XeLaTeX rendering is required.

This release does four things:

1. makes the ASCII-only limit of deterministic fallback rendering explicit,
2. expands rendering tests around non-ASCII identity and template-title inputs,
3. refreshes the root release markers so the README, changelog, and versioned docs are coherent,
4. records the current verification baseline and cleanup candidates.

---

## What Changed from v0.1.2

### Root Versioning Reconciliation

The repository already contained `docs/version-0-1-2-docs.md`, but the root docs still mixed `v0.1.1`, `v0.1.2`, and `Unreleased` references.

This release normalizes that state by:

- naming the previous top changelog block `v0.1.2`,
- advancing the root README version marker to `v0.1.3`,
- pointing the README documentation section at `docs/version-0-1-3-docs.md`.

### Deterministic Adapter Boundary Is Now Explicit

Files involved:

- `README.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/tests/rendering/test_pipeline.py`

The deterministic adapter remains useful for stable local smoke checks and evidence-oriented tests, but it should not be treated as a Unicode-safe substitute for `xelatex`.

The current repo now documents and tests that deterministic rendering fails clearly when non-ASCII text appears in:

- `full_name`
- `role`
- `organization`
- `address_lines`
- the resolved template display title

This matters because silent fallback behavior would make local preview output look more trustworthy than it actually is for real multilingual content.

### Rendering Test Expansion

`cardiff/tests/rendering/test_pipeline.py` now includes:

- parameterized non-ASCII checks across multiple identity preview fields,
- a patched-template test that verifies non-ASCII template titles fail clearly in deterministic mode.

Verified rendering command:

```powershell
cd d:\Programming\Repositories\cardiff\cardiff
python -m pytest tests/rendering -q -p no:cacheprovider
```

Observed result:

- `21 passed in 0.16s`

### Approved Sample Refresh

`cardiff/tests/fixtures/approved-samples/business-card/qr-evidence-stability.pdf` is part of the checked-in change set for this release.

Treat it as an approved sample artifact tied to the QR evidence stability test, not as disposable scratch output.

### Current Verification Snapshot

Commands run for this release:

```powershell
cd d:\Programming\Repositories\cardiff\cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

Observed results:

- `tests/contract`: `8 passed`
- `tests/rendering`: `21 passed`
- `tests/cli`: `11 passed`, `1 failed`

The remaining CLI failure is still the reference-comparison path.
The current mismatch is reported on these fields:

- `manifest_fingerprint`
- `request_fingerprint`

That path still exits with code `4`, which matches the repo's existing reference-mismatch behavior.

### Cleanup Candidates Carried Forward

These directories still exist in the workspace and should be removed manually by the user when appropriate:

- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/`
- `cardiff/pytest-cache-files-*/`
- `tmphk9u2kf5/`

### Other Markdown Files

No changes were required in:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

Reason:

This release changes rendering documentation and test coverage, but it does not alter contributor workflow rules, disclosure policy, or community standards.

---

## Files Touched in This Release

- `README.md`
- `CHANGELOG.md`
- `docs/version-0-1-3-docs.md`
- `cardiff/docs/render-pipeline.md`
- `cardiff/tests/rendering/test_pipeline.py`
- `cardiff/tests/fixtures/approved-samples/business-card/qr-evidence-stability.pdf`

---

## Next Steps

1. Refresh `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` so the CLI reference-comparison path can return exit code `0` again.
2. Decide whether deterministic mode should remain strictly ASCII-only or gain a separate transliteration/escaping strategy for developer previews.
3. Clean the lingering temporary QR and pytest-cache directories before relying on broad test collection.
