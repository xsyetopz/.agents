# Bounded Context: <Name>

> Locally authored template guidance, not evidence or a generated snapshot; source gap: record the exact source, revision, retrieval date, claim scope, and live verification result for external or current assertions in the completed artifact.

## Use this template

Use only when domain language, authority, state, and evolution form a real
semantic boundary. Do not create a context to satisfy a pattern checklist.

## Purpose

<Business/domain capability and why it exists.>

## Ubiquitous language

| Term | Meaning in this context | Invariant / rule | Conflicting external meaning |
|---|---|---|---|
| | | | |

## Authority

- Decisions owned:
- State owned:
- Facts published:
- Commands accepted:
- Queries answered:

## Domain model

### Entities and identity

- <entity>: <identity and lifecycle>

### Value objects

- <value>: <equality and validation>

### Aggregates / consistency boundaries

- <aggregate>: <invariants protected and transaction boundary>

Do not create an aggregate merely because tables are related.

## External relationships

| Other context | Relationship | Contract | Translation / anti-corruption rule |
|---|---|---|---|
| | | | |

## Failures and evolution

- Versioning:
- Idempotency:
- Retry/compensation:
- Migration:
- Deprecation:

## Verification

- Contract/evaluation:
- Cross-context translation test:
- Failure and migration evidence:
