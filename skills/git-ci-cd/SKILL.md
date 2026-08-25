---
name: git-ci-cd
description: Use this skill when authoring, reviewing, migrating, or diagnosing GitHub, GitLab, or Bitbucket CI/CD pipelines with trust controls; use $git-actions for hosted API calls and an application-debugging workflow for runtime code failures.
---

# Git CI/CD

Author, review, migrate, and diagnose CI/CD pipelines without weakening trust boundaries or failure signals.

## Workflow

1. Identify provider, event, trust boundary, required checks, services, artifacts, deployment target, environment controls, and rollback needs.
2. Reproduce failures locally when they are application-owned; inspect workflow owners, reusable workflows, settings, and logs for pipeline-owned behavior.
3. Load only the matching provider, security, or source reference from the direct routes below.
   - [Bitbucket Pipelines](references/bitbucket-pipelines.md) · [Cross-Platform CI Patterns](references/cross-platform-patterns.md) · [GitHub Actions](references/github-actions.md) · [GitHub Integrations](references/github-integrations.md)
   - [GitLab CI](references/gitlab-ci.md) · [CI/CD Security Checklist](references/security-checklist.md) · [Git CI/CD source map](references/sources.md)
4. Change the owning workflow with explicit trusted events, least permissions, immutable dependencies where available, lockfile installs, scoped caches, useful concurrency, retention, and visible failures.
5. Validate syntax, dependency resolution, permissions, secret flow, artifacts, platform lint, and local equivalents; use a hosted run when authorized and material.
6. Return the changed workflow, checks, trust analysis, rollback evidence, and unavailable hosted, runner-isolation, deployment, or provider-freshness evidence as `UNVERIFIED`.

## Gotchas

- Untrusted PR or MR code never receives write tokens or production secrets.
- Keep failures blocking; `continue-on-error`, `allow_failure`, exit-zero wrappers, and hidden errors are not fixes.
- Local lint cannot prove hosted settings, runner isolation, deployment safety, or secret masking.
- Route hosted REST or GraphQL calls to `$git-actions`, local Git and team policy to `$git-workflows`, and runtime failures that reproduce outside CI to application debugging.
- Use established repository formats and canonical inputs rather than custom schemas or generated files.
