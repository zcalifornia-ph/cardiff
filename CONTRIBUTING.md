# Contributing

Thanks for contributing to Cardiff.

Cardiff is now in an early pre-alpha implementation stage.
`UNIT-001` is complete, the first CLI operator flow is in place, and the checked-in repo now also includes QR-directive rendering work.
Contributions should stay tightly aligned with the approved roadmap instead of jumping ahead with disconnected features.

## Before You Start

- Check for an existing issue or discussion before starting work.
- Open an issue first for significant product, architecture, or workflow changes.
- Keep changes focused and easy to review.
- Read `README.md`, `REQUIREMENTS.md`, and the relevant docs under `cardiff/docs/` before starting implementation work.
- If you change the request contract, update `cardiff/docs/validation-contract.md` and the relevant tests in `cardiff/tests/contract/`.
- If you change template resolution, rendering behavior, or QR directive preprocessing, update `cardiff/docs/render-pipeline.md` and the relevant tests in `cardiff/tests/rendering/`, including `test_directives.py` when directive or vCard behavior changes.
- If you change CLI behavior, entrypoint wiring, status payloads, or exit-code semantics, update `cardiff/docs/cli-quickstart.md` and the relevant tests in `cardiff/tests/cli/`.
- If you change the approved sample request, template manifest semantics, deterministic render behavior, or any fingerprint-bearing artifact, refresh `cardiff/tests/fixtures/approved-samples/business-card/reference-evidence.json` and call that out in your pull request.
- Do not refresh reference evidence for path-only or line-ending-only checkout differences; the normalized evidence fingerprints are expected to stay stable across those environment details.
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
2. Create a short-lived branch from `rev`.
3. Name the branch in kebab-case and start it with the relevant Conventional Commit type.
4. Make the smallest cohesive change that solves the problem.
5. Update docs and tests when applicable.
6. Open a pull request targeting `rev` with clear context and verification details.
7. Delete the branch after the pull request is merged.

Example branch name:

```text
feat/add-cli-render-command
```

Branch policy notes:

- Use short-lived branches only.
- Keep one branch focused on one issue or cohesive change.
- Sync `rev` before creating a new branch.

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

## Verification Notes

Use the targeted suites for this repo state:

```powershell
cd cardiff
python -m pytest tests/contract -q -p no:cacheprovider
python -m pytest tests/rendering -q -p no:cacheprovider
python -m pytest tests/cli -q -p no:cacheprovider
```

The broad `python -m pytest tests -q -p no:cacheprovider` command can currently fail if temporary QR work directories are still present under `cardiff/tests/fixtures/approved-samples/business-card/`.
Clean those directories before relying on broad test collection.

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
