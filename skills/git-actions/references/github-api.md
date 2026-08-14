# GitHub REST API

Scope: GitHub REST (Representational State Transfer) API requests and `gh` command-line interface (CLI) examples. Resolve the repository, API version, endpoint permissions, and response schema before execution; examples with `POST`, `PUT`, `PATCH`, or `DELETE` are mutation examples and require explicit authorization.

Base URL: `https://api.github.com`

## Auth

```bash
# gh CLI (preferred)
gh auth status

# Personal access token
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     -H "X-GitHub-Api-Version: 2026-03-10" \
     https://api.github.com/...
```

## Pagination

GitHub uses Link headers. `gh` handles this automatically.

```bash
# With curl - follow Link headers manually or set per_page
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/owner/repo/releases?per_page=100&page=2"

# With gh - use --paginate
gh api --paginate /repos/owner/repo/releases --jq '.[].tag_name'
```

## Common endpoints

The create, trigger, and other write examples below are illustrative only. Before running one, confirm the exact repository, resource, effect, and token permission; use a read-only request when inspection is sufficient. If the provider rejects the API version, schema, or permission, stop and report `UNVERIFIED` rather than retrying a broader request.

### Releases

```bash
# Latest release
gh release view --repo owner/repo --json tagName,body -q '.tagName + "\n" + .body'

# List releases (last 20)
gh release list --repo owner/repo --limit 20

# Get a specific release by tag
gh api /repos/owner/repo/releases/tags/v1.2.3

# Raw API - latest (authenticated; omit the token only for intentionally public reads)
curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  https://api.github.com/repos/owner/repo/releases/latest | jq .
```

### Tags

```bash
# List tags
gh api /repos/owner/repo/tags --jq '.[].name'

# Compare two tags
gh api /repos/owner/repo/compare/v1.0.0...v2.0.0 --jq '.total_commits'
```

### Repository metadata

```bash
# Basic repo info
gh repo view owner/repo --json name,stargazerCount,defaultBranchRef

# List languages
gh api /repos/owner/repo/languages --jq 'keys'

# Get README
gh api /repos/owner/repo/readme --jq '.content' | base64 -d
```

### Issues

```bash
# Create
gh issue create --repo owner/repo --title "Bug" --body "Details"

# List open with label
gh issue list --repo owner/repo --label bug --limit 10 --json title,number

# Search issues
gh search issues --repo owner/repo "is:open label:bug"
```

### Pull requests

```bash
# Create
gh pr create --repo owner/repo --title "Fix" --body "Details" --base main

# List
gh pr list --repo owner/repo --state open --limit 10

# Check CI status
gh pr checks owner/repo 42
```

### Workflows

```bash
# List workflow runs
gh run list --repo owner/repo --limit 10

# Trigger a workflow
gh workflow run ci.yml --repo owner/repo -f param=value

# Watch a run
gh run watch <run-id> --repo owner/repo
```

## Rate limits

```bash
# Check limits
gh api /rate_limit --jq '.rate'
```

Rate limits vary by authentication method, endpoint, installation, and current provider policy. Inspect response headers or the provider rate-limit endpoint instead of relying on fixed numbers; unavailable limit evidence is `UNVERIFIED`.

## Sources

- [Git Actions source map](sources.md) — checked provider URLs and freshness limits.
- [GitHub REST API documentation](https://docs.github.com/en/rest) — endpoint and version reference.
- [Using pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) — link headers and page limits.
