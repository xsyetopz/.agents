---
name: architecture-design
description: architecture decisions, ADRs, bounded contexts, topology, quality tradeoffs; excludes local-only edits.
---

# Architecture Design

Turn a structural question into an implementable decision grounded in repository
facts, domain ownership, quality attributes, and executable verification.

## When to use

- Select package, module, service, storage, protocol, or deployment structure.
- Write an ADR, architecture report, decomposition, or migration plan.
- Review dependency direction, ownership, lifecycle, public contracts, or boundaries.
- Change topology or three or more sibling source files.
- Resolve reliability, security, performance, evolvability, operability, or cost forces.

## When NOT to use

- A local edit whose owner, boundary, and behavior stay unchanged.
- Naming or formatting work without a structural decision.
- Pattern selection without repository or product evidence.
- Runtime implementation work after the structure is already selected; use the owning implementation skill.

## Guardrails

- Inspect callers, contracts, tests, build graph, deployment topology, and repository guidance before deciding.
- Define decision, forces, constraints, owners, public contracts, and measurable quality scenarios.
- Compare at least two material candidates and a do-less baseline for nontrivial decisions.
- Give every changed path one durable owner, reason, visibility, lifecycle, dependencies, and consolidation rationale.
- Treat helpers, validation, types, managers, open, reduce, and commit as procedural roles, not automatic owners.
- Never pass by excluding paths, changing thresholds, disabling rules, adding ignores, or tolerating failed checks.

## Workflow

1. Frame scope, owner, stakeholders, constraints, and quality scenarios.
2. Discover current state, dependencies, control/data flow, failure ownership, and public surfaces.
3. Inventory tracked and untracked candidates and map source-path ownership.
4. Generate materially different candidates, including do-less; compare risk, reversibility, cost, and verification.
5. Record the selected structure, rejected alternatives, contracts, migration, rollback boundary, and evolution triggers.
6. Run capability preflight, focused tests, production entrypoint, architecture audit, and final diff inspection.

## Quick start

1. Start with [the ADR template](assets/adr.template.md) or [the architecture-report template](assets/architecture-report.template.md).
2. Load the [reference map](references/index.md), then use the [decision procedure and workflow](references/04-decision-procedure.md) with the [core model](references/01-core-model.md).
3. For topology work, activate `$architecture-enforce` and run its package-local preflight and audit.
4. Run `python3 scripts/check.py` and the focused report checks: `python3 scripts/skill_checks.py eval-cases`.

## Reference map

Load only what answers the current question:

- [Core model](references/01-core-model.md) — frame ownership, forces, and boundaries.
- [Pattern catalog](references/02-pattern-catalog.md) — compare candidate structures.
- [Reference map](references/index.md) — route trigger keywords to focused material.
- [Decision procedure and workflow](references/04-decision-procedure.md) — sequence evidence, gates, and tradeoffs.
- [Verification and evals](references/07-verification-and-evals.md) — define executable acceptance.
- [Failure modes](references/08-failure-modes.md) — test safety and architecture failure paths.
- [Worked examples](references/10-worked-examples.md) — calibrate reports and decisions.
- [Rigor modes](references/11-rigor-modes.md) — scale analysis to risk.

## Completion

Complete only when the decision is implementable, every changed source path has
a credible owner and rationale, required structural/runtime checks pass, and no
warning or error remains unresolved. Report paths, evidence, tradeoffs, and any
explicitly deferred risk.

## Validation

Run from this package directory:

```sh
python3 scripts/check.py
python3 scripts/skill_checks.py eval-cases
```

For a report, run `python3 scripts/skill_checks.py report REPORT --mode R3`; for
an architecture change, `$architecture-enforce` owns the full audit and its
focused tests. Static PASS is not behavioral proof.

## Related skills

- `$architecture-enforce` — enforce the selected topology and audit boundaries.
- `$repo-governance` — record durable ownership and repository policy.
- `$prompt-engineering` — design agent-system or tool-routing instruction architecture.
