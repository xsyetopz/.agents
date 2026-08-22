---
name: git-workflows
description: Local Git operations, Conventional Commit fallback enforcement, recovery, and team branching, merge, release, and integration policy.
---

# Git Workflows

Operate a local Git repository and design team integration policy with explicit scope, reversible steps, measured constraints, and verified evidence.

## Use this skill

- Inspect or change local status, diffs, branches, tags, staging, commits, restores, rebases, bisects, stashes, worktrees, patches, signing, submodules, or Git LFS.
- Establish commit-message policy and a tracked `commit-msg` hook when the repository has no contribution or commit guidance.
- Choose or audit branching, release, hotfix, merge, branch-protection, review, queue, or stale-branch policy.
- Do not use for hosted API calls, CI/CD workflow authoring, or remote mutation without exact authorization.
- Redirect hosted GitHub or GitLab API work to `$git-actions`, pipeline work to `$git-ci-cd`, and contributor documentation or CODEOWNERS to `$repo-docs`.

## Rules

- Inspect status, branch, upstream, relevant diffs, repository settings, and delivery constraints before mutation or policy selection. Preserve unrelated changes.
- Classify history and worktree effects. Record `HEAD` and recovery options before amend, rebase, reset, stash deletion, cherry-pick, or migration.
- Never infer authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, remote mutation, or deleting all stashes.
- Recommend the simplest integration model that meets measured constraints and map each policy to actual enforcement settings.
- Before adding a commit convention, inspect repository instructions, contribution documents, commit tooling, hooks, and effective Git configuration. Existing repository-owned guidance wins.
- When no contribution or commit guidance exists and commit-workflow mutation is authorized, default to Conventional Commits and install the tracked fallback `commit-msg` hook through the repository's existing hook manager or `.githooks`.
- Do not overwrite an existing hook, create a parallel hook system, or claim that a tracked client hook enforces remote clones or hosted merges.
- Do not claim hosted enforcement from prose or local output. Mark uninspected remote settings and effects `UNVERIFIED`.
- Do not invent custom schema files or custom generated files as outputs. Established Git hooks and repository-owned formats are allowed.

## Steps

1. Identify whether the request is a local Git operation, a team workflow decision, or both. Inspect status, branch, upstream, scoped diffs, settings, and relevant history.
2. Confirm exact mutation authority and classify consequences. Stop when destructive or remote effects lack authorization.
3. Load only the matching local-operation or team-policy route from `references/index.md`.
4. For commit workflow setup, apply the [Conventional Commits fallback](references/local/conventional-commits.md) only after proving that no existing guidance owns the decision.
5. For local work, stage explicit paths, run applicable checks, perform the authorized operation, and preserve a recovery path. For policy work, measure constraints, compare viable models, and map rules to enforcement.
6. Re-read status, history, settings, and recovery state. Verify the local result and directly observed enforcement only.
7. Report exact commands, changed or staged paths, policy gaps, evidence, and unverified remote state.

## Resources

- Start with the package [reference router](references/index.md).
- Load only the routed local-operation or team-policy guide needed for the task. Use the [Conventional Commits fallback](references/local/conventional-commits.md) only when the repository has no existing contribution or commit guidance.

## Verify

- Done means the requested local state or policy is achieved, unrelated changes remain intact, destructive effects have explicit authority and recovery evidence, and every policy claim maps to observed settings or is marked advisory.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- For local changes, run `git diff --check`, applicable repository tests, and final status/history inspection. For the fallback hook, invoke accepted and rejected message fixtures and verify `core.hooksPath`. For policy, inspect actual protection, checks, recent merges, migration, and rollback evidence.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark hooks, signatures, LFS objects, hosted settings, integration metrics, remote effects, and unavailable evidence `UNVERIFIED`.
