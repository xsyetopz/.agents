---
name: architecture-design
description: architecture decisions, ADRs, bounded contexts, topology, quality tradeoffs; excludes local-only edits.
---

# Architecture Design

Turn a structural question into an implementable decision grounded in repository facts, ownership, quality attributes, and executable checks.

## Use this skill

- Decide package, module, service, storage, protocol, deployment, ownership, public-contract, or multi-file structure.
- Write ADRs, architecture reports, decompositions, topology reviews, and migration plans for reliability, security, performance, evolvability, operability, or cost.
- Do not use for a local naming, formatting, or behavior-preserving edit with no structural effect.
- Redirect selected-topology enforcement to `$architecture-enforce`, policy ownership to `$repo-governance`, and agent-system or tool-routing prompt design to `$prompt-engineering`.

## Rules

- Inspect callers, contracts, tests, build and deployment graphs, public surfaces, and repository guidance before deciding.
- State scope, stakeholders, constraints, owners, boundaries, public contracts, and measurable quality scenarios.
- Compare at least two materially different candidates and a do-less baseline for every nontrivial decision.
- Give every changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate.
- Never hide warnings or failures with exclusions, threshold changes, ignores, disabled rules, or tolerated failed checks.

## Steps

1. Frame the decision, scope, owners, stakeholders, constraints, quality scenarios, and preserved contracts.
2. Discover source topology, dependencies, control and data flow, failure ownership, generated files, and public surfaces.
3. Inventory tracked, modified, staged, and non-ignored candidates; map each path to an owner and boundary.
4. Generate materially different candidates, including do-less; compare quality attributes, migration cost, rollback boundary, reversibility, and operational risk.
5. Record the selected structure, rejected alternatives, contracts, migration order, rollback boundary, ownership map, and evolution triggers in an ADR or report.
6. Run capability preflight, focused checks, production or integration entrypoints, architecture audit, and final diff inspection.

## Resources

- Start with the package [reference router](references/index.md).
- Use the [ADR template](assets/adr.template.md) and
  [architecture-report template](assets/architecture-report.template.md) when
  recording a decision.
- Use the [bounded-context](assets/bounded-context.template.md),
  [component-contract](assets/component-contract.template.md),
  [quality-attribute scenario](assets/quality-attribute-scenario.template.md),
  [decision matrix](assets/decision-matrix.template.tsv), and
  [domain map](assets/domain-map.template.tsv) templates when those artifacts
  are required.

## Verify

- Done means the decision records owners, boundaries, constraints, candidate trade-offs, migration, rollback, rejected alternatives, and measurable evidence.
- Run `python3 scripts/check.py`, `python3 scripts/skill_checks.py eval-cases`,
  and `python3 scripts/skill_checks.py report REPORT --mode R3` from this
  package.
- For topology work, run the selected enforcement skill's preflight, focused tests, full audit, and provider checks.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark live repository settings, integration runs, or unavailable provider evidence `UNVERIFIED` rather than inferring it.
