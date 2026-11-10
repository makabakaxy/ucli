# Layer mask operations

## create — Create a layer mask from the selection

```bash
ucli ps mask create --document-id 1
```

## delete — Delete the layer mask

```bash
ucli ps mask delete --document-id 1
```

## apply — Apply the layer mask into the pixels

```bash
ucli ps mask apply --document-id 1
```

## gradient — Apply a gradient on the layer mask

```bash
ucli ps mask gradient --document-id 1
```

Also supports: `--direction`, `--start-pct`, `--end-pct`, `--angle-deg`

## clipping create — Create a clipping mask

```bash
ucli ps mask clipping create --document-id 1
```

Also supports: `--layer-name`

## clipping release — Release a clipping mask

```bash
ucli ps mask clipping release --document-id 1
```

Also supports: `--layer-name`

Use `ucli ps mask <action> --help` for full parameter details.
