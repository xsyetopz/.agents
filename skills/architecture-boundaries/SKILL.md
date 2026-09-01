---
name: architecture-boundaries
description: Use this skill when making software architecture decisions, auditing or enforcing boundaries and topology, assigning ownership, or performing structural migrations; use ordinary implementation workflows for bounded changes that preserve the existing architecture.
---

# Architecture Boundaries

Choose, audit, or enforce software boundaries from repository evidence. Preserve behavior and supported contracts.

Capture the decision, context, owners, constraints, quality scenarios, acceptance evidence, and rollback boundary. Safe local inspection and edits may proceed inside the requested scope. External, destructive, costly, or scope-expanding actions require exact authorization.

## Workflow

1. Frame the decision or finding, scope, owners, constraints, quality scenarios, preserved contracts, completion evidence, and rollback boundary.
2. Inventory Git state, authored and generated source, callers, dependencies, build targets, tests, generators, deployables, and public surfaces; run the Python capability preflight and read-only audit when applicable.
3. Load only the matching design or enforcement reference from the direct routes below.
   - [Canonical Vocabulary and Universal Decomposition Model](references/design-01-core-model.md) · [Pattern Catalog](references/design-02-pattern-catalog.md) · [Cross-Domain Mappings](references/design-03-domain-mappings.md) · [Architecture Decision Procedure](references/design-04-decision-procedure.md)
   - [Canonical Flowgraphs](references/design-05-flowgraphs.md) · [Failure Modes and Anti-Patterns](references/design-08-failure-modes.md) · [Bibliography and Primary References](references/design-09-bibliography.md) · [Worked Examples](references/design-10-worked-examples.md)
   - [Separation of Concerns and GOOD/RED examples](references/separation-of-concerns-examples.md) (read when assigning responsibilities, reviewing topology, or evaluating a proposed split; RED marks a contrast, while GOOD is the implementation pattern)
   - [Prior-art protocol](references/prior-art-protocol.md) (read before transferring empirical claims; verify each cited ID for the local task and metric)
   - [Rigor Modes](references/design-11-rigor-modes.md) · [Executable architecture tooling](references/enforcement-audit-tooling.md) · [Structural examples](references/enforcement-examples.md) · [Language architecture catalog](references/enforcement-languages.md)
   - [Filename contract](references/enforcement-naming.md) · [Architecture Pattern Selection Catalog](references/enforcement-pattern-catalog.md) · [Architecture fitness rules](references/enforcement-principles.md) · [Authority sources](references/enforcement-sources.md)
   - [Test ownership and placement](references/enforcement-testing.md) · [Toolchain, build, and package ownership](references/enforcement-toolchains.md) · [Architecture verification and evidence](references/enforcement-verification.md)
4. Map current topology, a do-less baseline, and materially different candidates; compare migration cost, reversibility, operational risk, and measurable quality attributes.
5. Select the smallest cohesive structure and assign each changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate.
6. Implement the authorized slice through canonical source and repository-native configuration, changing generator inputs rather than generated output and preserving public entrypoints unless migration is explicit.
7. Run `python3 scripts/providers.py capabilities --root <repo> --format json`, `python3 scripts/audit_architecture.py <repo> --format json`, focused tests, production or integration entrypoints, architecture checks, and final diff inspection; return unresolved external or runtime evidence as `UNVERIFIED`.

## Gotchas

- Nontrivial topology requires explicit alternatives, rejected choices, migration order, and measurable quality scenarios.
- Warnings and blocking diagnostics remain at their owner until repaired; exclusions, ignores, advisory modes, threshold changes, and reduced tests leave the architecture uncorrected.
- Keep public contracts stable unless the authorized migration records the change and rollback path.
- Route repository governance to `$repository-docs`, pipeline gates to `$git-ci-cd`, and prompt or tool-routing design to a dedicated prompt-audit workflow.
- Use repository-native checks and formats; keep policy, evidence, and reports in existing repository-owned forms.
