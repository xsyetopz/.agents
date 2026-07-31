---
name: git-toolkit
description: Use for advanced local git operations beyond basic commit/push - interactive rebase, bisect, worktree, reflog recovery, stash workflows, submodule management, git-lfs, hooks, commit signing, patch manipulation, and repository archaeology. Do not use for platform APIs or CI/CD pipelines.
---

# Git Toolkit

Advanced git operations for power users. Every command should be understood
before it runs - git is destructive only when used without understanding.
Prefer `git reflog` as your undo safety net.

## When to use

- Interactive rebase: squashing, reordering, splitting, or dropping commits
- Bisecting to find the commit that introduced a bug
- Managing multiple worktrees for parallel feature branches
- Recovering lost commits or branches via reflog
- Stash workflows beyond `git stash pop` - partial stashes, named stashes,
  branch-from-stash
- Submodule updates, recursive operations, and migration to subtrees
- Git LFS setup, migration, and troubleshooting
- Git hooks: client-side (`pre-commit`, `commit-msg`) and server-side
- Commit signing with GPG or SSH keys
- Patch manipulation: `format-patch`, `am`, `apply`, `cherry-pick` ranges
- Repository archaeology: `blame`, `log -S`, `log -G`, `bisect` with scripts

## When NOT to use

- Basic `git add`, `git commit`, `git push` - use `git` directly
- GitHub/GitLab API operations - use `git-actions`
- CI/CD pipeline authoring - use `git-ci-cd`

## Quick start

1. **Before any destructive operation**, confirm `git status` is clean or
   intentionally dirty.
2. **Before rewriting history**, note the current HEAD: `git rev-parse HEAD`.
3. **If something goes wrong**, reach for `git reflog` first - it records every
   HEAD change for 90 days.
4. **When in doubt about a command's effect**, run it with `--dry-run` if
   supported, or explain it to the user before executing.

## Guardrails

This skill is strict and guarded. Commands are classified into three tiers.
Never downgrade a tier without explicit user approval. Full details with real
tool references in `references/tooling.md`.

Sources: [Git security best practices](https://dev.to/prankurpandeyy/git-
security-best-practices-for-keeping-your-code-safe-1nep), [git-
guardrails](https://git-guardrails.readthedocs.io/en/latest/), [pre-
commit](https://github.com/pre-commit/pre-commit),
[gitleaks](https://github.com/gitleaks/gitleaks), [git-filter-
repo](https://github.com/newren/git-filter-repo).

### Tier 1 - SAFE (run freely)

Read-only operations and reversible local changes:

- `git status`, `git log`, `git diff`, `git show`
- `git stash push`, `git stash pop`, `git stash apply`
- `git worktree add`, `git worktree list`, `git worktree remove`
- `git bisect start/reset` (read-only until you mark good/bad)
- `git reflog`, `git branch -l`, `git tag -l`
- `git format-patch`, `git cherry-pick` (no conflicts)
- `git submodule update --init`

### Tier 2 - CAUTION (explain consequence, then run)

Operations that modify local history or working state. Explain what will happen
in one sentence before executing:

- `git rebase -i`, `git rebase --onto`
- `git reset --soft`, `git reset --mixed`
- `git commit --amend` (on unpushed commits only)
- `git stash drop`, `git stash clear`
- `git cherry-pick` (with possible conflicts)
- `git submodule deinit`, `git rm` submodule
- `git lfs migrate import`

### Tier 3 - BLOCKED (require explicit user confirmation)

Operations that mutate shared history, destroy local data, or affect remotes.
Stop and ask for confirmation before running. Never proceed without the user's
explicit approval:

- `git push --force`, `git push --force-with-lease`, `git push --delete`
- `git reset --hard` (any context - too easy to lose work)
- `git clean -fd`, `git clean -fdx`, `git clean -xdf`
- `git branch -D`, `git branch -d` (on non-merged branches)
- `git commit --amend` on already-pushed commits
- `git rebase` on a branch that has been pushed
- `git filter-branch`, `git filter-repo`, BFG Repo Cleaner
- `git lfs migrate import --everything`
- `git stash clear` (all stashes)

### Pre-operation checklist

Before any Tier 2 or Tier 3 operation:

1. Print `git status --short` and `git branch --show-current`
2. Save HEAD: `HEAD_BACKUP=$(git rev-parse HEAD)`
3. If rewriting history, confirm the branch has no unpushed changes on remote:
`git fetch && git log --oneline origin/$(git branch --show-current)..HEAD`
4. After the operation, verify with `git status`

## Command catalog

### Interactive rebase

```bash
# Squash last 3 commits
git rebase -i HEAD~3

# Rebase onto main, preserving merges
git rebase -i --rebase-merges main

# Autosquash fixup/squash commits
git rebase -i --autosquash main
```

### Bisect

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out a midpoint commit - test it
git bisect good  # or: git bisect bad
# Repeat until the offending commit is found
git bisect reset
```

### Worktree

```bash
# Create a new worktree for a feature branch
git worktree add ../repo-feature feature-branch

# List worktrees
git worktree list

# Remove a worktree
git worktree remove ../repo-feature
```

### Stash workflows

```bash
# Stash with a name
git stash push -m "wip: refactoring auth module"

# Stash only untracked files
git stash push -u -m "untracked config files"

# Apply a stash without dropping it
git stash apply stash@{1}

# Create a branch from a stash
git stash branch recovered-work stash@{0}
```

### Reflog recovery

```bash
# View reflog
git reflog --date=iso

# Recover a "lost" commit
git checkout -b recovery-branch <commit-hash>

# Recover after a bad reset
git reset --hard HEAD@{1}
```

### Submodules

```bash
# Update all submodules recursively
git submodule update --init --recursive

# Pull latest for all submodules
git submodule foreach git pull origin main

# Deinit and remove a submodule
git submodule deinit -f path/to/submodule
git rm path/to/submodule
```

## Reference map

| If you need to... | Load |
|---|---|
| Interactive rebase strategies and fixup workflows | `references/rebase-guide.md` |
| Bisect with automated test scripts | `references/bisect-guide.md` |
| Worktree patterns for parallel development | `references/worktree-guide.md` |
| Stash tricks and recovery patterns | `references/stash-guide.md` |
| Reflog recovery and lost commit archaeology | `references/reflog-guide.md` |
| Submodule and git-lfs management | `references/submodule-lfs.md` |
| Git hooks: client-side and server-side | `references/hooks-guide.md` |
| Commit signing with GPG and SSH | `references/signing-guide.md` |
| Patch workflows: format-patch, am, cherry-pick | `references/patch-guide.md` |
| Security tooling: gitleaks, pre-commit, git-filter-repo | `references/tooling.md` |
| Team git configuration (`.gitconfig`) | `references/gitconfig.md` |
| File attributes (`.gitattributes`): EOL, diff, merge | `references/gitattributes.md` |
| Deep history search: pickaxe, blame, line log | `references/archaeology.md` |
| Release management: semver, tags, release branches | `references/release-management.md` |

## Related skills

- `git-actions` - GitHub/GitLab API, release fetching, repository management
- `git-ci-cd` - CI/CD pipeline design, workflow syntax, job debugging

## Validate

```sh
python3 scripts/validate_skill.py skills/git-toolkit
```
