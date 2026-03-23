# Business-Card Template Authoring

This guide is the contributor-facing policy for the approved `business-card` template package. It records what fields, options, and assets are supported for open source submissions without restating the full canonical validation or render rules.

Canonical references:

- Validation contract: [validation-contract.md](/cardiff/cardiff/docs/validation-contract.md)
- Render lifecycle and evidence model: [render-pipeline.md](/cardiff/cardiff/docs/render-pipeline.md)
- Approved asset-root fixture notes: [README.md](/cardiff/cardiff/tests/fixtures/approved-assets/README.md)

## Approved Template Package

- Template ID: `business-card`
- Manifest location: `cardiff/src/cardiff/templates/business-card/manifest.json`
- Entrypoint: `card.tex`
- Output: PDF
- Page size: `3.5in x 2.0in`
- Supported variants: `default` only
- Required asset slots for the approved template: `logo`
- Optional asset slots for the approved template: none

The shared contract can validate fields that the current approved template does not use yet. For Unit 2 review, contributors should treat the manifest as the final source of truth for template-specific support.

## Approved Field Map

Required identity fields:

- `identity.full_name`
- `identity.role`
- `identity.email`

Optional identity fields accepted by the canonical request contract:

- `identity.phone`
- `identity.organization`
- `identity.department`
- `identity.website`
- `identity.address_lines`
- `identity.pronouns`

Template selection fields:

- `template.id`
- `template.options.variant`
- `template.options.include_qr`
- `template.options.accent_hex`

Asset fields accepted by the shared contract:

- `assets.logo`
- `assets.avatar`

Current approved business-card rendering boundary:

- `assets.logo` is the only asset slot required by the approved business-card template.
- `assets.avatar` is not part of the approved business-card manifest and is not used by the current render path.
- Contributors should not submit business-card template changes that depend on new fields, new asset slots, or extra top-level request keys unless the validation contract and manifest are updated together.

Supported render placeholders today:

- `{{ full_name }}`
- `{{ role }}`
- `{{ email }}`
- `{{ organization }}`
- `{{ department }}`
- `{{ phone }}`
- `{{ website }}`
- `{{ pronouns }}`
- `{{ address_block }}`
- `{{ variant }}`
- `{{ accent_hex }}`
- `{{ logo_path }}`

Unknown placeholders are rejected before PDF generation with `template_placeholder_unknown`.
Contributors should treat that as a template-contract failure, not as a value that will be blanked automatically.

## Supported Options

- `variant` must be a symbolic slug. For the approved template, the only valid value is `default`.
- `include_qr` must be a boolean. The current template records QR state in the rendered output and review evidence as `enabled` or `disabled`.
- `accent_hex` must be a six-digit hex color such as `#0055AA`.

If a pull request proposes a new variant or a new option, it is out of scope unless the template manifest, validation coverage, and approval evidence are updated in the same change.

## Asset Packaging Rules

Asset paths are request data, not template package paths. Contributors should assume the caller supplies one or more approved asset roots and that all request asset references must resolve inside those roots.

Approved path expectations:

- Use relative paths such as `brand/logo.png` inside an approved asset root.
- Absolute paths are only acceptable when they still resolve inside an approved asset root supplied by the caller.
- Remote URLs are not supported.
- Parent traversal such as `../secret/logo.png` is rejected.
- Allowed file extensions are `.png`, `.jpg`, `.jpeg`, `.svg`, and `.pdf`.

Repository packaging boundary:

- Commit only redistributable placeholder assets, test fixtures, or openly licensed sample assets that the project is allowed to publish.
- Keep fixture assets under an approved asset-root layout such as [README.md](/cardiff/cardiff/tests/fixtures/approved-assets/README.md).
- Do not commit customer assets, internal brand kits, private QR payloads, or production contact data.
- Do not commit assets that require secret delivery channels or repository-specific access controls.

## Licensing Boundaries

Contributors are responsible for confirming that every committed asset can be redistributed with the repository.

May be committed:

- Original project-created placeholder graphics.
- Sample logos or marks that are explicitly open licensed or otherwise cleared for redistribution.
- Fonts only when their license allows repository redistribution and downstream open source use.
- Documentation that describes how proprietary assets are supplied externally.

Must be supplied externally by the caller or reviewer:

- Proprietary or customer-owned logos.
- Trademarked branded assets that are not cleared for redistribution.
- Commercial or otherwise restricted fonts without redistribution rights.
- QR payload data that embeds private endpoints, personal contact details, or customer-specific data.

When in doubt, do not commit the asset. Document the expected slot and path shape, and require external supply through approved asset roots instead.

## Review Checklist

Print-fidelity review:

- Confirm the request validates against the canonical contract before render.
- Confirm the template still resolves as `business-card` with variant `default`.
- Confirm page size remains `3.5in x 2.0in`.
- Confirm required text fields remain legible and within the intended layout.
- Confirm any committed asset resolves from an approved asset root and is licensed for redistribution.
- Confirm updated evidence under `cardiff/tests/fixtures/approved-samples/business-card/` matches the approved render behavior.

QR review:

- Confirm `include_qr` is explicitly `true` or `false` in the sample request under review.
- Confirm the rendered output and evidence reflect the expected QR state.
- Confirm the pull request does not embed private QR payload content in committed fixtures or docs.
- Confirm any QR-related asset or generator input follows the same approved asset-root and licensing rules.

## Submission Guidance

- Link pull requests back to the canonical contract or render-pipeline docs when a rule comes from shared infrastructure.
- Keep contributor docs aligned with the template manifest and the current validation tests.
- Prefer adding or updating placeholder assets and fixture documentation instead of introducing proprietary branded material.
