# Session and utility operations

## ping — Verify the Photoshop scripting engine responds

```bash
ucli ps app ping
```

## version — Get the detected Photoshop version

```bash
ucli ps app version
```

## capabilities — Get version-aware feature flags

```bash
ucli ps app capabilities
```

## state — Get a snapshot of the Photoshop session state

```bash
ucli ps app state --document-id 1
```

## preview — Export the active document as a base64 JPEG preview

```bash
ucli ps app preview --document-id 1
```

Also supports: `--max-dimension-px`, `--quality`

## submit-feedback — Record the answer to a product-feedback nudge

```bash
ucli ps app submit-feedback --choice yes
```

Also supports: `--suggestion`

## execute-script — Execute custom ExtendScript code inside Photoshop

```bash
ucli ps app execute-script --code "example" --document-id 1
```

Also supports: `--timeout-ms`

## play-action — Play a named action from an action set

```bash
ucli ps app play-action --action-name "Layer 1" --action-set-name "Layer 1" --document-id 1
```

Use `ucli ps app <action> --help` for full parameter details.
