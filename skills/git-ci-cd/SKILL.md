---
name: git-ci-cd
description: >
  Use when designing, debugging, or modifying CI/CD pipelines on GitHub Actions, GitLab CI, Bitbucket Pipelines, or CircleCI. Covers workflow syntax, job orchestration, matrix builds, caching, artifact management, environment secrets, container jobs, reusable workflows, and cross-platform CI troubleshooting. Do not use for local git operations or platform API calls.
---

# Git CI/CD

Design, debug, and maintain CI/CD pipelines across Git platforms. Treat each
pipeline as a deterministic build contract - every job must declare its inputs,
outputs, and failure mode.

## When to use

- Writing or modifying GitHub Actions workflow files (`.github/workflows/*.yml`)
- Debugging a failing CI job from pipeline logs
- Setting up matrix builds, caching, or artifact uploads
- Migrating pipelines between platforms (e.g. GitLab CI -> GitHub Actions)
- Designing reusable workflows or composite actions
- Auditing pipeline security (secrets exposure, unprotected branches, OIDC)
- Adding status checks, required reviewers, or branch protection rules

## When NOT to use

- Fetching release versions or interacting with the GitHub/GitLab API - use
  `git-actions`
- Local git operations (rebase, bisect, hooks) - use `git-toolkit`
- Writing application code that happens to run in CI

## Guardrails

CI/CD pipelines are the primary vector for supply-chain attacks and credential
leaks. This skill is strict and opinionated - it rejects patterns that weaken
the pipeline's security posture. Full details with real source citations in
`references/security-checklist.md`.

Sources: [GitLab CI/CD
hardening](https://docs.gitlab.com/security/hardening_cicd_recommendations/),
[Why GitHub CI/CD needs guardrails](https://hoop.dev/blog/why-github-ci-cd-
needs-guardrails), [GitHub OIDC](https://docs.github.com/en/actions/security-
for-github-actions/security-hardening-your-deployments/configuring-openid-
connect-in-cloud-providers).

### Hard blocks - reject on sight

These patterns must never appear in a workflow file. If found, stop and explain
why before suggesting a fix:

**`pull_request_target` from forks**

```yaml
# BLOCKED - runs in the target repo's context with full secrets access.
# An attacker's PR can exfiltrate tokens, modify releases, or deploy.
on: pull_request_target
```

Use `pull_request` with `workflow_run` for safe fork handling, or use an
approval gate with `pull_request_target` only after thorough review.

**Unpinned actions**

```yaml
# BLOCKED - uses a mutable tag. An attacker who compromises the action repo
# can inject code into every pipeline that uses it.
uses: actions/checkout@v4     # mutable tag
uses: docker/setup-buildx     # no version at all
```

Always pin to a full commit SHA:

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

**Secrets in logs**

```yaml
# BLOCKED - prints the secret value to the log, visible to anyone
# with read access to the repo.
- run: echo "Using token: ${{ secrets.TOKEN }}"
- run: curl -H "Authorization: Bearer $TOKEN" ... 2>&1 | tee log.txt
```

Never echo, print, or redirect secrets to stdout/stderr/file. GitHub masks
values automatically, but this is not a guarantee - masking fails on
transformed values, short strings, and debug mode.

**Unbounded permissions**

```yaml
# BLOCKED - workflow runs with full write access to the repo.
# A compromised action or script injection can push malicious code.
jobs:
  build:
    runs-on: ubuntu-latest
    # Missing: permissions: block
```

Always set minimal permissions at the workflow or job level:

```yaml
permissions:
  contents: read
  # Add only what each job actually needs
```

### Soft blocks - require justification

These patterns are allowed only with an explicit, documented reason:

- `actions: write` permission - allows triggering other workflows
- `id-token: write` - must be paired with OIDC, never long-lived secrets
- Self-hosted runners on public repos - fork PRs can run arbitrary code on your
  infra
- `workflow_dispatch` with user-supplied inputs used unsanitized in scripts
- `continue-on-error: true` on security-sensitive steps

### Required patterns - must be present

Every CI workflow must include:

1. **Concurrency group** to prevent stale deploys:
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```
2. **Timeout-minutes** on every job to cap runaway costs
3. **Pinned actions** - all `uses:` references use commit SHA with version
   comment

### Pre-merge review checklist

Before merging a PR that touches `.github/workflows/`:

- [ ] No `pull_request_target` on untrusted fork events
- [ ] All actions pinned to commit SHA
- [ ] `permissions:` block present with minimum scope
- [ ] No secrets echoed, logged, or passed to third-party actions without review
- [ ] Concurrency group set for deploy workflows
- [ ] Timeout set on every job
- [ ] Environment protection rules for production deploys
- [ ] OIDC used for cloud auth, not long-lived secrets

## Quick start

1. Identify the platform and the pipeline file location.
2. Read the platform-specific reference from the table below.
3. Before editing, inspect the existing pipeline: triggers, jobs, environments,
   secrets.
4. Make the minimal change. Test syntax locally before pushing:
   - GitHub Actions: `act` or push to a feature branch
   - GitLab CI: `gitlab-ci-local` or push with `CI_PIPELINE_SOURCE=push`
5. Watch the pipeline run. If it fails, read the logs - do not guess.

## Platform conventions

### GitHub Actions

- Workflow files: `.github/workflows/<name>.yml`
- Triggers: `on: [push, pull_request, workflow_dispatch]`
- Job strategy: `strategy.matrix` with `${{ matrix.os }}` etc.
- Secrets: `${{ secrets.NAME }}` - never echo or log
- Composite actions: `action.yml` with `runs.using: composite`
- Reusable workflows: `.github/workflows/<name>.yml` with `on: workflow_call`
- Default shell: `bash` with `set -eo pipefail`

### GitLab CI

- Pipeline config: `.gitlab-ci.yml` at repo root
- Triggers: `only`/`except`, `rules`, `workflow:rules`
- Job strategy: `parallel:matrix`
- Secrets: CI/CD Variables - `$VARIABLE_NAME`, masked in logs
- Templates: `include:` with `project`, `remote`, or `template`
- Default image: no default - always set `image:` per job or globally

### Bitbucket Pipelines

- Pipeline config: `bitbucket-pipelines.yml` at repo root
- Triggers: `pipelines.branches`, `pull-requests`
- Parallel steps: `step` with `parallel` and `runs-on`
- Secrets: Repository/Deployment variables - `$VARIABLE_NAME`
- Default image: `atlassian/default-image:latest` unless overridden

## Reference map

| If you need to... | Load |
|---|---|
| GitHub Actions workflow syntax and patterns | `references/github-actions.md` |
| GitLab CI pipeline syntax and patterns | `references/gitlab-ci.md` |
| Bitbucket Pipelines syntax | `references/bitbucket-pipelines.md` |
| Cross-platform CI patterns (caching, matrix, artifacts) | `references/cross-platform-patterns.md` |
| Security checklist for pipeline audits | `references/security-checklist.md` |
| GitHub integrations: Dependabot, CodeQL, Renovate, bots | `references/github-integrations.md` |

## Related skills

- `git-actions` - GitHub/GitLab API operations, release fetching, repository
  management
- `git-toolkit` - local git operations, hooks, bisect, worktree, stash
  workflows
- `architecture-enforce` - CI checks for architecture compliance

## Validate

```sh
python3 scripts/validate_skill.py skills/git-ci-cd
```
