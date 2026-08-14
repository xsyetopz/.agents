---
name: architecture-design
description: architecture decisions, ADRs, bounded contexts, topology, quality tradeoffs; excludes local-only edits.
---

# Architecture Design

Turn a structural question into an implementable decision grounded in repository
facts, ownership, quality attributes, and executable checks.

## Use this skill

Use this skill when a decision changes package, module, service, storage,
protocol, deployment, ownership, public contracts, or three or more sibling
source files. Use it for ADRs, architecture reports, decompositions, topology
reviews, and migration plans involving reliability, security, performance,
evolvability, operability, or cost.

## Rules

- Do not use it for a local naming, formatting, or behavior-preserving edit with no structural effect; use the owning implementation skill.
- Inspect callers, contracts, tests, build and deployment graphs, public surfaces, and repository guidance before deciding.
- State scope, stakeholders, constraints, owners, boundaries, public contracts, and measurable quality scenarios.
- Compare at least two materially different candidates and a do-less baseline for every nontrivial decision. Record risk, reversibility, cost, and verification for each.
- Give every changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate. Treat helpers, validation, types, managers, open, reduce, and commit as procedural roles, not automatic owners.
- Never hide a warning or failure with exclusions, threshold changes, ignores, disabled rules, or tolerated failed checks.

## Steps

1. Frame the decision, scope, owners, stakeholders, constraints, quality scenarios, and preserved contracts.
2. Discover current source topology, dependencies, control and data flow, failure ownership, generated files, and public surfaces.
3. Inventory tracked, modified, staged, and non-ignored candidates; map each source path to an owner and boundary.
4. Generate materially different candidates, including do-less; compare quality attributes, migration cost, rollback boundary, reversibility, and operational risk.
5. Record the selected structure, rejected alternatives, contracts, migration order, rollback boundary, ownership map, and evolution triggers in an ADR or report.
6. Run capability preflight, focused checks, production or integration entrypoints, architecture audit, and final diff inspection.

## Resources

Route only the material needed for the decision:

- [Reference index](references/index.md) — trigger-to-reference routing.
- [Core model](references/01-core-model.md) — ownership, forces, boundaries, and quality attributes.
- [Pattern catalog](references/02-pattern-catalog.md) — candidate structures and their preconditions.
- [Decision procedure](references/04-decision-procedure.md) — evidence sequence, gates, and tradeoffs.
- [Verification and evals](references/07-verification-and-evals.md) — executable acceptance and evidence.
- [Failure modes](references/08-failure-modes.md) — failure paths and unsafe shortcuts.
- [Worked examples](references/10-worked-examples.md) — reports and decisions across domains.
- [Rigor modes](references/11-rigor-modes.md) — scale analysis to risk.
- [Bibliography](references/09-bibliography.md) — primary architecture and evaluation sources.
- [ADR template](assets/adr.template.md), [architecture report](assets/architecture-report.template.md), [quality scenario](assets/quality-attribute-scenario.template.md), and [component contract](assets/component-contract.template.md) — record decisions and evidence.
- `$architecture-enforce` — apply the selected topology and audit boundaries; `$repo-governance` — persist ownership and repository policy; `$prompt-engineering` — design agent-system or tool-routing instruction architecture.

## Verify

Run from this package directory:

```sh
python3 scripts/check.py
python3 scripts/skill_checks.py eval-cases
python3 scripts/skill_checks.py report REPORT --mode R3
```

For topology work, activate `$architecture-enforce` and run its capability
preflight, focused tests, full audit, and provider checks. Accept the decision
only when required checks pass with no unresolved warning or error, every
changed path has an owner and rationale, and the report names evidence,
tradeoffs, migration, rollback, rejected alternatives, and deferred risk.
