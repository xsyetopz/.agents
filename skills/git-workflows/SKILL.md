---
name: git-workflows
description: Team branching, merge strategy, branch protection, and repository integration policy.
---

# Git Workflows

## Use this skill

- Choose or migrate a branching, release, hotfix, environment, or fork model.
- Select squash, rebase, merge-commit, merge-queue, or linear-history policy.
- Design or audit branch protection, reviews, status checks, bypasses, stale-branch cleanup, or integration metrics.
- Do not use for local Git execution, hosted API calls, or CI/CD workflow authoring.

## Rules

- Start with measured team size, release cadence, deployability, compliance, repository shape, and failure evidence.
- Recommend the simplest model that meets the constraints and name its enforcement setting.
- Prefer daily integration, short-lived branches, a protected mainline, and applicable checks.
- Prefer linear history unless release topology demonstrates a need for merge commits.
- Do not claim enforcement from prose. Inspect actual repository settings and label unimplemented rules advisory.
- Route local Git execution to `$git-toolkit`, platform settings or API calls to `$git-actions`, pipeline implementation to `$git-ci-cd`, and contributor policy or CODEOWNERS to `$repo-governance`.

## Steps

1. Inventory branches, protection, required checks, recent merges, and branch ages; measure branch lifetime, merge delay, conflict rate, release cadence, rollback needs, and current integration settings.
2. Record review, regulatory, environment, release, and emergency constraints.
3. Compare at least two viable models with the same constraints and explicit trade-offs.
4. Select branch origins and destinations, merge method, release source, deletion policy, and emergency path.
5. Map each rule to protection, required reviews and checks, queue, bypass ownership, automation, and audit evidence.
6. Define migration, rollback, metrics, and review date. Verify current settings or label them advisory.

Default to GitHub Flow or trunk-based development unless measured constraints require GitLab Flow, forking, or GitFlow.

## Resources

- [Reference index](references/index.md) for trigger-based route selection.
- [Branching models](references/branching-models.md) for model comparison and selection.
- [Merge strategies](references/merge-strategies.md) for integration-method trade-offs.
- [Branch protection](references/branch-protection.md) for repository enforcement templates.

## Verify

- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Confirm proposals against actual branch settings, protection rules, checks, and recent history; do not treat an unverified proposal as enforcement evidence.
- Finish only when the model follows measured constraints, every rule maps to an enforcement mechanism, and migration, rollback, metrics, emergency, and review paths are defined.
