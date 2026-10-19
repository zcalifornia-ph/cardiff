# [DOCUMENTATION] [rev] Update the stale test-count baseline in README.md and REQUIREMENTS.md

## Summary

`README.md` and `REQUIREMENTS.md` both state a verification baseline of 9 contract, 25 rendering, and 14 CLI tests passing. The suites have grown to 51, 46, and 19. `CONTRIBUTING.md` already documents the current counts, including the platform- and XeLaTeX-dependent skips. Contributors following the README therefore see far more tests than the documented baseline and cannot tell whether their run is correct. The desired outcome is that every root document states the same current counts, or points to the single place that does.

## Issue Type

Primary type: documentation

Labels:
- `documentation` (pre-existing)
- `good first issue` (pre-existing)
- `light work` (pre-existing)

Secondary types: none.

## Readiness Grade

AGENT_READY

The stale lines and the current reference counts are directly observed. The actual counts were measured on a clean export of the commit. The change is documentation-only, with a text-comparison oracle.

## Source Context

Path-scoped context in the current repository: `README.md`, with supporting reads of `REQUIREMENTS.md` and `CONTRIBUTING.md`.

## Detection Context

Detected in branch: `rev`

GitHub repository: zcalifornia-ph/cardiff

Local artifact path: `docs/issues/issue-documentation-readme.md`

Line numbers below are from `rev` at commit `5caba1e`.

## Blockers and Dependencies

No blockers identified from the loaded evidence.

## Scope

In scope:
- `README.md` line 305;
- the "Recorded Verification" expected-result list in `REQUIREMENTS.md` (lines 44-48).

Out of scope:
- Changing tests.
- Changing `CONTRIBUTING.md`, whose counts are already current.
- Other content in those files.

## Current / Observed Behavior

- `README.md` line 305: "The checked-in verification baseline is 9 contract, 25 rendering, and 14 CLI tests passing."
- `REQUIREMENTS.md` lines 46-48: "9 contract tests pass", "25 rendering tests pass", "14 CLI tests pass".
- `CONTRIBUTING.md` lines 116-120:
  - `tests/contract`: `50 passed, 1 skipped` (`51 passed` on Windows);
  - `tests/rendering`: `46 passed` (`42 passed, 4 skipped` without `xelatex` on `PATH`);
  - `tests/cli`: `19 passed`.
- Measured at `5caba1e` on Windows 11, Python 3.14.0, with `xelatex` on `PATH`: `51 passed` (contract), `46 passed` (rendering), `19 passed` (CLI).

## Expected / Target Behavior

`README.md` and `REQUIREMENTS.md` either state the same counts as `CONTRIBUTING.md`, including the Windows and no-XeLaTeX variants, or refer readers to the `CONTRIBUTING.md` Verification Notes instead of repeating numbers. No root document states 9, 25, or 14 as the current baseline.

## Reproduction Steps or Validation Steps

1. Run `grep -n "9 contract\|25 rendering\|14 CLI" README.md REQUIREMENTS.md` from the repository root.
2. From `cardiff/`, run `python -m pytest tests/contract -q -p no:cacheprovider`, `python -m pytest tests/rendering -q -p no:cacheprovider`, and `python -m pytest tests/cli -q -p no:cacheprovider`.
3. Failing observation: step 1 prints matches, and step 2 reports counts that differ from them. After the fix, step 1 prints nothing, and the documents agree with `CONTRIBUTING.md`.

## Environment and Evidence

- **Runtime for the measured counts:** Windows 11, Python 3.14.0, MiKTeX-XeTeX 4.16, in a clean `git archive` export of `5caba1e`.
- **Commands:** from `CONTRIBUTING.md` Verification Notes and `README.md`.

## Relevant Files, Symbols, and Tests

- `README.md`: line 305. Directly observed.
- `REQUIREMENTS.md`: lines 40-49 ("Recorded Verification"). Directly observed.
- `CONTRIBUTING.md`: lines 108-122 (Verification Notes). Directly observed.

## Agent Handoff Notes

- Preferred direction, as a hypothesis: point `README.md` and `REQUIREMENTS.md` at `CONTRIBUTING.md` for counts, so future test additions only need one edit.
- Search terms: `9 contract`, `25 rendering`, `14 CLI`, `Verification Notes`.
- Constraint: keep the surrounding command blocks unchanged.

## Acceptance Criteria

- [ ] `README.md` does not state 9 contract, 25 rendering, and 14 CLI tests as the baseline.
- [ ] `REQUIREMENTS.md` does not state 9 contract, 25 rendering, and 14 CLI tests as the expected result.
- [ ] Any test counts remaining in `README.md` match `CONTRIBUTING.md` lines 116-120.
- [ ] Any test counts remaining in `REQUIREMENTS.md` match `CONTRIBUTING.md` lines 116-120.
- [ ] No file outside `README.md` and `REQUIREMENTS.md` changes.

## Test / Verification Plan

- **Existing tests to run:** the three suites, to confirm the counts quoted (commands from `CONTRIBUTING.md`).
- **New tests likely needed:** none.
- **Manual check:** the grep in the validation steps.
- **Regression checks:** the links and command blocks around the edited lines still render.
- **Security and performance checks:** not applicable.

## Implementation Boundaries

- **Non-goals:** no restructuring of `README.md` or `REQUIREMENTS.md`.
- **Forbidden shortcuts:** do not delete the verification sections; correct or redirect them.
- **Conventions:** the existing heading and list style in each file.

## Risks and Review Focus

- **Documentation drift:** if counts are kept inline, they will go stale again with the next test added. Review whether a reference to `CONTRIBUTING.md` is the better choice.

## Work Mapping

Reporter-supplied context (codebase stability audit) -> `README.md`, `REQUIREMENTS.md` -> acceptance criteria above -> verification plan above.

## Open Questions

No open questions identified from the loaded evidence.

## Definition of Done

- [ ] code change is scoped to the in-scope list
- [ ] all acceptance criteria are observably met
- [ ] tests in the verification plan are added or updated and passing
- [ ] documentation, ADRs, or runbooks updated when the change requires it
- [ ] reviewer focus areas from the risk section are addressed
- [ ] work-mapping links are populated
- [ ] blocker/dependency status is resolved or explicitly carried forward
- [ ] issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots
