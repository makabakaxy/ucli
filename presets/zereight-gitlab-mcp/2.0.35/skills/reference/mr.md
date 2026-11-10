# Merge Request Commands

## create — Create a new merge request

```bash
ucli gitlab mr create --title "Fix bug" --source-branch feature/fix --target-branch main
ucli gitlab mr create --title "Add feature" --source-branch feature/add --target-branch main --project-id my-group/my-repo --description "Details here"
ucli gitlab mr create --title "WIP feature" --source-branch feature/wip --target-branch main --draft true
```

Also supports: `--project-id`, `--description`, `--assignee-ids`, `--reviewer-ids`, `--labels`, `--draft`, `--remove-source-branch`, `--squash`, `--allow-collaboration`, `--target-project-id`

## get — Get MR details (by IID or source branch)

```bash
ucli gitlab mr get --project-id my-group/my-repo --merge-request-iid 42
ucli gitlab mr get --project-id my-group/my-repo --source-branch feature/fix
```

Also supports: `--source-branch`

## list — List merge requests

```bash
ucli gitlab mr list --project-id my-group/my-repo
```

## update — Update a merge request

```bash
ucli gitlab mr update --project-id my-group/my-repo --merge-request-iid 42 --title "Updated title"
ucli gitlab mr update --project-id my-group/my-repo --merge-request-iid 42 --state-event close
```

Also supports: `--description`, `--target-branch`, `--assignee-ids`, `--reviewer-ids`, `--labels`, `--remove-source-branch`, `--squash`, `--draft`

## merge — Merge a merge request

```bash
ucli gitlab mr merge --project-id my-group/my-repo --merge-request-iid 42
ucli gitlab mr merge --project-id my-group/my-repo --merge-request-iid 42 --squash true --should-remove-source-branch true
```

Also supports: `--auto-merge`, `--merge-commit-message`, `--squash-commit-message`, `--merge-when-pipeline-succeeds`

## diff get — Get full diff of a merge request

```bash
ucli gitlab mr diff get --project-id my-group/my-repo --merge-request-iid 42
```

Also supports: `--source-branch`, `--view` (inline|parallel), `--excluded-file-patterns`

## diff changed-files — List changed file paths (Step 1 of code review)

```bash
ucli gitlab mr diff changed-files --project-id my-group/my-repo --merge-request-iid 42
```

Also supports: `--source-branch`, `--excluded-file-patterns`

## diff file — Get diffs for specific files (Step 2 of code review)

```bash
ucli gitlab mr diff file --project-id my-group/my-repo --merge-request-iid 42 --file-paths '["src/api/users.ts","src/repo/user.go"]'
```

Also supports: `--source-branch`, `--unidiff`

## diff list — List diffs with pagination

```bash
ucli gitlab mr diff list --project-id my-group/my-repo --merge-request-iid 42
```

Also supports: `--page`, `--per-page`, `--unidiff`

## approval get — Get approval state

```bash
ucli gitlab mr approval get --project-id my-group/my-repo --merge-request-iid 42
```

## approval approve — Approve a merge request

```bash
ucli gitlab mr approval approve --project-id my-group/my-repo --merge-request-iid 42
```

Also supports: `--sha`, `--approval-password`

## approval unapprove — Unapprove a merge request

```bash
ucli gitlab mr approval unapprove --project-id my-group/my-repo --merge-request-iid 42
```

## conflict get — Get MR conflicts

```bash
ucli gitlab mr conflict get --project-id my-group/my-repo --merge-request-iid 42
```

## thread create — Create a discussion thread on an MR

```bash
ucli gitlab mr thread create --project-id my-group/my-repo --merge-request-iid 42 --body "This looks problematic"
```

## thread resolve — Resolve a discussion thread

```bash
ucli gitlab mr thread resolve --project-id my-group/my-repo --merge-request-iid 42 --discussion-id abc123 --resolved true
```

## note create — Add a note to an MR

```bash
ucli gitlab mr note create --project-id my-group/my-repo --merge-request-iid 42 --body "LGTM!"
```

Use `ucli gitlab mr <action> --help` for full parameter details.
