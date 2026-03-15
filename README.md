# cardiff

<p align="center">
  <img src="repo/images/project_screen.png" alt="Cardiff project screenshot" width="900">
</p>

<p align="center">
  <strong>Business cards as code.</strong>
</p>

<p align="center">
  Cardiff is an open-source CLI and API for standardized, print-ready business cards and nameplates.
  It turns structured data into polished PDFs for individuals, teams, labs, departments, and institutional systems.
</p>

<p align="center">
  Version: <code>v0.0.1</code><br>
  Status: bootstrap and planning stage; implementation has not landed yet.
</p>

## Overview

Cardiff is being designed as a reproducible identity-material generation platform.
Instead of manually editing layouts in a design tool for every person, Cardiff aims to accept structured input such as config files, CSV exports, or API payloads and render consistent, branded, print-ready outputs.

The project has two intended operating modes:

- A CLI for individuals and technical users who want one-command PDF generation from structured data.
- An API service for departments, labs, offices, and admin systems that need standardized business cards or nameplates generated from institutional records.

## Why Cardiff

Most business card and nameplate workflows are manual, inconsistent, and hard to scale.
Cardiff is intended to improve that by making output:

- Beautiful by default, with print-ready typography and layout discipline.
- Reproducible, so designs and inputs can be versioned and regenerated.
- Automatable, so CSV and API-driven batch generation become possible.
- Standardized, so organizations can enforce approved layouts and branding.
- Flexible, so controlled personalization can happen without editing raw LaTeX.

## Current Repository State

This repository is at the initialization stage.
Right now, it contains the public project docs, the initial governance files, an empty package directory, and the screenshot asset for the planned product.

There is no released CLI, API service, or template engine in the repository yet.
If you are evaluating the project today, treat this repo as a product and documentation scaffold for the implementation work that follows.

## Planned Capabilities

The project direction defined for this repository includes:

- Single-card generation from a small config file.
- CSV-based batch generation for teams and institutions.
- FastAPI endpoints for integration with admin portals and database-backed systems.
- Template-driven rendering for business cards, nameplates, and related identity materials.
- Controlled customization for names, roles, emails, logos, colors, QR codes, and vCards.
- Deterministic PDF output suitable for print workflows.

## Target Architecture

Cardiff is planned around a simple pipeline:

```text
structured input -> validated models -> rendered LaTeX -> PDF compilation -> delivery via CLI or API
```

The intended stack currently includes:

- Python 3.12+
- Typer for the CLI
- FastAPI for service mode
- Pydantic for validation
- Jinja2 for template rendering
- XeLaTeX for PDF generation
- PyYAML and CSV input support
- pytest, ruff, and mypy for quality gates
- Docker and GitHub Actions for reproducible environments

These choices describe the current direction, not already-landed implementation.

## Repository Layout

The current repository shape is intentionally small:

```text
cardiff/
  cardiff/            # package directory placeholder
  docs/               # public documentation space
  learn/              # learning artifacts
  repo/images/        # public project images
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE.txt
```

## Getting Started

There is no installable release yet.

If you want to follow or contribute to the project now:

1. Clone the repository.
2. Read this README for product scope and direction.
3. Review `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`.
4. Open an issue before starting large implementation or architecture changes.

## Roadmap

- [ ] Phase 1: CLI MVP for single-card generation from structured config
- [ ] Phase 2: improved templates, QR support, logos, and better validation
- [ ] Phase 3: CSV batch generation for teams and institutional use
- [ ] Phase 4: FastAPI service mode for system integration
- [ ] Phase 5: reproducible packaging, CI, and deployment guidance

## Contributing

Contributions are welcome, especially around product design, template strategy, rendering architecture, CLI/API ergonomics, documentation, and future implementation work.
See `CONTRIBUTING.md` for the contribution workflow.

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
