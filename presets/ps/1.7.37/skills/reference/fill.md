# Fill operations

## color — Fill the layer or selection with a solid color

```bash
ucli ps fill color --red 255 --green 0 --blue 0
```

## gradient — Paint a two-color gradient on the layer

```bash
ucli ps fill gradient --from-red 255 --from-green 255 --from-blue 255 --to-red 255 --to-green 255 --to-blue 255 --document-id 1
```

Also supports: `--direction`

## content-aware — Fill the selection using Content-Aware Fill

```bash
ucli ps fill content-aware --document-id 1
```

Use `ucli ps fill <action> --help` for full parameter details.
