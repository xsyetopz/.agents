---
name: legacy-cleanup
description: Use this skill when removing obsolete aliases, shims, deprecated entrypoints, or compatibility paths after their consumers are gone; use $architecture-boundaries for an active migration or supported boundary redesign.
---

# Legacy Cleanup

Remove confirmed obsolete compatibility surfaces and every live route to them. Leave the supported replacement as the only active path.

Define the obsolete surface, replacement, consumers, public reach, retained history, and stop condition. Safe local search and edits may proceed. Deletion of shared, published, or externally owned paths requires authorization. Return removed paths, updated consumers, evidence, and unresolved reachability.

## Workflow

1. Read repository instructions, status, diff, the complete target, its owner and producer, and all consumers before editing.
2. Search exact names and structural forms for aliases, forwarding wrappers, shims, re-exports, deprecated commands, shadow packages, duplicate entrypoints, and stale paths.
3. Use the direct [removal workflow](references/removal-workflow.md) to classify each match and build a ledger of replacement, consumers, public reach, side effects, retained history, and ambiguity.
   - [GOOD/RED cleanup examples](references/examples.md) (read before removing an alias, shim, or deprecated entrypoint; RED marks a contrast, while GOOD is the cleanup pattern)
4. Stop when an active consumer, compatibility promise, generated owner, or replacement authority remains unresolved.
5. Remove the obsolete surface and update live imports, commands, tests, metadata, and inventory atomically; preserve release notes, migrations, source snapshots, and tests that still prove current behavior.
6. Re-run exact-name searches, focused consumer tests, repository-native checks, and final diff inspection; return removed paths, updated consumers, retained evidence, statuses, and unavailable runtime or external evidence as `UNVERIFIED`.

## Gotchas

- A cleanup request authorizes mutation only for the explicit repository and scope.
- Keyword matches can be active contracts, historical records, fixtures, external terms, or false positives.
- The canonical replacement must be live before removal; the resulting graph contains one supported path and no new alias, wrapper, fallback, re-export, or shadow path.
- Route active migration design to `$architecture-boundaries`, documentation history to `$repository-docs`, and skill-package structure to a dedicated skill-authoring workflow.
- Use established repository formats and canonical inputs; keep new output in existing repository-owned forms.
