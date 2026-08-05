---
name: git-ci-cd
description: >
  Use when designing, debugging, securing, optimizing, or modifying CI/CD pipelines on GitHub Actions, GitLab CI, Bitbucket Pipelines, or CircleCI. Covers workflow YAML, .github/workflows, .gitlab-ci.yml, jobs, stages, matrices, runners, caches, artifacts, reusable workflows, container jobs, services, environments, secrets, OIDC, permissions, concurrency, deployments, flaky pipelines, failing workflows, release automation, and cross-platform migration. Trigger phrases include CI failure, CD pipeline, GitHub Actions, GitLab CI, workflow file, build matrix, cache miss, artifact upload, runner, deployment job, reusable workflow, pipeline security, and status check. Not for local Git operations or platform API calls.
---

# Git CI/CD

Produce a least-privilege, reproducible pipeline whose failures remain visible and
whose behavior is validated on the owning platform when possible.

## When to use

- Creating or changing CI/CD workflow files, jobs, matrices, caches, artifacts, services, or deployments
- Debugging failed, flaky, slow, duplicated, or platform-specific pipeline behavior
- Securing tokens, permissions, OIDC, forks, reusable workflows, actions, images, and runners
- Migrating pipelines across GitHub, GitLab, Bitbucket, or CircleCI

## When NOT to use

- Local Git staging, commits, branches, or rebases; use git-toolkit
- GitHub or GitLab REST/GraphQL calls; use git-actions
- Selecting a branching model; use git-workflows
- Application build failures that reproduce outside CI and have no pipeline owner

## Guardrails

### Hard blocks - reject on sight

- Untrusted pull-request code running with write tokens or production secrets
- Mutable third-party action or image references where an immutable digest/SHA is supported
- Secrets printed, interpolated into shell code, or passed to untrusted steps
- Broad write permissions without a documented job-level need
- Suppressed failures through continue-on-error, allow_failure, exit-zero wrappers, or swallowed command errors
- Deployment from unreviewed or ambiguous refs

### Soft blocks - require justification

- Self-hosted runners for untrusted contributions
- Cache keys that permit untrusted cache poisoning
- Repository-wide permissions instead of job-level permissions
- Long-lived credentials where OIDC or short-lived tokens are available
- Large matrices or duplicate jobs without measured coverage value

### Required patterns - must be present

- Explicit permissions and trusted event selection
- Pinned third-party dependencies
- Deterministic dependency installation and lockfile use
- Cache keys tied to relevant manifests and platform dimensions
- Concurrency/cancellation where duplicate work is wasteful or unsafe
- Artifact retention and deployment environment controls appropriate to sensitivity
- Visible, non-suppressed validation failures

### Pre-merge review checklist

Verify event trust boundary, token permissions, shell quoting, expression injection,
secret flow, dependency pinning, cache trust, artifact contents, environment gates,
concurrency, timeouts, and rollback behavior.

## Quick start

1. Identify platform, event, trust boundary, required checks, and deployment targets.
2. Reproduce the failure locally when it belongs to application code.
3. Inspect current workflow, reusable owners, repository settings, and recent logs.
4. Load only the platform and security references needed.
5. Change the owning workflow without disabling or downgrading checks.
6. Validate syntax, local equivalents, platform lint, and an actual pipeline run when authorized and available.
7. Inspect job permissions, resolved dependencies, artifacts, and final status.

## Platform conventions

### GitHub Actions

Prefer job-level permissions, immutable action SHAs, trusted pull_request for fork
checks, environments for deployment, and reusable workflows with explicit inputs
and secrets.

### GitLab CI

Use rules instead of ambiguous only/except combinations, protected variables and
environments, explicit needs graphs, immutable images, and scoped job tokens.

### Bitbucket Pipelines

Use deployment environments, secured variables, explicit caches/artifacts, and
careful branch/PR conditions. Treat pipe versions as supply-chain dependencies.

### CircleCI

Use restricted contexts, pinned orbs/images, approval jobs for production, and
explicit workspace/artifact boundaries.

## Reference map

| Need | Load |
|---|---|
| GitHub Actions | references/github-actions.md |
| GitHub integrations | references/github-integrations.md |
| GitLab CI | references/gitlab-ci.md |
| Bitbucket Pipelines | references/bitbucket-pipelines.md |
| Cross-platform design | references/cross-platform-patterns.md |
| Security review | references/security-checklist.md |

## Completion

Complete when syntax and local checks pass, the real pipeline is exercised when
possible, permissions and trust boundaries are verified, failures remain blocking,
and skipped or environment-blocked validation is reported exactly.

## Related skills

- git-toolkit for local repository operations
- git-actions for platform API automation
- git-workflows for branch and merge policy
