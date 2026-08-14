---
name: git-ci-cd
description: CI/CD pipeline authoring, review, migration, and failure diagnosis across common Git hosts.
---

# Git CI/CD

## Use this skill

- Create or change workflow files, jobs, matrices, caches, artifacts, services, deployments, runners, or environments.
- Diagnose failed, flaky, slow, duplicated, or platform-specific pipeline behavior.
- Review permissions, OIDC, forks, reusable workflows, actions, images, caches, artifacts, runner isolation, and secret flow.
- Migrate a pipeline across GitHub, GitLab, Bitbucket, or another supported platform.
- Do not use for local Git commands, hosted REST or GraphQL calls, branching or merge policy, or application failures that reproduce outside CI.

## Rules

- Never run untrusted pull-request code with write tokens or production secrets. Never print secrets or hide command errors.
- Reject broad permissions, ambiguous deployment refs, unsafe caches, mutable dependencies when immutable pins are available, and deployment from unreviewed code unless an approved exception is documented.
- Require explicit trusted events and permissions, pinned dependencies, lockfile-based installation, relevant cache keys, useful concurrency, retention, environment controls, and visible failures.
- Do not weaken a check with `continue-on-error`, `allow_failure`, exit-zero wrappers, or hidden errors.
- Route local Git work to `$git-toolkit`, API calls to `$git-actions`, and branching or merge policy to `$git-workflows`.

## Steps

1. Identify the platform, event, trust boundary, required checks, deployment target, and rollback needs.
2. Reproduce an application failure locally when it is not pipeline-owned; inspect workflows, reusable owners, settings, and logs.
3. Load [security checklist](references/security-checklist.md) first, then only the platform references needed; use [GitHub integrations](references/github-integrations.md) when repository services are involved.
4. Change the owning workflow without disabling or downgrading checks.
5. Validate syntax, local equivalents, dependency resolution, permissions, artifacts, and platform lint or run when authorized.
6. Inspect final status, skipped or environment-blocked checks, and rollback behavior.

## Resources

- [Reference index](references/index.md) for trigger-based route selection.
- [Security checklist](references/security-checklist.md) for secrets, permissions, trust boundaries, caches, and dependencies.
- [GitHub Actions](references/github-actions.md) for GitHub workflow syntax and conventions.
- [GitHub integrations](references/github-integrations.md) for repository integrations and maintenance bots.
- [GitLab CI](references/gitlab-ci.md) for GitLab rules, needs, variables, and images.
- [Bitbucket Pipelines](references/bitbucket-pipelines.md) for deployment, variables, caches, and artifacts.
- [Cross-platform patterns](references/cross-platform-patterns.md) for migrations and invariants.

## Verify

- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Finish only when syntax and local checks pass, hosted validation runs when possible, permissions and trust boundaries are verified, failures remain blocking, and skipped or unavailable evidence is reported.
- Static checks do not prove hosted runs, runner isolation, or deployment safety; report those limits.
