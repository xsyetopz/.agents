# Artifact Contracts

The templates in `assets/` are normative starting points. Remove unused sections only with an explicit `Not applicable — reason` entry when the omission could otherwise hide risk.

## 1. Architecture report contract

Required headings:

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

Required identifiers:

- Objectives: `OBJ-001`
- Requirements: `REQ-001`
- Constraints: `CON-001`
- Exclusions: `EXC-001`
- Quality scenarios: `QA-CATEGORY-001`
- Components: `CMP-001`
- Interfaces/contracts: `IF-001`
- Risks: `RISK-001`
- Assumptions: `ASM-001`
- Decisions/ADRs: `ADR-001`
- Verification items: `VER-001`
- Slices: `SLICE-001`

## 2. Task contract

```markdown
## Task Contract

### Objective
- OBJ-001: ...

### Deliverable
- ...

### Requirements
- REQ-001: ...

### Constraints
- CON-001: ...

### Exclusions
- EXC-001: ...

### Definition of done
- ...
```

The objective MUST preserve the user's language where precision matters.

## 3. Evidence and uncertainty ledger

```markdown
| ID | Class | Statement | Source/observation | Impact | Validation |
|---|---|---|---|---|---|
| E-001 | FACT | ... | file/test/spec | high | already established |
| ASM-001 | ASSUMED | ... | reason | high if false | experiment/question |
| U-001 | UNKNOWN | ... | unavailable | medium | inspect X |
```

Never use confidence percentages without calibration evidence. Prefer impact and validation method.

## 4. Domain glossary

```markdown
| Term | Meaning in this context | Not to be confused with | Source/owner |
|---|---|---|---|
| ... | ... | ... | ... |
```

A bounded context MUST have a glossary or equivalent schema/specification when terminology is a material risk.

## 5. Boundary record

```markdown
### Boundary: <name>
- Type: semantic | ownership | trust | transaction | deployment | failure | performance | compatibility | lifecycle
- Inside responsibilities:
- Outside responsibilities:
- Owned state:
- Inbound contracts:
- Outbound contracts:
- Translation/validation:
- Failure isolation:
- Versioning/migration:
- Justifying forces:
```

## 6. Quality-attribute scenario

```markdown
### QA-<CATEGORY>-<NNN>: <name>
- Source:
- Stimulus:
- Environment:
- Artifact:
- Response:
- Response measure:
- Priority: critical | high | medium | low
- Architectural response:
- Verification:
```

A quality attribute without a measure is a preference, not a testable requirement.

## 7. Candidate record

```markdown
### Candidate <letter>: <name>
- Primary shape:
- Secondary patterns/tactics:
- State owner:
- Control authority:
- Dependency direction:
- Critical path:
- Failure/cancellation model:
- Extension model:
- Benefits:
- Liabilities:
- Assumptions:
- Hard-veto check:
- Replacement threshold:
```

## 8. Decision matrix

```markdown
| Criterion | Weight | Baseline | Candidate A | Candidate B | Evidence/notes |
|---|---:|---:|---:|---:|---|
| Semantic correctness | 5 |  |  |  |  |
```

Do not score an unknown as neutral. Mark `?` and resolve it or lower the verdict.

## 9. Component contract

```markdown
### CMP-<NNN>: <responsibility-bearing name>
- Purpose:
- Owns:
- Does not own:
- Inputs:
- Outputs:
- Preconditions:
- Postconditions:
- Invariants:
- Dependencies:
- Forbidden dependencies:
- Error taxonomy:
- Concurrency model:
- Idempotency/replay:
- Observability:
- Security assumptions:
- Test seam:
```

## 10. Interface contract

```markdown
### IF-<NNN>: <name>
- Interaction type: call | command | query | event | stream | job | protocol
- Producer/owner:
- Consumer:
- Schema:
- Semantics:
- Versioning:
- Ordering:
- Delivery:
- Timeout:
- Cancellation:
- Idempotency:
- Error mapping:
- Security:
- Telemetry:
- Contract tests:
```

## 11. ADR contract

One ADR per consequential decision:

```markdown
# ADR-<NNN>: <decision title>

- Status: proposed | accepted | rejected | superseded | deprecated
- Date: YYYY-MM-DD
- Deciders:
- Related: REQ-..., QA-..., RISK-...

## Context
Facts, forces, constraints, and problem. Separate assumptions.

## Decision drivers
Ranked list.

## Considered options
At least baseline and one material alternative.

## Decision
One clear choice.

## Consequences
Positive, negative, operational, migration, and verification consequences.

## Risks and mitigations
...

## Verification
How the decision will be tested or reviewed.

## Revisit triggers
Thresholds or evidence that would reopen the decision.
```

An ADR MUST NOT be a retrospective justification that hides rejected options.

## 12. Critical-flow contract

For each critical flow include:

- Trigger and actor
- Preconditions
- Ordered participants
- State reads/writes
- Side effects
- Success result
- Invalid input
- Dependency failure
- Timeout/cancellation
- Retry/compensation
- Observability
- Security checks

Use a sequence diagram where ordering matters and a state diagram where lifecycle matters.

## 13. Implementation slice

```markdown
### SLICE-<NNN>: <name>
- Architecture hypothesis proven:
- User-visible or externally observable behavior:
- Real input:
- Semantic rule/state transition:
- Port/effect:
- Output:
- Failure path:
- Tests:
- Instrumentation:
- Explicitly excluded:
- Exit criteria:
```

A slice that only creates directories, interfaces, mocks, or framework setup does not prove the architecture.

## 14. Verification matrix

```markdown
| Verification ID | Requirement/QA | Decision/component | Method | Fixture/environment | Pass criterion |
|---|---|---|---|---|---|
| VER-001 | REQ-001 | CMP-002 / ADR-001 | property test | ... | ... |
```

Each critical requirement must have at least one verification row.

## 15. Risk register

```markdown
| ID | Hazard | Trigger | Effect | Likelihood | Impact | Detection | Mitigation | Owner/status |
|---|---|---|---|---|---|---|---|---|
```

Do not use `low` likelihood to dismiss a catastrophic impact without reasoning.

## 16. Traceability matrix

```markdown
| Objective/requirement | Quality scenario | Decision | Component/interface | Verification |
|---|---|---|---|---|
| OBJ-001 / REQ-001 | QA-COR-001 | ADR-001 | CMP-001 / IF-001 | VER-001 |
```

Orphan decisions and orphan components are architecture smells.

## 17. Architecture conformance rules

Represent mechanically checkable rules where possible:

- Dependency direction and forbidden imports
- Public API ownership
- No infrastructure types in domain/core packages
- Only one writer to authoritative state
- All effects go through declared ports
- All message schemas are versioned
- No unbounded queue or retry loop
- No tool/plugin access outside declared capabilities
- No compiler pass leaves unverified IR at a named boundary

Use language-native architecture tests, static analysis, lint rules, build graph checks, or custom scripts.
