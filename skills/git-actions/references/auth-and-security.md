# Auth and Security

## GitHub

### GitHub token types

| Token | Scope | Best for |
| --- | --- | --- |
| `gh` CLI auth | Interactive OAuth | Interactive use, full repo access |
| Fine-grained PAT | Per-repo, per-permission | CI/CD, automation |
| Classic PAT | Broad scopes | Legacy tools, simple scripts |
| `GITHUB_TOKEN` | Per-workflow, ephemeral | GitHub Actions workflows |
| OAuth app token | User-authorized scopes | Third-party apps |

### GitHub setup

```bash
# gh CLI login
gh auth login

# Check status
gh auth status

# Token for scripts - set env var
export GITHUB_TOKEN=$(gh auth token)
```

### GitHub minimum permissions

Fine-grained PAT:

- Contents: Read-only
- Metadata: Read-only (auto-granted)

## GitLab

### GitLab token types

| Token | Scope | Best for |
| --- | --- | --- |
| Personal access token | User-level, scoped | Personal scripts |
| Project access token | Per-project, scoped | CI/CD, per-project automation |
| Group access token | Group-level, scoped | Multi-project automation |
| `CI_JOB_TOKEN` | Per-job, ephemeral | GitLab CI jobs |

### GitLab setup

```bash
# glab CLI login
glab auth login

# Check status
glab auth status

# Token for scripts - use env var
export GITLAB_TOKEN="glpat-..."
```

### GitLab minimum permissions

Personal access token scopes:

- `read_api` - Read API access
- `read_repository` - Read repository

## Security rules

1. **Never** hardcode tokens in scripts or pipeline YAML
2. **Never** echo, log, or print tokens
3. Use environment variables with restricted scope tokens
4. Prefer CLI tools (`gh`, `glab`) over raw `curl` - they handle auth and token
   refresh
5. For CI/CD, use platform-native secrets (`secrets.GITHUB_TOKEN`, CI/CD
   Variables)
6. Rotate PATs regularly - at least every 90 days
7. Use fine-grained tokens with minimum permissions, not classic PATs with broad
   scopes

## Operation safety

Every mutating API call must be confirmed. Default posture: read-only.

### Confirmation template

Before any POST/PUT/PATCH/DELETE:

```
Operation: <method /endpoint>
Resource: owner/repo, <specific target>
Effect: <one-sentence description>
Token scope: write
Proceed?
```

### Mutation catalog - requires confirmation

**GitHub (`gh`):** `release create/delete/upload`, `issue create/close/reopen`,
`pr create/merge/close`, `workflow run`, `run cancel/delete`, `secret set`,
`variable set`, `api --method POST/PUT/PATCH/DELETE`.

**GitLab (`glab`):** `release create/delete`, `mr create/merge`, `issue
create/close/reopen`, `pipeline run`, `variable set`.

Operations NOT requiring confirmation: `release list`, `issue list`, `pr list`,
`api <GET>`.

### Token hygiene

Never pass tokens in command strings visible to `/proc`:

```bash
# SAFE - token only in header
curl -sS -H "Authorization: Bearer $GITLAB_TOKEN" "$url"

# UNSAFE - token in command string
echo "curl -H 'Authorization: Bearer $TOKEN' $url"
```

After sensitive operations, clear shell history entries containing tokens.

### GraphQL injection prevention

Always use parameterized variables, never string interpolation:

```bash
# SAFE
gh api graphql -F owner="$owner" -F name="$name" -f query='
  query($owner: String!, $name: String!) { repository(owner: $owner, name: $name) { stargazerCount } }'

# UNSAFE
gh api graphql -f query="query { repository(owner: \"$owner\", name: \"$name\") { stargazerCount } }"
```

Source: [OWASP Secrets Management](<https://cheatsheetseries.owasp.org/cheatsheet>
s/Secrets_Management_Cheat_Sheet.html).

## Testing tokens

```bash
# GitHub
gh auth status
curl -sS -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/user

# GitLab
glab auth status
curl -sS -o /dev/null -w '%{http_code}' \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  https://gitlab.com/api/v4/user
```

Both should return `200`. A `401` means the token is invalid or expired.
