---
name: architecture-enforce
description: architecture enforcement, topology refactors, ownership boundaries, file shattering, three-plus sibling changes.
---

# Architecture Enforce

Turn architecture policy into repository evidence and blocking checks while preserving behavior unless a requested migration explicitly changes it.

## Use this skill

- Change or audit packages, directories, modules, schemas, APIs, tests, generated boundaries, build graphs, deployables, languages, storage, protocols, public contracts, or three or more sibling files.
- Use it for file shattering, flat folders, filename colonies, helper or manager proliferation, dependency cycles, ownership drift, and lint, test, architecture, or CI suppressions.
- Do not use for isolated formatting or comment edits, architecture ideation before a target is selected, or generated output when canonical generator input is available.
- Redirect target selection and ADRs to `$architecture-design`, repository policy to `$repo-governance`, and pipeline gates to `$git-ci-cd`.

## Rules

- Read repository instructions, owning code, callers, tests, build configuration, generators, and public contracts before editing.
- Assign every changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate.
- Prefer cohesive capability modules over one-type, one-operation, phase, helper, validation, or filename-prefix colonies.
- Inventory tracked, modified, staged, and non-ignored authored source; keep tracked files auditable.
- Every warning and error blocks. Never add ignores, exclusions, advisory modes, allow-failure paths, lower thresholds, or weakened tests.
- Change canonical generator inputs; do not hand-edit generated output. Preserve public entrypoints and contracts unless migration evidence records the change.

## Steps

1. Run capability discovery and inventory Git state, source candidates, manifests, tests, generators, and public surfaces.
2. Complete topology and dependency maps with path, owner, responsibility, reason, visibility, lifecycle, dependencies, and why each path remains separate.
3. State the owning cause, target structure, preserved contracts, candidate comparison, migration order, rollback boundary, and evidence plan.
4. Implement through cohesive package-local slices while preserving public entrypoints and canonical generator ownership.
5. Run focused tests, the production or integration entrypoint, the full audit, provider queries, and final diff inspection.
6. Resolve each diagnostic at its owning cause. If a checker is wrong, preserve the failing gate and report a reproducer instead of weakening it.

## Resources

- Start with the package [reference router](references/index.md).

## Verify

- Done means every changed path has a durable owner, the audit has zero warnings or errors, contracts are preserved or explicitly migrated, and no suppression bypass remains.
- Run `python3 scripts/check.py`, `python3 scripts/providers.py capabilities --root . --format json`, and `python3 scripts/audit_architecture.py . --format json` from this package.
- Run relevant package tests, including audit CLI, suppression, provider, and façade tests.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark missing provider data, hosted settings, integration runs, or unavailable runtime evidence `UNVERIFIED`.
