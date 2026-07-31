---
name: git-actions
description: Use when interacting with GitHub or GitLab through their HTTP APIs - fetching releases, tags, and latest versions, managing issues/PRs/merge requests, querying repository metadata, triggering workflows, or automating platform operations via REST and GraphQL. Do not use for local git commands or CI/CD pipeline authoring.
---

# Git Actions

Interact with GitHub and GitLab platforms through their APIs. Prefer the `gh`
CLI for GitHub and `glab` CLI for GitLab when they're available - they handle
auth and pagination. Fall back to raw HTTP only when the CLI doesn't cover the
endpoint.

## When to use

- Fetching the latest release version, tag, or asset from a repository
- Listing releases, comparing tags, or generating changelogs from release notes
- Creating or updating issues, pull requests, or merge requests via API
- Querying repository metadata: stars, forks, license, default branch
- Triggering workflow runs or checking pipeline status
- Managing repository settings, branch protection, or webhooks via API
- Searching code, commits, or issues across repositories
- Programmatic git hosting operations that `git` alone can't do

## When NOT to use

- Local git operations (commit, push, rebase) - use `git` directly or `git-
  toolkit`
- Writing CI/CD pipeline YAML - use `git-ci-cd`
- Simple `git clone` or `git remote` - those work without the platform API

## Guardrails

Platform APIs have the same blast radius as the token that authenticates them.
This skill defaults to read-only and requires explicit confirmation for any
operation that mutates repository state. See `references/auth-and-security.md`
for the mutation catalog, token hygiene rules, and GraphQL injection prevention.

Sources: [Git security best practices](https://dev.to/prankurpandeyy/git-
security-best-practices-for-keeping-your-code-safe-1nep), [OWASP Secrets Managem
ent](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_She
et.html).

### Default posture: read-only

Start every session by verifying the token has minimal scope. For GitHub, use
`gh auth token` and check the token type. For GitLab, verify the token scopes.

All commands default to GET requests. Never issue POST/PUT/PATCH/DELETE without
confirming the operation with the user first.

### Mutating operations - require confirmation

These operations must be confirmed explicitly before execution. State what will
change and ask:

- Creating or updating releases (`POST /releases`, `gh release create`)
- Creating, editing, or closing issues/PRs/merge requests
- Triggering workflow runs (`POST /actions/workflows/dispatches`)
- Changing repository settings, branch protection, or webhooks
- Deleting anything: branches, tags, releases, artifacts, webhooks
- Merging pull requests or accepting merge requests
- Adding or removing collaborators, teams, or deploy keys

### Token safety

- Tokens must come from environment variables, never hardcoded
- Never log, echo, print, or commit tokens - not even in error messages
- Prefer `gh`/`glab` CLI over raw `curl` - the CLI handles auth and token
  refresh
- When using raw HTTP, always use `-H "Authorization: Bearer $TOKEN"` - never
  pass
tokens in the URL query string (they appear in server logs)
- Use fine-grained tokens with minimum permissions:
  - Read-only for queries: `contents: read`, `metadata: read`
  - Write only when needed: add specific write scopes per operation
  - Never use classic PATs with broad `repo` scope when fine-grained tokens
    suffice

### Input validation

Before any API call that accepts user-supplied input:

1. Validate the input format (e.g., semver for tag names, URL-safe for repo
   names)
2. Shell-escape values used in `curl` or CLI arguments - prefer `--form` over
   string interpolation
3. For GraphQL, use parameterized queries with variables, never string
   interpolation:
   ```bash
   # Safe - variables are passed separately
   gh api graphql -F owner="$owner" -F name="$name" -f query='
     query($owner: String!, $name: String!) { ... }'

   # BLOCKED - string interpolation enables injection
   gh api graphql -f query="query { repository(owner: \"$owner\") { ... } }"
   ```

### GitHub-specific

- `gh` commands with `--repo` are read-only by default unless the subcommand is
explicitly mutating (e.g. `gh issue create`, `gh pr merge`)
- `gh api` with `--method POST/PUT/PATCH/DELETE` requires confirmation
- `gh release create`, `gh release delete`, `gh release upload` require
  confirmation

### GitLab-specific

- `glab` commands that create, update, or delete resources require confirmation
- Raw API `POST/PUT/DELETE` with `PRIVATE-TOKEN` requires confirmation and scope
  check
- Project ID discovery (`projects/owner%2Frepo`) must be the first step --
never guess a project ID

## Quick start

1. Check if `gh` (GitHub) or `glab` (GitLab) is installed: `which gh glab`
2. If available, use the CLI. If not, fall back to `curl` with an auth token.
3. For version fetching: identify the repo and the API endpoint. Use the
   reference table below.
4. Parse JSON responses with `jq` - never hand-parse with `grep` or `awk`.

### Auth

- GitHub: `gh auth status` or `Authorization: Bearer $GITHUB_TOKEN`
- GitLab: `glab auth status` or `PRIVATE-TOKEN: $GITLAB_TOKEN`
- Never log, echo, or commit tokens. Read them from environment variables.

## Common tasks

### Fetch latest release version

```bash
# GitHub - gh CLI (preferred)
gh release view --repo owner/repo --json tagName -q '.tagName'

# GitHub - raw API
curl -sS -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/owner/repo/releases/latest | jq -r '.tag_name'

# GitLab - glab CLI
glab release view --repo owner/repo latest

# GitLab - raw API
curl -sS "https://gitlab.com/api/v4/projects/${PROJECT_ID}/releases" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" | jq -r '.[0].tag_name'
```

### List releases

```bash
# GitHub
gh release list --repo owner/repo --limit 10

# GitLab
curl -sS "https://gitlab.com/api/v4/projects/${PROJECT_ID}/releases?per_page=10" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" | jq '.[].tag_name'
```

### Create an issue

```bash
# GitHub
gh issue create --repo owner/repo --title "Title" --body "Body"

# GitLab
glab issue create --repo owner/repo --title "Title" --description "Body"
```

## Reference map

| If you need to... | Load |
|---|---|
| GitHub REST API endpoints and pagination | `references/github-api.md` |
| GitHub GraphQL API patterns | `references/github-graphql.md` |
| GitLab REST API endpoints and pagination | `references/gitlab-api.md` |
| Fetching and comparing versions across platforms | `references/version-fetching.md` |
| Auth setup, token scopes, and security | `references/auth-and-security.md` |

## Related skills

- `git-ci-cd` - CI/CD pipeline design, workflow syntax, job debugging
- `git-toolkit` - local git operations, hooks, bisect, worktree

## Validate

```sh
python3 scripts/validate_skill.py skills/git-actions
```
