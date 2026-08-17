---
name: no-legacy-cleanup
description: Evidence-based removal of obsolete aliases, shims, deprecated entrypoints, and compatibility paths after their consumers are gone.
---

# No Legacy Cleanup

Remove obsolete compatibility surfaces without deleting active contracts or historical evidence.

## Use this skill

- Remove an obsolete alias, forwarding wrapper, compatibility shim, deprecated command, shadow package, duplicate entrypoint, or stale migration path.
- Finish a rename or consolidation after the canonical replacement is live and remaining consumers must move atomically.
- Do not use to design an active migration, break a supported public contract, erase release history, or delete a fixture that still verifies required behavior.
- Redirect active boundary or migration design to `/skill:software-architecture`, documentation history to `/skill:repo-docs`, and skill package structure to `/skill:skill-creator`.

## Rules

- Treat a cleanup request as mutation authority only when the exact repository and scope are explicit.
- Inspect the artifact, owner, producer, consumers, imports, commands, tests, generated output, side effects, and source authority before removal.
- Classify each match as a live compatibility surface, active contract, historical record, test fixture, external term, or false positive. Do not delete by keyword alone.
- Remove the obsolete surface and every live route to it in one complete change. Do not replace it with another alias, wrapper, fallback, re-export, or shadow path.
- Preserve release notes, migration records, required evaluation manifests, source snapshots, and tests that still prove current behavior unless their removal is separately authorized and supported by evidence.
- Do not invent custom schema files or custom generated files as outputs. Use only established repository-owned formats and canonical inputs.

## Steps

1. Read repository instructions, current status and diff, the complete target, and all local consumers before editing.
2. Search exact names and structural forms for aliases, wrappers, re-exports, forwarding modules, deprecated commands, duplicate paths, and stale references.
3. Build a removal ledger with the canonical replacement, consumers, public reach, side effects, retained historical evidence, and unresolved ambiguity.
4. Stop if an active consumer, compatibility promise, generated owner, or replacement authority is unresolved.
5. Remove the confirmed obsolete surface and update live imports, commands, tests, package metadata, and inventory documents atomically.
6. Re-run exact-name searches, focused behavior tests, package checks, and repository-native checks. Inspect the final diff for unrelated deletions or a newly introduced fallback.

## Resources

- Start with the package [reference router](references/index.md).

## Verify

- Done means confirmed obsolete surfaces and their live routes are absent, canonical consumers pass, retained history is named, no replacement alias was added, and the final diff matches the authorized scope.
- Run `python3 scripts/check.py` from this package. Also run exact-name searches, focused consumer tests, and the target repository's native checks.
- Record removed paths, updated consumers, commands and exit statuses, retained historical evidence, and remaining ambiguity. Classify unavailable consumer, external, or runtime evidence as `UNVERIFIED`.
