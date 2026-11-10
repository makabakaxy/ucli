# Sketchfab Commands

## sketchfab status — Check Sketchfab integration status

```bash
ucli blender sketchfab status
```

## sketchfab model search — Search for Sketchfab models

```bash
ucli blender sketchfab model search --query 'wooden chair'
ucli blender sketchfab model search --query 'sci-fi spaceship' --count 10
ucli blender sketchfab model search --query 'tree' --categories 'nature,plants'
```

Also supports: `--categories`, `--count`, `--downloadable`, `--user-prompt`

## sketchfab model preview — Preview model thumbnail

```bash
ucli blender sketchfab model preview --uid abc123def456
```

Also supports: `--user-prompt`

> Use to visually confirm a model before downloading.

## sketchfab model download — Download and import a Sketchfab model

```bash
ucli blender sketchfab model download --uid abc123def456 --target-size 1.0
ucli blender sketchfab model download --uid abc123def456 --target-size 0.1
ucli blender sketchfab model download --uid abc123def456 --target-size 4.5
```

Also supports: `--user-prompt`

> `--target-size` is in Blender units (meters). Examples: chair=1.0, car=4.5, cup=0.15.

Use `ucli blender sketchfab model <action> --help` for full parameter details.
