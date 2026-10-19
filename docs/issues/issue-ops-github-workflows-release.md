# [OPS] [rev] Run release verification on the same OS and XeLaTeX matrix as CI before publishing

## Summary

`.github/workflows/release.yml` runs its pre-publish test job on `ubuntu-latest` only, and it never installs XeLaTeX. The four XeLaTeX-gated rendering tests and the Windows-only contract test are therefore skipped. A tag can then be built and published to PyPI without those tests passing at the tagged commit. `.github/workflows/ci.yml` already runs Ubuntu and Windows with TeX Live and MiKTeX, and `CONTRIBUTING.md` already records the difference. The desired outcome is that release verification runs the same OS, Python, and XeLaTeX coverage as CI before the build and publish jobs run.

## Issue Type

Primary type: ops

Labels:
- `ops` (created before publication)
- `for experienced devs` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

Both workflows were read in full, and the difference is directly observed. `CONTRIBUTING.md` confirms it is known and intended to be temporary ("still"). The skip counts come from `CONTRIBUTING.md` and from the `skipif` guards in the test modules. Validation is a workflow run on a test tag or a `workflow_dispatch`-style dry run. The choice between a reusable workflow and duplicated steps is a non-blocking open question.

## Source Context

Path-scoped context in the current repository: `.github/workflows/release.yml`. Supporting reads:
- `.github/workflows/ci.yml`;
- `CONTRIBUTING.md` (Verification Notes);
- `cardiff/tests/rendering/test_pipeline.py` (XeLaTeX `skipif` guards).

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-ops-github-workflows-release.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

Related, text-only: #46 (closed) added the Windows leg to `ci.yml`. This issue carries the same coverage into `release.yml`.

## Scope

In scope:
- The `test` job in `.github/workflows/release.yml`:
  - an OS matrix of `ubuntu-latest` and `windows-latest`;
  - XeLaTeX installation and the compile check, matching `ci.yml`;
  - the same three suites.
- Keeping `build` and `publish` dependent on that job.

Out of scope:
- Changing `ci.yml` coverage.
- Changing the build, wheel-verification, or PyPI publish steps.
- Adding new test suites.

## Current / Observed Behavior

Observed in `.github/workflows/release.yml`:
- lines 46-53: job `test`, `runs-on: ubuntu-latest`, matrix `python-version: ["3.12", "3.13"]`;
- lines 54-91: checkout, Python setup, `pip install -e ".[dev]"`, cleanup, then the contract, rendering, and CLI suites. There is no XeLaTeX installation step;
- the `build` job needs `[validate_release, test]` (line 94), and `publish` needs `build` (lines 160-177).

Observed in `.github/workflows/ci.yml`:
- lines 13-20: `runs-on: ${{ matrix.os }}` with `os: [ubuntu-latest, windows-latest]`;
- lines 38-57: installs TeX Live (Linux) or MiKTeX (Windows);
- lines 59-67: compiles a check document before the tests.

Observed in `CONTRIBUTING.md`:
- line 111: "`release.yml` still verifies on `ubuntu-latest` only, without XeLaTeX.";
- lines 116-120: expected counts are `50 passed, 1 skipped` for contract on Ubuntu (`51 passed` on Windows), and `42 passed, 4 skipped` for rendering without `xelatex` on `PATH`.

Inferred: a release run today verifies 50 contract tests, 42 rendering tests, and 19 CLI tests, with 5 tests skipped, on Ubuntu only. A regression that only shows up with real XeLaTeX or on Windows can be published.

## Expected / Target Behavior

For a `v*` tag push, the release `test` job runs on `ubuntu-latest` and `windows-latest` for Python 3.12 and 3.13. It installs XeLaTeX exactly as `ci.yml` does, so its rendering suite reports `46 passed` with no XeLaTeX skips. `build` and `publish` run only after all four legs pass.

## Reproduction Steps or Validation Steps

1. Read `.github/workflows/release.yml` lines 46-91 and confirm there is no OS matrix and no XeLaTeX installation step.
2. Optional: in a fork, push a tag `v<version>` matching `cardiff/pyproject.toml` with the publish job disabled, and open the release `test` job log.
3. Failing observation: the rendering step reports `42 passed, 4 skipped`, and no Windows job exists. After the fix, the release run shows four `test` legs, and each rendering step reports `46 passed`.

## Environment and Evidence

- **Workflow files:** read at commit `5caba1e`.
- **Skip counts:** documented in `CONTRIBUTING.md` lines 116-120. Not re-measured in a GitHub Actions release run for this issue.
- **Local runs** at `5caba1e` on Windows 11 with Python 3.14.0 and MiKTeX: `51 passed` (contract), `46 passed` (rendering), `19 passed` (CLI).

## Relevant Files, Symbols, and Tests

- `.github/workflows/release.yml`: jobs `validate_release`, `test`, `build`, and `publish`. Directly observed.
- `.github/workflows/ci.yml`: job `test`, matrix and XeLaTeX steps. Directly observed.
- `CONTRIBUTING.md`: Verification Notes, lines 108-122. Directly observed.
- `cardiff/tests/rendering/test_pipeline.py`: the `skipif(shutil.which("xelatex") is None)` guards at lines 611 and 636. Directly observed.

## Agent Handoff Notes

- Copy or share the `ci.yml` steps that differ:
  - the `matrix.os` axis;
  - `defaults.run.shell: bash`;
  - the two XeLaTeX install steps;
  - the XeLaTeX compile check.
- Hypothesis to verify, not an instruction: a reusable workflow (`on: workflow_call`) that both `ci.yml` and `release.yml` call keeps the two from drifting again.
- Constraints:
  - Keep `permissions: contents: read` for the test job.
  - Keep the `id-token: write` permission only on `publish`.
  - Keep `build` depending on the test job.
- Search terms: `runs-on`, `Install XeLaTeX`, `needs:`.
- Assumption to avoid: CI passing on `main` or `rev` is not a release gate. `release.yml` runs on the tag push, independently of any earlier CI run.

## Acceptance Criteria

- [ ] The release `test` job runs on both `ubuntu-latest` and `windows-latest`.
- [ ] The release `test` job runs Python `3.12` and `3.13` on each OS.
- [ ] Each release `test` leg installs XeLaTeX before running the suites.
- [ ] Each release `test` leg reports `46 passed` for `tests/rendering` with no skips.
- [ ] The Windows release `test` legs report `51 passed` for `tests/contract`.
- [ ] `build` still requires every release `test` leg to pass.
- [ ] `CONTRIBUTING.md` no longer says that release verification runs without XeLaTeX.

## Test / Verification Plan

- **Existing tests to run:** the three suites, inside the new release matrix.
- **New tests likely needed:** none; this is workflow coverage.
- **Manual check:** a release run on a fork or a pre-release tag with publishing disabled; inspect the job list and the per-suite counts.
- **Regression checks:** tag-version validation (`validate_release`) still blocks mismatched tags; wheel verification and the smoke test still run.
- **Security checks:** the publish job's permissions and environment (`pypi`) are unchanged.
- **Performance checks:** expect longer release runs because of the MiKTeX installation. That is acceptable for a release gate (inferred).

## Implementation Boundaries

- **Non-goals:**
  - no change to what gets published;
  - no change to `ci.yml` behavior unless it is refactored into a shared workflow.
- **Forbidden shortcuts:**
  - Do not make the release `test` job optional.
  - Do not use `continue-on-error`.
- **Compatibility:** GitHub-hosted `ubuntu-latest` and `windows-latest` runners, as in `ci.yml`.
- **Conventions:** the step names and comments style used in `ci.yml`.

## Risks and Review Focus

- **Ops:** MiKTeX installation flakiness could block releases. Check that the `ci.yml` steps are copied exactly, including the package-database update and `AutoInstall`.
- **Security:** review workflow permissions on every job in the diff.
- **Documentation drift:** `CONTRIBUTING.md` Verification Notes.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `.github/workflows/release.yml`, `.github/workflows/ci.yml`, `CONTRIBUTING.md` -> acceptance criteria above -> verification plan above.

## Open Questions

- **Non-blocking, maintainer:** share the test job through a reusable workflow (`workflow_call`), or duplicate the steps in `release.yml`? Both satisfy the acceptance criteria. A shared workflow prevents future drift.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
