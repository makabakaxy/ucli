# PolyHaven Commands

## polyhaven status — Check PolyHaven integration status

```bash
ucli blender polyhaven status
```

## polyhaven category list — List asset categories

```bash
ucli blender polyhaven category list --asset-type textures
ucli blender polyhaven category list --asset-type hdris
```

Also supports: `--user-prompt`
Asset types: `hdris`, `textures`, `models`, `all`

## polyhaven asset search — Search for PolyHaven assets

```bash
ucli blender polyhaven asset search --asset-type textures
ucli blender polyhaven asset search --asset-type hdris --categories 'sky,outdoor'
ucli blender polyhaven asset search --asset-type models --categories 'furniture'
```

Also supports: `--categories`, `--user-prompt`

## polyhaven asset download — Download and import a PolyHaven asset

```bash
ucli blender polyhaven asset download --asset-id venice-sunset --asset-type hdris
ucli blender polyhaven asset download --asset-id wood-plank --asset-type textures --resolution 2k
ucli blender polyhaven asset download --asset-id barrel --asset-type models --resolution 1k --file-format gltf
```

Also supports: `--resolution`, `--file-format`, `--user-prompt`

## polyhaven texture set — Apply a texture to a scene object

```bash
ucli blender polyhaven texture set --object-name Cube --texture-id wood-plank
ucli blender polyhaven texture set --object-name "My Mesh" --texture-id concrete-floor
```

Also supports: `--user-prompt`

> Note: Texture must be downloaded first via `polyhaven asset download`.

Use `ucli blender polyhaven <action> --help` for full parameter details.
