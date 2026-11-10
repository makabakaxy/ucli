# Selection operations

## bounds — Get the bounds of the current selection

```bash
ucli ps selection bounds --document-id 1
```

## rectangle — Create a rectangular selection

```bash
ucli ps selection rectangle --left 10 --top 10 --right 10 --bottom 10 --document-id 1
```

Also supports: `--mode`

## ellipse — Create an elliptical selection

```bash
ucli ps selection ellipse --left 10 --top 10 --right 10 --bottom 10 --document-id 1
```

## all — Select the whole document

```bash
ucli ps selection all --document-id 1
```

## subject — Select the main subject of the layer

```bash
ucli ps selection subject --document-id 1
```

Also supports: `--sample-all-layers`

## deselect — Clear the current selection

```bash
ucli ps selection deselect --document-id 1
```

## invert — Invert the current selection

```bash
ucli ps selection invert --document-id 1
```

## expand — Expand the selection outward

```bash
ucli ps selection expand --pixels 10 --document-id 1
```

## contract — Contract the selection inward

```bash
ucli ps selection contract --pixels 10 --document-id 1
```

## feather — Feather the selection edges

```bash
ucli ps selection feather --pixels 10 --document-id 1
```

## save — Save the selection to an alpha channel

```bash
ucli ps selection save --document-id 1
```

Also supports: `--channel-name`

Use `ucli ps selection <action> --help` for full parameter details.
