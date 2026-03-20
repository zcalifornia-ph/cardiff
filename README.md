# cardiff

<p align="center">
  <img src="repo/images/project_screen.png" alt="Cardiff project screenshot" width="900">
</p>

<p align="center">
  <strong>Business cards as code.</strong>
</p>

<p align="center">
  Cardiff is an open-source rendering platform for standardized, print-ready business cards and adjacent identity materials.
  It turns structured records into validated render requests and reusable render outputs that later CLI, batch, and API workflows can share without drift.
</p>

<p align="center">
  Version: <code>v0.0.3</code><br>
  Status: pre-alpha; canonical contract and render pipeline foundation landed.
</p>

## Overview

Cardiff is building toward one shared rendering core for:

- individual CLI operators who want one-command PDF generation from structured data
- batch workflows for departments, labs, and administrative teams
- API integrations that need the same validation and rendering behavior as the CLI

The product direction remains the same: structured input should become consistent, branded, print-ready outputs without manual layout editing for every person.

## Current Implementation Slice

The repository is no longer bootstrap-only.
`UNIT-001 / BOLT-001A` and `UNIT-001 / BOLT-001B` are now implemented under the nested Python project in `cardiff/`.

What is in place today:

- a Python package scaffold with setuptools metadata in `cardiff/pyproject.toml`
- a public package surface in `cardiff/src/cardiff/`
- a framework-agnostic contract kernel in `cardiff/src/cardiff/contract/`
- a shared render pipeline in `cardiff/src/cardiff/rendering/`
- manifest-driven template resolution for the approved `business-card` template package in `cardiff/src/cardiff/templates/business-card/`
- JSON and YAML request loading that normalizes into one canonical request model
- validation rules for required identity fields, template selection, supported template options, and approved asset paths
- text sanitization hooks for later LaTeX-safe rendering
- deterministic local PDF generation plus a real `XeLaTeXAdapter` boundary for runtime parity work when `xelatex` is available
- contract-focused and rendering-focused tests and fixtures under `cardiff/tests/`
- implementation documentation in `cardiff/docs/validation-contract.md` and `cardiff/docs/render-pipeline.md`
- stored approval artifacts in `cardiff/tests/fixtures/approved-samples/business-card/`

## What Cardiff Can Do Right Now

The current codebase can validate a single-record render request and render the approved `business-card` template through the shared pipeline.

Supported behavior today:

- top-level request sections: `identity`, `template`, and optional `assets`
- required identity fields: `full_name`, `role`, `email`
- optional identity fields: `phone`, `organization`, `department`, `website`, `address_lines`, `pronouns`
- supported template options: `variant`, `include_qr`, `accent_hex`
- approved asset slots: `logo`, `avatar`
- template resolution through a manifest-backed symbolic template ID
- stable renderer outcomes with normalized evidence for deterministic review

Current validation and render failure classes include:

- `unknown_field`
- `missing_required`
- `invalid_type`
- `invalid_template`
- `invalid_asset_path`
- `unsafe_content`
- `template_not_found`
- `template_manifest_invalid`
- `template_asset_missing`
- `unsupported_template_option`
- `tex_compile_failed`
- `render_output_invalid`

## Current Rendering Boundary

The current render layer supports two adapter paths:

- `DeterministicTeXAdapter` for local deterministic output and test execution without `xelatex`
- `XeLaTeXAdapter` for real compiler-backed PDF generation when `xelatex` is available on `PATH`

This means the shared pipeline and template model are implemented now, while reference-runtime parity remains an explicit next step.

## What Has Not Landed Yet

The current implementation is still a pre-alpha foundation, not the full product surface.

Not yet implemented:

- CLI `validate` and `render` commands
- CSV batch orchestration
- FastAPI service mode
- richer template customization beyond the first approved business-card package
- pinned reference runtime and container parity for `xelatex`
- CI wiring, deployment packaging, and operations surfaces

## Target Architecture

The approved direction remains:

```text
structured input -> validated canonical request -> template resolution -> rendered TeX -> adapter compile -> PDF + normalized evidence -> delivery via CLI, batch, or API
```

The current and planned stack includes:

- Python 3.12+
- PyYAML for YAML request loading
- pytest for validation and render-pipeline tests
- Typer for future CLI work
- FastAPI for future service mode
- manifest-backed template packages plus XeLaTeX-oriented rendering boundaries
- Docker and CI runtime pinning for reproducible execution

## Repository Layout

```text
cardiff/
  cardiff/
    pyproject.toml
    src/cardiff/
      __init__.py
      contract/
      rendering/
      templates/
        business-card/
    tests/
      contract/
      rendering/
      fixtures/
        approved-assets/
        approved-samples/
    docs/
      validation-contract.md
      render-pipeline.md
    ai-dlc-docs/
      requirements/
      design-artifacts/
      traceability/
  repo/images/
  docs/
    version-0-0-2-docs.md
    version-0-0-3-docs.md
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE.txt
```

## Getting Started

The current runnable slice is the shared contract and render foundation.

1. Clone the repository.
2. Enter the Python project directory:

   ```powershell
   cd cardiff
   ```

3. Install the package and test dependencies:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

4. Run the current acceptance suite:

   ```powershell
   python -m pytest tests -q -p no:cacheprovider
   ```

Expected result: the full current test suite passes and confirms contract validation, template resolution, classified render failures, and deterministic render evidence behavior.

## Roadmap

- [x] `UNIT-001 / BOLT-001A`: canonical contract and validation foundation
- [x] `UNIT-001 / BOLT-001B`: render pipeline and template resolution
- [ ] `UNIT-001 / BOLT-001C`: CLI operator flow
- [ ] `UNIT-002`: template quality and controlled customization
- [ ] `UNIT-003`: CSV batch generation
- [ ] `UNIT-004`: FastAPI service mode
- [ ] `UNIT-005`: runtime packaging, CI, deployment, and ops readiness

## Documentation

Start with these project artifacts:

- `README.md` for the repo-level product and status summary
- `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md` for the implementation scope, bolt status, and traceability source of truth
- `cardiff/docs/validation-contract.md` for the canonical request contract
- `cardiff/docs/render-pipeline.md` for the implemented render pipeline and adapter behavior
- `docs/version-0-0-3-docs.md` for the full release notes beyond this README and changelog

## Contributing

Contributions are welcome, especially around render quality, CLI ergonomics, batch and API reuse, runtime parity, and documentation quality.
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
