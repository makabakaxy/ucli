# Layer operations — layer-order

## order position — Reorder the layer relative to a named layer

```bash
ucli ps layer order position --target-layer-name "Layer 1" --position ABOVE --document-id 1
```

## order top — Move the layer to the top of the stack

```bash
ucli ps layer order top --document-id 1
```

## order bottom — Move the layer to the bottom of the stack

```bash
ucli ps layer order bottom --document-id 1
```

## order up — Move the layer up one position

```bash
ucli ps layer order up --document-id 1
```

## order down — Move the layer down one position

```bash
ucli ps layer order down --document-id 1
```

Use `ucli ps layer <action> --help` for full parameter details.
