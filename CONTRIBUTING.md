# Contributing

Thanks for contributing to Cardiff.

Cardiff is now in an early pre-alpha implementation stage.
`UNIT-001` is complete and the first CLI operator flow is in place, so contributions should stay tightly aligned with the approved roadmap instead of jumping ahead with disconnected features.

## Before You Start

- Check for an existing issue or discussion before starting work.
- Open an issue first for significant product, architecture, or workflow changes.
- Keep changes focused and easy to review.
- Read `README.md`, `REQUIREMENTS.md`, and the relevant docs under `cardiff/docs/` before starting implementation work.
- If you change the request contract, update `cardiff/docs/validation-contract.md` and the relevant tests in `cardiff/tests/contract/`.
- If you change template resolution or rendering behavior, update `cardiff/docs/render-pipeline.md` and the relevant tests in `cardiff/tests/rendering/`.
- If you change CLI behavior, entrypoint wiring, status payloads, or exit-code semantics, update `cardiff/docs/cli-quickstart.md` and the relevant tests in `cardiff/tests/cli/`.
- Do not include generated Python cache files, bytecode, or editable-install metadata in a contribution.
- Make sure your work follows `CODE_OF_CONDUCT.md` and `SECURITY.md`.

## What Good Contributions Look Like

Strong contributions usually:

- solve a clearly described problem
- include documentation updates when behavior or scope changes
- include validation evidence such as tests, screenshots, logs, PDFs, or reproducible steps
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
- known risks, limitations, or follow-up work

Prefer small pull requests over large mixed changes.
If your work changes public behavior, update `README.md` and `CHANGELOG.md`.
If your work changes the canonical contract or approved scope, update `REQUIREMENTS.md` and the affected public docs as well.

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
