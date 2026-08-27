# GOOD/RED cleanup examples

Remove only a confirmed obsolete surface after proving replacement, consumers, and public reach. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Alias removal

### GOOD

```diff
--- a/cleanup-ledger.md
+++ b/cleanup-ledger.md
@@
+- old_cmd: no live consumers; replacement: new_cmd; public reach: internal; rollback: revert commit
--- a/bin/old_cmd
+++ /dev/null
@@
-exec new_cmd "$@"
```

### RED

```diff
--- a/bin/old_cmd
+++ b/bin/old_cmd
@@
+exec new_cmd "$@"
+# Kept as an unclassified permanent shim; consumer and compatibility status unknown.
```
