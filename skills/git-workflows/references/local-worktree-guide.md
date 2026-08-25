# Worktree Guide

Scope: local Git worktrees and shared object storage. A worktree is a linked checkout; inspect branch ownership and uncommitted state before removal, and never force-remove another worktree without authorization.

Git worktrees let you check out multiple branches simultaneously in separate
directories, linked to the same repository.

## When to use

- Working on a feature while another branch is mid-rebase
- Running tests or builds on one branch while editing another
- Reviewing a PR locally without stashing your current work
- Hotfix on main while deep in a long-running feature branch

## Create a worktree

```bash
# From existing branch
git worktree add ../project-hotfix hotfix/critical

# New branch + checkout
git worktree add -b feature/new-thing ../project-feature main
```

## List worktrees

```bash
git worktree list
```

Output:

```bash
/path/to/main-repo       abc1234 [main]
/path/to/project-hotfix  def5678 [hotfix/critical]
/path/to/project-feature ghi9012 [feature/new-thing]
```

The current worktree is marked with `(bare)` or is the one you're in.

## Remove a worktree

Removal can discard uncommitted files; list worktrees and inspect status first. `--force` and `prune` require explicit authorization, and another worktree's state is `UNVERIFIED` until inspected.

```bash
# Prune the directory and unregister
git worktree remove ../project-hotfix

# Force remove (even with uncommitted changes)
git worktree remove --force ../project-hotfix

# Prune stale entries (directories already deleted manually)
git worktree prune
```

## Worktree with detached HEAD

```bash
git worktree add --detach ../project-review HEAD~3
```

Useful for building or testing an old commit.

## Lock and unlock

Prevent a worktree from being pruned:

```bash
git worktree lock ../project-hotfix --reason "CI build in progress"
git worktree unlock ../project-hotfix
```

## Limitations

- You can't check out the same branch in two worktrees
- Worktrees share the same `.git` object store (efficient, but `.git` in
each worktree is a link)
- Submodules must be initialized per worktree
- `.gitignore` and hooks are shared across all worktrees
- Bare repositories can't have worktrees added to them

## Cleanup pattern

```bash
# Remove all worktrees except current
git worktree list | awk 'NR>1 {print $1}' | xargs git worktree remove
```

## Sources

- Git Workflows source map (see `local-sources.md`) — Git worktree and hosted-boundary references.
- [Git worktree documentation](https://git-scm.com/docs/git-worktree) — current lifecycle semantics.
