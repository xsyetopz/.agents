---
name: git-actions
description: >
  Use GitHub API or GitLab API for remote repository resources, pull requests, and workflow dispatch; not local Git commands or CI/CD authoring.
---

# Git Actions

Use the platform API with the minimum required permissions, explicit mutation
authority, and verifiable response handling.

## When to use

- Querying GitHub or GitLab repository, release, tag, issue, PR/MR, check, or workflow data
- Creating or updating platform resources after explicit authorization
- Triggering workflows or downloading artifacts through platform APIs
- Automating pagination, GraphQL queries, rate-limit handling, or repository settings

## When NOT to use

- Local status, diff, staging, commit, branch, tag, or rebase; use git-toolkit
- CI/CD YAML authoring; use git-ci-cd
- Branching-model selection; use git-workflows
- Public facts available from a normal read-only page when API access adds no value

## Guardrails

### Default posture: read-only

Run read-only API queries when they are necessary and credentials are already
available. Do not reveal tokens, broaden scopes, or write credentials to files or
logs.

### Mutating operations - require confirmation

Creating, editing, merging, dispatching, deleting, publishing, changing settings,
or otherwise mutating the remote platform requires exact user authorization for
the target and effect. A request to inspect does not authorize mutation.

### Token safety

- Prefer existing gh, glab, credential-helper, or environment authentication.
- Never print, persist, or transmit tokens outside the intended host.
- Request the least privilege and shortest lifetime available.
- Treat fork and pull-request content as untrusted input.

### Input validation

Resolve host, owner, repository, resource identifier, pagination, API version, and
intended mutation before calling. Validate user-provided URLs and prevent command,
path, GraphQL, or JSON injection.

### GitHub-specific

Use gh api or official REST/GraphQL endpoints. Pin API versions where applicable,
follow Link pagination, and verify permissions before write operations.

### GitLab-specific

Use glab api or versioned GitLab REST/GraphQL endpoints. URL-encode project paths,
handle instance-specific base URLs, and distinguish merge-request IID from global
IDs.

## Quick start

1. Identify platform, host, repository, resource, and read/write intent.
2. Load the relevant platform and auth reference.
3. Confirm mutation authority when needed.
4. Make the narrowest API call with explicit fields and pagination.
5. Validate status, response schema, and target identity.
6. Report the resulting resource ID/URL and any rate-limit or permission caveat.

## Common tasks

| Task | Preferred route | Load |
|---|---|---|
| Latest version or release | releases/tags endpoint | references/version-fetching.md |
| GitHub REST | gh api or official endpoint | references/github-api.md |
| GitHub GraphQL | gh api graphql | references/github-graphql.md |
| GitLab REST/GraphQL | glab api or official endpoint | references/gitlab-api.md |
| Authentication and scopes | existing credential surface | references/auth-and-security.md |

Keep commands in the task response specific to the resolved host and repository;
do not copy generic write examples before authority is established.

## Reference map

Use the Common tasks table. Load only the platform and operation references needed
for the request.

## Completion

Complete when the response is schema-checked, pagination is handled, the remote
target and effect are verified, secrets remain protected, and every mutation is
within explicit authorization.

## Related skills

- git-toolkit for local Git operations
- git-ci-cd for pipeline definitions
- git-workflows for branching and merge policy
