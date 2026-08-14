# GitHub REST API

Base URL: `https://api.github.com`

## Auth

```bash
# gh CLI (preferred)
gh auth status

# Personal access token
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
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

### Releases

```bash
# Latest release
gh release view --repo owner/repo --json tagName,body -q '.tagName + "\n" + .body'

# List releases (last 20)
gh release list --repo owner/repo --limit 20

# Get a specific release by tag
gh api /repos/owner/repo/releases/tags/v1.2.3

# Raw API - latest
curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" \
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

- Authenticated: 5000/hour
- Unauthenticated: 60/hour
- Search endpoints have separate, lower limits
