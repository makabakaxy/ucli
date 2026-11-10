# One-shot workflow recipes

## remove-background — Remove the background and isolate the subject

```bash
ucli ps recipe remove-background --document-id 1
```

Also supports: `--feather-px`, `--keep-shadow`, `--use-generative`

## enhance-portrait — Set up a non-destructive portrait enhancement

```bash
ucli ps recipe enhance-portrait --document-id 1
```

Also supports: `--intensity`, `--skin-smoothing`, `--use-neural-skin`

## prepare-for-web — Export a web-optimized version of the document

```bash
ucli ps recipe prepare-for-web --document-id 1
```

Also supports: `--max-dimension-px`, `--format`, `--quality`, `--path`

## export-social-variants — Export one JPEG per social media platform

```bash
ucli ps recipe export-social-variants --document-id 1
```

Also supports: `--platforms`, `--quality`

## apply-color-grade — Apply a named color grading preset

```bash
ucli ps recipe apply-color-grade --document-id 1
```

Also supports: `--preset`

## frequency-separation — Build a frequency separation stack

```bash
ucli ps recipe frequency-separation --document-id 1
```

Also supports: `--radius-px`

## batch-mockup-replace — Replace a smart object with each asset in a folder

```bash
ucli ps recipe batch-mockup-replace --smart-object-layer-name "Layer 1" --assets-dir /tmp/out --document-id 1
```

Also supports: `--quality`

## organize-layers — Rename and tidy the layer stack

```bash
ucli ps recipe organize-layers --document-id 1
```

Also supports: `--naming-scheme`, `--auto-group`

## gradient-fade — Fade the layer with a gradient mask

```bash
ucli ps recipe gradient-fade --document-id 1
```

Also supports: `--direction`, `--start-pct`, `--end-pct`, `--angle-deg`

## sky-blend — Composite a sky image with a gradient mask

```bash
ucli ps recipe sky-blend --sky-image-path /tmp/file.png --document-id 1
```

Also supports: `--horizon-pct`, `--feather-pct`, `--x`, `--y`, `--use-native-sky`

## dodge-burn — Set up a dodge and burn layer

```bash
ucli ps recipe dodge-burn --document-id 1
```

Also supports: `--blend-mode`

## remove-distraction — Remove distractions using AI or content-aware fill

```bash
ucli ps recipe remove-distraction --document-id 1
```

Also supports: `--feather-px`, `--use-generative`

## split-carousel — Split a wide document into carousel slices

```bash
ucli ps recipe split-carousel --slides 10 --document-id 1
```

Also supports: `--slide-width`, `--slide-height`, `--format`, `--quality`

## batch-watermark — Watermark every image in a folder

```bash
ucli ps recipe batch-watermark --assets-dir /tmp/out --document-id 1
```

Also supports: `--text`, `--logo-path`, `--position`, `--opacity`, `--margin-px`, `--font-size`, `--scale-pct`, `--quality`

## passport-photo — Turn a portrait into a passport photo

```bash
ucli ps recipe passport-photo --document-id 1
```

Also supports: `--spec`, `--make-sheet`, `--quality`

## csv-to-cards — Generate cards from a CSV file

```bash
ucli ps recipe csv-to-cards --csv-path /tmp/file.png --output-dir /tmp/out --document-id 1
```

Also supports: `--format`

## sticker-outline — Add a sticker outline

```bash
ucli ps recipe sticker-outline --document-id 1
```

Also supports: `--red`, `--green`, `--blue`, `--stroke-width`, `--stroke-opacity`, `--stroke-position`, `--shadow`, `--shadow-opacity`, `--shadow-size`, `--shadow-distance`, `--shadow-angle`, `--outline-style`, `--line-width`, `--line-red`, `--line-green`, `--line-blue`

Use `ucli ps recipe <action> --help` for full parameter details.
