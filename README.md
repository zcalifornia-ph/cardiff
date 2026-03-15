# cardiff

<p align="center">
  <img src="repo/images/project_screen.png" alt="Cardiff project screenshot" width="900">
</p>

<p align="center">
  <strong>Business cards as code.</strong>
</p>

<p align="center">
  Cardiff is an open-source rendering platform for standardized, print-ready business cards and adjacent identity materials.
  It turns structured records into validated render requests that later CLI, batch, and API workflows can reuse without drift.
</p>

<p align="center">
  Version: <code>v0.0.2</code><br>
  Status: pre-alpha; canonical contract and validation foundation landed.
</p>

## Overview

Cardiff is building toward one shared rendering core for:

- individual CLI operators who want one-command PDF generation from structured data
- batch workflows for departments, labs, and administrative teams
- API integrations that need the same validation and rendering behavior as the CLI

The product direction remains the same: structured input should become consistent, branded, print-ready outputs without manual layout editing for every person.

## Current Implementation Slice

The repository is no longer bootstrap-only.
`UNIT-001 / BOLT-001A` is now implemented under the nested Python project in `cardiff/`.

What is in place today:

- a Python package scaffold with setuptools metadata in `cardiff/pyproject.toml`
- a public package surface in `cardiff/src/cardiff/`
- a framework-agnostic contract kernel in `cardiff/src/cardiff/contract/`
- JSON and YAML request loading that normalizes into one canonical request model
- validation rules for required identity fields, template selection, and supported template options
- asset-path guardrails that constrain requests to approved roots and extensions
- text sanitization hooks for later LaTeX-safe rendering
- contract-focused tests and fixtures under `cardiff/tests/`
- implementation documentation in `cardiff/docs/validation-contract.md`

## What Cardiff Can Do Right Now

The current codebase can validate and sanitize a single-record render request before any PDF rendering exists.

Supported shape today:

- top-level sections: `identity`, `template`, and optional `assets`
- required identity fields: `full_name`, `role`, `email`
- optional identity fields: `phone`, `organization`, `department`, `website`, `address_lines`, `pronouns`
- template options: `variant`, `include_qr`, `accent_hex`
- asset slots: `logo`, `avatar`

Current validation outcomes include stable issue classes such as:

- `unknown_field`
- `missing_required`
- `invalid_type`
- `invalid_template`
- `invalid_asset_path`
- `unsafe_content`

## What Has Not Landed Yet

The current implementation is still an early foundation, not an end-to-end renderer.

Not yet implemented:

- template resolution and PDF generation
- CLI `validate` and `render` commands
- CSV batch orchestration
- FastAPI service mode
- runtime pinning, CI wiring, and deployment packaging

## Target Architecture

The approved direction remains:

```text
structured input -> validated canonical request -> template resolution -> rendered LaTeX -> PDF compilation -> delivery via CLI, batch, or API
```

The current and planned stack includes:

- Python 3.12+
- PyYAML for YAML request loading
- pytest for current contract validation tests
- Typer for future CLI work
- FastAPI for future service mode
- Jinja2 and XeLaTeX for later render-pipeline work
- Docker and CI runtime pinning for reproducible execution

## Repository Layout

```text
cardiff/
  cardiff/
    pyproject.toml
    src/cardiff/
      __init__.py
      contract/
    tests/
      contract/
      fixtures/
    docs/
      validation-contract.md
    ai-dlc-docs/
      requirements/
      design-artifacts/
      traceability/
  repo/images/
  docs/
  README.md
  CHANGELOG.md
  REQUIREMENTS.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE.txt
```

## Getting Started

The current runnable slice is the contract-validation layer.

1. Clone the repository.
2. Enter the Python project directory:

   ```powershell
   cd cardiff
   ```

3. Install the package and test dependencies:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

4. Run the contract test suite:

   ```powershell
   python -m pytest tests/contract -q -p no:cacheprovider
   ```

Expected result: the contract tests pass and confirm JSON/YAML parity, required-field validation, unknown-field rejection, asset safety rules, and unsafe-content rejection.

## Roadmap

- [x] `UNIT-001 / BOLT-001A`: canonical contract and validation foundation
- [ ] `UNIT-001 / BOLT-001B`: render pipeline and template resolution
- [ ] `UNIT-001 / BOLT-001C`: CLI operator flow
- [ ] `UNIT-002`: template quality and controlled customization
- [ ] `UNIT-003`: CSV batch generation
- [ ] `UNIT-004`: FastAPI service mode
- [ ] `UNIT-005`: runtime packaging, CI, deployment, and ops readiness

## Documentation

Start with these project artifacts:

- `README.md` for the repo-level product and status summary
- `REQUIREMENTS.md` for the current scope summary and source-of-truth links
- `cardiff/docs/validation-contract.md` for the implemented request contract
- `docs/version-0-0-2-docs.md` for the detailed notes on this version

## Contributing

Contributions are welcome, especially around contract hardening, template/render design, CLI ergonomics, documentation quality, and the next `UNIT-001` bolts.
See `CONTRIBUTING.md` for workflow expectations.

## License

Distributed under the Apache License 2.0.
See `LICENSE.txt` for the full license text.

## Contact

Maintainer: Zildjian E. California  
Email: zecalifornia@up.edu.ph  
GitHub: https://github.com/zcalifornia-ph/cardiff  
LinkedIn: https://www.linkedin.com/in/zcalifornia  
ORCID: https://orcid.org/0009-0002-2357-7606  
ResearchGate: https://www.researchgate.net/profile/Zildjian-California  
X/Twitter: https://twitter.com/zcalifornia_
