# Approved Assets Fixture

This directory is the example approved asset root used by contract, CLI, and render tests.

Current layout:

- `brand/logo.png`: redistributable placeholder logo used by the approved `business-card` fixture request

Contributor rules:

- Keep committed assets in this fixture directory redistributable and safe for open source publication.
- Preserve an approved asset-root layout where request paths stay relative, for example `brand/logo.png`.
- Do not add proprietary customer logos, private brand kits, or restricted fonts here.
- Do not add remote references or traversal-based paths; validation rejects those inputs.

If a template needs a proprietary or non-redistributable asset, document the expected slot and require external supply through caller-provided approved asset roots instead of committing the file to the repository.
