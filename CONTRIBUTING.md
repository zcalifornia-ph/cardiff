# Contributing

Thanks for contributing to Cardiff.

Cardiff is now in an early pre-alpha implementation stage.
`UNIT-001` is complete, the first CLI operator flow is in place, and the checked-in repo now also includes QR-directive rendering work.
The current repo also includes initial GitHub Actions validation and release workflows, though the broader `UNIT-005` runtime packaging and deployment scope is still open.
Contributions should stay tightly aligned with the approved roadmap instead of jumping ahead with disconnected features.

## Before You Start

- Check for an existing issue or discussion before starting work.
- Open an issue first for significant product, architecture, or workflow changes.
- Keep changes focused and easy to review.
- Read `README.md`, `REQUIREMENTS.md`, and the relevant docs under `cardiff/docs/` before starting implementation work.
- If you change the request contract, update `cardiff/docs/validation-contract.md` and the relevant tests in `cardiff/tests/contract/`.
- If you change template resolution, rendering behavior, or QR directive preprocessing, update `cardiff/docs/render-pipeline.md` and the relevant tests in `cardiff/tests/rendering/`, including `test_directives.py` when directive or vCard behavior changes.
- If you change template placeholder names, placeholder mapping, or approved template source files, add or update rendering tests that prove unknown placeholders fail before PDF generation instead of degrading silently.
- When a rendering test needs custom template source, use isolated temporary files instead of reusing fixed filenames inside the real approved template directory.
- If you change CLI behavior, entrypoint wiring, status payloads, or exit-code semantics, update `cardiff/docs/cli-quickstart.md` and the relevant tests in `cardiff/tests/cli/`.
- If you change the approved sample request, template manifest semantics, deterministic render behavior, or any fingerprint-bearing artifact, refresh `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` and call that out in your pull request.
- Do not refresh reference evidence for path-only or line-ending-only checkout differences; the normalized evidence fingerprints are expected to stay stable across those environment details.
- If you add or modify tracked Python source files, preserve the required attribution header and embedded Apache-2.0 license text so source attribution stays consistent across the maintained package/test surface.
- Do not include generated Python cache files, bytecode, or editable-install metadata in a contribution.
- Do not commit temporary QR work directories or generated directive scratch space from `cardiff/tests/fixtures/approved-samples/business-card/`.
- Make sure your work follows `CODE_OF_CONDUCT.md` and `SECURITY.md`.

## What Good Contributions Look Like

Strong contributions usually:

- solve a clearly described problem
- include documentation updates when behavior or scope changes
- include validation evidence such as tests, screenshots, logs, PDFs, or reproducible steps
- refresh or explicitly explain any approved evidence artifact that changes, especially `reference-evidence.json`
- avoid adding new CLI or framework dependencies when the existing contract or rendering kernels can be reused directly
- explain tradeoffs when introducing new dependencies, interfaces, or architecture
- avoid promising features that are not implemented yet

## Workflow

1. Fork the repository.
2. Create a short-lived branch from the integration branch you intend to target (`main` or `rev`).
3. Name the branch in kebab-case and start it with the relevant Conventional Commit type.
4. Make the smallest cohesive change that solves the problem.
5. Update docs and tests when applicable.
6. Open a pull request targeting that same integration branch with clear context and verification details.
7. Delete the branch after the pull request is merged.

Example branch name:

```text
feat/add-cli-render-command
```

Branch policy notes:

- Use short-lived branches only.
- Keep one branch focused on one issue or cohesive change.
- Sync the integration branch you plan to target before creating a new branch.
- The current GitHub Actions validation flow runs on pushes and pull requests for both `main` and `rev`.

## Commit Messages

Use Conventional Commits.

Examples:

```text
feat: add manifest-driven render pipeline
fix: prevent missing logo assets from reaching the render adapter
docs: clarify deterministic render evidence expectations
```

Common types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

## Pull Request Expectations

Each pull request should include:

- the problem being solved
- the approach taken
- validation evidence
- whether approved render evidence was refreshed or intentionally left mismatched
- known risks, limitations, or follow-up work

Prefer small pull requests over large mixed changes.
If your work changes public behavior, update `README.md` and `CHANGELOG.md`.
If your work changes the canonical contract or approved scope, update `REQUIREMENTS.md` and the affected public docs as well.
If your work changes packaging or release automation, keep `.github/workflows/release.yml`, the package metadata in `cardiff/pyproject.toml`, and the intended `v*` release tag consistent.

## Verification Notes

Use the targeted suites for this repo state:

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

These are the same suites enforced by `.github/workflows/ci.yml` and rerun by `.github/workflows/release.yml`.

The broad `python -m pytest tests -q -p no:cacheprovider` command can currently fail if temporary QR work directories or other stray temp directories are still present in the workspace.
Clean those directories before relying on broad test collection.

Expected current result:

- `tests/contract`: `9 passed`
- `tests/rendering`: `25 passed`
- `tests/cli`: `14 passed`

Release automation note:

- pushed `v*` release tags are expected to match the package version in `cardiff/pyproject.toml` exactly, for example `v0.1.7` -> `0.1.7`

## Review Standards

Reviewers may ask for:

- clearer problem framing
- tighter scope
- additional tests or validation
- better documentation
- safer defaults or a lower-risk design

## Security

Do not report vulnerabilities in public issues.
Use the process in `SECURITY.md` for responsible disclosure.

## Community Conduct

By participating in this project, you agree to follow `CODE_OF_CONDUCT.md`.
