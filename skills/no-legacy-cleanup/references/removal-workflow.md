# Removal workflow

## Candidate classes

| Class | Evidence | Action |
| --- | --- | --- |
| Live compatibility surface | A forwarding import, re-export, wrapper, fallback command, deprecated selector, duplicate package, or shadow path routes to a canonical implementation. | Remove only after every supported consumer and contract has moved. |
| Active contract | Current callers, public documentation, release policy, external integrations, or generated ownership still require the surface. | Stop. Plan an authorized migration instead of cleanup. |
| Historical evidence | Changelog entries, migration records, dated source snapshots, or release notes describe past behavior. | Retain unless exact removal is separately authorized. |
| Behavioral fixture | A test uses an old name or format to prove rejection, parsing, migration, or compatibility behavior. | Retain while the behavior remains required; rename only when the name itself is irrelevant. |
| External terminology | A platform or protocol calls a feature legacy, compatible, deprecated, or an alias. | Retain when it is accurate source material, not a repository route. |
| False positive | Ordinary words such as migration or alias do not create a reachable compatibility surface. | Record and leave unchanged. |

## Trace before removal

For each candidate, record:

- exact path, symbol, selector, command, or route;
- owner and canonical replacement;
- producer or generator, if any;
- imports, callers, documentation routes, tests, packaging metadata, and external reach;
- reads, writes, side effects, exit behavior, and failure behavior;
- evidence that the transition is complete;
- historical or behavioral records that must remain.

Use repository-native code search and relationship tools when available. Verify graph results in local source. Do not index, update, watch, clean, or delete a graph repository without explicit authority.

## Complete removal

1. Move remaining supported consumers to the canonical surface.
2. Remove the forwarding code, duplicate path, deprecated selector, or fallback.
3. Remove stale live documentation and inventory entries that still advertise it.
4. Update tests to exercise the canonical surface. Keep rejection and history fixtures when they still test current behavior.
5. Search again for the exact removed names and structural patterns.
6. Run focused consumer tests and repository-native checks.
7. Inspect the final diff. Reject any new wrapper, alias, fallback, custom schema, generated evidence file, or unrelated historical deletion.

If a supported consumer cannot move in the same authorized change, classify the cleanup as blocked and name the smallest decision or migration needed next.
