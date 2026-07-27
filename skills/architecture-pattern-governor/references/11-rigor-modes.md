# Rigor Modes

Choose the least expensive mode that can still make the architectural decision safely. Raise rigor when uncertainty, irreversibility, blast radius, novelty, or coordination cost rises.

## R0 — Orientation

Use for vocabulary clarification or an initial map where no decision will be implemented.

Required:

- Task contract
- Observed facts versus assumptions
- One context diagram or responsibility map
- Candidate pattern names with caveats
- Blocking unknowns

Forbidden:

- Final architecture claims
- Detailed implementation plans
- Framework recommendations presented as decisions

## R1 — Local design

Use for a contained component or command with low blast radius and easy rollback.

Required:

- G0–G3
- Two candidates or one candidate plus a justified baseline
- State owner and dependency direction
- One success flow and one failure flow
- Component contract
- Unit/contract test plan

May omit:

- Deployment view when there is no deployment change
- Full ATAM review
- Context map when there is one vocabulary and one boundary

## R2 — Subsystem design

Use for a subsystem, compiler pass family, CLI/TUI application, protocol implementation, service, or agent workflow.

Required:

- G0–G7
- At least three quality-attribute scenarios
- Candidate matrix
- Static, dynamic, data, and runtime views
- Timeout/cancellation/recovery behavior
- ADRs for significant decisions
- Vertical implementation slices
- Architecture conformance checks

## R3 — Enterprise or cross-domain architecture

Default for broad requests spanning domains, teams, persistence, extensibility, or multiple runtimes.

Required:

- Full workflow and all gates
- Strategic boundary/context analysis
- At least five quality-attribute scenarios
- At least three candidates including a do-less baseline
- Lightweight ATAM review with sensitivity and tradeoff points
- Trust/deployment/recovery views
- Migration and compatibility strategy
- Complete traceability ledger
- Negative and adversarial evaluation cases
- Independent review or review-agent pass

## R4 — High-assurance or safety/security critical

Use where failure may cause serious security, safety, legal, financial, or irreversible data harm.

R4 requires domain-specific assurance standards beyond this skill. This skill may structure the work but SHALL NOT claim certification or sufficiency.

Required in addition to R3:

- Named governing standard or assurance case method
- Formalized hazards/threats
- Explicit risk acceptance authority
- Independent verification
- Reproducible evidence and configuration control
- Formal or model-based analysis where proportionate
- Rollback/fail-safe behavior
- Audit trail for decisions and test evidence

## Escalation triggers

Raise one or more levels when any applies:

- More than one bounded context or semantic authority
- More than one process, host, trust zone, or persistent store
- Irreversible migration or protocol compatibility commitment
- User-provided constraints conflict or are incomplete
- Concurrency, nondeterminism, retries, or partial failure matter
- Third-party plugins or untrusted inputs cross the boundary
- Long-running autonomous agents can execute side effects
- Performance requirements depend on unmeasured assumptions
- A wrong decision would require broad rewrites

## De-escalation criteria

Lower rigor only when the decision is:

- Local and reversible
- Covered by a stable existing architecture
- Low-risk and well tested
- Not introducing a new boundary, state owner, protocol, or execution model

Record the rationale for de-escalation.

## Output budgets

Rigor controls evidence and completeness, not word count. Use terse tables and diagrams rather than omitting required reasoning.

| Mode | Typical candidate count | Quality scenarios | ADRs | Review |
| --- | ---: | ---: | ---: | --- |
| R0 | 1–2 sketches | 0–1 | 0 | Self-check |
| R1 | 2 + baseline | 2 | 0–1 | Self-check |
| R2 | 2–3 + baseline | 3–5 | 1–4 | Structured review |
| R3 | 3+ including baseline | 5+ | As needed | Independent/red-team |
| R4 | As assurance case requires | Hazard-driven | Controlled | Independent authority |
