---
name: architecture-design
description: Use for architecture selection, system decomposition, design documents, bounded contexts, flow diagrams, ADRs, quality-attribute tradeoffs, implementation plans, or architecture reviews across compilers, interpreters, runtimes, CLI/TUI, AI agents, web apps, binary formats, data systems, and distributed software. Trigger as well when creating, splitting, merging, moving, or renaming three or more sibling source files, or changing package/directory topology. Do not use for a tiny isolated edit with no architectural decision.
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
- Creating, splitting, merging, moving, or renaming three or more sibling
  source files, or changing package/module/directory/export topology

## When NOT to use

- Enforcing architecture rules in existing code - use `architecture-enforce` instead
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
8. Files are implementation units, not architecture boundaries by default. Do
   not plan one file per type, operation, phase, helper, or validation rule when
   the units share owner, change reason, visibility, lifecycle, dependencies,
   or test contract.
9. `Validation`, `Helpers`, `Open`, `Reduce`, and `Commit` are procedural roles,
   not durable owners, unless independent lifecycle, contract,
   visibility/dependency boundary, or failure policy is proven.
10. For a topology trigger, produce a source-topology map covering the
    candidate working tree, including untracked source, with path, owner,
    change reason, visibility, lifecycle, dependencies, and consolidation
    rationale. No unresolved warning or error finding may remain.
11. For repository-affecting work, run the architecture-enforce capability
    preflight and full audit before and after. The acceptance run is full,
    default, and fail-closed. The audit exposes no baseline, exclusion,
    disabled/advisory gate, threshold override, or exception-waiver mode.

### Check integrity and failure ownership (non-negotiable)

Lint, test, policy, provider, build, and architecture checks are part of the
design contract and must remain active. Never add or expand ignore directives
(including `.gitignore`, tool ignore files, or lint/check excludes), disable a
rule, provider, or CI job, lower severity, add `allow-failure` or
`continue-on-error`, exclude a failing path, alter a baseline, or weaken or
delete a test/check to obtain a green result. A suppression is not a design
decision, evidence, or acceptance proof.

Fix a failure at its owning cause and rerun the affected check. If the tool is
wrong, preserve the failing gate and capture a minimal reproducer (tool/version,
exact command and configuration, input, output, and exit code), then request
explicit authorization for a policy change. The architecture gate cannot pass
and remains blocked while a check is disabled, downgraded, excluded, made
advisory, or otherwise weakened; conversational approval is not authorization.

## Quick start

1. **Contract**: extract objective, constraints, exclusions, and definition of done (Phase 0).
2. **Candidate tree**: enumerate tracked and untracked files; if the work changes a repository, run the architecture-enforce preflight and full audit before editing (Phase 0–1).
3. **Evidence**: inspect code/docs/tests; classify every statement as fact/inference/assumption/unknown (Phase 1–2).
4. **Forces**: define quality-attribute scenarios with measurable responses (Phase 3).
5. **Candidates**: generate ≥2 materially different architectures; include a "do less" candidate for comparison (Phase 4).
6. **Decide**: select patterns with problem, preconditions, consequences, and exit criteria (Phase 5).
7. **Specify**: produce semantic, static, dynamic, data, runtime, and deployment views (Phase 6–7).
8. **Review**: ATAM-style tradeoff/risk review; write ADRs; plan vertical slices (Phase 8–9).
9. **Verify**: map each critical requirement to an executable test and rerun the unmodified audit after edits (Phase 10–11).

The "do less" candidate is a design comparison, not a passing baseline. A
pre-change audit is diagnostic evidence, not a waiver. Acceptance is based on
the default full-repository gate, the topology map, and zero unresolved warning
or error findings.

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

- `architecture-enforce` - After design decisions are made, use this to turn
  them into executable boundary checks, dependency rules, and audit gates.

## Maintenance

```sh
# From the repository root:
python3 scripts/validate_skill.py skills/architecture-design
python3 skills/architecture-design/scripts/skill_checks.py eval-cases
python3 skills/architecture-design/scripts/skill_checks_test.py
```
