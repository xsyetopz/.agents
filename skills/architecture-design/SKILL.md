---
name: architecture-design
description: Use for architecture selection, system decomposition, design documents, bounded contexts, flow diagrams, ADRs, quality-attribute tradeoffs, implementation plans, or architecture reviews across compilers, interpreters, runtimes, CLI/TUI, AI agents, web apps, binary formats, data systems, and distributed software. Do not use for a tiny isolated edit with no architectural decision.
---

# Architecture Design

Produce architecture decisions that are traceable to evidence, domain semantics,
quality attributes, and verifiable consequences. Treat patterns as candidate
responses to forces, never as fashionable answers.

## When to use

- Choosing an architecture style (MVC, MVU, DDD, pipeline, ports-and-adapters, event-driven)
- Decomposing a system into modules, bounded contexts, or deployable units
- Writing an Architecture Decision Record (ADR)
- Comparing candidate architectures against quality-attribute scenarios
- Reviewing an existing design for risks, tradeoffs, or missing failure paths

## When NOT to use

- Enforcing architecture rules in existing code — use `architecture-enforce` instead
- A single-file, single-function edit with no structural choice
- Picking frameworks/libraries before the architecture is decided

## Non-negotiables

1. Separate **facts**, **user assertions**, **inferences**, **assumptions**, and **unknowns**.
2. Do not select a named pattern before identifying the domain, forces, and boundaries.
3. Do not apply DDD by default. DDD is justified only when domain complexity warrants it.
4. Every selected architecture MUST name at least one disadvantage, risk, and rejected alternative.
5. Do not implement or generate code before Gates G0–G6 pass.
6. Do not silently expand scope. Place unrequested work in **Deferred / Out of Scope**.
7. Fail closed: when a missing fact can invalidate the architecture, stop and request it.

## Quick start

1. **Contract**: extract objective, constraints, exclusions, and definition of done (Phase 0).
2. **Evidence**: inspect code/docs/tests; classify every statement as fact/inference/assumption/unknown (Phase 1–2).
3. **Forces**: define quality-attribute scenarios with measurable responses (Phase 3).
4. **Candidates**: generate ≥2 materially different architectures; include a "do less" baseline (Phase 4).
5. **Decide**: select patterns with problem, preconditions, consequences, and exit criteria (Phase 5).
6. **Specify**: produce semantic, static, dynamic, data, runtime, and deployment views (Phase 6–7).
7. **Review**: ATAM-style tradeoff/risk review; write ADRs; plan vertical slices (Phase 8–9).
8. **Verify**: map each critical requirement to an executable test (Phase 10–11).

Full 11-phase workflow: [references/workflow.md](references/workflow.md).

## Reference map

| If you need to... | Load |
|---|---|
| Understand the canonical vocabulary and universal decomposition model | `references/01-core-model.md` |
| Compare or select named patterns | `references/02-pattern-catalog.md` |
| Map patterns to specific domains | `references/03-domain-mappings.md` |
| Score candidates and apply rigor levels | `references/04-decision-procedure.md` |
| Produce or check flows/sequences/state transitions | `references/05-flowgraphs.md` |
| Produce ADRs, context maps, contracts, or implementation slices | `references/06-artifact-contracts.md` |
| Review a design or define acceptance tests | `references/07-verification-and-evals.md` |
| Check for anti-patterns | `references/08-failure-modes.md` |
| Source grounding and citations | `references/09-bibliography.md` |
| See worked examples for a classified domain | `references/10-worked-examples.md` |
| Determine required analysis depth | `references/11-rigor-modes.md` |
| Full step-by-step procedure | `references/workflow.md` |

## Related skills

- `architecture-enforce` — After design decisions are made, use this to turn
  them into executable boundary checks, dependency rules, and audit gates.

## Maintenance

```sh
python3 scripts/validate_skill.py
```
