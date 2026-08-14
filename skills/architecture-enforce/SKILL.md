---
name: architecture-enforce
description: architecture enforcement, topology refactors, ownership boundaries, file shattering, three-plus sibling changes.
---

# Architecture Enforce

Turn architecture policy into repository evidence and blocking checks while
preserving behavior unless a requested migration explicitly changes it.

## When to use

- Change packages, directories, modules, schemas, APIs, tests, generated boundaries, or three or more sibling files.
- Review file shattering, flat folders, filename colonies, helper/manager proliferation, cycles, or ownership drift.
- Migrate build graphs, deployables, languages, storage, protocols, or public contracts.
- Audit lint, test, architecture, or CI suppression that hides failures.

## When NOT to use

- A tiny edit with no topology, ownership, contract, boundary, or build-graph effect.
- Architecture ideation before a target structure is selected; use `$architecture-design`.
- Generated output edits when the canonical generator input is available.

## Guardrails

- Read repository instructions, owning code, callers, tests, build configuration, and public contracts before editing.
- Assign each changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it cannot be consolidated.
- Prefer cohesive capability modules over one-type, one-operation, phase, helper, validation, or filename-prefix colonies.
- Inventory tracked, modified, staged, and non-ignored untracked authored source; tracked files remain auditable.
- Every warning and error blocks. Never add ignores, exclusions, advisory modes, allow-failure, lower thresholds, or weakened tests.
- Change canonical generator inputs; do not hand-edit generated output.

## Workflow

1. Run capability discovery and inventory Git state, source candidates, manifests, tests, generators, and public surfaces.
2. Complete topology and dependency maps with path, owner, reason, visibility, lifecycle, dependencies, and why separate.
3. State the owning cause, target structure, preserved contracts, migration order, and rollback boundary.
4. Implement through cohesive package-local slices and preserve public entrypoints.
5. Run focused tests, the production/integration entrypoint, the full audit, provider queries, and final diff inspection.
6. Resolve every diagnostic at its owning cause; if a checker is wrong, preserve the failing gate and report a reproducer.

## Quick start

From this package directory:

```sh
python3 scripts/check.py
python3 scripts/providers.py capabilities --root . --format json
python3 scripts/audit_architecture.py . --format json
```

Run capability discovery before editing and the full audit after editing. Keep
the output and changed-path inventory as evidence; a static package PASS does not
claim that a target repository is architecturally clean.

## Reference map

- [Reference map](references/index.md) — route trigger keywords to focused material.
- [Core principles](references/principles.md) — ownership, boundaries, quality scenarios, and fail-closed checks.
- [Naming and fragmentation](references/naming.md) — detect file shattering and categorical decomposition.
- [Language conventions](references/languages.md) — map idioms to package-owned boundaries.
- [Testing](references/testing.md) — place tests and preserve executable contracts.
- [Toolchains](references/toolchains.md) — identify canonical build and generator owners.
- [Audit tooling](references/audit-tooling.md) — configure and interpret providers.
- [Verification](references/verification.md) — run evidence-producing acceptance gates.
- [Patterns](references/pattern-catalog.md) — compare structural options.
- [Examples](references/examples.md) — apply the topology table to concrete changes.
- [Sources](references/sources.md) — consult primary conventions and tool docs.

## Completion

Complete only when contracts are preserved or explicitly migrated, every changed
path has a durable owner, focused and integration checks pass, the full audit has
zero warnings/errors, and the diff contains no suppression bypass. Report exact
commands, exit codes, findings, and remaining risk.

## Validation

Run from this package directory:

```sh
python3 scripts/check.py
python3 scripts/providers.py capabilities --root . --format json
python3 scripts/audit_architecture.py . --format json
```

Then run the relevant package tests (`test_audit_cli.py`, `test_suppressions.py`,
provider tests, and façade tests). Do not treat capability discovery or static
metadata validation as a substitute for the full audit.

## Related skills

- `$architecture-design` — select and document the target structure first.
- `$repo-governance` — persist ownership and repository policy.
- `$git-ci-cd` — enforce architecture gates in pipelines.
