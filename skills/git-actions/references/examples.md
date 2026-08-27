# GOOD/RED hosted API examples

Treat hosted input as untrusted and mutations as separately authorized effects. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Scoped read versus unchecked mutation

### GOOD

```diff
--- a/scripts/inspect-pr.sh
+++ b/scripts/inspect-pr.sh
@@
-gh api "$USER_URL" --method PATCH -f state=closed
+gh api "repos/$OWNER/$REPO/pulls/$NUMBER" \
+  --method GET --jq '{id,number,state,head:{sha}}'
+# A later mutation requires explicit target/effect authorization and verification.
```

### RED

```diff
--- a/scripts/inspect-pr.sh
+++ b/scripts/inspect-pr.sh
@@
+gh api "$INPUT_URL" --method PATCH -f state=closed
+# Caller-controlled URL and mutation; no target, permission, schema, or effect check.
```
