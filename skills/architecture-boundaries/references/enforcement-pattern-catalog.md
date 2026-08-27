# Architecture Pattern Selection Catalog

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against authority sources (see `enforcement-sources.md`) is required.

Select an architecture from product constraints, operating model, and enforceable dependency rules--not fashion, framework defaults, or a desire to look "enterprise." A pattern is accepted only when its boundary can be named, its invariants can be tested or reviewed, and its operational cost has an accountable owner. Prefer the smallest coherent model; add a boundary only when it protects a real change, failure, scaling, security, data, or ownership concern.

## Contents

- Selection baseline; modular monolith; layered/clean/hexagonal/ports-adapters
- DDD bounded contexts; event-driven; CQRS/event sourcing; pipeline/data-oriented
- Actor/reactive/concurrency; plugins; microservices
- Strangler, anti-corruption layer, saga, and transactional outbox
- Functional core/imperative shell; shared design-pattern guardrails
- Pattern combinations; ADR template

## Selection Baseline

- Start with a modular monolith for one product and one deployment unit. It is the default, not a transitional embarrassment.
- Use language- and ecosystem-idiomatic module systems before introducing generic abstractions, service locators, dependency-injection containers, or repository layers.
- Treat network calls, durable messages, databases, filesystems, clocks, processes, and third-party SDKs as I/O boundaries with explicit failure and lifecycle semantics.
- Map dependency rules to the compiler, package manager, visibility model, and test topology supported by each language family.
- A pattern must make a material constraint easier to enforce. If it only adds types, folders, interfaces, handlers, or ceremony, reject it.

## Modular Monolith

**Use when:** one deployable can meet availability, scaling, release, and ownership needs; capabilities share transactions or data; the team needs fast local development and coherent end-to-end testing.

**Required invariants:**

- Modules align to durable capabilities or bounded contexts, not technical buckets.
- Each module exposes a narrow public contract; sibling modules never import private paths or mutate each other's persistence directly.
- Dependency direction is acyclic and is checked by build visibility, package rules, linting, or architecture tests.
- Composition occurs at an application boundary; modules use explicit composition rather than globals or registries.

**Operational trade-offs:** simple deployment and observability, inexpensive local transactions, and low latency; releases and resource limits remain coupled, so discipline is required to prevent a distributed-monolith-shaped codebase.

**Reject when:** independently deployed, scaled, regulated, or failure-isolated workloads are already necessary and cannot be achieved within one process; or module boundaries cannot be enforced by the language and build topology.

## Layered, Clean, Hexagonal, and Ports-and-Adapters

**Use when:** business or application policy must survive changes to delivery mechanisms, persistence, vendors, or frameworks. Apply ports-and-adapters at real I/O boundaries; use strict layers only where they express a dependency rule.

**Required invariants:**

- Dependencies point inward: delivery and infrastructure depend on application/domain policy.
- Ports are owned by the policy that needs them and describe required behavior, not a database, ORM, HTTP client, or vendor API.
- Adapters translate protocol, persistence, retry, error, authentication, and lifecycle semantics at the edge.
- Entrypoints and composition roots wire concrete adapters; domain/application code does not import framework or transport types.
- Each layer or port has behavior, ownership, and a test boundary. Pass-through wrappers are removed.

**Operational trade-offs:** replacement and focused testing improve, but translation code and abstraction cost increase. Debugging crosses boundaries and requires good tracing and error context.

**Reject when:** code is primarily a pipeline, compiler, simulation, UI state machine, or simple CRUD workflow with no meaningful inward policy; or interfaces merely mirror one implementation.

## Domain-Driven Design and Bounded Contexts

**Use when:** different business areas use overloaded terms, change independently, have distinct rules, or need explicit ownership and integration contracts.

**Required invariants:**

- A bounded context has a named model, language, owner, public contract, and persistence authority.
- Terms retain one meaning within a context; translation happens at explicit integration boundaries.
- Aggregates protect stated consistency rules; they are not object graphs loaded by default.
- Cross-context integration uses published contracts, events, or an orchestration owner--not shared tables, private imports, or leaked entities.

**Operational trade-offs:** reduces semantic coupling and makes ownership legible, but demands domain discovery, contract versioning, and deliberate integration work.

**Reject when:** the domain is small and vocabulary is genuinely shared; a context would contain only renamed CRUD types; or no team can own the boundary and its integration contract.

## Event-Driven Architecture

**Use when:** consumers need asynchronous reactions, fan-out, decoupled timing, auditability, or integration across durable ownership boundaries.

**Required invariants:**

- Event names describe completed facts in the publisher's language; commands, queries, and implementation events are not disguised as domain events.
- Message schemas are versioned and compatibility rules are explicit.
- Producers and consumers are idempotent; ordering, duplication, retries, dead-letter handling, retention, and replay ownership are documented.
- Delivery guarantees are stated precisely. Assume at-least-once unless the transport and end-to-end design prove otherwise.
- Observability includes correlation, causation, consumer lag, failure rate, and poison-message visibility.

**Operational trade-offs:** enables independent consumption and temporal decoupling, but introduces eventual consistency, operational tooling, schema governance, and incident complexity.

**Reject when:** a synchronous call or local transaction is sufficient; the event is only an internal method call; or no owner can operate the broker, replay process, and schema evolution.

## CQRS and Event Sourcing

**Use when:** write-side invariants and read-side access patterns are materially different, or when an append-only business history, replay, temporal audit, and deterministic reconstruction are genuine requirements.

**Required invariants:**

- CQRS separates command intent from read models without necessarily requiring separate services or datastores.
- Commands validate against authoritative state and emit explicit outcomes; read models are disposable projections with measured freshness.
- Event-sourced streams have stable event schemas, stream identity, optimistic concurrency rules, upcasters/migration policy, snapshots where justified, and a recovery/replay procedure.
- Projection consumers are idempotent, observable, rebuildable, and remain downstream projections rather than untracked state owners.

**Operational trade-offs:** read optimization, audit history, and temporal reasoning improve; debugging, privacy deletion, schema evolution, backfills, and eventual consistency become expensive operational concerns.

**Reject when:** conventional transactional state plus an audit log satisfies the requirement; read/write differences are speculative; or the organization cannot support event retention, replay, and projection repair.

## Pipeline and Data-Oriented Design

**Use when:** work naturally flows through ordered transformations over data: compilers, media, ETL, numerical workloads, simulation, streaming, protocol processing, and high-throughput systems.

**Required invariants:**

- Stages have explicit input/output contracts, ownership of mutation, failure behavior, and backpressure or capacity semantics.
- Data representation and locality drive hot-path design; measure before introducing batching, pools, SIMD, or lock-free structures.
- Stage ordering, retryability, determinism, and side effects are explicit. Isolate I/O stages from pure transformations where possible.
- Each stage can be tested with representative fixtures and production-sized performance evidence where performance is a requirement.

**Operational trade-offs:** improves throughput reasoning and profiling, but makes ad hoc cross-stage state and business-object abstractions harmful. Backpressure, partial failure, and data lineage need operational design.

**Reject when:** the primary complexity is business policy and transactional consistency rather than transformation flow; or stages only wrap one another without distinct data ownership.

## Actor, Reactive, and Concurrency-Oriented Design

**Use when:** independent stateful entities, high concurrency, asynchronous I/O, resilience boundaries, supervision, or flow control dominate the problem.

**Required invariants:**

- State ownership is single-writer: an actor owns its state, or synchronization and invariants are explicitly documented.
- Messages, cancellation, deadlines, mailbox/capacity limits, backpressure, supervision, and restart semantics are designed--not delegated to defaults.
- Blocking work is isolated from event loops, executors, and scheduler threads.
- Shared mutable state, hidden global caches, and fire-and-forget tasks are forbidden unless their lifecycle and failure ownership are explicit.
- Concurrency correctness is proven with race, load, failure, and shutdown tests appropriate to the runtime.

**Operational trade-offs:** isolates failure and improves scalability for suitable workloads, but increases nondeterminism, observability needs, test difficulty, and resource-management risk.

**Reject when:** ordinary structured concurrency with scoped tasks and clear ownership is sufficient; actor boundaries only imitate classes; or no operational model exists for overload and failure.

## Plugin Architecture

**Use when:** independently developed extensions must be discovered, versioned, enabled, upgraded, or isolated without changing the host's core policy.

**Required invariants:**

- The host owns a small, versioned extension contract, lifecycle, compatibility policy, discovery mechanism, and failure boundary.
- Plugins declare capabilities and permissions; loading is explicit, authenticated where relevant, and observable.
- Plugin APIs avoid leaking host internals and define resource, threading, shutdown, and error behavior.
- The host remains useful with a plugin absent, disabled, incompatible, or failed.

**Operational trade-offs:** supports extensibility and independent delivery, but creates compatibility, security, support, packaging, and lifecycle obligations.

**Reject when:** all extensions ship and evolve with the host; variation can be implemented as a normal module behind a stable internal interface; or plugins would execute untrusted code without a credible isolation model.

## Microservices

**Use when:** a workload needs independently managed deployment, scaling, reliability isolation, data ownership, security/regulatory isolation, or team autonomy that one deployable cannot responsibly provide.

**Required invariants:**

- A service owns its data and business capability; other services use published APIs or events.
- Every cross-process contract specifies authentication, authorization, timeout, cancellation, retries, idempotency, versioning, rate limits, observability, and failure behavior.
- Services are independently buildable, deployable, monitored, and recoverable with an accountable operating owner.
- Distributed consistency is explicit; workflows tolerate partial failure and delayed delivery.

**Operational trade-offs:** allows independent evolution and fault/scaling boundaries, but multiplies deployment, security, latency, test, data-consistency, and incident-response costs.

**Reject when:** the motivation is team size, folder organization, trend-following, or anticipated scale; shared transactions and rapid coordinated change remain dominant; or platform operations cannot provide service-level reliability controls.

## Migration and Distributed-Consistency Patterns

### Strangler Fig

**Use when:** replacing a legacy system incrementally while preserving a stable external contract.

**Required invariants:** route ownership is explicit; each migrated capability has parity criteria and observability; old and new paths share an explicit parity rule; and each cutover has a rollback or forward-repair procedure.

**Operational trade-offs:** lowers replacement risk and enables incremental learning, but temporarily increases routing, data synchronization, and operational complexity.

**Reject when:** the legacy boundary cannot be intercepted, parallel operation would violate correctness or security, or a bounded replacement is cheaper and safer.

### Anti-Corruption Layer

**Use when:** integrating with a legacy or external model while keeping its terminology, lifecycle, errors, and invariants at the boundary.

**Required invariants:** translation is owned at the boundary; foreign types remain outside the local model; mappings preserve failure and data-quality semantics; and changes are contract-tested.

**Operational trade-offs:** prevents semantic contamination but adds mapping and maintenance cost.

**Reject when:** the models are truly the same and an adapter would only rename fields; or the boundary has no owner to maintain contract drift.

### Saga

**Use when:** a business workflow spans independently committed resources and requires explicit compensation or forward recovery.

**Required invariants:** each step defines idempotency, durable progress, timeouts, retry policy, compensation or terminal failure policy, correlation, and human-repair ownership. Compensations are business actions, not presumed database rollbacks.

**Operational trade-offs:** coordinates distributed work without pretending there is a global transaction, but creates temporal complexity and reconciliation work.

**Reject when:** one local transaction can enforce the invariant; steps cannot be compensated or safely forward-repaired; or the business cannot define acceptable partial outcomes.

### Transactional Outbox

**Use when:** state changes and published messages remain durable and consistent under crash/retry conditions.

**Required invariants:** the business write and outbox record commit atomically; relay publication is idempotent; consumers deduplicate; retention and replay are managed; and monitoring detects backlog and publish failure.

**Operational trade-offs:** improves delivery reliability without distributed transactions, but adds storage, relay, ordering, and operational burden.

**Reject when:** no durable message publication is required; or a single system already provides an end-to-end atomic, observable guarantee that satisfies the contract.

## Functional Core, Imperative Shell

**Use when:** policy can be expressed as deterministic transformations while I/O, time, randomness, and lifecycle are edge concerns. It complements--not replaces--modular, layered, or pipeline boundaries.

**Required invariants:**

- The core receives explicit data and returns values, decisions, or declared effects; it does not read globals, clocks, files, networks, or framework state.
- The shell owns I/O sequencing, resource lifecycle, retries, logging, and translation of effects into concrete adapters.
- Domain invariants are tested through deterministic examples and property-based tests where the value space warrants it.

**Operational trade-offs:** makes policy easy to test and reason about, but excessive purity can hide lifecycle concerns in opaque effect plumbing or force awkward abstractions.

**Reject when:** the core would only pass framework objects through wrappers; the problem is intrinsically stateful and lifecycle-heavy with no stable pure policy; or the language/runtime offers a clearer idiomatic boundary.

## Shared design-pattern guardrails

Use a named design pattern only when its force and invariant are visible in the
code. Keep the implementation idiomatic for the language family; a pattern
catalog is not a license to create a class hierarchy.

| Pattern | Use when | Enforce | Reject when |
| --- | --- | --- | --- |
| **Strategy / Policy** | One decision has multiple replaceable algorithms or rules. | The owner defines a small capability contract; selection and policy stay outside the algorithms; each strategy has independent examples or property tests. | Variants are never selected, differ only by constants, or an interface hides one implementation. |
| **Adapter / Translator** | A foreign API, schema, protocol, or lifecycle must meet a local contract. | Translation owns validation, error mapping, retries, resource lifecycle, and telemetry; foreign types do not cross inward. | The adapter only renames identical fields or becomes a second domain/service layer. |
| **State machine** | Valid behavior depends on explicit lifecycle states and transitions. | States, events, guards, illegal transitions, persistence/recovery, and side effects are explicit and exhaustively tested. | Boolean flags or callbacks already express the lifecycle clearly, or the machine becomes an unbounded event switch. |
| **Decorator / Middleware** | Cross-cutting behavior composes around a stable capability. | Ordering, short-circuiting, error, cancellation, and resource ownership are explicit; decorators do not change the contract silently. | Middleware is a hidden global pipeline, duplicates business policy, or creates untraceable nesting. |
| **Observer / Publish-subscribe** | Multiple consumers need decoupled notification of a stable fact. | Subscriber lifecycle, delivery, ordering, duplication, backpressure, and failure isolation are owned; events remain facts, not commands in disguise. | A direct call is clearer, consumers need immediate authoritative results, or no owner can operate the subscription boundary. |
| **Repository / Unit of Work** | A domain needs a persistence boundary with transaction or aggregate semantics. | The domain-facing contract expresses queries and invariants, not ORM methods; transaction, consistency, identity, and error behavior are tested. | The type merely forwards CRUD calls, leaks ORM entities, or adds an interface for one unreplaceable database. |
| **Factory** | Construction selects a valid product by configuration, platform, plugin, or lifecycle policy. | The factory owns selection and validation; products expose a stable capability; construction failures and cleanup are explicit. | It wraps a direct constructor, hides dependency wiring, or becomes a global service locator. |

## Pattern-Combination Rules

1. Start with modular-monolith boundaries. Add ports-and-adapters at external I/O; do not use ports to turn every internal call into an interface.
2. A bounded context may be a module first and a service later. A network boundary is justified by operating constraints, not DDD vocabulary alone.
3. Layered and hexagonal rules may coexist: layers organize policy direction; ports define policy-to-I/O seams. Keep the composition root outside both.
4. Event-driven integration is appropriate between contexts or services when temporal decoupling is required. It does not replace synchronous commands that need immediate authoritative decisions.
5. CQRS can be local to one module or service. Event sourcing is optional and requires independent justification beyond CQRS.
6. Use an outbox for durable state-to-event publication. Use a saga only for a multi-resource business workflow; neither is a default for ordinary requests.
7. Pipeline and actor models may coexist when actors own partitions and pipelines transform their data. Define who owns ordering, capacity, and failure; do not mix shared mutable state into both.
8. Functional core/imperative shell is an internal design technique. It must preserve the selected module, context, and deployment boundaries rather than create a parallel architecture.
9. Plugin contracts belong at host extension boundaries, not between ordinary internal modules.
10. During migration, use anti-corruption layers at foreign-model boundaries and strangler routing at replacement boundaries. Remove both when the legacy boundary is gone unless a durable external integration remains.

## Architecture Decision Record Template

```md
# ADR-<number>: <decision in outcome form>

## Status
Proposed | Accepted | Superseded by ADR-<number>

## Context
Describe the verified product, ownership, data, deployment, failure, and operational constraints. Name the affected capability and public contracts.

## Decision
State the selected pattern, boundary owner, dependency direction, composition point, and non-negotiable invariants.

## Consequences
List operational responsibilities, observability, security, migration, test, and on-call implications. Distinguish accepted costs from unresolved risks.

## Alternatives Rejected
For each plausible alternative, state the concrete constraint it fails or the cost that makes it unjustified.

## Enforcement and Proof
Name the package/module rules, architecture checks, contract tests, runtime signals, and review owner that prove the decision remains true.

## Exit or Review Trigger
State the measurable condition that requires revisiting, replacing, or removing this decision.
```

## Sources

- Architecture source map (see `enforcement-sources.md`); verify the linked source record before relying on current or external claims.
