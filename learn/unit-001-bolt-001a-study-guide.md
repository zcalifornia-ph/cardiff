# Unit 1 Bolt 1A Study Guide

## Title

Understanding `UNIT-001 / BOLT-001A`: Building Cardiff's Canonical Contract and Validation Kernel

## Quick Diagnostic Read

You are ready for this guide if you can:

- read small Python modules without panicking,
- understand what a data model is,
- follow a test and explain what behavior it is checking.

What is new and high-value in this bolt:

- turning YAML and JSON into one canonical request shape,
- separating parsing from validation from sanitization,
- rejecting unsafe inputs before any renderer exists,
- making tests act as contract documentation, not just bug checks.

## One-Sentence Objective

Understand how `BOLT-001A` turns Cardiff's "safe structured input" requirement into an actual Python contract kernel that later CLI, batch, API, and renderer work can all reuse without drift.

## Why This Bolt Matters

This bolt is the front gate of Cardiff.

Later Units will add:

- CLI commands,
- batch CSV workflows,
- a FastAPI service,
- actual PDF rendering.

But all of those rely on one shared question:

"What counts as a valid render request?"

If that answer is inconsistent, the product becomes fragile fast.

So this bolt solves the right first problem:

- define the request model,
- define the failure taxonomy,
- define the sanitization boundary,
- define the asset-path guardrails,
- prove the behavior with focused tests.

Mental model:

- renderer logic draws the card,
- this bolt decides what is even allowed to reach the renderer.

## Plan A / Plan B

### Plan A (Recommended): Code-First in 75-120 Minutes

1. Read `cardiff/src/cardiff/contract/models.py`.
2. Read `cardiff/src/cardiff/contract/loaders.py`.
3. Read `cardiff/src/cardiff/contract/validation.py`.
4. Read `cardiff/src/cardiff/contract/sanitization.py`.
5. Read the tests in `cardiff/tests/contract/`.
6. Use this guide to connect the modules into one flow.

### Plan B: Test-First in 45-90 Minutes

1. Read `cardiff/tests/contract/test_models.py`.
2. Read `cardiff/tests/contract/test_validation.py`.
3. Read `cardiff/tests/contract/test_security.py`.
4. Ask what production code must exist to satisfy those tests.
5. Read the implementation after that.

Use Plan B if production code feels abstract but examples and assertions make immediate sense to you.

## System View (Mental Model)

```text
input source
  -> load_request_document()
      -> RawRequestDocument
  -> parse_render_request()
      -> decoded mapping
  -> validate_render_request()
      -> field checks
      -> template checks
      -> asset-path checks
      -> unsafe-content checks
  -> result
      -> ValidationResult(accepted + RenderRequest)
      or
      -> ValidationResult(rejected + ValidationIssue[])
```

This is not the renderer.
It is the contract kernel in front of the renderer.

Think of it as a compiler front end:

- parsing decides whether the source document is structurally readable,
- validation decides whether the content obeys the rules,
- sanitization prepares safe text for later rendering.

## What We Built (Artifact Map)

### Code

- `cardiff/pyproject.toml`
- `cardiff/src/cardiff/__init__.py`
- `cardiff/src/cardiff/contract/__init__.py`
- `cardiff/src/cardiff/contract/errors.py`
- `cardiff/src/cardiff/contract/models.py`
- `cardiff/src/cardiff/contract/loaders.py`
- `cardiff/src/cardiff/contract/validation.py`
- `cardiff/src/cardiff/contract/sanitization.py`

### Tests and Fixtures

- `cardiff/tests/conftest.py`
- `cardiff/tests/contract/test_models.py`
- `cardiff/tests/contract/test_validation.py`
- `cardiff/tests/contract/test_security.py`
- `cardiff/tests/fixtures/requests/valid-request.json`
- `cardiff/tests/fixtures/requests/valid-request.yaml`
- `cardiff/tests/fixtures/approved-assets/README.md`

### Docs and Review Artifacts

- `cardiff/docs/validation-contract.md`
- `REQUIREMENTS.md`
- supplemental design, ADR, and traceability notes captured during `UNIT-001 / BOLT-001A` review

### Verification

- `python -m pytest tests/contract -q -p no:cacheprovider`
- Result on March 15, 2026: `8 passed`

## Guided Walkthrough

## 1) Start With the Public Language of the System

Open `cardiff/src/cardiff/contract/models.py` first.

This file defines the nouns that the rest of the bolt speaks:

- `RawRequestDocument`
- `ValidationIssue`
- `AssetReference`
- `TemplateSelection`
- `IdentityProfile`
- `RenderRequest`
- `ValidationResult`

This is a very good first move because it answers:

- what data exists,
- what shape it has,
- what the system returns on success and failure.

### Why `dataclass(frozen=True, slots=True)` matters

This is worth understanding.

- `dataclass` gives you clean model objects without verbose boilerplate.
- `frozen=True` makes instances immutable after creation.
- `slots=True` keeps them lightweight and more explicit.

Why that is good here:

- contract objects should be predictable,
- validation results should not mutate accidentally,
- later adapters should treat these as stable value objects.

High-yield takeaway:

- immutability is a cheap way to reduce accidental state bugs in boundary code.

## 2) Understand the Success and Failure Surface

`ValidationResult` is the core return type.

It contains:

- `outcome`
- `request`
- `issues`

This is a strong design decision because callers do not need exceptions for normal validation failures.

Instead, they can ask:

- was the request accepted?
- if yes, what canonical request object do I get?
- if no, what deterministic issues should I show?

That makes future CLI and API behavior easier to keep aligned.

CLI can print issues.
API can serialize issues.
Batch mode can attach issues to rows.

One kernel, multiple surfaces.

## 3) Learn the Loading Layer Before the Validation Layer

Read `cardiff/src/cardiff/contract/loaders.py`.

Its job is simple:

- accept a path, stream, or raw string,
- infer JSON versus YAML,
- decode the source,
- hand the decoded mapping to validation.

The important functions are:

- `load_request_document()`
- `parse_render_request()`
- `load_and_validate_request()`

### Why this separation is good

It avoids mixing concerns.

- loading answers: "Can I read and decode this source?"
- validation answers: "Does this decoded object obey Cardiff's rules?"

That means a parse failure becomes `contract_error`, while a bad field becomes something more specific like:

- `missing_required`
- `unknown_field`
- `invalid_type`

This distinction is important because users should not get one vague "bad input" blob.

## 4) The Validation Pipeline Is the Real Heart of the Bolt

Read `cardiff/src/cardiff/contract/validation.py` carefully.

This file is doing the main engineering work.

It defines:

- allowed top-level fields,
- required identity fields,
- allowed template fields,
- allowed template options,
- allowed asset slots,
- allowed asset extensions,
- symbolic slug rules,
- hex color rules.

This is the rulebook.

### The key validation stages

`validate_render_request()` does this:

1. reject non-mapping payloads,
2. reject unknown top-level fields,
3. validate `identity`,
4. validate `template`,
5. validate `assets`,
6. return either deterministic issues or a canonical `RenderRequest`.

That is a clean pipeline.

You should notice two things:

- validation is explicit, not magical,
- issue ordering is deterministic because `_finalize_issues()` sorts them.

That second detail is easy to miss, but it matters for testing and predictability.

If bad input produces issues in random order, tests become noisy and user experience becomes harder to trust.

## 5) Study the Identity Rules Like a Reviewer

The identity rules are small on purpose.

Required fields:

- `full_name`
- `role`
- `email`

Optional fields:

- `phone`
- `organization`
- `department`
- `website`
- `pronouns`
- `address_lines`

### Why small scope is correct here

The goal of this bolt is not "support every possible profile field."
The goal is "prove the contract boundary works."

A smaller field set gives you:

- stricter validation,
- clearer docs,
- fewer accidental edge cases,
- faster learning.

This is good scoping discipline.

## 6) Template Safety Is About Symbolic Control

The template rules matter because raw paths are dangerous.

`template.id` must be a symbolic slug like:

- `business-card`

Not:

- `../templates/evil.tex`
- `C:\something\random`

That is a security and architecture decision at the same time.

Security reason:

- you do not want user input selecting arbitrary files.

Architecture reason:

- templates should be chosen by logical identity, not filesystem accident.

This is a very good example of one rule solving two problems at once.

## 7) Asset Validation Teaches Defensive Filesystem Thinking

`validate_asset_reference()` is worth special attention.

It rejects:

- unsupported asset slots,
- remote URLs,
- absolute paths outside approved roots,
- parent traversal like `..`,
- unsupported file extensions.

This is the right mindset for any system that touches files based on input.

You never want to trust path strings just because they look convenient.

High-yield mental model:

- a user-provided path is not a file,
- it is an attack surface until proven safe.

## 8) Sanitization Is a Boundary, Not a Cosmetic Helper

Read `cardiff/src/cardiff/contract/sanitization.py`.

This file does two related things:

- normalize whitespace,
- reject unsafe control fragments and escape LaTeX-sensitive characters.

Unsafe patterns include backslashes and template-like fragments.

Then safe text is escaped with `LATEX_ESCAPE_MAP`.

### Why this matters

You are not rendering yet, but you are already shaping the future rendering boundary.

That is exactly the right time to decide:

- what text is unsafe,
- what gets escaped,
- what later layers are allowed to assume.

If sanitization is bolted on later, you get inconsistent behavior and security drift.

## 9) Tests Are the Fastest Way to Understand Behavior

The tests are small and high-signal.

### `test_models.py`

Teaches:

- JSON and YAML must normalize into the same contract,
- successful inputs get sanitized,
- canonical structure is shared across formats.

### `test_validation.py`

Teaches:

- missing required fields fail before rendering,
- unknown fields are rejected deterministically,
- invalid template IDs and option types are surfaced clearly.

### `test_security.py`

Teaches:

- parent traversal is rejected,
- remote asset URLs are rejected,
- seeded LaTeX control content is rejected.

This is the part many learners miss:

- tests are not only proofs,
- they are executable summaries of the intended system behavior.

## 10) The Supplemental Design Artifacts Still Matter After the Code Lands

Do not ignore the docs just because implementation now exists.

The supporting design artifacts still serve different purposes:

- the domain-design notes explain the concepts and invariants,
- the logical-design notes explain module boundaries and flow,
- the `BOLT-001A` ADR explains why this path was chosen,
- the traceability notes link the bolt to tests, risks, and downstream checks,
- `REQUIREMENTS.md` records the bolt as complete with evidence.

This is how you keep implementation, design, and lifecycle evidence synchronized.

That is a professional engineering habit, not busywork.

## Copy-Paste Commands

### Read the Core Files

```powershell
Get-Content cardiff\src\cardiff\contract\models.py
```

```powershell
Get-Content cardiff\src\cardiff\contract\loaders.py
```

```powershell
Get-Content cardiff\src\cardiff\contract\validation.py
```

```powershell
Get-Content cardiff\src\cardiff\contract\sanitization.py
```

### Read the Tests

```powershell
Get-Content cardiff\tests\contract\test_models.py
```

```powershell
Get-Content cardiff\tests\contract\test_validation.py
```

```powershell
Get-Content cardiff\tests\contract\test_security.py
```

### Run the Verification Command

```powershell
cd d:\Programming\Repositories\cardiff\cardiff
python -m pytest tests/contract -q -p no:cacheprovider
```

Expected result:

- `8 passed`

## Pitfalls + Debugging (High Yield)

### 1) Confusing Parsing Errors With Validation Errors

- Symptom: you treat malformed YAML and bad contract fields as the same kind of failure.
- Fix: keep the layers separate in your head.

Rule:

- decode failure -> `contract_error`
- readable but invalid data -> specific validation issue codes

### 2) Thinking Sanitization Means "Accept Anything"

- Symptom: you expect unsafe content to be auto-fixed.
- Fix: remember the contract rejects some content and escapes other content.

Good boundary rule:

- benign special characters can be escaped,
- dangerous control patterns should be rejected.

### 3) Forgetting Why Symbolic Template IDs Exist

- Symptom: raw paths feel "more flexible."
- Fix: ask what that flexibility would permit.

If input can point anywhere, you lose both safety and contract clarity.

### 4) Ignoring Deterministic Issue Ordering

- Symptom: issue order seems like a minor detail.
- Fix: remember that predictable ordering improves tests, CLI output, and API consistency.

### 5) Treating the Tests as Secondary

- Symptom: you read the code only and skip the tests.
- Fix: read the tests early. They are the quickest summary of the behavior we promised.

### 6) Missing the Reason for the Framework-Agnostic Choice

- Symptom: you ask why Pydantic was not used immediately.
- Fix: read the ADR again.

The answer is not "Pydantic is bad."
The answer is "this bolt needed a stable reusable boundary before framework coupling."

## Skill Transfer: What You Should Internalize

After this bolt, you should be able to explain:

1. Why a multi-surface product needs one canonical contract early.
2. Why loading, validation, and sanitization should be separate stages.
3. Why symbolic identifiers are safer than raw paths.
4. Why stable issue codes matter for future CLI, batch, and API behavior.
5. Why tests are part of the contract, not an afterthought.

If you can explain those five clearly, you understood the real engineering value of this bolt.

## Practice Drill (25-45 Minutes)

### Task

Do one design-plus-code drill:

1. Add one new optional identity field called `linkedin_url`.
2. Update the contract rules consistently.
3. Decide whether it belongs in docs immediately.
4. Add one passing test and one failing test for it.
5. Re-run the contract suite.

### What this drill teaches

- how contract drift starts,
- how one field change affects models, validation, docs, and tests,
- how to make a controlled contract change instead of a sloppy one.

### Self-Check

You pass if you can answer:

- where the new field must be added,
- which tests need to change,
- whether the validation doc must change,
- why this is a contract change and not "just one more property."

## Mini Competency Map

- Level 1: Can explain the flow from input source to `ValidationResult`.
- Level 2: Can explain why each module exists and what boundary it owns.
- Level 3: Can add a small contract field without breaking deterministic behavior.
- Level 4: Can review future CLI or API adapters and detect contract drift or security regressions.

## 24-72 Hour Next Steps

1. Re-run the tests yourself and inspect one passing and one failing case.
2. Write one sample request in YAML and the same request in JSON from memory.
3. Explain the difference between `ValidationIssue`, `ValidationResult`, and `RenderRequest` without looking.
4. Before starting `BOLT-001B`, sketch how the renderer should consume `RenderRequest` without re-validating business rules.

---

This guide should leave you with one strong habit: when a system will have multiple entry points, stabilize the contract and failure language early so the rest of the product has solid ground to stand on.
