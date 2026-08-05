# Component Contract: <CMP-NNN / name>

## Use this template

Use when a component owns an independently testable capability or boundary.
Remove unused fields; do not invent interfaces, layers, or failure modes merely
to complete the template.

- Boundary / context:
- Classification: semantic core | application coordinator | adapter | projection | infrastructure | policy | scheduler | parser | validator | other

## Purpose

<One precise responsibility.>

## Inputs

| Input | Type/schema | Preconditions | Authority |
|---|---|---|---|
| | | | |

## Outputs

| Output | Type/schema | Postconditions | Consumer |
|---|---|---|---|
| | | | |

## Invariants

1. <invariant>

## State

- Owned state:
- Lifetime:
- Persistence:
- Consistency:

## Dependencies

- Allowed:
- Forbidden:
- Side-effect ports:

## Failure contract

| Error class | Cause | Caller action | Retryable | Observable signal |
|---|---|---|---|---|
| | | | | |

## Concurrency and cancellation

- Execution model:
- Synchronization:
- Cancellation point:
- Backpressure/resource bound:

## Idempotency and replay

<keys, deduplication, ordering, replay semantics>

## Security and trust

<input trust, validation, authority, sensitive data, privilege>

## Test seam

<unit, contract, property, model, fault, or integration test>

Record the observable effect and final diagnostic/report checks separately when
an agent or tool executes the component workflow.
