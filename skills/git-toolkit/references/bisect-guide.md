# Bisect Guide

Scope: local `git bisect` regression isolation. A good commit is known to pass and a bad commit is known to fail under the same reproducible test; missing or flaky evidence makes the result `UNVERIFIED`.

## Manual bisect

```bash
git bisect start
git bisect bad HEAD           # current commit has the bug
git bisect good v1.0.0        # this commit was fine

# Git checks out a midpoint. Test it:
# - If buggy: git bisect bad
# - If clean: git bisect good

# Repeat until git identifies the first bad commit.

git bisect reset              # return to original HEAD
```

## Automated bisect

```bash
git bisect start HEAD v1.0.0
git bisect run ./test-for-bug.sh
git bisect reset
```

The script must exit:

- `0` if the commit is good (no bug)
- `1-127` (excluding 125) if the commit is bad
- `125` if the commit can't be tested (skip it)

Example test script:

```bash
#!/bin/bash
# test-for-bug.sh
make clean && make || exit 125  # skip if can't build
./run-tests --only-failing      # exit 0 if tests pass, non-zero if fail
```

## Bisect by file path

Narrow bisect to changes affecting a specific path:

```bash
# Only blame commits that touched src/auth/
git bisect start - src/auth/
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test.sh
```

## Bisect log and replay

```bash
# Save bisect state
git bisect log > bisect-log.txt

# Replay later
git bisect replay bisect-log.txt
```

## Skip unbuildable commits

```bash
git bisect start HEAD v1.0.0
git bisect run sh -c '
  make || exit 125
  ./test
'
```

If `make` fails (exit non-zero), it's not 125, so the commit would be marked
bad. Must explicitly `exit 125` to skip.

## Visualize remaining range

```bash
git bisect visualize    # opens gitk showing the suspect range
```

## Practical tips

- Start wide, then narrow: `HEAD~100` first, then bisect within the found range
- Prefer automated bisect over manual - fewer mistakes
- Test script should be deterministic and fast
- If the bug is intermittent, run the test multiple times per commit
- Use `git bisect old` / `git bisect new` instead of `good`/`bad` for
non-regression searches (e.g., "when was this feature added?")

## Sources

- [Git Toolkit source map](sources.md) — Git reference and evidence limits.
- [Git reference](https://git-scm.com/docs) — bisect command semantics.
