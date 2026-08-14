---
name: git-workflows
description: Team branching, merge strategy, branch protection, and repository integration policy.
---

# Git Workflows

Select and verify a team integration model from measured repository and delivery constraints.

## Use this skill

- Choose or migrate a branching, release, hotfix, environment, or fork model.
- Select squash, rebase, merge-commit, merge-queue, or linear-history policy.
- Design or audit branch protection, reviews, status checks, bypasses, stale-branch cleanup, or integration metrics.
- Do not use for local Git execution, hosted API calls, or CI/CD workflow authoring.
- Redirect local Git execution to `$git-toolkit`, platform settings or API calls to `$git-actions`, pipeline implementation to `$git-ci-cd`, and contributor policy or CODEOWNERS to `$repo-governance`.

## Rules

- Start with measured team size, release cadence, deployability, compliance, repository shape, and failure evidence.
- Recommend the simplest model that meets constraints and name its enforcement setting.
- Prefer daily integration, short-lived branches, a protected mainline, and applicable checks.
- Prefer linear history unless release topology demonstrates a need for merge commits.
- Do not claim enforcement from prose. Inspect actual repository settings and label unimplemented rules advisory.

## Steps

1. Inventory branches, protection, required checks, recent merges, and branch ages; measure branch lifetime, merge delay, conflict rate, release cadence, rollback needs, and current integration settings.
2. Record review, regulatory, environment, release, and emergency constraints.
3. Use the reference router to compare viable branching and merge models.
4. Select branch origins and destinations, merge method, release source, deletion policy, and emergency path.
5. Map each rule to protection, required reviews and checks, queue, bypass ownership, automation, and audit evidence.
6. Define migration, rollback, metrics, and review date. Verify current settings or label them advisory.

## Resources

- Start with the package [reference router](references/index.md).
- Run the package [checker](scripts/check.py) for structural evidence.

## Verify

- Done means the model follows measured constraints, every rule maps to an enforcement mechanism, and migration, rollback, metrics, emergency, and review paths are defined.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Confirm proposals against actual branch settings, protection rules, checks, and recent history; do not treat an unverified proposal as enforcement evidence.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark hosted settings, integration metrics, and unavailable repository evidence `UNVERIFIED`.
