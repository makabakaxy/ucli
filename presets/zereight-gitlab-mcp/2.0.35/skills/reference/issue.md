# Issue Commands

## create — Create a new issue

```bash
ucli gitlab issue create --title "Fix memory leak" --project-id my-group/my-repo
ucli gitlab issue create --title "Add dark mode" --project-id my-group/my-repo --description "Implement dark mode support" --labels '["enhancement","ui"]'
ucli gitlab issue create --title "Performance bug" --project-id my-group/my-repo --issue-type issue --assignee-ids '[42]'
```

Also supports: `--description`, `--assignee-ids`, `--labels`, `--milestone-id`, `--issue-type` (issue|incident|test_case|task), `--weight`

## get — Get issue details

```bash
ucli gitlab issue get --project-id my-group/my-repo --issue-iid 10
```

## list — List issues

```bash
ucli gitlab issue list --project-id my-group/my-repo
ucli gitlab issue list --project-id my-group/my-repo --state opened --labels '["bug"]'
```

Also supports: `--assignee-id`, `--assignee-username`, `--author-id`, `--author-username`, `--confidential`, `--created-after`, `--created-before`, `--due-date`, `--labels`, `--milestone`, `--issue-type`, `--iteration-id`, `--scope` (created_by_me|assigned_to_me|all), `--search`, `--state` (opened|closed|all), `--page`, `--per-page`

## my — List issues assigned to me

```bash
ucli gitlab issue my
ucli gitlab issue my --state opened --project-id my-group/my-repo
```

Also supports: `--project-id`, `--state`, `--labels`, `--milestone`, `--search`, `--created-after`, `--updated-after`, `--page`, `--per-page`

## update — Update an issue

```bash
ucli gitlab issue update --project-id my-group/my-repo --issue-iid 10 --title "Updated title"
ucli gitlab issue update --project-id my-group/my-repo --issue-iid 10 --state-event close
```

Also supports: `--description`, `--assignee-ids`, `--labels`, `--milestone-id`, `--due-date`, `--weight`, `--issue-type`, `--confidential`

## delete — Delete an issue

```bash
ucli gitlab issue delete --project-id my-group/my-repo --issue-iid 10
```

## note create — Add a note to an issue

```bash
ucli gitlab issue note create --project-id my-group/my-repo --issue-iid 10 --body "Looking into this now"
```

Also supports: `--discussion-id`, `--created-at`

## link create — Link two issues

```bash
ucli gitlab issue link create --project-id my-group/my-repo --issue-iid 10 --target-project-id my-group/my-repo --target-issue-iid 20 --link-type relates_to
```

Also supports: `--link-type` (relates_to|blocks|is_blocked_by)

## discussion list — List issue discussions

```bash
ucli gitlab issue discussion list --project-id my-group/my-repo --issue-iid 10
```

Use `ucli gitlab issue <action> --help` for full parameter details.
