# Text layer operations

## create — Create a new text layer

```bash
ucli ps text create --text 'Hello' --fontSize 48
```

Also supports: `--x`, `--y`, `--font-size`, `--font-name`, `--tracking`, `--leading`, `--auto-leading`, `--kind`, `--box-width`, `--box-height`, `--alignment`, `--red`, `--green`, `--blue`

## update — Replace the text content of the active text layer

```bash
ucli ps text update --text "example" --document-id 1
```

## set-color — Set the color of the active text layer

```bash
ucli ps text set-color --red 255 --green 255 --blue 255 --document-id 1
```

## set-alignment — Set the alignment of the active text layer

```bash
ucli ps text set-alignment --alignment LEFT --document-id 1
```

## set-style — Set layer-wide typography on the text layer

```bash
ucli ps text set-style --document-id 1
```

Also supports: `--tracking`, `--leading`, `--auto-leading`, `--kind`, `--box-width`, `--box-height`, `--alignment`, `--font-name`, `--font-size`, `--red`, `--green`, `--blue`

## set-ranges — Apply mixed styles to ranges inside a text layer

```bash
ucli ps text set-ranges --ranges '[]' --document-id 1
```

## font list — List installed fonts

```bash
ucli ps text font list --document-id 1
```

Also supports: `--query`, `--limit`

## font install — Install a font file

```bash
ucli ps text font install --file-path /tmp/file.png --document-id 1
```

## font set — Set the font family and size of the text layer

```bash
ucli ps text font set --font-name "Layer 1" --document-id 1
```

Also supports: `--font-size`

Use `ucli ps text <action> --help` for full parameter details.
