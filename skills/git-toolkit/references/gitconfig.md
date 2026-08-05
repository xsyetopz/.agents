# Git Configuration

## Use this reference

Load this reference when gitconfig is part of the requested local Git state transition. Inspect current status and history first, preserve unrelated work, identify recovery, and verify the resulting state.

Team-wide git configuration patterns. Git reads config from four places in order
of increasing precedence. Source: `git-config(1)` man page.

## Config hierarchy

| Level | Path | Scope |
| --- | --- | --- |
| System | `/etc/gitconfig` | All users on the machine |
| Global | `~/.gitconfig` | Current user, all repos |
| Local | `.git/config` | This repo only |
| Worktree | `.git/config.worktree` | This worktree only |

Higher precedence overrides lower. Use `git config --list --show-origin` to see
where each value comes from.

## Team-shared configuration

Git does not natively support a "project config" that commits to the repo. The
workaround: commit a setup script that applies settings.

### Approach 1: Setup script (recommended)

```bash
#!/bin/bash
# scripts/git-setup.sh - run once after clone

git config core.autocrlf input
git config pull.rebase true
git config push.default current
git config push.useForceIfIncludes true
git config commit.gpgsign true
git config core.hooksPath .githooks
```

### Approach 2: Makefile target

```makefile
.PHONY: git-setup
git-setup:
 git config core.autocrlf input
 git config pull.rebase true
 git config push.default current
 git config core.hooksPath .githooks
```

## Security-critical settings

From [dev.to Git security best practices](https://dev.to/prankurpandeyy/git-security-best-practices-for-keeping-your-code-safe-1nep):

```bash
# Force push only if local tracking branch matches remote
# Prevents overwriting someone else's pushed work
git config --global push.useForceIfIncludes true

# Push only the current branch, not all branches
# Prevents accidentally pushing WIP branches
git config --global push.default current

# Prevent Git from running commands in directories owned by
# a different user (CVE-2022-24765 mitigation)
git config --global safe.directory /path/to/repo

# Require GPG signature verification on merge and pull
git config --global merge.verifySignatures true
git config --global pull.verifySignatures true
```

## Workflow-critical settings

```bash
# Always rebase on pull, never create merge commits
# Critical for linear history workflows
git config pull.rebase true

# Autostash before rebase - prevents "cannot rebase: you have
# unstaged changes" errors
git config rebase.autoStash true

# Auto-squash fixup commits during interactive rebase
git config rebase.autoSquash true

# Prune deleted remote branches on fetch
git config fetch.prune true
git config fetch.pruneTags true

# Set default branch name for new repos (GitHub default is main)
git config --global init.defaultBranch main
```

## Diff and merge settings

```bash
# Better diff algorithm - patience or histogram produce cleaner
# output for code, especially across moved blocks
git config diff.algorithm histogram

# Color in diffs, status, branch listing
git config color.ui auto

# Use a three-way merge conflict style - shows base, ours, theirs
git config merge.conflictstyle zdiff3

# Automatically resolve known conflicts (e.g. generated files)
# git config rerere.enabled true
```

## Commit template

```bash
# Team-wide commit message template
git config commit.template .gitcommit-template
```

`.gitcommit-template`:

```bash
# <type>(<scope>): <subject>
# |<----  Using a Maximum Of 72 Characters ---->|

# Explain why this change is being made.

# Type: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert
# Scope: the module or component being changed
```

## Conditional includes

Apply different config based on directory path. Useful for work/personal repo
separation:

```gitconfig
# ~/.gitconfig
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work

[includeIf "gitdir:~/personal/"]
    path = ~/.gitconfig-personal
```

## Audit script

```bash
#!/bin/bash
# scripts/git-audit-config.sh - verify required settings

required=(
  "pull.rebase true"
  "push.default current"
  "push.useForceIfIncludes true"
  "core.hooksPath .githooks"
)

for setting in "${required[@]}"; do
  key="${setting% *}"
  expected="${setting#* }"
  actual="$(git config "$key")"
  if [ "$actual" != "$expected" ]; then
    echo "MISSING: git config $key $expected (current: $actual)"
  fi
done
```
