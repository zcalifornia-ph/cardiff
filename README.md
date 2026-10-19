<a id="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<div align="center">
  <a href="https://github.com/zcalifornia-ph/cardiff">
    <img src="repo/images/project_screen.png" alt="Cardiff project screenshot" width="900">
  </a>

  <h3 align="center">CARDIFF</h3>

  <p align="center">
    <strong>Business cards as code.</strong>
  </p>

  <p align="center">
    Cardiff is an open-source rendering platform for standardized, print-ready business cards and adjacent identity materials.
    It turns structured records into validated render requests and reusable render outputs that later CLI, batch, and API workflows can share without drift.
  </p>

  <p align="center">
    Version: <code>v0.1.7</code> public release line<br>
    Status: pre-alpha; <code>UNIT-001</code> is complete and the current repo head now includes QR-directive rendering support, explicit Unicode-safe local rendering guidance, stable normalized-evidence comparison, fail-fast rejection of unknown template placeholders before PDF generation, initial GitHub Actions validation/release workflows, and normalized Python source attribution headers for the current tracked package/test surface.
    <br />
    <a href="REQUIREMENTS.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="cardiff/docs/cli-quickstart.md">View CLI Quickstart</a>
    &middot;
    <a href="https://github.com/zcalifornia-ph/cardiff/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/zcalifornia-ph/cardiff/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#current-implementation-slice">Current Implementation Slice</a></li>
    <li><a href="#what-cardiff-can-do-right-now">What Cardiff Can Do Right Now</a></li>
    <li><a href="#current-command-surface">Current Command Surface</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#1-prerequisites">1. Prerequisites</a></li>
        <li><a href="#2-clone-and-install">2. Clone and install</a></li>
        <li><a href="#3-environment-setup">3. Environment setup</a></li>
        <li><a href="#4-database-setup">4. Database setup</a></li>
        <li><a href="#5-run-locally">5. Run locally</a></li>
        <li><a href="#6-verify-the-setup">6. Verify the setup</a></li>
        <li><a href="#7-troubleshooting">7. Troubleshooting</a></li>
      </ul>
    </li>
    <li><a href="#repository-layout">Repository Layout</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#documentation">Documentation</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## About The Project

### Overview

Cardiff is building toward one shared rendering core for:

- individual CLI operators who want one-command PDF generation from structured data
- batch workflows for departments, labs, and administrative teams
- API integrations that need the same validation and rendering behavior as the CLI

The product direction remains the same: structured input should become consistent, branded, print-ready outputs without manual layout editing for every person.

### Built With

* [![Python][Python]][Python-url]
* [![XeLaTeX][XeLaTeX]][XeLaTeX-url]
* [![PyYAML][PyYAML]][PyYAML-url]
* [![segno][segno-badge]][segno-url]
* [![pytest][pytest-badge]][pytest-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Current Implementation Slice

The repository now contains a complete `UNIT-001` baseline under the nested Python project in `cardiff/`, plus a public requirements snapshot at `REQUIREMENTS.md`.

What is in place today:

- a Python package scaffold with setuptools metadata in `cardiff/pyproject.toml` for the `cardiff-cli` distribution
- a public package surface in `cardiff/src/cardiff/`
- normalized Apache attribution and embedded license headers across the tracked Python source files currently maintained in-tree
- a framework-agnostic contract kernel in `cardiff/src/cardiff/contract/`
- a shared render pipeline in `cardiff/src/cardiff/rendering/`, including QR/vCard directive preprocessing in `directives.py`
- manifest-driven template resolution for the approved `business-card` template package in `cardiff/src/cardiff/templates/business-card/`
- a first CLI adapter in `cardiff/src/cardiff/cli.py` with `validate` and `render` commands
- installed-package and source-checkout entry paths through `cardiff/src/cardiff/__main__.py` and `cardiff/cardiff.py`
- deterministic local PDF generation for stable ASCII-only smoke checks plus a real `XeLaTeXAdapter` boundary for Unicode-safe runtime parity when `xelatex` is available
- CLI, contract, and rendering tests and fixtures under `cardiff/tests/`, including directive-focused coverage in `cardiff/tests/rendering/test_directives.py`
- GitHub Actions workflows under `.github/workflows/` for targeted validation on pushes and pull requests plus tag-gated release verification and distribution builds
- implementation documentation in `cardiff/docs/validation-contract.md`, `cardiff/docs/render-pipeline.md`, and `cardiff/docs/cli-quickstart.md`
- contributor-facing template guidance in `cardiff/docs/template-authoring.md`
- stored approval artifacts in `cardiff/tests/fixtures/approved-samples/business-card/`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## What Cardiff Can Do Right Now

The current codebase can validate a single-record render request and render the approved `business-card` template end to end through the shared CLI and rendering core.

Supported behavior today:

- load JSON and YAML request files into one canonical request model
- validate required identity fields, supported template options, and approved asset paths before rendering
- render the approved `business-card` template to a requested PDF path
- preprocess the template's `\cardiffqr[...]` directive into a generated QR PNG or deterministic placeholder, depending on adapter mode
- reject templates that reference unknown placeholders before PDF generation starts
- emit structured JSON status payloads for `validate` and `render` commands
- surface stable validation and render failure classes
- run deterministic local renders and compare normalized evidence against the approved reference record
- expose runtime metadata that later portability, batch, and API work can reuse

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Current Command Surface

The current operator flow is:

```text
structured request file -> canonical validation -> approved template resolution -> placeholder validation + fill -> optional QR directive preprocessing -> TeX adapter compile -> PDF artifact + structured status + normalized evidence
```

CLI entry paths available now:

- `python -m cardiff ...` from the `cardiff/` project root
- `cardiff ...` after editable or standard installation

Current commands:

- `validate`
- `render`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### 1. Prerequisites

- **Git** to clone the repository. The repository does not pin a Git version.
- **Python 3.12 or newer.** `cardiff/pyproject.toml` requires Python `>=3.12`; CI currently tests Python `3.12` and `3.13`.
- **pip**, included with Python, to install the project. Cardiff's build configuration requires `setuptools>=68`.
- The package dependencies are installed by pip: `PyYAML>=6,<7` and `segno>=1.6,<2`. The development dependency is `pytest>=8,<9`.
- **Optional:** XeLaTeX on `PATH` for Unicode-safe real PDF rendering. No XeLaTeX version is pinned in the repository. Without it, Cardiff uses its deterministic fallback, which supports ASCII-only preview/title text.

Before cloning the project, install Git and Python 3.12 or newer. Use the commands for your operating system:

```powershell
# Windows 10/11 (PowerShell with WinGet)
winget install --id Git.Git --exact
winget install --id Python.Python.3.12 --exact
```

```bash
# macOS (with Homebrew)
brew install git python@3.12
```

```bash
# Ubuntu 24.04
sudo apt update
sudo apt install -y git python3.12 python3.12-venv
```

On Windows without WinGet, download and run the installers from [git-scm.com](https://git-scm.com/downloads) and [python.org/downloads/](https://www.python.org/downloads/); enable **Add Python to PATH** in the Python installer. Other Linux distributions may use different package names or repositories; use their package manager to install Git and Python 3.12 or newer.

#### Optional: GitHub CLI

The GitHub CLI (`gh`) is not required to install or run Cardiff. It is useful for working with GitHub from a terminal—for example, viewing and checking repository issues and pull requests. On Windows with WinGet, install it with:

```powershell
winget install GitHub.cli --source winget
```

1. Open a new terminal and check that the tools are available and Python meets the minimum version:

   ```powershell
   git --version
   python --version
   python -m pip --version
   ```

   `python --version` must report Python 3.12 or newer. On macOS/Linux, if the command is `python3` or `python3.12`, use that command in place of `python` below.
2. **Optional, for Unicode-safe real rendering:** install one of these TeX distributions. Each command installs the distribution or XeLaTeX package named in its comment:

   ```powershell
   # Windows: install MiKTeX with WinGet
   winget install --id MiKTeX.MiKTeX --exact
   ```

   ```bash
   # macOS: install MacTeX with Homebrew
   brew install --cask mactex
   ```

   ```bash
   # Ubuntu 24.04: install XeLaTeX from TeX Live
   sudo apt install -y texlive-xetex
   ```

   These are package-manager installs; the Ubuntu command installs TeX Live's XeLaTeX package rather than the full TeX Live collection. You can also use the official installers for [TeX Live](https://www.tug.org/texlive/), [MacTeX](https://www.tug.org/mactex/), or [MiKTeX](https://miktex.org/). Ensure the `xelatex` executable is available on `PATH`, then check it with:

   ```powershell
   xelatex --version
   ```

   This is not required for the deterministic ASCII-only rendering path.

Node.js, PHP, Composer, and a database are not part of the current project stack.

### 2. Clone and install

From the directory where you keep your source code, clone the repository and enter the Python package directory:

```powershell
git clone https://github.com/zcalifornia-ph/cardiff.git
cd cardiff\cardiff
```

Create and activate a virtual environment, then install Cardiff and its test dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

For Bash or Zsh, activate the same virtual environment with:

```bash
source .venv/bin/activate
```

This command installs Cardiff in editable mode along with its declared runtime dependencies (`PyYAML` and `segno`) and development test dependency (`pytest`). It provides the `cardiff` command; the distribution name in package metadata is `cardiff-cli`.

### 3. Environment setup

There is no `.env.example` file, and the current CLI does not require runtime environment variables or secrets. No `.env` file needs to be created.

| Variable | Purpose | Secret? | Where to get its value |
| --- | --- | --- | --- |
| None defined | The current CLI has no environment-variable configuration. | N/A | No value required. |

### 4. Database setup

The current project does not use a database and contains no database configuration, migrations, or seeders. There is no database to create and no default account for testing. The sample request in `tests/fixtures/requests/valid-request.yaml` is test input, not an account.

### 5. Run locally

Cardiff currently runs as a command-line tool; it does not start a development server or provide a local web URL. From the `cardiff/` package directory, validate the checked-in sample request:

```powershell
python -m cardiff validate tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets
```

Render the same request to a PDF using the deterministic adapter:

```powershell
python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output output/business-card.pdf --deterministic
```

The PDF is written to `output/business-card.pdf`. Use the `cardiff` command instead of `python -m cardiff` if you prefer the installed console entry point.

### 6. Verify the setup

The validation command should print a JSON success status and exit with code `0`. The render command should report success and create the PDF at the requested output path.

Run the targeted test suites used by GitHub Actions CI:

```powershell
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

The checked-in verification baseline test counts are documented in [CONTRIBUTING.md](CONTRIBUTING.md#verification-notes).
### 7. Troubleshooting

- **Python version is too old:** confirm Python is `3.12+`, then create the virtual environment with that interpreter and reinstall the package dependencies.
- **PowerShell cannot find `cardiff` or `cardiff` runs the wrong Python:** activate `.venv` in the `cardiff/` package directory, or run the documented `python -m cardiff` commands there.
- **Non-ASCII text fails to render:** install XeLaTeX and ensure `xelatex` is on `PATH`, or use `--deterministic` only with ASCII-only preview/title text.
- **Tests fail during broad collection due to temporary directories:** run the three targeted test commands above. The CI workflow removes transient test directories before running them; a broad `python -m pytest tests -q -p no:cacheprovider` run may encounter leftover temporary directories.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repository Layout

```text
cardiff/
  .github/
    workflows/
      ci.yml
      release.yml
  cardiff/
    cardiff.py
    pyproject.toml
    src/cardiff/
      __init__.py
      __main__.py
      cli.py
      contract/
      rendering/
        directives.py
      templates/
        business-card/
    tests/
      cli/
      contract/
      rendering/
        test_directives.py
      fixtures/
        approved-assets/
        approved-samples/
    docs/
      cli-quickstart.md
      render-pipeline.md
      template-authoring.md
      validation-contract.md
  docs/
    version-0-0-2-docs.md
    version-0-0-3-docs.md
    version-0-0-4-docs.md
    version-0-1-0-docs.md
    version-0-1-1-docs.md
    version-0-1-2-docs.md
    version-0-1-3-docs.md
    version-0-1-4-docs.md
    version-0-1-5-docs.md
    version-0-1-6-docs.md
    version-0-1-7-docs.md
  learn/
    unit-001-bolt-001a-study-guide.md
  README.md
  REQUIREMENTS.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] `UNIT-001 / BOLT-001A`: canonical contract and validation foundation
- [x] `UNIT-001 / BOLT-001B`: render pipeline and template resolution
- [x] `UNIT-001 / BOLT-001C`: CLI operator flow
- [ ] `UNIT-002`: template quality and controlled customization
- [ ] `UNIT-003`: CSV batch generation
- [ ] `UNIT-004`: FastAPI service mode
- [ ] `UNIT-005`: runtime packaging, broader CI, deployment, and ops readiness

Initial GitHub Actions validation and release workflows are already in-tree, but the broader `UNIT-005` runtime packaging, deployment, and operational-readiness scope remains open.

See the [open issues](https://github.com/zcalifornia-ph/cardiff/issues) for proposed features and known gaps.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Documentation

Start with these project artifacts:

- `README.md` for the repo-level product and status summary
- `CHANGELOG.md` for the latest repo-state notes, cleanup candidates, and release history
- `REQUIREMENTS.md` for the public implementation scope, current unit status, and acceptance baseline
- `cardiff/docs/validation-contract.md` for the canonical request contract
- `cardiff/docs/render-pipeline.md` for the shared render pipeline and adapter behavior
- `cardiff/docs/cli-quickstart.md` for the current CLI workflow and exit-code contract
- `cardiff/docs/template-authoring.md` for the approved business-card template package rules and contributor-facing template expectations
- `.github/workflows/ci.yml` for the current targeted validation matrix on pushes and pull requests
- `.github/workflows/release.yml` for the current tag-gated release verification and publish flow
- `learn/unit-001-bolt-001a-study-guide.md` for the guided walkthrough of the contract foundation
- `docs/version-0-1-7-docs.md` for the latest checked-in versioned documentation-release notes beyond this README and changelog

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are welcome, especially around render quality, CLI ergonomics, batch and API reuse, runtime parity, and documentation quality.
See `CONTRIBUTING.md` for workflow expectations.

1. Fork the repository.
2. Create a short-lived branch from the integration branch you intend to target (`main` or `rev`).
3. Make the smallest cohesive change that solves the problem.
4. Update docs and tests when applicable.
5. Open a pull request targeting that same integration branch with clear context and verification details.
6. Delete the short-lived branch after merge.

### Top Contributors

<a href="https://github.com/zcalifornia-ph/cardiff/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zcalifornia-ph/cardiff" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the Apache License 2.0.
See `LICENSE.txt` for the full license text.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Maintainer: [@zcalifornia_](https://twitter.com/zcalifornia_) - zecalifornia@up.edu.ph

Project Link: [https://github.com/zcalifornia-ph/cardiff](https://github.com/zcalifornia-ph/cardiff)

LinkedIn: [https://www.linkedin.com/in/zcalifornia](https://www.linkedin.com/in/zcalifornia)

ORCID: [https://orcid.org/0009-0002-2357-7606](https://orcid.org/0009-0002-2357-7606)

ResearchGate: [https://www.researchgate.net/profile/Zildjian-California](https://www.researchgate.net/profile/Zildjian-California)

X/Twitter: [https://twitter.com/zcalifornia_](https://twitter.com/zcalifornia_)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* The Python ecosystem packages used in this repository, especially `setuptools`, `PyYAML`, and `pytest`.
* The XeLaTeX toolchain that Cardiff targets for runtime parity when real compiler execution is available.
* The broader template-driven document tooling ecosystem that informs Cardiff's contract-first rendering approach.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/zcalifornia-ph/cardiff.svg?style=for-the-badge
[contributors-url]: https://github.com/zcalifornia-ph/cardiff/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zcalifornia-ph/cardiff.svg?style=for-the-badge
[forks-url]: https://github.com/zcalifornia-ph/cardiff/network/members
[stars-shield]: https://img.shields.io/github/stars/zcalifornia-ph/cardiff.svg?style=for-the-badge
[stars-url]: https://github.com/zcalifornia-ph/cardiff/stargazers
[issues-shield]: https://img.shields.io/github/issues/zcalifornia-ph/cardiff.svg?style=for-the-badge
[issues-url]: https://github.com/zcalifornia-ph/cardiff/issues
[license-shield]: https://img.shields.io/github/license/zcalifornia-ph/cardiff.svg?style=for-the-badge
[license-url]: https://github.com/zcalifornia-ph/cardiff/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/zcalifornia
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[XeLaTeX]: https://img.shields.io/badge/XeLaTeX-008080?style=for-the-badge&logo=latex&logoColor=white
[XeLaTeX-url]: https://www.latex-project.org/
[PyYAML]: https://img.shields.io/badge/PyYAML-CB171E?style=for-the-badge
[PyYAML-url]: https://pyyaml.org/
[segno-badge]: https://img.shields.io/badge/segno-111111?style=for-the-badge
[segno-url]: https://segno.readthedocs.io/
[pytest-badge]: https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white
[pytest-url]: https://pytest.org/
