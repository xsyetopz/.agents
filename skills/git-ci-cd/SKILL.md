---
name: git-ci-cd
description: CI/CD pipeline authoring, review, migration, and failure diagnosis across GitHub, GitLab, and Bitbucket with trust controls.
---

# Git CI/CD

Author, review, migrate, and diagnose continuous integration and continuous delivery (CI/CD) pipelines without weakening trust or failure signals. This package covers workflow files and hosted runner behavior, not hosted API calls or local application debugging.

## Use this skill

- Create or change workflow files, jobs, matrices, caches, artifacts, services, deployments, runners, or environments.
- Diagnose failed, flaky, slow, duplicated, or platform-specific pipeline behavior.
- Review permissions, OpenID Connect (OIDC), forks, reusable workflows, actions, images, caches, artifacts, runner isolation, and secret flow.
- Migrate a pipeline across GitHub, GitLab, Bitbucket, or another supported platform when the target syntax and trust model are explicit.
- Do not use for local Git commands, hosted REST or GraphQL calls, branching or merge policy, or application failures that reproduce outside CI.
- Redirect local Git work to `$git-toolkit`, hosted API calls to `$git-actions`, and branching or merge policy to `$git-workflows`.

## Rules

- Never run untrusted pull-request (PR) or merge-request (MR) code with write tokens or production secrets. Never print secrets or hide command errors.
- Reject broad permissions, ambiguous deployment refs, unsafe caches, mutable dependencies when immutable pins are available, and deployment from unreviewed code unless an approved exception is documented.
- Require explicit trusted events and permissions, pinned dependencies, lockfile-based installation, relevant cache keys, useful concurrency, retention, environment controls, and visible failures.
- Do not weaken a check with `continue-on-error`, `allow_failure`, exit-zero wrappers, or hidden errors.
- Distinguish provider syntax from local recommendations. A passing local lint does not prove hosted settings, runner isolation, deployment safety, or secret masking.

## Steps

1. Identify platform, event, trust boundary, required checks, deployment target, and rollback needs.
2. Reproduce an application failure locally when it is not pipeline-owned; inspect workflows, reusable owners, settings, and logs.
3. Load only the matching route from `references/index.md`, then use the source map for current provider syntax and security claims.
4. Change the owning workflow without disabling or downgrading checks.
5. Validate syntax, local equivalents, dependency resolution, permissions, artifacts, and platform lint or run when authorized.
6. Inspect final status, skipped or environment-blocked checks, rollback behavior, and evidence freshness.

## Resources

- Start with the package-local [reference router](references/index.md).
- Use the package-local [source map](references/sources.md) for provider URLs, diagram syntax, scope, and freshness.

## Verify

- Done means syntax and local checks pass, hosted validation runs when possible, permissions and trust boundaries are verified, failures remain blocking, and skipped or unavailable evidence is reported.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Inspect dependency pins, permissions, cache scope, artifacts, runner isolation, deployment ref, rollback path, and the provider source record.
- Report commands, exit codes, changed paths, evidence, and remaining limits. Mark hosted runs, runner isolation, deployment safety, provider freshness, or unavailable evidence `UNVERIFIED`.
