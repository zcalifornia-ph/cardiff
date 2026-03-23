# Cardiff CLI Quickstart

## Scope

`BOLT-001C` adds the first operator-facing CLI for Cardiff. The CLI reuses the canonical contract from `cardiff.contract` and the shared render pipeline from `cardiff.rendering`.

Use `python -m cardiff` in a source checkout. After installation, the `cardiff` console script is equivalent.

## Validate One Request

```bash
python -m cardiff validate tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets
```

The command prints one JSON status object to standard output and returns exit code `0` when the request is accepted.

## Render One PDF

```bash
python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output tests/fixtures/approved-samples/business-card/determinism-output.pdf --deterministic
```

Behavior:

- The request is validated before any render work starts.
- Parent directories for the output PDF are created automatically when needed.
- The CLI reports the resolved source path, template ID, output path, and runtime metadata in its JSON status payload.
- `--deterministic` forces the deterministic adapter even if `xelatex` is installed locally.

## Compare Against Stored Reference Evidence

```bash
python -m cardiff render tests/fixtures/requests/valid-request.yaml --approved-asset-root tests/fixtures/approved-assets --output tests/fixtures/approved-samples/business-card/determinism-output.pdf --deterministic --reference-evidence tests/fixtures/approved-samples/business-card/reference-evidence.json
```

When the current normalized render evidence matches the approved reference JSON, the command returns exit code `0`. If the PDF renders successfully but the normalized evidence differs, the command returns exit code `4` and reports the mismatched fields in `reference_comparison`.

The reference-evidence comparison normalizes the template manifest and the canonical request payload before hashing, so the approved record stays portable across checkout path and line-ending differences.

## Exit Codes

- `0`: command succeeded
- `1`: canonical validation rejected the request
- `2`: CLI usage or required file/path error
- `3`: render pipeline failure after validation succeeded
- `4`: render succeeded but reference-evidence comparison failed
