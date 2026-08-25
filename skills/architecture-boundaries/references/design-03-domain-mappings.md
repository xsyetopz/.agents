# Cross-Domain Mappings

> Locally authored guidance, not a primary source or generated snapshot; source gap: live verification of standards, provider behavior, and other current claims against the bibliography (see `design-09-bibliography.md`) is required before relying on them.

These mappings help classify a system. They are not prescriptions. The “MVC-like” columns show analogies only; the **preferred primary shape** usually names the stronger architecture.

| # | Domain | Semantic core / “Model” | Projection / “View” | Control / “Controller” | Preferred primary shape | Critical invariants |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Batch compiler | AST/IR, symbol/type state, target model | diagnostics, object code, IR dumps | driver and pass manager | staged pipeline + verified IR + backend ports | phase ordering, IR validity, deterministic diagnostics |
| 2 | Incremental compiler | dependency graph, semantic snapshots, cached analyses | diagnostics and partial artifacts | invalidation/recompute scheduler | demand-driven dataflow + incremental cache | cache keys reflect semantics; stale analysis never reused |
| 3 | Interpreter | AST/bytecode, environment, store, language values | printed values, errors, debugger views | evaluator/dispatcher | interpreter or abstract machine + effect ports | evaluation order, scope, error and resource semantics |
| 4 | JIT compiler | profiling state, IR tiers, code cache | machine code, deopt metadata, traces | tiering policy and compilation scheduler | runtime + staged compilation + feedback loop | safe points, deopt correctness, executable-memory policy |
| 5 | Virtual machine | machine state, stack/frames, heap, module instances | traces, debugger/profiler, embedding API | instruction dispatcher, scheduler, GC coordination | abstract machine + runtime services | instruction semantics, validation, memory and trap rules |
| 6 | Garbage collector | object graph, allocation metadata, roots | metrics and diagnostics | collector policy/safepoint coordinator | policy/mechanism split + concurrent state machine | reachability, write barriers, pause/concurrency safety |
| 7 | Language server / IDE engine | workspace semantic model, index, document versions | diagnostics, completions, symbols, edits | protocol handlers and request scheduler | incremental semantic core + adapters + cancellation | document-version coherence, bounded latency, cancel safety |
| 8 | Debugger | process/thread state, symbols, breakpoints | source/disassembly/register views | command dispatcher and event loop | state machine + protocol adapters | stop-state consistency, target/control ownership |
| 9 | Static analyzer | normalized program model, facts, lattice state | findings, traces, SARIF/reports | analysis scheduler/fixpoint engine | dataflow/fixpoint + rule plugins | monotonicity or convergence assumptions; source mapping |
| 10 | Reverse-engineering platform | memory map, symbols, typed IR, provenance | disassembly, decompiler output, graphs | analysis manager and user command routing | plugin microkernel + analysis pipeline + evidence graph | provenance, non-destructive edits, reproducible analysis |
| 11 | Build system | target/action DAG, declared inputs, cache state | logs, artifacts, graph visualization | dependency scheduler/executor | DAG + content-addressed cache + sandboxed workers | complete dependency declaration, hermetic action identity |
| 12 | Package manager | package graph, constraints, lock state | resolution plan, lockfile, messages | resolver and transaction coordinator | constraint solving + repository adapters + transaction plan | reproducible resolution, integrity, rollback |
| 13 | CLI command | domain/application state | human text, JSON, exit status | argument parser and command dispatcher | ports/adapters + application services | stable exit codes, stdout/stderr discipline, idempotency |
| 14 | Interactive shell | session environment, job table, syntax tree | prompt, output, job status | parser, expansion/evaluation loop, job controller | interpreter + state machine + process adapters | quoting/expansion semantics, signal and job-control rules |
| 15 | TUI application | immutable or controlled app model | terminal renderer | update/event loop | MVU + effect commands | all state transitions pass through update; resize/input safe |
| 16 | Desktop GUI | domain model plus presentation state | widgets/windows | controllers, presenters, view-models, or reducers | MVC/MVP/MVVM/MVU + application core | domain state not owned by widgets; UI thread rules |
| 17 | Mobile app | offline/local domain state, sync state | screens and notifications | navigation/update/use cases | MVU/MVVM + repository/sync workflow | lifecycle recovery, conflict resolution, permission boundaries |
| 18 | Web frontend | client app state, cache, form state | DOM/UI projection | event handlers/reducers/router | component architecture + MVU/reducer + effect layer | source-of-truth clarity, cancellation, stale response handling |
| 19 | Server-rendered web app | domain/application state | HTML views | routes/controllers | MVC or page-controller + application services | authorization before use case; view not domain authority |
| 20 | Web API | domain state and resources | JSON/protobuf representations | transport adapter + application service | hexagonal + command/query boundary | stable contracts, validation, auth, idempotency, versioning |
| 21 | GraphQL service | domain/application model, schema semantics | typed response graph | resolver execution and request planner | schema boundary + application ports + batching | field auth, N+1 control, consistent error/null semantics |
| 22 | Database engine | catalog, pages/records, transactions, indexes | result sets, plans, metrics | parser/planner/executor/transaction manager | layered engine + iterator/vectorized pipeline | ACID/isolation, crash recovery, page integrity |
| 23 | Query optimizer | relational/algebraic IR, statistics, equivalence classes | chosen plan and explain output | rule/cost search controller | memoized search + rewrite rules + cost model | semantic equivalence, termination/budget, stable cost inputs |
| 24 | Storage engine | pages/segments, WAL, cache, metadata | read results and operational metrics | transaction, buffer, compaction coordinators | log-structured or page architecture + recovery state machine | durability ordering, checksums, atomic metadata transitions |
| 25 | Filesystem | namespace, inodes/objects, allocation maps | file API, directory listings, diagnostics | VFS operations, journal/recovery control | layered namespace/storage + journaling | namespace/data consistency, crash recovery, permission rules |
| 26 | ETL pipeline | typed datasets, lineage, transformation semantics | sink datasets, reports | orchestrator and stage scheduler | pipeline/DAG + schema contracts | lineage, idempotency, partition correctness, replay |
| 27 | Stream processor | event-time state, windows, offsets, operators | outputs/materialized views | runtime scheduler/checkpoint coordinator | dataflow graph + stateful operators | exactly/at-least-once contract, watermark/window semantics |
| 28 | Workflow engine | durable workflow state and history | status/read models | deterministic workflow interpreter/scheduler | durable state machine + activity workers | replay determinism, idempotent activities, timeout/compensation |
| 29 | Message broker | topics/queues, offsets, subscriptions, retained data | consumer/admin APIs and metrics | routing, replication, delivery scheduler | log/queue core + protocol adapters | ordering scope, durability, ack/redelivery semantics |
| 30 | Distributed service | bounded-context state and durable records | APIs/read models/events | application service, consensus/workflow as needed | bounded contexts + explicit consistency + adapters | ownership, retries, partitions, schema compatibility |
| 31 | Event-sourced service | event stream and aggregate state | projections/read models | command handler and event append | event sourcing + CQRS where justified | expected version, immutable event history, projection replay |
| 32 | Protocol implementation | connection/session state, frames, negotiated parameters | decoded messages, telemetry | parser/state machine/timers | parser-validator + protocol state machine | framing bounds, transition legality, timeout and version rules |
| 33 | Binary format parser | schema, parsed structure, normalized IR | object API, hex annotations, re-encoding | decoder/validator | schema-driven parser + validation + projection | bounds, endianness, alignment, version and unknown-field policy |
| 34 | Serializer/codecs | semantic values and schema | byte/text representation | encoder/decoder dispatch | functional core + streaming adapters | round-trip/canonicalization rules, limits, compatibility |
| 35 | Agent harness | task contract, run state, evidence, budgets, memory | user output, traces, summaries | orchestrator/policy loop | state machine + scheduler/executor + tool ports | user-goal integrity, capability bounds, evidence provenance |
| 36 | Multi-agent system | shared task graph, evidence/decision ledger | integrated report and per-agent traces | parent orchestrator and verifier | bounded workers + blackboard/evidence store + verifier | single decision authority, no unsourced peer claims, stop budgets |
| 37 | Retrieval-augmented system | corpus/index metadata, retrieved evidence, citations | grounded answer and source view | query planner/retriever/ranker | staged retrieval pipeline + evidence ledger | source identity, freshness, citation entailment, injection isolation |
| 38 | Plugin platform | core domain model, extension registry/capabilities | host UI/API contributions | lifecycle and capability manager | microkernel + versioned extension contracts | isolation, compatibility, least privilege, failure containment |
| 39 | Observability platform | telemetry model, schemas, time series/traces/logs | dashboards, alerts, queries | ingestion/query/rule schedulers | pipeline + storage/query engines + projections | timestamp/identity semantics, cardinality limits, retention |
| 40 | Security scanner | asset/code model, rules, evidence, finding state | findings and remediation reports | scan planner and rule executor | plugin rules + evidence pipeline + dedup workflow | reproducibility, severity provenance, false-positive control |
| 41 | Game engine | world/ECS state, physics state, assets | rendered frames/audio/UI | game loop, systems scheduler, input mapping | ECS or scene graph + fixed/variable step loops | deterministic update ordering where required, frame budget |
| 42 | Simulation | model state, parameters, random streams | plots, snapshots, outputs | timestep/event scheduler | discrete-event or timestep engine | reproducibility, numerical stability, event ordering |
| 43 | Embedded controller | plant/device state, calibration, safety state | telemetry, display, actuator commands | control loop and mode state machine | state machine + control/dataflow + hardware ports | timing deadlines, safe states, sensor/actuator bounds |
| 44 | Robotics stack | world/robot state, maps, plans | visualization, telemetry, commands | planner/executive/control loops | layered autonomy + dataflow + state machines | coordinate frames, timing, safety interlocks, degraded modes |
| 45 | Kernel subsystem | process/device/memory state | syscalls, proc/debug interfaces, telemetry | scheduler/interrupt/syscall dispatch | mechanisms + policy modules + event-driven core | privilege, race freedom, resource lifetime, interrupt context |
| 46 | Network proxy/gateway | routing/policy/session state | forwarded responses, metrics | connection/event loop and policy engine | reactor/proactor + filter chain + policy core | streaming/backpressure, timeout, header/protocol correctness |
| 47 | Migration/compatibility layer | source/target semantic models and mapping rules | converted artifacts and discrepancy report | migration planner/runner | anti-corruption layer + staged transformation + reconciliation | loss accounting, resumability, version mapping, rollback |
| 48 | ML training system | model/optimizer state, dataset lineage, experiment config | checkpoints, metrics, reports | trainer/orchestrator/scheduler | dataflow + durable checkpoints + experiment ledger | reproducibility, seed/data/version identity, checkpoint integrity |
| 49 | ML inference service | model/version state, request context, caches | predictions and explanations | router/batcher/runtime scheduler | serving pipeline + resource scheduler + adapters | model/version traceability, latency budgets, fallback semantics |
| 50 | Configuration engine | typed config model, defaults, provenance | effective config, diagnostics | loader/merge/validation coordinator | parser-validator + layered sources + immutable snapshot | deterministic precedence, provenance, schema/version validation |

## Detailed domain notes

### Compiler and language-development systems

Do not force MVC onto compiler phases. The core concern is usually **representation preservation and transformation**:

```text
source -> tokens -> syntax -> semantic model -> IR(s) -> target artifact
                     |             |             |
                 diagnostics   verification   lowering/codegen
```

The compiler driver or pass manager resembles a controller only in the weak sense that it coordinates stages. Diagnostics and artifacts resemble views only as projections. Name the architecture pipeline/pass-manager/IR-centered unless an actual interactive IDE loop dominates.

Recommended boundaries:

- Frontend language semantics
- Shared or multi-level IR
- Optimization/analysis passes
- Target lowering/backend
- Tooling and diagnostics
- Runtime/ABI contract

Required proofs:

- Each lowering preserves defined semantics.
- Invalid IR cannot silently reach later stages.
- Diagnostics retain source provenance.
- Pass analysis invalidation is correct.

### Interpreter and runtime systems

A runtime is best described as an **abstract machine plus services**:

```text
program/module + machine state -> dispatch/execute -> new machine state/effects
```

Separate:

- Language semantics
- Machine representation
- Memory management
- Scheduling/concurrency
- Native/host interface
- Instrumentation/debugging
- Embedding API

Do not place telemetry or debugger state into the semantic machine state unless the specification requires it.

### CLI and TUI systems

For non-interactive CLI:

```text
argv/stdin -> transport parsing -> application command -> domain operation
          -> formatter -> stdout/stderr + exit status
```

For TUI:

```text
terminal/input event -> update(model, message) -> model' + effects
model' -> render -> terminal
results/errors -> messages -> update
```

Critical distinctions:

- Parsing command syntax is not domain validation.
- Exit status is part of the public contract.
- Human output and machine output need separate formatters.
- Terminal widgets must not become the authoritative application state.

### Agent harnesses

Use the following role mapping:

| Role | Agent-harness realization |
| --- | --- |
| Semantic core | immutable task contract, constraints, evidence, decision state |
| Controller | orchestrator/policy loop, scheduler, budget and stop-condition enforcement |
| View | user response, trace, progress summary, review diff |
| Ports | tools, models, files, shell, browser, MCP, APIs |

A model is not the architecture. The harness includes state, tool contracts, authority, persistence, recovery, tracing, and verification.

Required boundaries:

- User intent and task contract
- Planning/decomposition
- Tool capability and approval
- Working memory/evidence
- Durable progress
- Verification/evaluation
- Output projection

Never use free-form conversation history as the only source of durable workflow state.

### Binary and protocol systems

Use staged trust:

```text
untrusted bytes
  -> frame bounds
  -> structural parse
  -> semantic validation
  -> normalized typed representation
  -> domain use / display / re-encoding
```

The parser is not the model. The schema and normalized semantics are the model; the decoder is a controller/transformer; the object view, disassembly, or re-encoding is a projection.

Required controls:

- Explicit byte/bit order
- Length and recursion limits
- Integer overflow checks
- Unknown field/version policy
- Canonical vs lossless round-trip policy
- Streaming and partial-input behavior
- Fuzz/property/differential tests

### Distributed systems

Do not begin with microservices. Begin with ownership and consistency:

1. Which bounded context owns each fact?
2. Which operation requires atomicity?
3. Which partitions and failures are expected?
4. Which latency and availability measures dominate?
5. Which integrations require published language or anti-corruption translation?

A service boundary is justified only by semantic, ownership, trust, deployment, failure, or scaling forces.

## Sources

- Package bibliography (see `design-09-bibliography.md`); verify the linked source record before relying on current or external claims.
