# ADR-<NNN>: <Decision title>

> Locally authored template guidance, not evidence or a generated snapshot; source gap: record the exact source, revision, retrieval date, claim scope, and live verification result for external or current assertions in the completed artifact.

## Use this template

Use for one architecturally significant decision. Replace every placeholder with
repository evidence; remove sections that do not apply instead of filling them
with generic prose.

- Status: Proposed | Accepted | Rejected | Superseded
- Date: <YYYY-MM-DD>
- Deciders: <roles>
- Supersedes / superseded by: <ADR or none>
- Related: <OBJ/REQ/QA/RISK IDs>

## Context

<Observed facts, forces, and uncertainty. Avoid solution language where possible.>

## Decision drivers

1. <quality scenario or hard constraint>
2. <quality scenario or hard constraint>

## Considered options

### Option A - Do-less baseline

- Description:
- Benefits:
- Liabilities:
- Evidence:

### Option B - <name>

<same fields>

The do-less baseline is a design comparison, not an acceptance baseline or a
waiver for unresolved audit findings.

## Decision

<One architecturally significant decision.>

## Rationale

<Why this option best fits the ranked drivers.>

## Consequences

### Positive

- <consequence>

### Negative

- <accepted cost or limitation>

### Risks and mitigations

- <risk -> mitigation / experiment>

## Compliance and verification

- <test, review, static rule, benchmark, or operational measure>
- Check integrity: no ignore or lint/check exclusion, disabled rule/provider/job,
  lowered severity or threshold, altered baseline, `allow-failure`,
  `continue-on-error`, excluded failing path, or weakened/deleted test/check was
  used to obtain a green result.
- If a tool is wrong, attach a minimal reproducer (tool/version, exact command
  and configuration, input, output, and exit code) and explicit policy-change
  authorization; keep the architecture gate blocked while the check is
  weakened.

Record observed commands, outputs, and exit codes. Evaluate implementation
effects separately from the review summary.

## Exit criteria

<Conditions under which this decision must be revisited.>
