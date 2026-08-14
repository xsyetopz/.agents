---
name: git-workflows
description: team branching, merge strategy, branch protection, integration policy; excludes local Git and CI implementation.
---

# Git Workflows

## When to use

- Choose or migrate a branching, release, hotfix, environment, or fork model.
- Select squash, rebase, merge-commit, merge-queue, or linear-history policy.
- Design or audit branch protection, reviews, status checks, bypasses, stale-branch cleanup, or integration metrics.

## When NOT to use

- Local status, staging, commits, amends, rebases, or restores; route to `git-toolkit`.
- GitHub or GitLab API calls; route to `git-actions`.
- CI/CD workflow authoring; route to `git-ci-cd`.

## Guardrails

- Start from measured team size, release cadence, deployability, compliance, repository shape, and failure evidence.
- Recommend the simplest model that meets constraints; do not prescribe policy without its enforcement setting.
- Prefer daily integration and short-lived branches; protect the mainline and require applicable checks.
- Prefer linear history unless release topology has a demonstrated need for merge commits.
- Do not claim enforcement from prose: inspect actual repository settings and mark unimplemented rules.

## Workflow

1. Measure branch lifetime, merge delay, conflict rate, release cadence, rollback needs, and current integration settings.
2. Record review, regulatory, environment, release, and emergency constraints.
3. Compare at least two viable models using the same constraints and explicit tradeoffs.
4. Select branch origins/destinations, merge method, release source, deletion policy, and emergency path.
5. Map each rule to protection, required reviews/checks, queue, bypass ownership, automation, and audit evidence.
6. Define migration, rollback, metrics, and review date; verify current settings or label them advisory.

## Quick start

```text
Inventory branches, protection, required checks, recent merges, and branch ages.
Compare GitHub Flow or trunk-based development with one evidence-backed alternative.
Choose the smallest enforceable model and write its migration and emergency path.
```

Default to GitHub Flow or trunk-based development unless measured constraints require GitLab Flow, forking, or GitFlow.

## Reference map

- [Reference index](references/index.md) for trigger-based route selection.
- [Branching models](references/branching-models.md) for model comparison and selection.
- [Merge strategies](references/merge-strategies.md) for integration method tradeoffs.
- [Branch protection](references/branch-protection.md) for repository enforcement templates.

## Completion

Complete when a model follows measured constraints, every rule maps to an enforcement mechanism, migration and emergency paths are defined, and current settings are verified or clearly marked unimplemented.

## Validation

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
```

Confirm policy against actual branch settings, protection rules, checks, and recent history; do not treat an unverified proposal as enforcement evidence.

## Related skills

- `git-toolkit` for local Git execution and commits
- `git-ci-cd` for required pipeline checks
- `git-actions` for platform settings through APIs
- `repo-governance` for contributor policy and CODEOWNERS
