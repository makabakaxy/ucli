# Project Commands

## activate — Activate a project by name or path

```bash
# Activate by registered name
ucli serena project activate --project my-project

# Activate by path
ucli serena project activate --project /path/to/my/project
```

## check-onboarding — Check if project onboarding was performed

```bash
ucli serena project check-onboarding
```

> Call this before working on a project to verify onboarding status.

## onboarding — Perform project onboarding

```bash
ucli serena project onboarding
```

> Call this if `check-onboarding` indicates onboarding has not been done. Call at most once per conversation.

Use `ucli serena project <action> --help` for full parameter details.
