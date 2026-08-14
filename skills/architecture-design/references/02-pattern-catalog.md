# Pattern Catalog

> Locally authored guidance, not a primary source or generated snapshot; source gap: live verification of standards, provider behavior, and other current claims against the [bibliography](09-bibliography.md) is required before relying on them.

Use this catalog to generate and test candidates. It is not a menu from which the most fashionable item is selected.

For every selected pattern, prove its **problem**, **forces**, **preconditions**, **mechanism**, and **consequences** in the current system.

## 1. Layered architecture

**Problem:** Separate responsibilities by abstraction or policy level.

**Use when:** Dependencies can be directed; different concerns evolve at different rates; test seams matter.

**Avoid when:** Every request must cross ceremonial layers; performance demands collapse boundaries; layer names hide feature cohesion.

**Canonical shape:** interface -> application -> domain -> infrastructure abstractions, with infrastructure adapters implementing ports.

**Invariants:** No forbidden upward dependency; domain semantics do not require presentation or storage frameworks.

**Tests:** Dependency rules, layer contract tests, domain tests without infrastructure.

## 2. Hexagonal architecture / ports and adapters

**Problem:** Protect application behavior from input and output technologies.

**Use when:** Multiple interfaces or infrastructure implementations exist; deterministic tests are valuable; external systems are volatile.

**Avoid when:** The system is a small single-purpose adapter; ports simply duplicate every library API.

**Canonical shape:** application core defines purpose-oriented ports; adapters translate protocols and technologies.

**Invariants:** Ports express application conversations, not vendor-specific mechanics; adapters do not own domain policy.

**Tests:** In-memory adapter tests, contract suites shared by adapter implementations.

## 3. Onion / clean architecture

**Problem:** Keep policy independent from mechanisms through inward dependency direction.

**Use when:** Long-lived business or semantic rules must outlast frameworks.

**Avoid when:** “Use-case” classes become pass-through boilerplate; all code is forced into concentric folders without real boundaries.

**Invariants:** Inner policy has no compile-time dependency on outer delivery or infrastructure details.

## 4. Classic MVC

**Problem:** Separate domain state, its display, and interactive control.

**Use when:** Interactive software has multiple views or input modes and a model with independent meaning.

**Avoid when:** There is no persistent/semantic model, no interactive feedback loop, or the dominant structure is a pipeline.

**Invariants:** View representation does not become authoritative state; controller does not absorb all domain logic.

## 5. MVP

**Problem:** Isolate presentation behavior from a difficult-to-test view technology.

**Use when:** Passive view interfaces enable deterministic presenter tests.

**Avoid when:** Presenter becomes an application-wide god object or mirrors widgets one-for-one.

## 6. MVVM

**Problem:** Expose UI-ready state and commands through a binding-oriented abstraction.

**Use when:** The UI platform has real binding semantics and observable state.

**Avoid when:** View-model is merely the domain model renamed; binding hides uncontrolled side effects.

## 7. MVU / reducer architecture

**Problem:** Make interactive state transitions explicit and reproducible.

**Use when:** Event-loop applications, TUIs, frontends, editors, or stateful agents benefit from immutable state and message-driven updates.

**Avoid when:** State is huge and copying is uncontrolled; effects bypass the update loop; message types become an unstructured dumping ground.

**Canonical shape:** `Message + Model -> New Model + Effects`; view is a projection; effect results return as messages.

**Invariants:** State changes occur only through update transitions; effects are described at the boundary.

**Tests:** Transition tables, property tests, replay tests.

## 8. Presentation Model

**Problem:** Represent complex presentation state independently of widgets.

**Use when:** Multiple UI technologies or complex enablement/validation rules exist.

**Avoid when:** It duplicates domain state without a projection reason.

## 9. PAC (Presentation–Abstraction–Control)

**Problem:** Compose complex interactive systems from hierarchical cooperating agents.

**Use when:** Independent interactive regions require local control and recursive composition.

**Avoid when:** A simpler component hierarchy or MVU loop suffices.

## 10. Pipeline / pipe-and-filter

**Problem:** Transform a stream or representation through ordered, composable stages.

**Use when:** Compilers, ETL, codecs, build steps, analysis tools, and media/data processing have stage-local contracts.

**Avoid when:** Stages require uncontrolled shared mutable state; backtracking and global optimization dominate; stage boundaries force repeated expensive conversions.

**Invariants:** Stage input/output contracts are explicit; ordering constraints are declared; invalid intermediate state is detected.

**Tests:** Stage unit tests, golden tests, end-to-end fixtures, pass-order invariants.

## 11. Pass manager

**Problem:** Schedule analyses and transformations over an intermediate representation.

**Use when:** Multiple compiler/static-analysis passes have dependencies, invalidation rules, nesting, or target-specific pipelines.

**Avoid when:** A fixed three-step transformation needs no reusable analysis or scheduling.

**Invariants:** Required analyses are available; invalidated analyses are not reused; IR verification occurs at declared points.

## 12. Interpreter

**Problem:** Execute a language or rule representation by mapping syntax/IR constructs to behavior.

**Use when:** Semantics must be explicit, inspectable, portable, or dynamically extensible.

**Avoid when:** Direct compilation or table-driven execution is substantially simpler and sufficient.

**Canonical shape:** syntax/IR + environment/store + evaluator/dispatcher + effects.

**Invariants:** Evaluation order, scope, error semantics, and resource limits match the language specification.

## 13. Virtual machine / abstract machine

**Problem:** Define execution through machine state and instruction transitions independent of host details.

**Use when:** Portability, sandboxing, small implementation size, runtime instrumentation, or multi-language hosting matters.

**Avoid when:** The machine abstraction merely wraps host calls without stable semantics.

**Invariants:** Machine state, instruction semantics, validation, traps, memory model, and embedding boundary are specified.

## 14. Visitor

**Problem:** Add operations across a stable object/AST shape without placing every operation on nodes.

**Use when:** Syntax categories are stable and operations proliferate.

**Avoid when:** Node types change frequently; pattern matching or algebraic data types provide clearer exhaustiveness.

## 15. Dataflow / DAG

**Problem:** Express work through dependencies between values or tasks.

**Use when:** Build systems, ML graphs, ETL, spreadsheets, query plans, and schedulers can exploit dependency structure and parallelism.

**Avoid when:** Hidden side effects make dependencies incomplete; cycles lack explicit fixed-point semantics.

**Invariants:** All material dependencies are represented; cache keys include semantic inputs; cycle behavior is defined.

## 16. State machine / statechart

**Problem:** Make legal states and transitions explicit.

**Use when:** Protocols, workflows, devices, UI modes, parsers, and agents have lifecycle constraints.

**Avoid when:** State is fabricated to model simple sequential code; transition guards remain implicit elsewhere.

**Invariants:** Every event in every state has defined behavior or rejection; entry/exit actions and concurrency semantics are explicit.

## 17. Event-driven architecture

**Problem:** Decouple producers and consumers in time, deployment, or ownership.

**Use when:** Independent reaction, fan-out, audit, integration, or asynchronous scaling is required.

**Avoid when:** A direct call is sufficient; ordering, duplication, and eventual consistency are not acceptable or designed.

**Invariants:** Event ownership, schema, ordering scope, delivery guarantee, idempotency, and replay policy are explicit.

## 18. CQRS

**Problem:** Command and query models have materially different requirements.

**Use when:** Task-oriented commands, different read shapes, scaling, security, or consistency models justify separation.

**Avoid when:** CRUD over one model is adequate; duplicated models add more complexity than value.

**Invariants:** Command authority is clear; read-model staleness and reconciliation are defined.

## 19. Event sourcing

**Problem:** Preserve state as a sequence of authoritative events.

**Use when:** Audit, temporal queries, reconstruction, and event-centered domain semantics justify operational complexity.

**Avoid when:** Events cannot be made stable, deletion/privacy requirements conflict, or snapshots/rebuilds are unmanageable.

**Invariants:** Event immutability, versioning, ordering, idempotent projection, snapshot semantics, and correction policy.

## 20. Actor model

**Problem:** Encapsulate concurrent mutable state behind asynchronous message processing.

**Use when:** Independent entities, location transparency, supervision, and message-based concurrency are natural.

**Avoid when:** Cross-actor invariants require constant coordination; request chains obscure latency and failure.

**Invariants:** One actor owns its state; message ordering scope and mailbox bounds are explicit; blocking work is controlled.

## 21. Supervisor–worker

**Problem:** Isolate work units and recover them under explicit policy.

**Use when:** Agents, processes, actors, job runners, and services can fail independently.

**Avoid when:** Retrying non-idempotent work causes corruption; supervision policy is unspecified.

**Invariants:** Restart scope, retry budget, escalation, poison-task handling, and durable progress are explicit.

## 22. Scheduler–executor

**Problem:** Separate deciding what/when to run from performing work.

**Use when:** Builds, workflows, agent harnesses, batch systems, runtimes, and distributed jobs need budgets, queues, priorities, or retries.

**Avoid when:** Scheduler duplicates domain decisions or executor owns hidden scheduling policy.

**Invariants:** Work identity, lease/ownership, cancellation, resource budget, and completion semantics are explicit.

## 23. Blackboard

**Problem:** Coordinate heterogeneous solvers around shared evolving knowledge.

**Use when:** Planning, diagnosis, synthesis, or multi-agent work benefits from opportunistic contributions and a common evidence state.

**Avoid when:** Shared state becomes untyped prompt soup; no authority resolves contradictions.

**Invariants:** Blackboard schema, provenance, conflict resolution, scheduler policy, and completion criteria.

## 24. Orchestrator–workers for AI agents

**Problem:** Bound model-driven work while retaining decomposition and parallelism.

**Use when:** Tasks can be partitioned, tools need policy, and outputs can be independently verified.

**Avoid when:** Agents duplicate work, share no authoritative state, or delegation overhead exceeds task complexity.

**Canonical shape:** task contract -> orchestrator/policy -> bounded workers/tools -> evidence store -> verifier -> result projection.

**Invariants:** User goal is immutable except by user change; tool capabilities are least privilege; budgets and stop conditions are enforced; claims require evidence.

## 25. Workflow / saga

**Problem:** Coordinate long-running multi-step work across transactional boundaries.

**Use when:** Work survives process failure, includes human approval, or needs compensation.

**Avoid when:** A local transaction is available and sufficient.

**Invariants:** Durable state, idempotent steps, timeout, compensation, and manual recovery are explicit.

## 26. Reactor

**Problem:** Demultiplex readiness events to handlers in an event loop.

**Use when:** High-concurrency I/O and a small number of threads are appropriate.

**Avoid when:** Handlers block or CPU-heavy work starves the loop.

## 27. Proactor

**Problem:** Initiate asynchronous operations and process completion events.

**Use when:** Platform async I/O completion is a first-class mechanism.

**Avoid when:** The platform/runtime does not provide useful completion semantics.

## 28. Microkernel / plugin architecture

**Problem:** Keep a stable minimal core while extensions supply variable capabilities.

**Use when:** IDEs, language tools, agents, build systems, and product families need independent extensions.

**Avoid when:** Every plugin requires privileged internal access; versioning and isolation are absent.

**Invariants:** Extension API, lifecycle, capability grants, compatibility, isolation, and failure containment.

## 29. Repository

**Problem:** Present domain-oriented collection access while hiding persistence mechanics.

**Use when:** Aggregate retrieval/persistence semantics differ from raw database operations.

**Avoid when:** It creates generic CRUD abstractions or conceals important query/performance behavior.

## 30. Unit of Work

**Problem:** Track changes and coordinate persistence as one consistency unit.

**Use when:** An application transaction spans multiple domain objects and the persistence mechanism supports it.

**Avoid when:** Long-lived units retain stale state; distributed work is falsely treated as atomic.

## 31. Anti-corruption layer

**Problem:** Prevent an external or legacy model from contaminating the local model.

**Use when:** Integrating incompatible semantics, legacy APIs, vendor schemas, or protocols.

**Avoid when:** Translation adds no semantic value and duplicates a stable shared language.

**Invariants:** Translation direction and lossiness are documented; external identifiers and errors are mapped explicitly.

## 32. Strangler migration

**Problem:** Replace a legacy system incrementally behind a routing boundary.

**Use when:** Big-bang replacement is too risky and behavior can be partitioned.

**Avoid when:** Shared state cannot be separated and dual writes lack reconciliation.

**Invariants:** Routing ownership, source of truth, migration order, compatibility, rollback, and observability.

## 33. Sidecar / adapter process

**Problem:** Add cross-cutting or compatibility behavior without modifying the main process.

**Use when:** Deployment allows co-location and independent lifecycle is valuable.

**Avoid when:** Network/process boundaries add unacceptable latency or failure modes.

## 34. Entity–Component–System

**Problem:** Compose many data-oriented entities from capabilities and process them efficiently.

**Use when:** Games, simulations, visualization, or high-volume entity processing benefit from data-oriented iteration.

**Avoid when:** Rich object invariants and heterogeneous behavior are clearer as ordinary domain objects.

## 35. Broker / message bus

**Problem:** Mediate communication, routing, transformation, and location between participants.

**Use when:** Protocol or topology decoupling is required.

**Avoid when:** The broker becomes a hidden central domain model or single point of policy ambiguity.

## 36. Shared-nothing partitioning

**Problem:** Scale and isolate state by assigning disjoint ownership.

**Use when:** Keys can partition work and cross-partition coordination is limited.

**Avoid when:** Core invariants are global or hot keys dominate.

## 37. Cache-aside / materialized projection

**Problem:** Serve expensive reads from derived state.

**Use when:** Staleness is bounded and invalidation/rebuild is defined.

**Avoid when:** The cache is silently treated as authoritative.

## 38. Parser–validator–IR

**Problem:** Convert untrusted or encoded input into a semantically valid representation.

**Use when:** Binary formats, protocols, compilers, configuration, or importers need staged trust and diagnostics.

**Canonical shape:** framing/lexing -> structural parse -> validation -> normalized IR/model -> projections/effects.

**Invariants:** Bounds checked before read; structural validity precedes semantic use; unknown/versioned fields have policy.

## 39. Command bus / application service

**Problem:** Route use-case commands through a consistent transaction, authorization, and observability boundary.

**Use when:** Many interfaces invoke the same application operations.

**Avoid when:** It becomes reflective indirection with no policy value.

## 40. Functional core, imperative shell

**Problem:** Isolate deterministic computation from effects.

**Use when:** Parsing, planning, pricing, compilation, validation, reducers, and agent policy can be tested as pure transformations.

**Avoid when:** Copying or abstraction overhead violates measured constraints; the “core” still hides effects.

## Pattern-combination rules

Patterns commonly compose at different levels:

- DDD bounded contexts + hexagonal architecture + application services.
- Compiler pipeline + pass manager + functional transformations + plugin backends.
- TUI MVU + ports/adapters for filesystem/network effects.
- Agent orchestrator + scheduler/executor + state machine + append-only audit log.
- Distributed service + CQRS + event-driven integration, without necessarily using event sourcing.
- Binary parser + validator + normalized IR + visitor/pipeline transformations.

Do not combine patterns merely to appear comprehensive. Every added pattern must remove a named risk or satisfy a named quality scenario.

## Sources

- [Package bibliography](09-bibliography.md); verify the linked source record before relying on current or external claims.
