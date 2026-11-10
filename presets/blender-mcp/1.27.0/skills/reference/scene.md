# Scene Commands

## scene get — Get current scene information

```bash
ucli blender scene get --user-prompt 'show me the scene'
ucli blender scene get --user-prompt 'list all objects'
```

## scene object get — Get details about a specific object

```bash
ucli blender scene object get --object-name Cube
ucli blender scene object get --object-name "My Mesh"
```

Also supports: `--user-prompt`

## scene viewport screenshot — Capture viewport screenshot

```bash
ucli blender scene viewport screenshot
ucli blender scene viewport screenshot --max-size 1200
```

Also supports: `--user-prompt`

Use `ucli blender scene <action> --help` for full parameter details.
