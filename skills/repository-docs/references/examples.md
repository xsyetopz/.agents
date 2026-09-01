# GOOD/RED documentation and governance examples

Tie claims to canonical source and give rules an owner and observable enforcement. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Sourced claim and enforced rule

### GOOD

```diff
--- a/README.md
+++ b/README.md
@@
-Deploys are always safe.
+Deploys run the required checks in `.github/workflows/release.yml`; verify the current workflow before changing this claim.
--- a/CODEOWNERS
+++ b/CODEOWNERS
@@
+/.github/workflows/ @release-maintainers
```

### RED

```diff
--- a/README.md
+++ b/README.md
@@
+Deploys are always safe and every change is reviewed.
```

The RED claim has neither bounded source truth nor evidence of enforcement.
