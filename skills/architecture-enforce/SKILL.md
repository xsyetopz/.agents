---
name: architecture-enforce
description: >
  Use when implementing, reviewing, refactoring, migrating, or enforcing repository architecture across packages, modules, deployables, APIs, schemas, build graphs, generated code, tests, benchmarks, and cross-language boundaries. Trigger on package or directory topology changes and whenever three or more sibling source files are created, split, merged, moved, or renamed. Keywords include architecture audit, boundary violation, file shattering, filename colony, flat cluster, microfile fragmentation, helper file, manager file, circular dependency, forbidden import, layering violation, public API drift, schema boundary, ownership, cohesion, coupling, dependency direction, source topology, inline tests, lint suppression, ignored findings, fitness function, and structural refactor. Enforce fail-closed verification without waivers or suppression.
---

# Architecture Enforce

Turn architecture policy into repository evidence and blocking checks. Preserve
behavior unless the requested architecture change explicitly alters it.

## When to use

- Changing packages, directories, modules, schemas, APIs, tests, generated boundaries, or three or more sibling source files
- Reviewing file shattering, flat folders, filename colonies, helper/manager proliferation, cycles, or ownership drift
- Migrating build graphs, deployables, languages, storage, protocols, or public contracts
- Auditing lint, test, architecture, or CI suppression used to hide failures

## When NOT to use

- A tiny edit with no boundary, topology, ownership, contract, or build-graph effect
- Architecture ideation before a target structure is selected; use architecture-design

## Non-negotiable contract

### Ownership and boundaries

- Read repository instructions, owning code, callers, tests, build configuration, and public contracts before editing.
- Assign each changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it cannot be consolidated.
- Prefer capability modules over one-type, one-operation, one-phase, helper, validation, or filename-prefix colonies.
- Helpers, Validation, Types, Managers, Open, Reduce, and Commit are procedural roles, not owners.
- Keep tests and benchmarks in owned test surfaces unless a language contract requires otherwise.
- Change canonical generator inputs; do not hand-edit generated output.

### Topology and decomposition gate

Inventory tracked, modified, staged, untracked, and ignored authored source. For
every created, moved, split, merged, or renamed path, record:

| Path | Owner | Reason | Visibility | Lifecycle | Dependencies | Why separate |
|---|---|---|---|---|---|---|

Missing rows block acceptance. A file justified only by declaration category,
operation phase, test convenience, or anticipated reuse must be consolidated.

### Fail-closed acceptance

- Every warning and error blocks.
- Existing findings are not a baseline or waiver.
- Generated, vendored, ignored, artifact, snapshot, migration, or test-root labels do not silently remove authored source.
- No accepted downgrade, exclusion, threshold, exception, or advisory mode exists.

### Check integrity and failure ownership

Never pass by adding ignores or suppression comments, disabling a rule/provider/job,
lowering severity, changing thresholds or baselines, excluding paths, adding
allow-failure or continue-on-error, swallowing command failures, or weakening or
deleting tests and checks. Fix the underlying code or owning checker. If the
checker is wrong, keep acceptance blocked and report a minimal reproducer.

## Quick start - mandatory audit protocol

1. Run capability discovery.
2. Inventory Git state, source candidates, manifests, tests, generators, and public surfaces.
3. Complete the topology and dependency maps.
4. State the owning cause, target structure, preserved contracts, migration order, and rollback boundary.
5. Implement through canonical sources in cohesive slices.
6. Run focused tests and the production or integration entrypoint.
7. Run the full audit and relevant provider queries.
8. Inspect the final diff and resolve every diagnostic.

Commands:

    python3 skills/architecture-enforce/scripts/providers.py capabilities --root . --format json
    python3 skills/architecture-enforce/scripts/audit_architecture.py . --format json

## Enforcement profiles

Profiles change questions, never the gate:

- Module/package: ownership, dependency direction, public API, tests
- Distributed system: deployables, protocols, data ownership, failure domains
- Compiler/runtime: phases, IR ownership, transitions, diagnostics
- Data/storage: schema ownership, migration, compatibility, recovery
- Cross-language: generated boundary, ABI/schema contract, canonical source
- Agent system: authority, tools, state, orchestration, observable effects

## Reference map

| Need | Load |
|---|---|
| Core rules | references/principles.md |
| Naming and fragmentation | references/naming.md |
| Language conventions | references/languages.md |
| Tests and benchmarks | references/testing.md |
| Toolchains | references/toolchains.md |
| Audit tooling | references/tooling.md |
| Verification | references/verification.md |
| Patterns and quality attributes | references/patterns.md, references/quality-attributes.md |
| Examples | references/examples.md |
| Sources | references/sources.md |

## Completion

Complete only when contracts are preserved or explicitly migrated, every changed
path has a durable owner, focused and integration checks pass, the full audit has
zero warnings/errors, and the diff contains no suppression bypass.

## Related skills

- architecture-design for selecting the structure
- repo-governance for durable ownership policy
- git-ci-cd for pipeline enforcement
