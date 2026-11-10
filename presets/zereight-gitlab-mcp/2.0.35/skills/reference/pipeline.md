# Pipeline & CI Commands

## pipeline list — List pipelines

```bash
ucli gitlab pipeline list --project-id my-group/my-repo
ucli gitlab pipeline list --project-id my-group/my-repo --status failed --ref main
```

Also supports: `--scope` (running|pending|finished|branches|tags), `--status`, `--ref`, `--sha`, `--yaml-errors`, `--username`, `--updated-after`, `--updated-before`, `--page`, `--per-page`

## pipeline get — Get pipeline details

```bash
ucli gitlab pipeline get --project-id my-group/my-repo --pipeline-id 1234
```

## pipeline create — Trigger a new pipeline

```bash
ucli gitlab pipeline create --project-id my-group/my-repo --ref main
ucli gitlab pipeline create --project-id my-group/my-repo --ref feature/branch
```

Also supports: `--variables`

## pipeline retry — Retry a failed pipeline

```bash
ucli gitlab pipeline retry --project-id my-group/my-repo --pipeline-id 1234
```

## pipeline cancel — Cancel a running pipeline

```bash
ucli gitlab pipeline cancel --project-id my-group/my-repo --pipeline-id 1234
```

## pipeline job list — List all jobs in a pipeline

```bash
ucli gitlab pipeline job list --project-id my-group/my-repo --pipeline-id 1234
```

## pipeline job get — Get job details

```bash
ucli gitlab pipeline job get --project-id my-group/my-repo --job-id 5678
```

## pipeline job output — Get job log output

```bash
ucli gitlab pipeline job output --project-id my-group/my-repo --job-id 5678
```

## pipeline job play — Trigger a manual job

```bash
ucli gitlab pipeline job play --project-id my-group/my-repo --job-id 5678
```

## pipeline job retry — Retry a failed job

```bash
ucli gitlab pipeline job retry --project-id my-group/my-repo --job-id 5678
```

## pipeline job cancel — Cancel a running job

```bash
ucli gitlab pipeline job cancel --project-id my-group/my-repo --job-id 5678
```

## pipeline artifact list — List job artifacts

```bash
ucli gitlab pipeline artifact list --project-id my-group/my-repo --job-id 5678
```

## pipeline artifact download — Download artifact archive

```bash
ucli gitlab pipeline artifact download --project-id my-group/my-repo --job-id 5678
```

## pipeline artifact get-file — Get a specific artifact file

```bash
ucli gitlab pipeline artifact get-file --project-id my-group/my-repo --job-id 5678 --artifact-path dist/app.zip
```

Use `ucli gitlab pipeline <action> --help` for full parameter details.
