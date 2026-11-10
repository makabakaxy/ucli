# Layer operations — layer

## create — Create a new empty layer

```bash
ucli ps layer create --document-id 1
```

Also supports: `--name`

## delete — Delete the active layer

```bash
ucli ps layer delete --document-id 1
```

## list — List all layers in the document

```bash
ucli ps layer list --document-id 1
```

## select — Select a layer by exact name

```bash
ucli ps layer select --name "Layer 1" --document-id 1
```

## duplicate — Duplicate the active layer

```bash
ucli ps layer duplicate --document-id 1
```

Also supports: `--new-name`

## rename — Rename the active layer

```bash
ucli ps layer rename --name "Layer 1" --document-id 1
```

## merge-visible — Merge all visible layers into one

```bash
ucli ps layer merge-visible --document-id 1
```

## rasterize — Rasterize the active layer

```bash
ucli ps layer rasterize --document-id 1
```

## move — Move the active layer by an offset

```bash
ucli ps layer move --delta-x 10 --delta-y 10 --document-id 1
```

## scale — Scale the active layer by a percentage

```bash
ucli ps layer scale --scale-percent 10 --document-id 1
```

Also supports: `--center-anchor`

## rotate — Rotate the active layer

```bash
ucli ps layer rotate --degrees 10 --document-id 1
```

## fit — Fit the active layer to the document canvas

```bash
ucli ps layer fit --document-id 1
```

Also supports: `--fill-document`

## apply-style — Apply a layer style such as shadow or stroke

```bash
ucli ps layer apply-style --document-id 1
```

Also supports: `--style`, `--red`, `--green`, `--blue`, `--opacity`, `--size`, `--distance`, `--angle`

Use `ucli ps layer <action> --help` for full parameter details.
