# Filter operations

## blur — Apply Gaussian Blur

```bash
ucli ps filter blur --radius 10 --document-id 1
```

## motion-blur — Apply Motion Blur

```bash
ucli ps filter motion-blur --angle 10 --radius 10 --document-id 1
```

## smart-blur — Apply Smart Blur

```bash
ucli ps filter smart-blur --radius 10 --threshold 10 --document-id 1
```

Also supports: `--mode`, `--quality`

## sharpen — Apply Unsharp Mask sharpening

```bash
ucli ps filter sharpen --amount 10 --radius 10 --document-id 1
```

Also supports: `--threshold`

## high-pass — Apply the High Pass filter

```bash
ucli ps filter high-pass --radius 10 --document-id 1
```

## noise — Add noise to the layer

```bash
ucli ps filter noise --amount 10 --document-id 1
```

Also supports: `--distribution`, `--monochromatic`

## neural — Apply a Neural Filter

```bash
ucli ps filter neural --filter skin_smoothing --document-id 1
```

Also supports: `--smoothness`, `--blur`, `--reference-layer-id`

Use `ucli ps filter <action> --help` for full parameter details.
