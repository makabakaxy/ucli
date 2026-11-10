# Generative AI operations

## fill — Fill the selection with Generative Fill

```bash
ucli ps ai fill --prompt "example" --document-id 1
```

## remove — Remove content with the AI Remove tool

```bash
ucli ps ai remove --document-id 1
```

Also supports: `--feather-px`, `--auto-select-subject`

## expand — Extend the canvas with Generative Expand

```bash
ucli ps ai expand --document-id 1
```

Also supports: `--prompt`, `--direction`

## upscale — Upscale the document with Generative Upscale

```bash
ucli ps ai upscale --document-id 1
```

Also supports: `--target-scale`

## sky-replacement — Replace the sky

```bash
ucli ps ai sky-replacement --document-id 1
```

Also supports: `--sky-image-path`

## generate-image — Generate an image from a text prompt

```bash
ucli ps ai generate-image --prompt "example" --document-id 1
```

Also supports: `--width`, `--height`

Use `ucli ps ai <action> --help` for full parameter details.
