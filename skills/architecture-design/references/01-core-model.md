# Canonical Vocabulary and Universal Decomposition Model

> Locally authored guidance, not a primary source or generated snapshot; source gap: live verification of standards, provider behavior, and other current claims against the [bibliography](09-bibliography.md) is required before relying on them.

## 1. Distinguish the levels of design language

| Term | Meaning | Evidence required |
| --- | --- | --- |
| Requirement | A needed capability, constraint, or quality | User statement, contract, standard, observed system need |
| Quality attribute | A measurable property of behavior under a scenario | Scenario and response measure |
| Architectural force | A pressure that makes one design consequence preferable to another | Requirement, risk, environment, economics, team topology |
| Architectural style | A family of component, connector, and constraint arrangements | Structural and behavioral correspondence |
| Pattern | A reusable problem–forces–solution–consequences relationship | Preconditions and tradeoffs hold in this context |
| Tactic | A localized design move used to affect a quality attribute | Expected mechanism and measurable effect |
| Framework | Reusable code and conventions that embody some patterns | API/runtime constraints, not merely popularity |
| Architecture decision | A consequential choice difficult or expensive to reverse | Alternatives, forces, decision, consequences |
| Module | A static implementation unit | Cohesion and dependency rule |
| Component | A runtime or replaceable responsibility unit | Contract and interaction |
| Boundary | A line across which semantics, ownership, trust, deployment, or failure behavior changes | Explicit reason and contract |

Never treat these as synonyms.

## 2. Universal four-part decomposition

Many systems can be reasoned about through four roles. These are not mandatory class names.

1. **Semantic core**
   - Authoritative concepts, rules, state, transformations, and invariants.
   - Answers: “What is true?” and “What transitions are valid?”

2. **Control / coordination**
   - Converts stimuli into ordered operations, schedules work, manages transactions or workflows, and selects policies.
   - Answers: “What happens next, under whose authority?”

3. **Projection / representation**
   - Produces views, diagnostics, serialized forms, reports, read models, telemetry, or generated artifacts.
   - Answers: “How is state or a result made observable or consumable?”

4. **Ports / effects**
   - Interfaces to files, networks, clocks, databases, processes, devices, models, tools, and external services.
   - Answers: “Where does the system touch an environment it does not control?”

A valid architecture may combine or multiply these roles. The model is useful only when it clarifies ownership and flow.

## 3. MVC and its relatives

### Classic MVC

- **Model:** application-domain state and behavior.
- **View:** display of model state.
- **Controller:** interprets user interaction and changes model/view behavior.
- Often includes observation from model to views and direct controller/view collaboration.

### MVP

- Presenter mediates between passive or supervised view and model.
- Useful when view testability or platform isolation dominates.

### MVVM

- View binds to a view-model that exposes state and commands.
- Useful where a binding runtime is a real architectural constraint.

### MVU / Elm Architecture

- Model is immutable application state.
- Update is a total or controlled state-transition function over messages.
- View is a pure or mostly pure projection.
- Effects are returned as commands and fed back as messages.

### Presentation Model

- A UI-independent representation of screen state and behavior.
- Useful when multiple renderers or complex UI state need deterministic tests.

### PAC

- Hierarchical agents, each split into presentation, abstraction, and control.
- Useful for complex interactive systems with recursive composition.

### Required caution

MVC is not a synonym for “data, logic, output.” The architecture must show independent semantic state, a representation, and a real interaction/control role. For compilers, runtimes, and protocols, pipeline, machine, dataflow, interpreter, or ports-and-adapters models often explain the dominant forces better.

## 4. DDD vocabulary

### Domain

A sphere of knowledge or activity to which the software is applied.

### Model

A selective abstraction that explains and solves domain problems. A model is not a complete copy of reality.

### Ubiquitous language

The shared language used in discussion, documentation, tests, and code within a bounded context.

### Bounded context

A boundary inside which a particular model and vocabulary are consistent and applicable.

### Context map relationships

- Partnership
- Shared kernel
- Customer–supplier
- Conformist
- Anti-corruption layer
- Open host service
- Published language
- Separate ways
- Big ball of mud

### Tactical building blocks

- Entity
- Value object
- Aggregate and aggregate root
- Domain event
- Domain service
- Factory
- Repository
- Specification

These are optional. The strategic model can be useful without tactical object patterns.

## 5. Boundary types

A boundary MUST be justified by at least one of these changes:

| Boundary | What changes across it |
| --- | --- |
| Semantic | Vocabulary, invariants, interpretation |
| Ownership | Team or component authority over state |
| Trust | Identity, privilege, validation responsibility |
| Transaction | Atomicity or consistency guarantee |
| Deployment | Process, host, region, device, release cadence |
| Failure | Independent failure and recovery behavior |
| Performance | Latency, throughput, locality, memory budget |
| Compatibility | Version, ABI, wire format, target platform |
| Lifecycle | Creation, retention, migration, deletion |

A directory boundary without one of these reasons is not necessarily architectural.

## 6. State ownership

Every mutable fact MUST have one authoritative owner at a given consistency scope.

For each state item record:

- Identity and schema
- Owner
- Readers
- Writers
- Lifetime
- Consistency model
- Persistence model
- Version/migration rule
- Replay/rollback behavior
- Security classification

Red flags:

- Two components both believe they are authoritative.
- Cached projections are edited directly.
- Workflow state is hidden in prompts, UI widgets, logs, or retry queues.
- Configuration and runtime state are conflated.
- Event history and current state disagree without a reconciliation rule.

## 7. Control authority

Name the component that decides:

- Which operation runs
- In what order
- Under what policy
- With which budget
- When to retry, cancel, compensate, or stop
- How work is resumed after failure

Common control models:

| Model | Authority |
| --- | --- |
| Request/response | Request handler or application service |
| Event loop | Dispatcher/update function |
| Pipeline | Driver/pass manager/stage scheduler |
| Workflow | Durable workflow engine |
| Actor | Each actor over its state and mailbox |
| Blackboard | Scheduler over shared knowledge state |
| Agent harness | Orchestrator/policy loop with tool boundary |
| Runtime | Interpreter/JIT/scheduler over machine state |
| Build system | Dependency scheduler over DAG |

“Distributed control” is not an excuse to omit authority. Specify local authority and coordination protocol.

## 8. Dependency direction

Dependencies SHOULD point toward more stable policy and semantic abstractions, while effects implement ports defined by the core or application layer.

A useful default:

```text
interfaces/adapters -> application coordination -> semantic core
infrastructure      -> declared ports         <- application coordination
```

Exceptions are allowed when justified by performance, language/runtime mechanics, generated code, or framework inversion. Record the exception and its consequence.

## 9. Commands, queries, events, and projections

- **Command:** request to perform an operation; may be rejected.
- **Query:** request for information; should not intentionally change domain state.
- **Event:** statement that something occurred; semantics depend on ownership and delivery guarantees.
- **Projection:** derived representation optimized for a consumer.
- **Notification:** signal that may carry less semantic commitment than a domain event.

Do not call every message an event. Do not call a mutable request an event merely because it is placed on a queue.

## 10. Invariants and contracts

An invariant is a condition that MUST hold over a defined scope. It needs:

- Scope
- Enforcement point
- Concurrency assumptions
- Failure behavior
- Verification method

Examples:

- Compiler IR remains well-typed after every verified pass.
- A workflow step is committed at most once per idempotency key.
- A binary decoder never reads beyond the declared frame boundary.
- An agent tool call cannot exceed granted capability or budget.
- A TUI model transition is deterministic for a given message and state.

## 11. Quality-attribute scenario form

Use this exact structure:

```text
QA-ID:
Source:
Stimulus:
Environment:
Artifact:
Response:
Response measure:
Priority:
Evidence/validation:
```

Example:

```text
QA-PERF-01
Source: interactive CLI user
Stimulus: requests completion for a 100k-file repository
Environment: warm index, laptop-class machine
Artifact: completion subsystem
Response: returns ranked candidates without blocking input
Response measure: p95 < 100 ms; peak additional RSS < 150 MB
Priority: high
Evidence/validation: benchmark fixture and latency histogram
```

## 12. Architecture views

Use views to answer different questions, not to repeat one box diagram.

| View | Required question |
| --- | --- |
| Context | Who uses or integrates with the system? |
| Static structure | Where are responsibilities and dependencies? |
| Dynamic | What happens in a scenario over time? |
| State/data | What is authoritative, derived, persistent, or versioned? |
| Runtime/concurrency | What executes concurrently and how is it controlled? |
| Deployment | Where does it run and fail? |
| Security | Where are trust, identity, privilege, and validation boundaries? |
| Evolution | How can it be extended, migrated, or replaced? |

## 13. The minimum architecture thesis

A defensible design can be summarized as:

> Because **forces and evidence**, we assign **state and responsibilities** to **components/boundaries**, connected by **contracts and control flow**, accepting **consequences**, and verify the result through **measures and tests**.

If any bold phrase is missing, the architecture is incomplete.

## Sources

- [Package bibliography](09-bibliography.md); verify the linked source record before relying on current or external claims.
