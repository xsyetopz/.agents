---
name: git-workflows
description: >
  Use when selecting, designing, migrating, enforcing, or auditing team Git branching and integration policy: GitHub Flow, trunk-based development, GitFlow, GitLab Flow, forking workflow, monorepo branching, release branches, feature branches, pull requests, merge queues, squash merge, rebase merge, merge commits, linear history, branch protection, required reviews, required status checks, branch lifetime, and branch deletion. Trigger when the user asks which branching model, merge strategy, PR policy, protected-branch rule, commit-history policy, or release flow a team should use. Not for local status, add, stage, commit, amend, reset, rebase execution, or other repository commands; use git-toolkit. Not for CI/CD YAML; use git-ci-cd.
---

# Git Workflows

Select a team integration model from delivery constraints, then pair every policy
with the repository setting or automation that enforces it.

## When to use

- Choosing or migrating a branching model
- Defining feature, release, hotfix, environment, or fork workflows
- Selecting squash, rebase, merge-commit, merge-queue, or linear-history policy
- Designing branch protection, review, status-check, and branch-lifetime rules
- Auditing merge conflict rate, release lag, stale branches, or integration delay

## When NOT to use

- Running local Git commands, staging, committing, amending, or rebasing; use git-toolkit
- Writing CI/CD YAML; use git-ci-cd
- Calling GitHub or GitLab APIs; use git-actions

## Guardrails

- Start from team size, release cadence, deployability, compliance, repository shape, and current failure evidence.
- Recommend the simplest model that meets those constraints.
- Do not prescribe a workflow without its enforcement settings.
- Avoid long-lived feature branches; integrate at least daily where product constraints permit.
- Protect the mainline, require applicable checks, and automate stale-branch deletion.
- Prefer linear history unless a release model has a demonstrated need to preserve branch topology.

## Decision workflow

1. Measure current branch lifetime, merge delay, conflict rate, release cadence, and rollback needs.
2. Identify regulatory, review, environment, and release constraints.
3. Compare at least two viable models using the same constraints.
4. Select branch origins, merge destinations, merge method, release source, and deletion policy.
5. Define branch protection, required reviews/checks, merge queue, bypass ownership, and emergency path.
6. Record migration steps, rollback, metrics, and review date.

## Models

| Model | Best fit | Default integration | Main risk |
|---|---|---|---|
| GitHub Flow | Most teams shipping continuously | short PR branch to main | weak release discipline if environments are unmanaged |
| Trunk-based | High-throughput teams with strong CI and feature flags | hours-long branch or direct trunk | requires excellent tests and incremental design |
| GitLab Flow | Explicit environment promotion | main to environment branches | environment branches can drift |
| Forking | External contributors and open source | fork PR to upstream | slower feedback and permission complexity |
| GitFlow | Scheduled, versioned products with long stabilization | feature/develop/release/main | ceremony, delayed integration, merge debt |

Default to GitHub Flow or trunk-based development unless evidence requires a
heavier model.

## Merge strategies

| Strategy | Use when | Tradeoff |
|---|---|---|
| Squash merge | A PR is one reviewable change | discards internal commit sequence |
| Rebase merge | Individual commits are intentional and buildable | preserves noisy commits if discipline is weak |
| Merge commit | Branch topology is operationally meaningful | non-linear history complicates bisect and revert |
| Merge queue | Main must remain green under concurrent merges | adds queue latency and platform dependence |

Enforce the selected method at repository level. Define who can bypass it and how
that bypass is audited.

## Verification

Inspect actual repository settings, protected branches, merge methods, status
checks, branch ages, and recent merge history. Do not present a policy document as
proof that enforcement exists.

## Reference map

| Need | Load |
|---|---|
| Detailed model comparison | references/branching-models.md |
| Merge strategy tradeoffs | references/merge-strategies.md |
| Protection templates | references/branch-protection.md |

## Completion

Complete when the selected model follows measured constraints, every rule maps to
an enforcement mechanism, migration and emergency paths are defined, and current
settings are verified or clearly marked unimplemented.

## Related skills

- git-toolkit for local Git execution and commits
- git-ci-cd for required pipeline checks
- git-actions for platform settings through APIs
- repo-governance for CONTRIBUTING.md and CODEOWNERS
