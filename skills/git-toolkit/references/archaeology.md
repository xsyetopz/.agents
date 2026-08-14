# Git Archaeology

Scope: local Git history search and attribution using commits, refs, and path-limited inspection. A ref is a name pointing to an object; commands read the current checkout unless an explicit repository and revision are supplied. Do not infer authorship or intent from a matching line alone.

Finding when and why code changed. Not `git log` - the deep tools.

## Finding when a string was added or removed

### `git log -S` (pickaxe)

Finds commits that changed the number of occurrences of a string.

```bash
# When was this function first introduced?
git log -S "func authenticateUser" --source --all

# When was this error message removed?
git log -S "connection refused" --oneline

# Find commits that added or removed this import
git log -S "import React from" --oneline - '*.tsx'
```

`-S` looks at the diff of each commit. If the string's occurrence count changed
(added or removed), the commit is shown. This is not a grep of the file at that
point in history - it's specifically about when the string appeared or
disappeared from the diff.

### `git log -G` (regular expression pickaxe)

Like `-S` but with a regex pattern. Finds commits where the diff matches the
regex.

```bash
# Find commits that changed any error code pattern
git log -G "ERR_[A-Z_]+" --oneline

# Find when a TODO was added with a specific format
git log -G "TODO\(@\w+\)" --oneline

# Any commit that touched a line with a SQL injection pattern
git log -G "SELECT.*\+.*FROM" - '*.py'
```

## Tracking a function across moves and renames

### `git log -L` (line log / history of a code block)

Traces the evolution of a specific function or line range across file renames.

```bash
# Trace the history of main() - follows it across renames
git log -L :main:src/main.go

# Trace line range 100-120 of a file
git log -L 100,120:src/auth.go

# Trace a regex-matched function
git log -L '/func handleRequest/:/^}/':src/server.go
```

### `git blame` with move detection

```bash
# Standard blame
git blame src/auth.go

# Detect lines moved from other files
git blame -M src/auth.go

# Detect lines moved or copied from other commits
git blame -C -C -C src/auth.go

# Ignore whitespace changes (find the real author, not the reformatter)
git blame -w src/auth.go

# Show the commit that last touched a specific line range
git blame -L 100,150 src/auth.go
```

## Finding deleted files

```bash
# List all deleted files
git log --diff-filter=D --summary | grep delete

# Find the last commit that had a deleted file
git log --all --full-history - '**/deleted-file.go'

# Show the contents of a file before it was deleted
git show <commit-hash>^:path/to/deleted-file.go

# Restore a deleted file
git checkout <commit-hash>^ - path/to/deleted-file.go
```

## Finding file history across renames

```bash
# Follow a file through renames
git log --follow -p - path/to/current-name.go

# Show the rename in the log
git log --follow --name-status - path/to/file

# Find all names a file has had
git log --follow --format='%H' - path/to/file | \
  tail -1 | xargs git diff-tree --no-commit-id --name-only -r
```

## Finding the commit that introduced a bug (manual bisect target)

```bash
# Find when a file first appeared
git log --diff-filter=A - 'path/to/file'

# Find the last commit that touched a line
git log -n 1 -L 42,42:path/to/file

# Find when a test started failing
git log -S "test_that_fails" - '**/*_test.*'

# Find commits around a specific date that touched a file
git log --after="2024-06-01" --before="2024-06-15" - path/to/file
```

## Bulk archaeology - finding patterns across history

```bash
# All commits that removed a TODO
git log --all --oneline -S "TODO" --diff-filter=M

# Commits where a specific person changed a specific directory
git log --author="Jane" - 'src/auth/**'

# Commits with "fix" in the message, touching test files
git log --all --grep="fix" - '**/*_test.*'

# The five biggest commits by line count
git log --format='%H' | while read hash; do
  git diff --shortstat "$hash^" "$hash" 2>/dev/null
done | sort -t',' -k2 -rn | head -5
```

## Preventing archaeology breakage

Common practices that break `git blame` and `git log -S`:

1. **Mass reformatting commits.** A single commit that reformats the entire
codebase destroys blame. Use `.git-blame-ignore-revs`:

   ```bash
   # .git-blame-ignore-revs - list of commits to skip during blame
   abc1234567890def  # Reformat with Prettier
   def0987654321abc  # Migrate to tabs

   # Configure git to use it:
   git config blame.ignoreRevsFile .git-blame-ignore-revs
   ```

2. **Moving files without `git mv`.** Git's rename detection is heuristic.
Use `git mv` for moves. If mass-moving, make it a single commit with nothing
else so the rename detection has maximum signal.

3. **Squashing unrelated changes.** A squash merge that combines a refactor
with a new feature in one commit makes it impossible to bisect to the precise
change that caused a regression.

## Sources

- [Git Toolkit source map](sources.md) — Git reference and hosted-boundary sources.
- [Git reference](https://git-scm.com/docs) — current command semantics.
