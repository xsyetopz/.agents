# Stash Guide

Scope: local stash creation, application, deletion, and recovery. A stash is local work-in-progress state; inspect its contents and target branch before applying or dropping it, and never clear all stashes without explicit authorization.

## Why stash

Stash captures uncommitted changes - both staged and unstaged - and reverts
the working tree to HEAD. It's for temporary work-in-progress that you don't
want to commit yet.

## Core operations

```bash
git stash                    # stash everything (tracked files only)
git stash pop                # apply latest stash + drop it
git stash apply              # apply latest stash, keep it
git stash drop               # discard latest stash
git stash list               # show all stashes
```

## Named stashes

```bash
git stash push -m "wip: refactoring auth module"
git stash list
# stash@{0}: On feature/auth: wip: refactoring auth module
git stash pop stash@{0}
```

## Stash untracked or ignored files

```bash
git stash push -u            # include untracked files
git stash push -a            # include untracked + ignored files
```

## Partial stash (only some files)

```bash
git stash push path/to/file1 path/to/file2
git stash push -m "only config changes" config/*.yaml
```

## Stash staged changes only

```bash
git stash push --staged      # stash ONLY staged changes, leave unstaged alone
```

## Keep index (staged files remain staged)

```bash
git stash push --keep-index  # stash unstaged changes, keep staged
```

Useful when you've staged some work and want to test without the unstaged noise.

## Create a branch from a stash

```bash
git stash branch my-recovered-work stash@{0}
```

Creates a new branch from the stash's parent commit, applies the stash, and
drops it. This is the safest way to recover a stash that no longer applies
cleanly.

## Show stash contents

```bash
git stash show -p stash@{0}        # full diff
git stash show --stat stash@{0}    # summary only
```

## Clear all stashes

`git stash clear` is irreversible for locally reachable stash refs. List and inspect stashes, obtain explicit authorization, and report recovery evidence as `UNVERIFIED` if reflog or object inspection was not run.

```bash
git stash clear
```

Irreversible. Use `git stash list` first to confirm.

## Stash workflows

### Quick context switch

```bash
git stash push -m "wip"
git checkout other-branch
# ... work ...
git checkout original-branch
git stash pop
```

### Test without uncommitted changes

```bash
git stash push --keep-index --include-untracked
./run-tests
git stash pop
```

### Move work to a new branch

```bash
git stash push -m "half-done feature"
git checkout -b feature/new-approach main
git stash pop
```

## Recovery

Stashes live in `.git/refs/stash`. If you accidentally drop one, check:

```bash
git fsck --unreachable | grep commit | cut -d' ' -f3 | xargs git log --merges --no-walk --grep='WIP on'
```

Or use `git reflog show stash` if refs/stash history is available.

## Sources

- [Git Workflows source map](sources.md) — Git recovery and hosted-boundary references.
- [Git stash documentation](https://git-scm.com/docs/git-stash) — current stash semantics.
