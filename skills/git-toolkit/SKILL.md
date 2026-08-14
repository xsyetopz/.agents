---
name: git-toolkit
description: Local Git inspection, history, worktrees, staging, recovery, patches, and commits.
---

# Git Toolkit

Inspect and change a local Git repository with explicit scope, recovery evidence, and clean status.

## Use this skill

- Inspect or change local status, diffs, branches, tags, staging, commits, or restores.
- Construct Conventional Commits, amend or fix up unpublished work, or recover references with reflog.
- Handle local rebases, cherry-picks, bisects, stashes, worktrees, patches, hooks, signing, submodules, or LFS.
- Do not use for hosted GitHub or GitLab APIs, CI/CD authoring, team branching or merge policy, or remote mutation without exact authorization.
- Redirect hosted API work to `$git-actions`, pipeline work to `$git-ci-cd`, and team policy to `$git-workflows`.

## Rules

- Inspect status, branch and upstream, and relevant diffs before mutation; preserve unrelated changes.
- Treat read-only inspection and a requested new local commit as safe. Classify every other history or worktree mutation before running it.
- For amend, rebase, reset, stash deletion, cherry-pick, or migration, record HEAD and recovery options, state consequences, and verify afterward.
- Never infer authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, `filter-repo`, or deleting all stashes.

## Steps

1. Run `git status --short --branch`, inspect the current branch and upstream, and read scoped diffs.
2. Confirm the request is local and classify its effect. Stop when a destructive operation lacks exact authorization.
3. Use the reference router to select the narrowest operation guide.
4. Stage explicit paths when scope is bounded; before a commit or patch, run `git diff --cached --check`, applicable checks, and inspect the staged diff.
5. Perform the authorized operation.
6. Re-read status, history, and recovery state; report exact results and remaining risk.

## Resources

- Start with the package [reference router](references/index.md).
- Run the package [checker](scripts/check.py) for structural evidence.

## Verify

- Done means the requested local state is achieved, unrelated changes remain intact, authorized paths are the only changed or staged content, and status, history, recovery, and validation evidence are reported.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- For a local commit or patch, also run `git diff --check` and applicable repository tests; report every unrun check.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark remote effects, unavailable hooks, signing, repository tests, or other unrun evidence `UNVERIFIED`.
