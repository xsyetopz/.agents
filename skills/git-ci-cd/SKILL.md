---
name: git-ci-cd
description: CI/CD pipelines, GitHub Actions, GitLab CI, runners, workflow YAML; excludes local Git APIs.
---

# Git CI/CD

Produce a least-privilege, reproducible pipeline whose failures remain visible and whose trust boundaries are explicit.

## When to use

- Create or change workflow files, jobs, matrices, caches, artifacts, services, deployments, runners, or environments.
- Diagnose failed, flaky, slow, duplicated, or platform-specific pipeline behavior.
- Review tokens, permissions, OIDC, forks, reusable workflows, actions, images, caches, artifacts, or runner isolation.
- Migrate a pipeline across GitHub, GitLab, Bitbucket, or CircleCI.

## When NOT to use

- Local Git staging, commits, branches, or rebases; use `$git-toolkit`.
- GitHub or GitLab REST/GraphQL calls; use `$git-actions`.
- Branching or merge-policy selection; use `$git-workflows`.
- Application failures that reproduce outside CI and have no pipeline owner.

## Guardrails

- Reject untrusted pull-request code with write tokens or production secrets, mutable dependencies where immutable pins are supported, secret printing, and swallowed failures.
- Reject broad permissions, ambiguous deployment refs, unsafe caches, or deployment from unreviewed code; require a documented exception for soft-risk patterns.
- Require explicit trusted events and permissions, pinned dependencies, lockfile-based installation, relevant cache keys, useful concurrency, retention, environment controls, and visible failures.
- Never weaken a check with `continue-on-error`, `allow_failure`, exit-zero wrappers, or hidden command errors to make a run pass.

## Workflow

1. Identify platform, event, trust boundary, required checks, deployment target, and rollback needs.
2. Reproduce application failures locally when they are not pipeline-owned; inspect workflows, reusable owners, settings, and logs.
3. Load only the platform and security references needed.
4. Change the owning workflow without disabling or downgrading checks.
5. Validate syntax, local equivalents, dependency resolution, permissions, artifacts, and platform lint or run when authorized.
6. Inspect final status, skipped or environment-blocked checks, and rollback behavior.

## Quick start

Load [security checklist](references/security-checklist.md), then the platform reference: [GitHub Actions](references/github-actions.md), [GitLab CI](references/gitlab-ci.md), [Bitbucket Pipelines](references/bitbucket-pipelines.md), or [cross-platform patterns](references/cross-platform-patterns.md). Use [GitHub integrations](references/github-integrations.md) when repository services are involved.

## Reference map

- [Reference index](references/index.md) for trigger-based route selection.
- Security, trust boundaries, secrets, caches, and dependencies: [security checklist](references/security-checklist.md).
- GitHub workflow conventions: [GitHub Actions](references/github-actions.md), [GitHub integrations](references/github-integrations.md).
- GitLab rules, needs, variables, and images: [GitLab CI](references/gitlab-ci.md).
- Bitbucket deployment, variables, caches, and artifacts: [Bitbucket Pipelines](references/bitbucket-pipelines.md).
- Cross-platform migration and invariants: [cross-platform patterns](references/cross-platform-patterns.md).

## Completion

Complete when syntax and local checks pass, the real pipeline is exercised when possible, permissions and trust boundaries are verified, failures remain blocking, and skipped or environment-blocked validation is reported exactly.

## Validation

Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package. Static checks do not prove a hosted run, runner isolation, or deployment safety; report unavailable external evidence.

## Related skills

- `$git-toolkit` for local repository operations.
- `$git-actions` for remote platform API automation.
- `$git-workflows` for branch and merge policy.
