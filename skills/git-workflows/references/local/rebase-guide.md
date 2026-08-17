# Interactive Rebase Guide

Scope: local history rewriting with rebase, interactive editing, conflict resolution, and abort/recovery. Rebase changes commit identities; record the original `HEAD`, preserve a recovery ref, and do not force-push without explicit authorization.

## Core operations

### Squash commits

```bash
git rebase -i HEAD~4
```

In the editor, change `pick` to `squash` (or `s`) for commits to merge into the
previous one.

```text
pick abc1234 Add feature
squash def5678 Fix typo
squash ghi9012 Address review
pick jkl3456 Add tests
```

Result: the first commit absorbs the next two.

### Fixup workflow

```bash
# Make a fixup commit (for the previous commit)
git commit --fixup HEAD

# Later, autosquash during rebase
git rebase -i --autosquash HEAD~5
```

`fixup` commits are squashed and their message is discarded. `squash` commits
are squashed and their message is kept for editing.

### Reorder commits

In the interactive editor, move lines up or down. The commits are replayed in
the new order.

### Split a commit

Mark the commit with `edit` (or `e`):

```bash
# During rebase, when stopped at the target commit
git reset HEAD^
git add file1 file2
git commit -m "Part one"
git add file3 file4
git commit -m "Part two"
git rebase --continue
```

### Drop a commit

Change `pick` to `drop` (or `d`), or delete the line entirely.

## Reword a commit message

Change `pick` to `reword` (or `r`). The rebase stops so you can edit the
message.

## Rebase onto main

```bash
# Standard
git rebase main

# Interactive with merge preservation
git rebase -i --rebase-merges main

# Rebase only the commits on this branch
git rebase -i --onto main HEAD~5
```

## Conflict resolution

```bash
# During a conflict
git status                    # see conflicted files
# Resolve conflicts in editor
git add resolved-files
git rebase --continue

# Skip a commit entirely
git rebase --skip

# Abort the rebase
git rebase --abort
```

## Safety

- Always know `HEAD` before starting: `git rev-parse HEAD`
- If something goes wrong, `git reflog` shows every step
- `git rebase --abort` restores pre-rebase state
- Rebase only unpushed commits on shared branches
- `git push --force-with-lease` after rebase, not `--force`

## Sources

- [Git Workflows source map](sources.md) — Git history and hosted-boundary sources.
- [Git rebase documentation](https://git-scm.com/docs/git-rebase) — current rebase semantics.
