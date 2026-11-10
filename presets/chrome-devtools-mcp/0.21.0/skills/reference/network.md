# Network Commands

## list — List all network requests for the current page

```bash
# All requests
ucli chrome-devtools network list

# Only XHR and fetch requests
ucli chrome-devtools network list --resource-types '["xhr","fetch"]'

# Paginated
ucli chrome-devtools network list --page-size 100 --page-idx 0
```

Also supports: `--page-size`, `--page-idx`, `--resource-types`, `--include-preserved-requests`

## get — Get details of a network request

```bash
# By request ID
ucli chrome-devtools network get --reqid 5

# Selected request in DevTools panel (omit reqid)
ucli chrome-devtools network get

# Save request/response bodies to files
ucli chrome-devtools network get --reqid 5 --request-file-path /tmp/req.json --response-file-path /tmp/res.json
```

Also supports: `--reqid`, `--request-file-path`, `--response-file-path`

Use `ucli chrome-devtools network <action> --help` for full parameter details.
