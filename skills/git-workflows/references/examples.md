# GOOD/RED local Git examples

Record recovery before history-changing operations and preserve unrelated work. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Reviewable commit slices

Plan each commit before staging it. Keep the staged paths or hunks explicit, and make the order and revert consequence visible to reviewers.

### GOOD

```text
# Plan: one coherent concern per commit; behavior/tests depend on the rename,
# generated output depends on its source, and docs/policy follow the behavior.
# Record that dependency and revert in the reverse dependency order when needed.
# 1. mechanical rename: src/old_name -> src/new_name; independently revertable.
git add -- src/old_name src/new_name
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "refactor: rename old name"
git commit -m "refactor: rename old name"

# 2. behavior: only the semantic implementation hunks.
git add -p -- src/new_name
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "feat: change behavior"
git commit -m "feat: change behavior"

# 3. tests: only the test files for the behavior slice.
git add -- tests/test_new_name.py
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "test: cover changed behavior"
git commit -m "test: cover changed behavior"

# 4. generated source and generated output: a dedicated slice.
git add -- generated/source generated/output
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "build: refresh generated source and output"
git commit -m "build: refresh generated source and output"

# 5. documentation: a separately reviewable and revertable slice.
git add -- docs/behavior.md
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "docs: describe the new behavior"
git commit -m "docs: describe the new behavior"

# 6. policy: a separately reviewable and revertable slice.
git add -- policy/behavior.md
git diff --cached --check && git diff --cached && git diff --cached --name-status
# Inspect proposed subject: "policy: record the new behavior"
git commit -m "policy: record the new behavior"
```

### RED

```text
# Valid-looking subject, but the staged diff mixes renames, behavior, tests,
# generated files, documentation, and policy with no explicit slice boundary.
git add -A
git commit -m "feat: update everything"
```

The RED catch-all is not reviewable or safely revertable merely because its subject follows a commit convention.

## Recovery before rebase

### GOOD

```diff
--- a/commands/rebase.txt
+++ b/commands/rebase.txt
@@
+git status --short
+git rev-parse HEAD > /tmp/head.before-rebase
+git branch backup/rebase-$(git rev-parse --short HEAD)
+git rebase origin/main
```

### RED

```diff
--- a/commands/rebase.txt
+++ b/commands/rebase.txt
@@
+git reset --hard origin/main
+git clean -fdx
+# Discards work and offers no recovery boundary.
```
