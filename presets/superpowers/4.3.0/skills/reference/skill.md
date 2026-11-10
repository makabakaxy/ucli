# Skill Commands

## list — List all available Superpowers skills

```bash
ucli superpowers skill list
```

No additional parameters.

## get — Read full content of a skill by name

```bash
# Read a skill before performing the task it covers
ucli superpowers skill get --skill-name brainstorming

# Load a debugging skill
ucli superpowers skill get --skill-name systematic-debugging

# Load a development workflow skill
ucli superpowers skill get --skill-name test-driven-development
```

Also supports: `--skill-name` (required)

Use `ucli superpowers skill <action> --help` for full parameter details.
