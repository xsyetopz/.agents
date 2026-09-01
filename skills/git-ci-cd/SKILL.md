---
name: git-ci-cd
description: Author, review, migrate, or diagnose GitHub, GitLab, or Bitbucket CI/CD pipeline files with explicit trust controls. Use for pipeline behavior; not for hosted API mutations or application failures that reproduce outside CI.
---

# Git CI/CD

Author, review, migrate, and diagnose CI/CD pipelines while preserving trust boundaries and visible status signals.

Define the provider, event, trust boundary, required checks, artifacts, deployment effect, and rollback condition. Safe local inspection and validation may proceed. Hosted runs, deployment, secret changes, and other external effects require authorization. Return changed workflows, checks, permissions, and unresolved hosted evidence.

## Start with evidence

1. Identify provider, event, trust boundary, required checks, services, artifacts, deployment target, environment controls, and rollback needs.
2. Reproduce failures locally when they are application-owned; inspect workflow owners, reusable workflows, settings, and logs for pipeline-owned behavior.

## Workflow

1. Load only the matching provider, security, or source reference from the direct routes below.
   - [Bitbucket Pipelines](references/bitbucket-pipelines.md) · [Cross-Platform CI Patterns](references/cross-platform-patterns.md) · [GitHub Actions](references/github-actions.md) · [GitHub Integrations](references/github-integrations.md)
   - [GitLab CI](references/gitlab-ci.md) · [CI/CD Security Checklist](references/security-checklist.md) · [Git CI/CD source map](references/sources.md)
   - [GOOD/RED trust-boundary examples](references/examples.md) (read before editing events, permissions, checkout, secrets, or deploy steps; RED marks a contrast, while GOOD is the workflow pattern)
2. Change the owning workflow with explicit trusted events, least permissions, immutable dependencies where available, lockfile installs, scoped caches, useful concurrency, retention, and visible status signals.

## Validation

1. Validate syntax, dependency resolution, permissions, secret flow, artifacts, platform lint, and local equivalents; use a hosted run when authorized and material.
2. Return the changed workflow, checks, trust analysis, rollback evidence, and unavailable hosted, runner-isolation, deployment, or provider-freshness evidence as `UNVERIFIED`.

## Boundaries

- Code from an untrusted PR or MR runs with read-only permissions and no production secrets.
- Keep required checks blocking; `continue-on-error`, `allow_failure`, exit-zero wrappers, and hidden errors weaken the gate.
- Local lint cannot prove hosted settings, runner isolation, deployment safety, or secret masking.
- Hosted API mutations, local Git policy, and application failures that reproduce outside CI are separate concerns. Handle them directly when included in scope; never stop to locate or install a companion skill.
- Use established repository formats and canonical inputs; keep new output in existing repository-owned forms.
