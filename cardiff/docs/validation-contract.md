# Cardiff Validation Contract

## Scope

`BOLT-001A` defines the first canonical request contract that later CLI, batch, and API adapters must reuse. The contract validates and sanitizes one single-record render request before any template rendering or TeX compilation exists.

Contributor-facing business-card template guidance lives in [template-authoring.md](/cardiff/cardiff/docs/template-authoring.md). That document explains which parts of this shared contract are approved for the current open source template package.

## Accepted Top-Level Shape

```yaml
identity:
  full_name: "Ada Lovelace"
  role: "Computing Pioneer"
  email: "ada@example.com"
  phone: "+44 20 5555 0101"
  organization: "Analytical Engine Lab"
  department: "Research"
  website: "https://example.com"
  address_lines:
    - "123 Logic St."
    - "London"
  pronouns: "she/her"
template:
  id: business-card
  options:
    variant: default
    include_qr: true
    accent_hex: "#0055AA"
assets:
  logo: brand/logo.png
  avatar: portraits/ada.jpg
```

## Contract Rules

- `identity`, `template`, and optional `assets` are the only supported top-level fields.
- Required identity fields are `full_name`, `role`, and `email`.
- Optional identity fields are `phone`, `organization`, `department`, `website`, `address_lines`, and `pronouns`.
- `template.id` must be a symbolic slug such as `business-card`; file-system paths are rejected.
- Supported template options are `variant`, `include_qr`, and `accent_hex`.
- Asset slots are currently limited to `logo` and `avatar`.
- Asset paths must stay inside approved asset roots supplied by the caller and must use an approved file extension.
- Business-text fields are sanitized for LaTeX-sensitive characters and unsafe control fragments are rejected.

## Failure Taxonomy

The validation layer returns stable issue codes:

- `contract_error`
- `unknown_field`
- `missing_required`
- `invalid_type`
- `invalid_template`
- `invalid_asset_path`
- `unsafe_content`

Each issue includes:

- `code`
- `field`
- `message`
- `severity`

## Behavior Notes

- JSON and YAML are both accepted, but both normalize into the same canonical request structure.
- Validation errors are returned before any render pipeline exists.
- Unknown fields are rejected instead of ignored so downstream CLI, batch, and API consumers cannot drift silently.
- Sanitized requests preserve the original business meaning while escaping LaTeX-significant characters for later rendering stages.

## Approved Template Notes

- The shared contract currently accepts asset slots `logo` and `avatar`, but the approved `business-card` template package only requires `logo`.
- The shared contract currently accepts template options `variant`, `include_qr`, and `accent_hex`; template-specific support is finalized during template resolution.
- For the current approved `business-card` manifest, `variant=default` is the only supported variant.
- Asset references must remain relative to approved asset roots or be absolute paths inside approved asset roots. Parent traversal and remote URLs are rejected.
