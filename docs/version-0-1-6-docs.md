# Version 0.1.6 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.6
- **Release Date:** 2026-03-24
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 (complete), initial CI/release automation and metadata alignment

---

## Executive Summary

Version 0.1.6 is a release-engineering and documentation-alignment update.
The main behavior change is that the repository now has initial GitHub Actions workflows that verify the real integration paths and prevent tagged releases from publishing unless version metadata and the targeted test suites agree.

This release does five things:

1. adds GitHub Actions CI coverage for pushes and pull requests targeting the current integration branches,
2. reruns the targeted test baseline before tagged releases can build or publish distributions,
3. rejects mismatched release tags before any publish step starts,
4. aligns package metadata and public docs to `v0.1.6` and the `cardiff-cli` distribution name,
5. records the latest verification baseline and current cleanup candidates.

---

## What Changed from v0.1.5

### GitHub Actions CI Now Covers The Real Integration Paths

Files involved:

- `.github/workflows/ci.yml`

The previous workflow draft only covered pull requests targeting `rev`.
That left merges to `main` without protection, even though the repo's broader branching guidance was already mixed between `main` and `rev`.

This release corrects that by:

- running CI on pushes to both `main` and `rev`,
- running pull-request validation for both `main` and `rev`,
- keeping the targeted contract, rendering, and CLI suites on Python `3.12` and `3.13`.

The goal is not to solve all of `UNIT-005`.
It is to make the current repository automation actually cover the integration branches that contributors can use today.

### Transient Test Cleanup Now Matches Cardiff's Real Workspace Artifacts

Files involved:

- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`

The original cleanup step removed `qr-*`, which does not match Cardiff's actual transient test directories.

This release updates the cleanup behavior so the workflows now remove the directories the repo really accumulates before running tests, including:

- `.cardiff-qr/`
- `_directive-work/`
- `cardiff-qr-*`
- `tests/fixtures/tmp*`
- project-root `pytest-cache-files-*`
- project-root `tmp*`

This matters because the current repo already documents that stray temporary directories can interfere with broader test collection.
The workflow cleanup should therefore target the real artifacts, not an unrelated naming pattern.

### Tagged Releases Now Fail Fast On Metadata Drift And Test Regressions

Files involved:

- `.github/workflows/release.yml`
- `cardiff/pyproject.toml`

The previous release workflow built and published on any `v*` tag without first proving that the tag matched package metadata or that the targeted verification baseline still passed.

This release adds a gated release flow:

- a metadata-validation job reads the package version from `cardiff/pyproject.toml`,
- the workflow fails immediately if the pushed tag does not match that version,
- the targeted contract, rendering, and CLI suites rerun across Python `3.12` and `3.13`,
- distribution build runs only after metadata validation and tests succeed,
- PyPI publish remains downstream of a successful build.

This is still an initial automation slice, not a full deployment system.
But it closes the most obvious gap: tags should not publish unverified or version-drifted artifacts.

### Package Metadata And Public Docs Were Realigned

Files involved:

- `cardiff/pyproject.toml`
- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `docs/version-0-1-6-docs.md`

The public root docs and package metadata now describe the same repo state.

Specific alignment updates include:

- `README.md` now points to `v0.1.6` and the latest versioned documentation note,
- `REQUIREMENTS.md` now records the initial CI/release automation baseline and the `cardiff-cli` distribution naming,
- `CHANGELOG.md` now records this work as the new `v0.1.6` release entry instead of leaving it as an `Unreleased` fragment,
- `CONTRIBUTING.md` now keeps the release-tag example aligned to the current version line,
- `cardiff/pyproject.toml` now uses version `0.1.6` while preserving the `cardiff` console command surface.

This keeps the repo's public release markers, release workflow expectations, and package metadata from drifting apart again.

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

These are the same targeted suites now enforced by the checked-in CI and release workflows.

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

This release changes repository automation, package metadata alignment, and contributor/public documentation, but it does not alter vulnerability disclosure policy or community conduct rules.

---

## Files Touched in This Release

- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `cardiff/pyproject.toml`
- `README.md`
- `REQUIREMENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `docs/version-0-1-6-docs.md`

---

## Next Steps

1. Decide whether the repository should continue supporting both `main` and `rev` as integration targets or fully normalize on one protected trunk path.
2. Expand `UNIT-005` beyond the initial workflow baseline with broader collection safety, release-process documentation, deployment packaging, and operations readiness artifacts.
