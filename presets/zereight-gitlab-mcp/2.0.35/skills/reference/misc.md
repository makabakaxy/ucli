# Miscellaneous Commands

## branch create — Create a new branch

```bash
ucli gitlab branch create --project-id my-group/my-repo --branch feature/my-feature --ref main
```

Also supports: `--project-id`, `--ref`

## branch diffs — Get diffs between two branches/commits

```bash
ucli gitlab branch diffs --project-id my-group/my-repo --from main --to feature/branch
ucli gitlab branch diffs --project-id my-group/my-repo --from main --to feature/branch --excluded-file-patterns '["^vendor/"]'
```

Also supports: `--straight`, `--excluded-file-patterns`

## deployment list — List deployments

```bash
ucli gitlab deployment list --project-id my-group/my-repo
```

## deployment get — Get a specific deployment

```bash
ucli gitlab deployment get --project-id my-group/my-repo --deployment-id 123
```

## environment list — List environments

```bash
ucli gitlab environment list --project-id my-group/my-repo
```

## environment get — Get a specific environment

```bash
ucli gitlab environment get --project-id my-group/my-repo --environment-id 5
```

## milestone create — Create a milestone

```bash
ucli gitlab milestone create --project-id my-group/my-repo --title "v2.0 Release"
ucli gitlab milestone create --project-id my-group/my-repo --title "Sprint 5" --due-date 2026-04-30
```

Also supports: `--description`, `--due-date`, `--start-date`

## milestone list — List milestones

```bash
ucli gitlab milestone list --project-id my-group/my-repo
```

Also supports: `--state`, `--search`

## milestone get — Get a specific milestone

```bash
ucli gitlab milestone get --project-id my-group/my-repo --milestone-id 10
```

## milestone update — Edit a milestone

```bash
ucli gitlab milestone update --project-id my-group/my-repo --milestone-id 10 --title "Updated title" --state-event close
```

## milestone delete — Delete a milestone

```bash
ucli gitlab milestone delete --project-id my-group/my-repo --milestone-id 10
```

## milestone issues — Get milestone issues

```bash
ucli gitlab milestone issues --project-id my-group/my-repo --milestone-id 10
```

## label list — List project labels

```bash
ucli gitlab label list --project-id my-group/my-repo
```

Also supports: `--with-counts`, `--search`

## label create — Create a label

```bash
ucli gitlab label create --project-id my-group/my-repo --name bug --color "#ff0000"
```

Also supports: `--description`, `--priority`

## label delete — Delete a label

```bash
ucli gitlab label delete --project-id my-group/my-repo --label-id bug
```

## commit list — List commits

```bash
ucli gitlab commit list --project-id my-group/my-repo
```

## commit get — Get commit details

```bash
ucli gitlab commit get --project-id my-group/my-repo --sha abc1234
```

## commit diff — Get commit diff

```bash
ucli gitlab commit diff --project-id my-group/my-repo --sha abc1234
```

## namespace list — List namespaces

```bash
ucli gitlab namespace list
ucli gitlab namespace list --search my-ns
```

Also supports: `--owned`, `--page`, `--per-page`

## namespace verify — Verify if a namespace path exists

```bash
ucli gitlab namespace verify --path my-namespace
```

## group projects — List projects in a group

```bash
ucli gitlab group projects --group-id my-group
ucli gitlab group projects --group-id my-group --include-subgroups true
```

Also supports: `--search`, `--order-by`, `--sort`, `--archived`, `--visibility`, `--page`, `--per-page`

## user get — Get user details by usernames

```bash
ucli gitlab user get --usernames '["john_doe"]'
```

## event list — List events for current user

```bash
ucli gitlab event list
```

## event project-list — List events for a project

```bash
ucli gitlab event project-list --project-id my-group/my-repo
```

## misc note — Add a note to an issue or MR

```bash
ucli gitlab misc note --noteable-type issue --body "Comment text" --project-id my-group/my-repo --noteable-iid 42
```

## misc upload-markdown — Upload file for markdown use

```bash
ucli gitlab misc upload-markdown --project-id my-group/my-repo --file-path /path/to/image.png
```

## misc download-attachment — Download an uploaded file

```bash
ucli gitlab misc download-attachment --project-id my-group/my-repo --secret abc123 --filename image.png
```

Use `ucli gitlab <group> <action> --help` for full parameter details.
