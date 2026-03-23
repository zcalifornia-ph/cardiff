# Version 0.1.2 Documentation Release Notes

## Document Metadata

- **Version:** v0.1.2
- **Release Date:** 2026-03-23
- **Status:** pre-alpha
- **Associated Unit:** UNIT-001 (complete), QR-directive rendering additions

---

## Executive Summary

Version 0.1.2 represents a documentation and developer-experience update to the Cardiff repository. The core rendering functionality from v0.1.1 remains unchanged, but this release adds:

1. **QR Code Directive Support** - New preprocessing layer for generating QR codes containing vCard contact data
2. **Virtual Environment Documentation** - Updated quickstart guide with venv setup instructions
3. **Expanded Test Coverage** - New directive-focused tests in `test_directives.py`
4. **Contributor Guidance Updates** - Clarified expectations for QR-related artifacts and reference evidence maintenance

This release does not introduce breaking changes to the canonical request contract or CLI interface.

---

## What Changed from v0.1.1

### New Rendering Pipeline Feature: QR Directives

**File:** `cardiff/src/cardiff/rendering/directives.py` (new)

The QR directive system allows templates to include a special `\cardiffqr[...]` command that gets preprocessed before TeX compilation:

```latex
\cardiffqr[width=0.6in]  % Gets replaced with \includegraphics or comment
```

**How it works:**

1. **Deterministic mode** (for testing): Replaces directive with a TeX comment
2. **Real rendering mode**: Generates a QR code PNG containing vCard 3.0 data, then replaces directive with `\includegraphics`

**vCard fields included:**
- Full name (`FN:`)
- Role/title (`TITLE:`)
- Email (`EMAIL:`)
- Organization and department (`ORG:`)
- Phone (`TEL:`)
- Website (`URL:`)
- Address (`ADR:`)
- Pronouns note (`NOTE:`)

### Updated Files

| File | Change Summary |
|------|----------------|
| `README.md` | Added venv setup steps, segno badge, QR directive documentation, updated test expectations |
| `CHANGELOG.md` | Added Unreleased section with cleanup candidates and verification notes |
| `CONTRIBUTING.md` | Added guidance for QR directive testing and reference evidence refresh |
| `cardiff/pyproject.toml` | Added `segno>=1.6,<2` dependency |
| `cardiff/src/cardiff/rendering/__init__.py` | Exported new directive functions |
| `cardiff/src/cardiff/rendering/pipeline.py` | Integrated QR directive preprocessing |
| `cardiff/src/cardiff/rendering/tex.py` | Added `deterministic` flag to adapters |
| `cardiff/src/cardiff/templates/business-card/card.tex` | Added `\cardiffqr` directive usage |
| `cardiff/tests/rendering/test_directives.py` | New test file with 9 directive tests |

---

## Technical Deep Dive

### Architecture: Directive Preprocessing

The directive system sits between template substitution and TeX compilation:

```
Request -> Validation -> Template Substitution -> QR Directive Resolution -> TeX Compile -> PDF
```

**Key design decisions:**

1. **Separation of concerns**: QR generation is isolated from core rendering
2. **Deterministic fallback**: Tests can run without QR image I/O
3. **Temporary file isolation**: QR PNGs are generated in temp directories that clean up automatically

### Security Considerations

**Current protections:**
- Identity fields are sanitized before vCard generation (via `sanitize_text()` in validation layer)
- QR code generation happens in isolated temp directories
- No direct file system exposure to user input

**Known gaps (to address in future bolts):**
- vCard URL fields are not protocol-validated (could contain `javascript:` or `file:` URLs)
- No size limits on vCard payload (potential DoS via oversized QR codes)
- Template file integrity is assumed (not verified against modification)

### Test Coverage

**New tests in `test_directives.py`:**

| Test Class | Test Count | Coverage |
|------------|------------|----------|
| `TestBuildVcard` | 3 | vCard field inclusion/omission |
| `TestGenerateQrPng` | 1 | QR PNG generation validation |
| `TestResolveQrDirectives` | 3 | Directive replacement behavior |
| `TestResolveQrDirectivesDeterministic` | 2 | Deterministic mode behavior |

**Total:** 9 new tests

---

## Developer Workflow Changes

### New Prerequisites

Install the `segno` library for QR code generation:

```powershell
python -m pip install segno>=1.6,<2
```

This is now listed in `pyproject.toml` dependencies.

### Updated Quickstart Flow

```powershell
cd cardiff

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# or
source .venv/bin/activate     # bash/zsh

# Install dependencies
python -m pip install -e ".[dev]"

# Run tests
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

### Known Test Caveats

**Reference evidence mismatch:**
The stored `reference-evidence.json` file contains fingerprints that are now stale relative to the current template manifest. The reference-comparison test will return exit code `4` (mismatch) until refreshed.

**Temporary QR directories:**
Non-deterministic rendering runs may leave behind `cardiff-qr-*/` directories under `cardiff/tests/fixtures/approved-samples/business-card/`. These should be cleaned before running broad test collection:

```powershell
Remove-Item -Recurse -Force cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/
Remove-Item -Recurse -Force cardiff/pytest-cache-files-*/
```

---

## Contributor Guidelines Updates

### When to Refresh Reference Evidence

Update `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` when:

- Template manifest changes (dimensions, fields, options)
- Approved sample request changes
- Deterministic output behavior changes
- Any fingerprint-bearing artifact is modified

### When to Update Directive Tests

Update `cardiff/tests/rendering/test_directives.py` when:

- vCard field mapping changes
- QR generation parameters change (scale, error correction level)
- Directive syntax changes
- New directive types are added

### Files to Exclude from Commits

Never commit:
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/`
- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/pytest-cache-files-*/`
- `*.pyc`, `__pycache__/`, `.venv/`

---

## Verification Checklist

Before merging work that touches QR directives or rendering:

- [ ] `python -m pytest tests/contract -q -p no:cacheprovider` passes (8 tests)
- [ ] `python -m pytest tests/rendering -q -p no:cacheprovider` passes (16 tests)
- [ ] `python -m pytest tests/cli -q -p no:cacheprovider` passes (5 of 6 tests; reference comparison expected to fail)
- [ ] Temporary QR directories cleaned from test fixtures
- [ ] Reference evidence refreshed if fingerprints changed
- [ ] `CONTRIBUTING.md` updated if workflow changed
- [ ] `CHANGELOG.md` updated with new entries

---

## Migration Notes

### For Existing Users

No migration required. This is a backward-compatible update.

### For Contributors

If you have existing branches:
1. Pull latest `rev` branch
2. Run `python -m pip install -e ".[dev]"` to get `segno`
3. Clean temporary QR directories
4. Re-run tests to confirm baseline

---

## Next Steps (v0.1.3 Planning)

Planned work for the next version:

1. **BOLT-002A** - Template specification with exact dimensions, bleed, safe margins, and field placement
2. **Reference evidence refresh** - Update fingerprints to match current template state
3. **Security hardening** - Add URL protocol validation and vCard size limits
4. **Template integrity verification** - Hash templates and verify before rendering

---

## Appendix: File Inventory

### New Files
- `cardiff/src/cardiff/rendering/directives.py`
- `cardiff/tests/rendering/test_directives.py`

### Modified Files
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `cardiff/pyproject.toml`
- `cardiff/src/cardiff/rendering/__init__.py`
- `cardiff/src/cardiff/rendering/pipeline.py`
- `cardiff/src/cardiff/rendering/tex.py`
- `cardiff/src/cardiff/templates/business-card/card.tex`

### Cleanup Candidates (For Deletion)
- `cardiff/tests/fixtures/approved-samples/business-card/cardiff-qr-*/`
- `cardiff/tests/fixtures/approved-samples/business-card/.cardiff-qr/`
- `cardiff/tests/fixtures/approved-samples/business-card/_directive-work/`
- `cardiff/pytest-cache-files-*/`
- `tmphk9u2kf5/`

---

*This documentation is part of the Cardiff release process. For questions, see SECURITY.md or open an issue.*
