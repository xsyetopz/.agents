# Patch Workflows

## Creating patches

### format-patch

```bash
# Create patches for the last 3 commits
git format-patch -3

# Create patches for commits on this branch since main
git format-patch main

# With a custom output directory
git format-patch -o patches/ main

# Single-file patch per commit, with thread
git format-patch --stdout main > all-commits.patch
```

Output files: `0001-commit-subject.patch`, `0002-commit-subject.patch`, etc.

### Creating a diff patch (uncommitted changes)

```bash
git diff > changes.patch
git diff --staged > staged-changes.patch
```

## Applying patches

### git am (from format-patch)

```bash
# Apply a single patch (creates a commit)
git am 0001-fix-bug.patch

# Apply all patches in a directory
git am patches/*.patch

# Apply with patch file from stdin
git am < 0001-fix-bug.patch
```

`git am` preserves the original author, date, and message.

### git apply (from git diff)

```bash
# Apply without committing
git apply changes.patch

# Show what would be applied
git apply --stat changes.patch

# Check if it applies cleanly (dry run)
git apply --check changes.patch

# Apply in reverse (undo)
git apply --reverse changes.patch
```

### Handling failed applies

```bash
# am - resolve conflicts
git am 0001-fix-bug.patch
# (conflict)
# Resolve conflicts, then:
git add resolved-files
git am --continue

# Skip a patch
git am --skip

# Abort
git am --abort

# apply with fallback to 3-way merge
git apply --3way changes.patch
```

## Cherry-pick

```bash
# Single commit
git cherry-pick abc1234

# Range of commits (exclusive start, inclusive end)
git cherry-pick abc1234..def5678

# Cherry-pick without committing
git cherry-pick -n abc1234

# Edit the commit message
git cherry-pick -e abc1234

# Cherry-pick a merge commit
git cherry-pick -m 1 abc1234
```

`-m 1` picks the first parent's changes (usually the branch you merged into).

Conflicts during cherry-pick: resolve, then `git cherry-pick --continue`. Or
abort: `git cherry-pick --abort`.

## When to use which

| Scenario | Tool |
| --- | --- |
| Send commits for review (preserves author) | `format-patch` -> `am` |
| Share uncommitted WIP | `diff` -> `apply` |
| Grab a specific commit from another branch | `cherry-pick` |
| Backport a fix to a release branch | `cherry-pick` |
| Apply a PR from a fork without the fork remote | `.patch` URL -> `am` |

## GitHub PR patches

Every PR has a `.patch` and `.diff` URL:

```bash
# Download PR as patch (preserves commits)
curl -sSL https://github.com/owner/repo/pull/42.patch | git am

# Download PR as diff (single squashed diff)
curl -sSL https://github.com/owner/repo/pull/42.diff | git apply
```
