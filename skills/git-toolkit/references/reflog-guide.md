# Reflog Guide

The reflog records every change to HEAD and branch tips. It's your undo safety
net - commits are not truly lost until the reflog expires (default 90 days).

## View reflog

```bash
git reflog                    # HEAD reflog
git reflog --date=iso         # with ISO timestamps
git reflog show main          # specific branch reflog
git reflog --all              # all refs
```

## Recover after a bad reset

```bash
# You did: git reset --hard HEAD~5
# You lost commits. But reflog remembers.

git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~5
# def5678 HEAD@{1}: commit: Important work
# ...

git reset --hard HEAD@{1}     # back to the commit before the reset
```

## Recover a deleted branch

```bash
# You did: git branch -D feature/experiment
# Find the last commit:

git reflog --all | grep feature/experiment
# ghi9012 feature/experiment@{0}: branch: Created from HEAD

git checkout -b feature/experiment ghi9012
```

## Recover after a bad rebase

```bash
# Rebase went wrong, but you haven't done anything else since.

git reflog
# jkl3456 HEAD@{0}: rebase (finish): ...
# mno7890 HEAD@{1}: rebase (start): ...
# pqr1234 HEAD@{2}: commit: Work before rebase

git reset --hard HEAD@{2}     # back to pre-rebase state
```

## Undo a commit (not just the message)

```bash
# After git commit --amend or a bad commit
git reset --soft HEAD@{1}     # keep changes staged
git reset --mixed HEAD@{1}    # keep changes unstaged (default)
git reset --hard HEAD@{1}     # discard changes entirely
```

## Find dangling commits

```bash
# Commits not reachable from any ref
git fsck --lost-found
# Shows "dangling commit <hash>" entries

# Inspect one
git show <hash>

# Recover it
git branch recovered-work <hash>
```

## Expiration

- Default: 90 days for unreachable objects, 30 days for reachable objects
- Reflog expires entries, not the underlying objects
- Once expired, commits with no other ref become true dangling objects - still
  recoverable via `git fsck --lost-found` until garbage collection

```bash
# View expiration config
git config gc.reflogExpire       # default 90 days
git config gc.reflogExpireUnreachable  # default 30 days
```

## Practical habits

1. Before any history rewrite, note where you are: `git rev-parse HEAD`
2. After a mistake, go to reflog first - don't panic-`reset`
3. `HEAD@{1}` means "where HEAD was one step ago"
4. `HEAD@{5.minutes.ago}` and `HEAD@{yesterday}` are also valid
5. For absolute safety: `git branch backup-before-risky-operation HEAD`
