# GitLab REST API

Base URL: `https://gitlab.com/api/v4` (or self-hosted instance URL)

## Auth

```bash
# glab CLI (preferred)
glab auth status

# Personal access token
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/..."

# OAuth token
curl -H "Authorization: Bearer $OAUTH_TOKEN" \
  "https://gitlab.com/api/v4/..."
```

## Project IDs

GitLab uses project IDs (integers) or URL-encoded paths:

```bash
# Get project by path
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/owner%2Frepo"

# URL-encode: / becomes %2F
PROJECT_ID=$(curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/owner%2Frepo" | jq -r '.id')
```

## Pagination

```bash
# Per-page and page params
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases?per_page=100&page=2"

# Link header
curl -I -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases?per_page=100"

# With glab
glab api --paginate "projects/$PROJECT_ID/releases?per_page=100" | jq '.[].tag_name'
```

## Common endpoints

### Releases

```bash
# List releases
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases" | jq '.[].tag_name'

# Get latest release
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases?per_page=1" | jq '.[0].tag_name'

# Create release via API
curl -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -F "tag_name=v1.0.0" -F "description=Release notes" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases"
```

### Tags

```bash
# List tags
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/repository/tags" | jq '.[].name'

# Specific tag
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/repository/tags/v1.0.0"
```

### Repository metadata

```bash
# Project info
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID" | jq '{name, star_count, default_branch}'

# List languages
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/languages"
```

### Merge requests

```bash
# Create
curl -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -F "source_branch=feature" -F "target_branch=main" \
  -F "title=Fix bug" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/merge_requests"

# List open
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/merge_requests?state=opened"

# Get pipeline status for MR
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/merge_requests/$MR_IID/pipelines"
```

### Pipelines

```bash
# Trigger pipeline
curl -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -F "ref=main" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/pipeline"

# List recent pipelines
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/pipelines?per_page=5"
```

## Rate limits

GitLab.com: 2000 requests/minute for authenticated users (may vary). Check
headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`.
