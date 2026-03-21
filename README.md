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
  Version: <code>v0.0.4</code><br>
  Status: pre-alpha; <code>UNIT-001</code> is complete and the first CLI operator flow is now implemented.
</p>

## Overview

Cardiff is building toward one shared rendering core for:

- individual CLI operators who want one-command PDF generation from structured data
- batch workflows for departments, labs, and administrative teams
- API integrations that need the same validation and rendering behavior as the CLI

The product direction remains the same: structured input should become consistent, branded, print-ready outputs without manual layout editing for every person.

## Current Implementation Slice

The repository now contains a complete `UNIT-001` baseline under the nested Python project in `cardiff/`.

What is in place today:

- a Python package scaffold with setuptools metadata in `cardiff/pyproject.toml`
- a public package surface in `cardiff/src/cardiff/`
- a framework-agnostic contract kernel in `cardiff/src/cardiff/contract/`
- a shared render pipeline in `cardiff/src/cardiff/rendering/`
- manifest-driven template resolution for the approved `business-card` template package in `cardiff/src/cardiff/templates/business-card/`
- a first CLI adapter in `cardiff/src/cardiff/cli.py` with `validate` and `render` commands
- installed-package and source-checkout entry paths through `cardiff/src/cardiff/__main__.py` and `cardiff/cardiff.py`
- deterministic local PDF generation plus a real `XeLaTeXAdapter` boundary for runtime parity work when `xelatex` is available
- CLI, contract, and rendering tests and fixtures under `cardiff/tests/`
- implementation documentation in `cardiff/docs/validation-contract.md`, `cardiff/docs/render-pipeline.md`, and `cardiff/docs/cli-quickstart.md`
- stored approval artifacts in `cardiff/tests/fixtures/approved-samples/business-card/`

## What Cardiff Can Do Right Now

The current codebase can validate a single-record render request and render the approved `business-card` template end to end through the shared CLI and rendering core.

Supported behavior today:

- load JSON and YAML request files into one canonical request model
- validate required identity fields, supported template options, and approved asset paths before rendering
- render the approved `business-card` template to a requested PDF path
- emit structured JSON status payloads for `validate` and `render` commands
- surface stable validation and render failure classes
- run deterministic local renders and compare normalized evidence against the approved reference record
- expose runtime metadata that later portability, batch, and API work can reuse

## Current Command Surface

The current operator flow is:

```text
structured request file -> canonical validation -> approved template resolution -> TeX adapter compile -> PDF artifact + structured status + normalized evidence
```

CLI entry paths available now:

- `python -m cardiff ...` from the `cardiff/` project root
- `cardiff ...` after editable or standard installation

Current commands:

- `validate`
- `render`

## Getting Started

1. Clone the repository.
2. Enter the Python project directory:

   ```powershell
   cd cardiff
   ```

3. Install the package and test dependencies:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

4. Validate the approved sample request:

   ```powershell
   python -m cardiff validate tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets
   ```

5. Render the approved sample PDF with deterministic evidence comparison:

   ```powershell
   python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output tests/fixtures/approved-samples/business-card/determinism-output.pdf --deterministic --reference-evidence tests/fixtures/approved-samples/business-card/reference-evidence.json
   ```

6. Run the current acceptance suite:

   ```powershell
   python -m pytest tests -q -p no:cacheprovider
   ```

Expected result: the current test suite passes and confirms CLI behavior, contract validation, template resolution, classified render failures, and deterministic render evidence behavior.

## Repository Layout

```text
cardiff/
  cardiff/
    cardiff.py
    pyproject.toml
    src/cardiff/
      __init__.py
      __main__.py
      cli.py
      contract/
      rendering/
      templates/
        business-card/
    tests/
      cli/
      contract/
      rendering/
      fixtures/
        approved-assets/
        approved-samples/
    docs/
      cli-quickstart.md
      render-pipeline.md
      validation-contract.md
    ai-dlc-docs/
      requirements/
      design-artifacts/
      traceability/
  docs/
    version-0-0-2-docs.md
    version-0-0-3-docs.md
    version-0-0-4-docs.md
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE.txt
```

## Roadmap

- [x] `UNIT-001 / BOLT-001A`: canonical contract and validation foundation
- [x] `UNIT-001 / BOLT-001B`: render pipeline and template resolution
- [x] `UNIT-001 / BOLT-001C`: CLI operator flow
- [ ] `UNIT-002`: template quality and controlled customization
- [ ] `UNIT-003`: CSV batch generation
- [ ] `UNIT-004`: FastAPI service mode
- [ ] `UNIT-005`: runtime packaging, CI, deployment, and ops readiness

## Documentation

Start with these project artifacts:

- `README.md` for the repo-level product and status summary
- `cardiff/ai-dlc-docs/requirements/REQUIREMENTS.md` for the implementation scope, bolt status, and traceability source of truth
- `cardiff/docs/validation-contract.md` for the canonical request contract
- `cardiff/docs/render-pipeline.md` for the shared render pipeline and adapter behavior
- `cardiff/docs/cli-quickstart.md` for the current CLI workflow and exit-code contract
- `docs/version-0-0-4-docs.md` for the full release notes beyond this README and changelog

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
