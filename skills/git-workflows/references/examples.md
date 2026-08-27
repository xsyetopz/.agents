# GOOD/RED local Git examples

Record recovery before history-changing operations and preserve unrelated work. **RED** is a contrast for review; use GOOD as the implementation pattern.

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
