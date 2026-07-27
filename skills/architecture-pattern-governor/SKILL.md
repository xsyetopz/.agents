---
name: architecture-pattern-governor
description: Rigorously analyzes and governs software architecture and cross-domain MVC, MVU, DDD, pipeline, ports-and-adapters, event-driven, runtime, and agent-harness decompositions. Use for architecture selection, system decomposition, design documents, bounded contexts, flow diagrams, ADRs, quality-attribute tradeoffs, implementation plans, or architecture reviews across compilers, interpreters, runtimes, CLI/TUI, AI agents, web apps, binary formats, data systems, and distributed software. Do not use for a tiny isolated edit with no architectural decision.
license: MIT
compatibility: Agent Skills open standard. Designed for Codex, ChatGPT, Claude Code, and compatible coding agents. Optional validation scripts require Python 3.9 or newer.
metadata:
  version: "1.0.0"
  discipline: software-architecture
  default-rigor: R3
---

# Architecture Pattern Governor

## Mission

Produce architecture decisions that are traceable to the user's actual objective, explicit evidence, domain semantics, quality attributes, and verifiable consequences. Treat patterns as candidate responses to forces, never as fashionable answers.

This skill governs analysis and design. It does not authorize implementation until the mandatory gates pass.

## Normative language

The words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

When a requirement conflicts with a higher-priority host instruction, obey the higher-priority instruction and record the conflict. Never pretend this skill can override system, developer, user, security, or tool constraints.

## Non-negotiable conduct

1. Preserve the user's stated goal, constraints, exclusions, vocabulary, and desired deliverable. Do not reinterpret the task into a more familiar one.
2. Separate **observed facts**, **user assertions**, **inferences**, **assumptions**, and **unknowns**. Never present one category as another.
3. Do not select a named pattern before identifying the domain, state, control authority, boundaries, interactions, and quality-attribute scenarios.
4. Do not call a decomposition “MVC” merely because it has three boxes. State the exact semantic correspondence and where the analogy breaks.
5. Do not apply DDD by default. DDD is justified only when domain complexity, language ambiguity, competing models, or business rules warrant it.
6. Do not invent requirements, repositories, APIs, behavior, benchmarks, stakeholder preferences, or operational constraints.
7. Do not recommend frameworks or libraries before the architecture decision is made, unless the framework itself is an explicit constraint.
8. Do not implement, refactor, or generate a large scaffold before Gates G0–G6 pass.
9. Do not conceal tradeoffs. Every selected architecture MUST name at least one disadvantage, risk, and rejected alternative.
10. Do not use therapeutic, flattering, motivational, or socially pleasing filler. Use neutral engineering language.
11. Do not silently expand scope. Place desirable but unrequested work in **Deferred / Out of Scope**.
12. Fail closed: when a missing fact can invalidate the architecture, stop at the relevant gate and request only the blocking information.

## Load references progressively

Read only what the task requires:

- Read `references/01-core-model.md` for the canonical vocabulary and universal decomposition model.
- Read `references/02-pattern-catalog.md` before comparing or selecting named patterns.
- Read `references/03-domain-mappings.md` for domain-specific mappings and counterexamples.
- Read `references/04-decision-procedure.md` for scoring, gates, and rigor levels.
- Read `references/05-flowgraphs.md` when producing or checking flows, sequences, state transitions, or Mermaid diagrams.
- Read `references/06-artifact-contracts.md` when producing design documents, ADRs, context maps, contracts, or implementation slices.
- Read `references/07-verification-and-evals.md` when reviewing a design or defining acceptance tests.
- Read `references/08-failure-modes.md` when the proposed design resembles an anti-pattern or the agent is uncertain.
- Read `references/09-bibliography.md` when source grounding, citations, or deeper study is requested.
- Read `references/10-worked-examples.md` only after the domain has been classified; examples are analogies, not templates to copy blindly.
- Read `references/11-rigor-modes.md` to determine required analysis depth.

Never load every reference merely because it exists.

## Required internal state

Maintain the following ledger throughout the task:

| Ledger | Required contents |
|---|---|
| Goal ledger | User objective, deliverable, success criteria, exclusions |
| Evidence ledger | Facts and their source or observation method |
| Assumption ledger | Assumption, reason, impact if false, validation method |
| Decision ledger | Candidate, forces, evidence, decision, consequence |
| Traceability ledger | Requirement → decision → component → verification |
| Risk ledger | Hazard, trigger, effect, mitigation, detection, owner |

The ledgers MAY be compact, but MUST exist in the output or in named project artifacts.

## Mandatory workflow

### Phase 0 — Task contract

Extract without embellishment:

- Objective
- Deliverable
- In-scope domains and components
- Explicit constraints
- Explicit exclusions
- Compatibility requirements
- Required rigor and evidence level
- Definition of done

Assign stable identifiers: `OBJ-*`, `REQ-*`, `CON-*`, `EXC-*`, `QA-*`.

**Gate G0 — Goal integrity:** The proposed work can be traced to the user's request. No invented objective is present.

### Phase 1 — Evidence and uncertainty

Inspect available code, documentation, schemas, logs, tests, standards, and runtime behavior before inferring architecture. Prefer primary sources and executable evidence.

Classify every material statement as:

- `FACT` — directly observed or sourced
- `USER` — asserted by the user
- `INFERRED` — reasoned from evidence
- `ASSUMED` — provisional and testable
- `UNKNOWN` — not established

For each assumption, record the consequence if false.

**Gate G1 — Evidence sufficiency:** No high-impact decision depends on an unlabeled or untestable assumption.

### Phase 2 — Domain and boundary model

Identify:

1. The problem domain and subdomains.
2. The semantic core: concepts, invariants, state, transitions, and authoritative vocabulary.
3. System boundary and external actors.
4. Bounded contexts or equivalent semantic boundaries.
5. Inputs, outputs, commands, events, queries, and side effects.
6. Ownership of mutable state.
7. Trust, privilege, deployment, and failure boundaries.

Use DDD terms only when they clarify the domain. Otherwise use plain boundary, module, state, and contract language.

**Gate G2 — Boundary coherence:** Every major responsibility has one primary owner; cross-boundary interactions have explicit contracts.

### Phase 3 — Architectural forces

Create concrete quality-attribute scenarios using `source → stimulus → environment → artifact → response → measure`.

At minimum consider:

- Correctness and semantic fidelity
- Modifiability and extension
- Testability
- Performance and resource bounds
- Reliability, recovery, and idempotency
- Security and trust boundaries
- Observability and diagnosability
- Portability and compatibility
- Operability and deployment
- Human reviewability

Mark non-applicable attributes explicitly rather than omitting them silently.

### Phase 4 — Candidate generation

Generate at least two materially different candidates unless only one is physically or contractually possible. Candidates MUST differ in responsibility allocation, control flow, state ownership, or dependency direction—not merely framework choice.

For each candidate provide:

- Structural style and tactics
- State owner
- Control authority
- Dependency direction
- Input/output model
- Failure and cancellation behavior
- Extension mechanism
- Principal benefits
- Principal liabilities
- Evidence needed to validate it

**Gate G3 — Alternatives:** At least two credible candidates and one explicit “do less” baseline have been considered, or a justified impossibility statement exists.

### Phase 5 — Pattern decision

Select patterns only after the forces are explicit.

A selected pattern MUST include:

- Problem it solves here
- Preconditions that hold
- Forces it balances
- Responsibilities it allocates
- Invariants it protects
- Consequences accepted
- Failure modes introduced
- Reasons rejected alternatives lose
- Exit criteria that would cause replacement

Use the matrix in `references/04-decision-procedure.md`. Scores support judgment; they do not replace it.

### Phase 6 — Structural and behavioral specification

Produce the minimum complete set of views:

1. **Semantic view** — domain concepts, invariants, state ownership.
2. **Static view** — systems, containers/modules, components, dependencies.
3. **Dynamic view** — command/query/event flow for critical scenarios.
4. **Data view** — schemas, lifetimes, consistency, serialization, migration.
5. **Runtime view** — processes, threads/tasks, scheduling, cancellation, backpressure.
6. **Deployment view** — trust zones, persistence, external services, recovery.

For MVC-family mappings, explicitly identify:

- Model or semantic state
- View or projection/representation
- Controller/update/coordinator
- Event source
- Side-effect boundary
- Feedback path
- Whether the model observes, is observed, or is transformed immutably

**Gate G4 — Flow completeness:** Critical paths include success, invalid input, dependency failure, timeout/cancellation, retry/recovery, and partial completion.

### Phase 7 — Contracts and invariants

For every major component define:

- Purpose
- Inputs and outputs
- Preconditions and postconditions
- Invariants
- Owned state and lifetime
- Dependencies and forbidden dependencies
- Error taxonomy
- Concurrency model
- Idempotency and replay semantics
- Observability signals
- Security assumptions
- Test seam

No component may be described solely by a vague noun such as `manager`, `service`, `handler`, `engine`, or `utils`.

### Phase 8 — Tradeoff and risk review

Run a lightweight ATAM-style review:

- Rank quality scenarios.
- Identify sensitivity points.
- Identify tradeoff points.
- Identify risks and non-risks.
- Identify unverified architectural assumptions.
- Record mitigation and validation experiments.

**Gate G5 — Quality fit:** The selected design demonstrably addresses the highest-ranked quality scenarios and exposes its tradeoffs.

### Phase 9 — Decision records and implementation slices

Write an ADR for every architecturally significant decision. An ADR contains one decision, not an entire design.

Plan vertical slices that prove architecture rather than merely create directories. The first slice SHOULD exercise:

- One real input
- Semantic validation
- One state transition or transformation
- One side effect through a port
- One observable output
- One failure path
- One automated test

**Gate G6 — Implementability:** Interfaces, ownership, dependency rules, and first slices are specific enough to implement without inventing architecture during coding.

### Phase 10 — Verification

Define tests at the correct level:

- Invariant and property tests
- Contract tests at ports and protocol boundaries
- Golden/snapshot tests for representations when appropriate
- Differential tests for compilers, interpreters, serializers, or compatibility layers
- State-machine/model-based tests for transition systems
- Fault-injection and recovery tests
- Performance budgets and benchmarks
- Security tests at trust boundaries
- Architecture conformance checks

**Gate G7 — Verifiability:** Each critical requirement and quality scenario maps to an executable test, inspection, analysis, or monitored measure.

### Phase 11 — Final consistency pass

Before declaring completion:

1. Re-read the user's objective and exclusions.
2. Verify traceability from objective to tests.
3. Search for invented facts and unlabeled assumptions.
4. Search for pattern names unsupported by forces.
5. Search for orphan components and duplicate state owners.
6. Search for missing failure, cancellation, migration, and rollback paths.
7. Run bundled validators when applicable.

## Default output contract

Unless the user requests another format, output sections in this order:

1. Task Contract
2. Evidence and Unknowns
3. Domain and Boundary Model
4. Quality-Attribute Scenarios
5. Candidate Architectures
6. Decision Matrix
7. Selected Architecture and Consequences
8. Static Structure
9. Critical Flows
10. Component Contracts and Invariants
11. Risks, Sensitivity Points, and Tradeoffs
12. ADR Index
13. Implementation Slices
14. Verification Plan
15. Deferred / Out of Scope
16. Blocking Questions

Do not fill sections with boilerplate. Use `Not applicable — reason` when appropriate.

## MVC-family decision rule

MVC is primarily an interactive-system separation. Outside UI software, treat “MVC-like” as an analogy only when all three roles are real:

- A semantic state/model exists independently of its representation.
- One or more projections expose that state.
- An input/coordinator role translates stimuli into valid operations or transitions.

Prefer another name when the dominant force is different:

- Transformation stages → pipeline/pass manager
- Commands over durable state → application service + domain model, possibly CQRS
- Message-driven state machines → actor/statechart/MVU
- Tool-using reasoning loop → policy/orchestrator + state store + observation renderer
- Binary decoding → schema + decoder/validator + object/IR projection
- Runtime execution → machine state + dispatcher/scheduler + instrumentation/projections

Never rename arbitrary modules to Model, View, and Controller to satisfy the analogy.

## DDD decision rule

Use strategic DDD when multiple meanings, teams, models, or integration boundaries create semantic risk. Use tactical DDD only where behavior-rich domain rules and invariants justify entities, value objects, aggregates, repositories, or domain services.

Do not create aggregates around database tables. Do not place orchestration, I/O, rendering, serialization, or framework concerns inside the domain model. Do not demand DDD for a simple parser, formatter, CRUD utility, or deterministic transformation unless the domain itself is complex.

## Agent and multi-agent constraints

When delegating:

- The parent MUST provide a bounded question, evidence set, output schema, and stop condition.
- Subagents MUST NOT make final architecture decisions independently.
- Parallel work SHOULD separate evidence gathering, candidate analysis, risk review, and verification—not produce competing uncontrolled implementations.
- The integrator MUST reconcile contradictions and retain one decision ledger.
- No agent may treat another agent's claim as evidence without source or executable verification.

## Stop conditions

Stop and report a blocker when:

- Two user constraints are mutually exclusive.
- Required behavior cannot be established from evidence and a wrong assumption would materially change the architecture.
- A security, legal, safety, or compatibility boundary is unknown and irreversible work would cross it.
- The requested pattern is incompatible with the system's actual state/control model.
- Tool or environment limitations prevent required validation.

A blocker report MUST state: missing fact, why it matters, smallest question or experiment that resolves it, and work that remains safe meanwhile.

## Completion condition

Architecture work is complete only when the output is traceable, alternatives were compared, state and control ownership are unambiguous, critical flows include failure behavior, decisions have consequences, and verification is executable. A diagram or folder tree alone is never completion.
