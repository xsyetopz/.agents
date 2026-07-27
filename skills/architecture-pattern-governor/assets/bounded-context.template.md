# Bounded Context: <Name>

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
