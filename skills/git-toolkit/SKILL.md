---
name: git-toolkit
description: local Git inspection, history, worktrees, staging, recovery, patch operations; excludes hosted APIs and CI.
---

# Git Toolkit

## When to use

- Inspect or change a local repository: status, diffs, branches, tags, staging, commits, or restores.
- Construct Conventional Commits, amend or fix up unpublished work, or recover with reflog.
- Handle local rebases, cherry-picks, bisects, stashes, worktrees, patches, hooks, signing, submodules, or LFS.

## When NOT to use

- GitHub or GitLab API operations; route to `git-actions`.
- CI/CD pipeline authoring; route to `git-ci-cd`.
- Team branching, merge, or protection policy; route to `git-workflows`.
- Push, publish, release, or remote mutation without exact authorization.

## Guardrails

- Inspect status, branch/upstream, and relevant diffs before mutation; preserve unrelated changes.
- Treat read-only inspection and a requested new local commit as safe; classify history/worktree mutations before running them.
- For amend, rebase, reset, stash deletion, cherry-pick, or migration, record HEAD and recovery, state consequences, and verify afterward.
- Never infer authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, filter-repo, or deleting all stashes.

## Workflow

1. Read `git status --short --branch`, the current branch/upstream, and scoped diffs.
2. Decide whether the request is local and classify its effect; stop for blocked operations without explicit confirmation.
3. Select the narrowest command sequence, staging explicit paths when scope is bounded.
4. Before commit or patch output, run `git diff --cached --check` and applicable checks; inspect the staged diff.
5. Perform the authorized operation, then re-read status, history, and recovery state and report exact results.

## Quick start

```bash
git status --short --branch
git diff
git diff --cached --check
```

For a requested commit, stage only authorized paths, inspect `git diff --cached`, use `type(scope): imperative summary`, commit once, and verify `git log -1 --oneline` plus status.

## Reference map

Start with the [Reference index](references/index.md), then load only the guide needed for the request:

- [Git security tooling](references/git-security-tooling.md) for secret scanning and safe Git tooling choices.
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

## Completion

Complete when the requested local state is achieved, unrelated changes remain intact, authorized paths are the only changed or staged content, and status/history and validation evidence are reported truthfully.

## Validation

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
```

For a local commit or patch, also run `git diff --check` (and the repository's applicable tests) and report any unrun checks.

## Related skills

- `git-workflows` for team branching, merge, and protection policy
- `git-actions` for GitHub or GitLab APIs
- `git-ci-cd` for pipeline configuration
