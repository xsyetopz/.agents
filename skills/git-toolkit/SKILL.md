---
name: git-toolkit
description: Local Git inspection, history, worktrees, staging, recovery, patches, and commits.
---

# Git Toolkit

## Use this skill

- Inspect or change a local repository: status, diffs, branches, tags, staging, commits, or restores.
- Construct Conventional Commits, amend or fix up unpublished work, or recover references with reflog.
- Handle local rebases, cherry-picks, bisects, stashes, worktrees, patches, hooks, signing, submodules, or LFS.
- Do not use for hosted GitHub or GitLab APIs, CI/CD pipeline authoring, team branching or merge policy, or remote mutation without exact authorization.

## Rules

- Inspect status, branch and upstream, and relevant diffs before mutation; preserve unrelated changes.
- Treat read-only inspection and a requested new local commit as safe. Classify every other history or worktree mutation before running it.
- For amend, rebase, reset, stash deletion, cherry-pick, or migration, record HEAD and recovery options, state consequences, and verify afterward.
- Never infer authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, `filter-repo`, or deleting all stashes.
- Route hosted API work to `$git-actions`, pipeline work to `$git-ci-cd`, and team policy to `$git-workflows`.

## Steps

1. Run `git status --short --branch`, inspect the current branch and upstream, and read scoped diffs.
2. Confirm the request is local and classify its effect. Stop when a destructive operation lacks exact authorization.
3. Select the narrowest command sequence and stage explicit paths when scope is bounded.
4. Before a commit or patch, run `git diff --cached --check`, applicable checks, and inspect the staged diff.
5. Perform the authorized operation.
6. Re-read status, history, and recovery state; report exact results and remaining risk.

The initial inspection is:

```bash
git status --short --branch
git diff
git diff --cached --check
```

For a requested commit, stage only authorized paths, inspect `git diff --cached`, use `type(scope): imperative summary`, commit once, and verify `git log -1 --oneline` plus status.

## Resources

- [Reference index](references/index.md) for operation-based route selection.
- [Git security tooling](references/git-security-tooling.md) for secret scanning and safe Git tooling.
- [Rebase guide](references/rebase-guide.md) for rebase, squash, fixup, or split history.
- [Bisect guide](references/bisect-guide.md) for regression isolation.
- [Reflog guide](references/reflog-guide.md) for recovery and lost refs.
- [Worktree guide](references/worktree-guide.md) for parallel local workspaces.
- [Stash guide](references/stash-guide.md) for preserving partial work.
- [Patch guide](references/patch-guide.md) for format-patch, apply, am, or cherry-pick.
- [Archaeology](references/archaeology.md) for pickaxe, blame, or history tracing.
- [Release management](references/release-management.md) for local tags and release history.
- [Hooks guide](references/hooks-guide.md) for hook behavior and setup.
- [Signing guide](references/signing-guide.md) for commit or tag signing.
- [Submodule and LFS](references/submodule-lfs.md) for those repositories.
- [Git configuration](references/gitconfig.md) for config precedence and safety settings.
- [Git attributes](references/gitattributes.md) for EOL, diff, merge, or binary behavior.

## Verify

- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- For a local commit or patch, also run `git diff --check` and the repository's applicable tests; report every unrun check.
- Finish only when the requested local state is achieved, unrelated changes remain intact, authorized paths are the only changed or staged content, and status, history, recovery, and validation evidence are reported.
