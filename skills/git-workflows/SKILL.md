---
name: git-workflows
description: Local Git inspection and recovery plus team branching, merge, release, and repository integration policy.
---

# Git Workflows

Operate a local Git repository and design team integration policy with explicit scope, reversible steps, measured constraints, and verified evidence.

## Use this skill

- Inspect or change local status, diffs, branches, tags, staging, commits, restores, rebases, bisects, stashes, worktrees, patches, signing, submodules, or Git LFS.
- Choose or audit branching, release, hotfix, merge, branch-protection, review, queue, or stale-branch policy.
- Do not use for hosted API calls, CI/CD workflow authoring, or remote mutation without exact authorization.
- Redirect hosted GitHub or GitLab API work to `/skill:git-actions`, pipeline work to `/skill:git-ci-cd`, and contributor documentation or CODEOWNERS to `/skill:repo-docs`.

## Rules

- Inspect status, branch, upstream, relevant diffs, repository settings, and delivery constraints before mutation or policy selection. Preserve unrelated changes.
- Classify history and worktree effects. Record `HEAD` and recovery options before amend, rebase, reset, stash deletion, cherry-pick, or migration.
- Never infer authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, remote mutation, or deleting all stashes.
- Recommend the simplest integration model that meets measured constraints and map each policy to actual enforcement settings.
- Do not claim hosted enforcement from prose or local output. Mark uninspected remote settings and effects `UNVERIFIED`.
- Do not invent custom schema files or custom generated files as outputs. Use only established repository-owned formats and canonical inputs.

## Steps

1. Identify whether the request is a local Git operation, a team workflow decision, or both. Inspect status, branch, upstream, scoped diffs, settings, and relevant history.
2. Confirm exact mutation authority and classify consequences. Stop when destructive or remote effects lack authorization.
3. Load only the matching local-operation or team-policy route from `references/index.md`.
4. For local work, stage explicit paths, run applicable checks, perform the authorized operation, and preserve a recovery path. For policy work, measure constraints, compare viable models, and map rules to enforcement.
5. Re-read status, history, settings, and recovery state. Verify the local result and directly observed enforcement only.
6. Report exact commands, changed or staged paths, policy gaps, evidence, and unverified remote state.

## Resources

- Start with the package [reference router](references/index.md).
- Load only the routed local-operation or team-policy guide needed for the task.

## Verify

- Done means the requested local state or policy is achieved, unrelated changes remain intact, destructive effects have explicit authority and recovery evidence, and every policy claim maps to observed settings or is marked advisory.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- For local changes, run `git diff --check`, applicable repository tests, and final status/history inspection. For policy, inspect actual protection, checks, recent merges, migration, and rollback evidence.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark hooks, signatures, LFS objects, hosted settings, integration metrics, remote effects, and unavailable evidence `UNVERIFIED`.
