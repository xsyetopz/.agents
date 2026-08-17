# Git Configuration

Scope: local Git configuration precedence and safety settings. Common Vulnerabilities and Exposures (CVE) identifiers in examples identify a published issue; they do not prove that a local installation is affected. A configuration key may come from system, global, local, command, or worktree scope; inspect the effective value before changing it, and do not assume hosted policy follows local config.

Team-wide git configuration patterns. Git reads config from four places in order
of increasing precedence. Source: `git-config(1)` man page.

## Config hierarchy

| Level | Path | Scope |
| --- | --- | --- |
| System | `/etc/gitconfig` | All users on the machine |
| Global | User-level config (path reported by Git) | Current user, all repos |
| Local | `.git/config` | This repo only |
| Worktree | `.git/config.worktree` | This worktree only |

Higher precedence overrides lower. Use `git config --list --show-origin` to see
where each value comes from.

## Team-shared configuration

Git does not natively support a "project config" that commits to the repo. The
workaround: commit a setup script that applies settings. Treat that script as reviewable code: global settings persist outside the repository and require explicit approval before execution.

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

The following Git settings are local safety guidance; verify the effective scope
and repository policy before changing them:

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
# In the user-level config, replace `/path/to` with each repository root:
[includeIf "gitdir:/path/to/work/"]
    path = /path/to/gitconfig-work

[includeIf "gitdir:/path/to/personal/"]
    path = /path/to/gitconfig-personal
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

## Sources

- [Git Workflows source map](sources.md) — Git reference and hosted-boundary sources.
- [Git configuration documentation](https://git-scm.com/docs/git-config) — current precedence and key semantics.
