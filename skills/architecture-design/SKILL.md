---
name: architecture-design
description: >
  Use for architecture decisions, ADRs, bounded contexts, or quality-attribute tradeoffs; not a tiny isolated edit without architectural impact.
---

# Architecture Design

Produce an implementable decision tied to repository evidence, domain ownership,
quality attributes, and executable acceptance checks. Patterns are candidates,
not starting answers.

## When to use

- Selecting system, package, module, service, storage, protocol, or deployment structures
- Writing an ADR, architecture report, decomposition plan, or migration plan
- Reviewing dependency direction, ownership, lifecycle, public contracts, or cross-language boundaries
- Changing package or directory topology or three or more sibling source files
- Resolving latency, throughput, reliability, security, evolvability, operability, or cost forces

## When NOT to use

- A local edit whose owner, boundary, and behavior remain unchanged
- Naming or formatting work without a structural decision
- Pattern selection without repository or product evidence

## Non-negotiables

- Inspect the repository, callers, contracts, tests, build graph, and deployment topology needed to establish current state.
- Define the decision, forces, constraints, owners, public contracts, and quality scenarios before selecting a pattern.
- Compare at least two material candidates plus a do-less baseline for nontrivial decisions.
- Map every created, moved, split, merged, or renamed source path to one durable owner, reason, visibility, lifecycle, dependencies, and consolidation rationale.
- Helpers, Validation, Types, Managers, Open, Reduce, and Commit are procedural roles, not automatic owners.
- Reject one-type, one-operation, one-phase, helper, or validation file decomposition when ownership and lifecycle are shared.
- Every warning or error from the required architecture audit blocks completion.
- Never pass by excluding paths, changing thresholds or baselines, disabling rules, adding exceptions or ignores, tolerating CI failure, or weakening checks.

## Workflow

1. Frame the decision, scope, owner, stakeholders, constraints, and measurable quality scenarios.
2. Discover current state, dependencies, control/data flow, failure ownership, and public surfaces.
3. Inventory tracked and untracked candidates and complete the source-path ownership map.
4. Generate materially different candidates, including the do-less option.
5. Compare consequences using identical scenarios, migration risk, reversibility, operational cost, and verification.
6. Record the selected structure, rejected alternatives, contracts, sequence, rollback boundary, and evolution triggers.
7. Run capability preflight, full architecture audit, focused tests, production entrypoint, and final diff inspection.

## Quick start

Use assets/architecture-report.template.md or assets/adr.template.md, then run:

~~~sh
python3 skills/architecture-enforce/scripts/providers.py capabilities --root . --format json
python3 skills/architecture-enforce/scripts/audit_architecture.py . --format json
~~~

The audit has one fixed gate. Resolve every warning and error.

## Output contract

Include the decision and scope, evidence and current-state map, quality scenarios,
source-topology ownership map, candidates, tradeoffs, contracts, dependency
direction, migration, rollback, executable verification, rejected alternatives,
and evolution triggers.

## Reference map

| Need | Load |
|---|---|
| Core model | references/01-core-model.md |
| Pattern candidates | references/02-pattern-catalog.md |
| Domain mappings | references/03-domain-mappings.md |
| Decision procedure | references/04-decision-procedure.md |
| Flow diagrams | references/05-flowgraphs.md |
| Artifact contracts | references/06-artifact-contracts.md |
| Verification and evals | references/07-verification-and-evals.md |
| Failure modes | references/08-failure-modes.md |
| Worked examples | references/10-worked-examples.md |
| Rigor selection | references/11-rigor-modes.md |
| End-to-end workflow | references/workflow.md |

## Completion

Complete only when the decision is implementable, every changed source path has a
credible owner, required runtime and structural checks pass, and no unresolved
warning or error remains.

## Related skills

- architecture-enforce for implementation and auditing
- repo-governance for durable architecture policy
- prompt-engineering for agent-system instruction architecture
