---
name: architecture-enforce
description: architecture enforcement, topology refactors, ownership boundaries, file shattering, three-plus sibling changes.
---

# Architecture Enforce

Turn architecture policy into repository evidence and blocking checks while
preserving behavior unless a requested migration explicitly changes it.

## Use this skill

Use this skill when changing or auditing packages, directories, modules, schemas,
APIs, tests, generated boundaries, build graphs, deployables, languages,
storage, protocols, public contracts, or three or more sibling files. Use it for
file shattering, flat folders, filename colonies, helper or manager
proliferation, dependency cycles, ownership drift, and lint, test, architecture,
or CI suppressions.

Do not use it for an isolated formatting or comment edit, architecture ideation
before a target is selected (use `$architecture-design`), or generated output
when the canonical generator input is available.

## Rules

- Read repository instructions, owning code, callers, tests, build configuration, generators, and public contracts before editing.
- Assign every changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate.
- Prefer cohesive capability modules over one-type, one-operation, phase, helper, validation, or filename-prefix colonies.
- Inventory tracked, modified, staged, and non-ignored untracked authored source; keep tracked files auditable.
- Every warning and error blocks. Never add ignores, exclusions, advisory modes, allow-failure paths, lower thresholds, or weakened tests.
- Change canonical generator inputs; do not hand-edit generated output.
- Preserve public entrypoints and contracts unless the migration explicitly records the change, migration order, rollback boundary, and verification.

## Steps

1. Run capability discovery and inventory Git state, source candidates, manifests, tests, generators, and public surfaces.
2. Complete topology and dependency maps with path, owner, responsibility, reason, visibility, lifecycle, dependencies, and why each path remains separate.
3. State the owning cause, target structure, preserved contracts, candidate comparison, migration order, rollback boundary, and evidence plan.
4. Implement through cohesive package-local slices while preserving public entrypoints and canonical generator ownership.
5. Run focused tests, the production or integration entrypoint, the full audit, provider queries, and final diff inspection.
6. Resolve each diagnostic at its owning cause. If a checker is wrong, preserve the failing gate and report a reproducer instead of weakening it.

## Resources

Route only the material needed for the audit:

- [Reference index](references/index.md) — trigger-to-reference routing.
- [Core principles](references/principles.md) — ownership, boundaries, quality scenarios, and fail-closed checks.
- [Naming and fragmentation](references/naming.md) — file shattering and categorical decomposition.
- [Language conventions](references/languages.md) — ecosystem boundaries and naming authority.
- [Testing](references/testing.md) — test placement and executable contracts.
- [Toolchains](references/toolchains.md) — build and generator ownership.
- [Audit tooling](references/audit-tooling.md) — providers and audit interpretation.
- [Verification](references/verification.md) — evidence-producing acceptance gates.
- [Pattern catalog](references/pattern-catalog.md) — structural alternatives and tradeoffs.
- [Examples](references/examples.md) — topology tables and migrations.
- [Authority sources](references/sources.md) — primary conventions and tool documentation.
- `$architecture-design` — select and document the target structure first; `$repo-governance` — persist ownership and repository policy; `$git-ci-cd` — enforce architecture gates in pipelines.

## Verify

Run from this package directory:

```sh
python3 scripts/check.py
python3 scripts/providers.py capabilities --root . --format json
python3 scripts/audit_architecture.py . --format json
```

Then run the relevant package tests, including `test_audit_cli.py`,
`test_suppressions.py`, provider tests, and façade tests. Accept only when
contracts are preserved or explicitly migrated, every changed path has a durable
owner, the audit has zero warnings or errors, and the diff contains no
suppression bypass. Report exact commands, exit codes, findings, evidence,
remaining risk, and any rollback boundary.
