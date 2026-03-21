# Version 0.1.1 Docs

## Quick Diagnostic Read

`v0.1.1` is a documentation patch release over the completed `UNIT-001` code baseline.
No CLI contract, rendering behavior, or acceptance evidence changed in this release; the work is focused on making the root documentation surface easier to navigate and easier to trust.

## One-Sentence Objective

Document the README-centered public docs refresh, version-alignment updates, and cleanup notes that landed after `v0.1.0`.

## Why This Version Matters

`v0.1.0` established the first complete Cardiff MVP slice.
`v0.1.1` makes that slice easier for readers and contributors to understand by tightening the public landing page, aligning version markers, and recording cleanup candidates without changing runtime behavior.

## Plan A / Plan B

Plan A: read `README.md`, then `CHANGELOG.md`, then this file to understand the current public docs surface.

Plan B: read `REQUIREMENTS.md`, compare the current docs references, then inspect the exact release diff for `README.md`, `CHANGELOG.md`, `REQUIREMENTS.md`, `cardiff/pyproject.toml`, and `docs/version-0-1-1-docs.md`.

## Artifact Map

- `README.md`
- `CHANGELOG.md`
- `REQUIREMENTS.md`
- `docs/version-0-1-1-docs.md`
- `cardiff/pyproject.toml`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

## What Changed In This Version

### 1. The Root README Was Reframed Around The Sample Template

The root `README.md` now follows the public structure from `agent/reference/sample-readme.md` more closely.
That includes:

- GitHub shield badges near the top
- a centered project header block with screenshot and action links
- a collapsible table of contents
- a `Built With` section using badge-style links
- back-to-top anchors throughout the document
- richer footer sections for contributors, acknowledgments, and contact details

The Cardiff-specific product description, implementation slice, command surface, roadmap, and documentation pointers were preserved rather than replaced.

### 2. Template Leakage Was Removed From The Live README

The earlier in-progress README state had stray placeholder markers and a wrong inherited project heading.
This release normalizes the file so the public page no longer leaks template artifacts such as a `VERZOLA` title or placeholder `#` markers.

### 3. Version References Were Realigned To `v0.1.1`

This release updates the visible public version line so the README, requirements snapshot, changelog entry, and Python package metadata agree on the current documentation release marker.

### 4. Cleanup Candidates Were Recorded Instead Of Deleted

Generated Python caches and editable-install metadata are currently present in the working tree.
Per repository rules, they were not deleted automatically.
Instead, they are recorded in `CHANGELOG.md` under `### For Deletion` so the maintainer can remove them deliberately before or after committing.

## Behavior Available Now

Cardiff still provides the same functional baseline as `v0.1.0`:

- JSON and YAML single-record request loading
- canonical request validation before rendering
- approved `business-card` template rendering
- CLI `validate` and `render` commands
- deterministic render evidence comparison
- shared contract and rendering components for future batch and API work

The change in `v0.1.1` is documentation clarity, not runtime capability.

## Verification

This release is documentation and metadata only.
Verification focused on consistency and public readability:

```powershell
git diff -- README.md CHANGELOG.md REQUIREMENTS.md cardiff/pyproject.toml docs/version-0-1-1-docs.md
rg -n "v0\\.1\\.1|version-0-1-1-docs" README.md CHANGELOG.md REQUIREMENTS.md docs cardiff/pyproject.toml
```

Expected result:

- root docs reference `v0.1.1` consistently
- `README.md` no longer contains stray template leakage
- `CHANGELOG.md` records current generated-artifact cleanup candidates

## Known Gaps

- No runtime or API behavior changed in this release.
- Badge rendering depends on GitHub metadata and external badge/image services.
- Generated caches remain on disk until the maintainer removes them manually.

## Practice Task

Compare `docs/version-0-1-0-docs.md` and `docs/version-0-1-1-docs.md`.
Then explain which changes are product-scope changes versus documentation-surface changes.

## Next Steps

1. Keep the README structure stable as future Units land instead of reworking the landing page every release.
2. Remove the recorded generated artifacts before publishing a clean commit history.
3. If a future release changes public behavior, update `README.md`, `REQUIREMENTS.md`, `CHANGELOG.md`, and the matching version docs together.
