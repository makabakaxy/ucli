# Color and tone adjustments

## brightness-contrast — Adjust brightness and contrast

```bash
ucli ps adjust brightness-contrast --brightness 10 --contrast 10 --document-id 1
```

## hue-saturation — Adjust hue, saturation and lightness

```bash
ucli ps adjust hue-saturation --hue 10 --saturation 10 --lightness 10 --document-id 1
```

## auto-levels — Run Auto Levels

```bash
ucli ps adjust auto-levels --document-id 1
```

## auto-contrast — Run Auto Contrast

```bash
ucli ps adjust auto-contrast --document-id 1
```

## curves — Create a Curves adjustment layer

```bash
ucli ps adjust curves --document-id 1
```

Also supports: `--preset`

## vibrance — Create a Vibrance adjustment layer

```bash
ucli ps adjust vibrance --document-id 1
```

Also supports: `--vibrance`, `--saturation`

## exposure — Create an Exposure adjustment layer

```bash
ucli ps adjust exposure --document-id 1
```

Also supports: `--exposure`, `--offset`, `--gamma`

## photo-filter — Create a Photo Filter adjustment layer

```bash
ucli ps adjust photo-filter --document-id 1
```

Also supports: `--red`, `--green`, `--blue`, `--density`, `--preserve-luminosity`

## gradient-map — Create a Gradient Map adjustment layer

```bash
ucli ps adjust gradient-map --document-id 1
```

Also supports: `--reverse`

## lut — Apply a Color Lookup LUT adjustment layer

```bash
ucli ps adjust lut --lut "example" --document-id 1
```

## desaturate — Desaturate the layer to grayscale

```bash
ucli ps adjust desaturate --document-id 1
```

## invert — Invert the colors of the layer

```bash
ucli ps adjust invert --document-id 1
```

Use `ucli ps adjust <action> --help` for full parameter details.
