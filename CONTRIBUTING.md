# Contributing

Thanks for contributing to Cardiff.

Cardiff is currently in the bootstrap stage, so contributions should stay tightly aligned with the project direction: a CLI and API for standardized, print-ready business cards and nameplates generated from structured data.

## Before You Start

- Check for an existing issue or discussion before starting work.
- Open an issue first for significant product, architecture, or workflow changes.
- Keep changes focused and easy to review.
- Make sure your work follows `CODE_OF_CONDUCT.md` and `SECURITY.md`.

## What Good Contributions Look Like

Strong contributions usually:

- solve a clearly described problem
- include documentation updates when behavior or scope changes
- include validation evidence such as tests, screenshots, logs, or reproducible steps
- explain tradeoffs when introducing new dependencies, interfaces, or architecture
- avoid promising features that are not implemented yet

## Workflow

1. Fork the repository.
2. Create a short-lived branch from `main`.
3. Name the branch in kebab-case and start it with the relevant Conventional Commit type.
4. Make the smallest cohesive change that solves the problem.
5. Update docs and tests when applicable.
6. Open a pull request with clear context and verification details.

Example branch name:

```text
feat/add-csv-batch-parser
```

## Commit Messages

Use Conventional Commits.

Examples:

```text
feat: add initial CSV batch parsing contract
fix: prevent invalid logo path handling
docs: clarify planned API service scope
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
