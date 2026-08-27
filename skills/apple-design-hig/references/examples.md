# GOOD/RED implementation examples

Use the smallest native control that preserves semantics, discoverability, and accessibility. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Native action and accessibility

### GOOD

```diff
--- a/DeleteView.swift
+++ b/DeleteView.swift
@@
-Image(systemName: "trash")
+Button("Delete", systemImage: "trash", role: .destructive) { delete() }
+    .accessibilityHint("Removes this item")
```

### RED

```diff
--- a/DeleteView.swift
+++ b/DeleteView.swift
@@
+Image(systemName: "trash")
+    .onTapGesture { delete() }
+    // No button semantics, label, role, keyboard/focus behavior, or HIG evidence.
```
