# Canonical Flowgraphs

> Locally authored diagram guidance, not a primary source or generated snapshot; source gap: live verification of renderer behavior through the [bibliography](09-bibliography.md) is required before relying on syntax or architecture claims.

GitHub renders Mermaid from a fenced `mermaid` block using a
version-dependent renderer. Use `flowchart` with stable IDs, quote labels that
contain punctuation, and use `A -->|label| B` for labeled edges. Probe the
target renderer with an `info` diagram as described in the
[GitHub Mermaid compatibility note](09-bibliography.md#github-mermaid-compatibility);
no local render result is claimed here.

All diagrams use Mermaid. Adapt names to the actual system. Do not copy a graph without checking state ownership, control authority, and failure paths.

## 1. Master architecture workflow

```mermaid
flowchart TD
    U["User objective and constraints"] --> C["Task contract with stable IDs"]
    C --> E["Evidence and uncertainty ledger"]
    E --> B["Domain, state, and boundary model"]
    B --> Q["Quality-attribute scenarios"]
    Q --> A["Generate baseline and alternatives"]
    A --> D["Decision matrix and hard vetoes"]
    D -->|failed gate| X["Return to earliest invalid phase"]
    D -->|candidate selected| S["Static and dynamic specification"]
    S --> R["Risk and tradeoff review"]
    R --> I["ADRs and vertical slices"]
    I --> V["Executable verification plan"]
    V --> F["Final traceability and consistency pass"]
```

## 2. Gate state machine

```mermaid
stateDiagram-v2
    [*] --> G0
    G0: Goal integrity
    G1: Evidence sufficiency
    G2: Boundary coherence
    G3: Credible alternatives
    G4: Flow completeness
    G5: Quality fit
    G6: Implementability
    G7: Verifiability

    G0 --> G1: pass
    G1 --> G2: pass
    G2 --> G3: pass
    G3 --> G4: pass
    G4 --> G5: pass
    G5 --> G6: pass
    G6 --> G7: pass
    G7 --> Complete: pass

    G0 --> Blocked: conflict or invented goal
    G1 --> Blocked: high-impact unknown
    G2 --> Revise: ambiguous ownership
    G3 --> Revise: pattern-first design
    G4 --> Revise: missing failure/cancel path
    G5 --> Revise: unmet quality scenario
    G6 --> Revise: interfaces still invented during coding
    G7 --> Revise: no executable evidence
```

## 3. Classic MVC-style interaction

```mermaid
sequenceDiagram
    actor User
    participant View
    participant Controller
    participant Model
    participant Effect as External Port

    User->>View: interaction
    View->>Controller: normalized input/event
    Controller->>Model: command or operation
    alt valid transition
        Model->>Effect: requested side effect through port
        Effect-->>Model: result/event
        Model-->>View: state change/observation
        View-->>User: updated projection
    else invalid input or invariant failure
        Model-->>Controller: typed rejection
        Controller-->>View: error presentation model
        View-->>User: actionable diagnostic
    end
```

## 4. MVU / reducer loop

```mermaid
flowchart LR
    EVT["Input or effect result message"] --> UPD["update message model"]
    UPD --> NEW["New model"]
    UPD --> CMD["Effect commands"]
    NEW --> VIEW["Pure projection/render"]
    VIEW --> OUT["UI or TUI"]
    CMD --> FX["Effect interpreter/ports"]
    FX --> EVT
```

## 5. DDD bounded-context interaction

```mermaid
flowchart LR
    subgraph A["Bounded Context A"]
        AM["Domain model A"]
        AS["Application service A"]
        AO["Published port"]
        AS --> AM
        AS --> AO
    end

    subgraph ACL["Anti-corruption layer"]
        T["Translator and policy"]
    end

    subgraph B["Bounded Context B"]
        BI["Inbound adapter"]
        BS["Application service B"]
        BM["Domain model B"]
        BI --> BS --> BM
    end

    AO --> T --> BI
```

## 6. Batch compiler

```mermaid
flowchart LR
    SRC["Source snapshot"] --> LEX["Lex/parse"]
    LEX --> AST["Syntax tree"]
    AST --> SEM["Name/type/semantic analysis"]
    SEM --> HIR["High-level IR"]
    HIR --> PM["Pass manager"]
    PM --> MIR["Lower IR"]
    MIR --> BE["Target backend"]
    BE --> ART["Object/module artifact"]

    LEX -. diagnostics .-> DIAG["Diagnostic projection"]
    SEM -. diagnostics .-> DIAG
    PM -. remarks and verification .-> DIAG
    BE -. diagnostics .-> DIAG

    PM --> VER{"IR valid?"}
    VER -->|no| STOP["Stop with verifier failure"]
    VER -->|yes| MIR
```

## 7. Incremental compiler / language server

```mermaid
flowchart TD
    EDIT["Document change with version"] --> SNAP["Workspace snapshot"]
    SNAP --> INV["Dependency invalidation"]
    INV --> SCHED["Demand-driven scheduler"]
    SCHED --> PARSE["Incremental parse"]
    SCHED --> SEM["Incremental semantics"]
    SCHED --> IDX["Index update"]
    PARSE --> CACHE["Versioned analysis cache"]
    SEM --> CACHE
    IDX --> CACHE
    CACHE --> PROJ["Diagnostics/completion/symbol projection"]
    CANCEL["Cancellation or newer version"] --> SCHED
    SCHED -->|discard stale result| DROP["No publication"]
```

## 8. Interpreter / abstract machine

```mermaid
flowchart LR
    CODE["AST or bytecode"] --> DISPATCH["Evaluator/dispatcher"]
    STATE["Environment, stack, heap"] --> DISPATCH
    DISPATCH --> STEP["Instruction/expression transition"]
    STEP --> STATE2["New machine state"]
    STEP --> FX["Declared effect"]
    FX --> HOST["Host port"]
    HOST --> RES["Result/trap/event"]
    RES --> DISPATCH
    STATE2 --> DISPATCH
    DISPATCH --> OUT["Value, trap, trace"]
```

## 9. Runtime with JIT feedback

```mermaid
flowchart TD
    MOD["Validated module"] --> EXEC["Interpreter/baseline executor"]
    EXEC --> PROF["Profiling counters"]
    PROF --> POLICY{"Tiering policy"}
    POLICY -->|cold| EXEC
    POLICY -->|hot| JIT["JIT compiler"]
    JIT --> CODE["Code cache + deopt metadata"]
    CODE --> FAST["Optimized execution"]
    FAST --> GUARD{"Assumption holds?"}
    GUARD -->|yes| FAST
    GUARD -->|no| DEOPT["Deoptimize to safe state"]
    DEOPT --> EXEC
```

## 10. Non-interactive CLI

```mermaid
flowchart LR
    ARGV["argv/env/stdin"] --> TP["Transport parsing"]
    TP -->|syntax error| USAGE["Usage diagnostic + stable exit code"]
    TP --> CMD["Typed application command"]
    CMD --> AUTH["Validation/authorization"]
    AUTH -->|reject| ERR["Typed application error"]
    AUTH --> USE["Use-case coordinator"]
    USE --> DOM["Domain operation"]
    DOM --> PORT["Filesystem/network/process ports"]
    PORT --> RES["Result"]
    RES --> FMT{"Output mode"}
    FMT --> HUMAN["Human formatter -> stdout/stderr"]
    FMT --> MACHINE["JSON/structured formatter -> stdout"]
```

## 11. TUI

```mermaid
sequenceDiagram
    participant Term as Terminal/Input
    participant Loop as Event Loop
    participant Update
    participant Model
    participant Effect as Effect Ports
    participant Render

    Term->>Loop: key/mouse/resize/timer
    Loop->>Update: message + current model
    Update->>Model: produce next immutable state
    Update->>Effect: commands
    Model->>Render: project state
    Render-->>Term: terminal frame
    Effect-->>Loop: completion/error message
```

## 12. Agent harness

```mermaid
flowchart TD
    USER["User request"] --> CONTRACT["Immutable task contract"]
    CONTRACT --> ORCH["Orchestrator/policy state machine"]
    EVID["Evidence and decision store"] --> ORCH
    ORCH --> PLAN["Bounded task graph"]
    PLAN --> SCHED["Budgeted scheduler"]
    SCHED --> W1["Worker/model"]
    SCHED --> W2["Worker/model"]
    W1 --> BROKER["Tool capability broker"]
    W2 --> BROKER
    BROKER --> TOOLS["Files/shell/web/MCP/APIs"]
    TOOLS --> OBS["Typed observations with provenance"]
    OBS --> EVID
    W1 --> CAND["Candidate result"]
    W2 --> CAND
    CAND --> VERIFY["Independent verifier/evals"]
    VERIFY -->|fail| ORCH
    VERIFY -->|pass| PROJ["User-facing result and audit trace"]
    STOP["Budget, cancellation, approval, stop conditions"] --> ORCH
```

## 13. Long-running agent recovery

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Running: claim task
    Running --> Checkpointed: persist state/evidence
    Checkpointed --> Running: continue
    Running --> WaitingApproval: privileged action
    WaitingApproval --> Running: approved
    WaitingApproval --> Cancelled: denied/cancelled
    Running --> RetryableFailure: transient failure
    RetryableFailure --> Running: budgeted retry
    RetryableFailure --> ManualReview: budget exhausted
    Running --> PermanentFailure: invariant or policy violation
    Running --> Completed: verifier passes
    Checkpointed --> Ready: process restart and resume
```

## 14. Web API through ports and adapters

```mermaid
flowchart LR
    HTTP["HTTP adapter"] --> VALID["Transport validation/auth"]
    VALID --> APP["Application command/query"]
    APP --> DOMAIN["Domain model"]
    APP --> PORTS["Declared ports"]
    PORTS --> DB["Persistence adapter"]
    PORTS --> EXT["External-service adapter"]
    DOMAIN --> RESULT["Domain result/error"]
    RESULT --> MAP["Representation mapping"]
    MAP --> RESP["Versioned HTTP response"]
```

## 15. Binary parser with staged trust

```mermaid
flowchart LR
    BYTES["Untrusted bytes/stream"] --> FRAME["Framing and size limits"]
    FRAME --> STRUCT["Structural decoder"]
    STRUCT -->|bounds/encoding failure| PERR["Parse error with offset"]
    STRUCT --> VAL["Semantic validation"]
    VAL -->|invariant/version failure| VERR["Validation error"]
    VAL --> IR["Normalized typed IR"]
    IR --> API["Object/query API"]
    IR --> HEX["Annotated hex/disassembly projection"]
    IR --> ENC["Encoder"]
    ENC --> ROUND["Round-trip/canonicalization checks"]
```

## 16. Event-driven service

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant App
    participant Store
    participant Bus
    participant Projection

    Client->>API: command + idempotency key
    API->>App: typed command
    App->>Store: atomic state/event append
    Store-->>App: committed version
    App-->>API: accepted/result
    Store->>Bus: publish via outbox/commit log
    Bus->>Projection: integration event
    Projection->>Projection: idempotent update
    Projection-->>Client: query/read model later
```

## 17. Durable workflow / saga

```mermaid
flowchart TD
    START["Start command"] --> HIST["Append workflow event"]
    HIST --> DECIDE["Deterministic workflow decision"]
    DECIDE --> ACT["Schedule activity"]
    ACT --> WORK["Idempotent worker"]
    WORK -->|success| HIST
    WORK -->|retryable failure| RETRY["Backoff + bounded retry"]
    RETRY --> ACT
    WORK -->|permanent failure| COMP["Compensate or manual repair"]
    COMP --> HIST
    DECIDE -->|complete| DONE["Terminal state"]
```

## 18. Vertical architecture slice

```mermaid
flowchart LR
    INPUT["One real input"] --> ADAPTER["Real inbound adapter"]
    ADAPTER --> USE["One application operation"]
    USE --> CORE["Semantic rule/invariant"]
    CORE --> PORT["One declared effect port"]
    PORT --> IMPLEMENT["Minimal real adapter or controlled fake"]
    IMPLEMENT --> OUTPUT["One observable output"]
    CORE --> FAIL["One failure path"]
    OUTPUT --> TEST["Automated acceptance test"]
    FAIL --> TEST
```

## 19. Contradiction resolution

```mermaid
flowchart TD
    CLAIMS["Conflicting claims or designs"] --> SRC{"Independent sources/evidence?"}
    SRC -->|no| UNKNOWN["Mark unknown; do not vote"]
    SRC -->|yes| REPRO{"Executable reproduction possible?"}
    REPRO -->|yes| TEST["Run controlled experiment"]
    REPRO -->|no| AUTH["Rank primary authority and scope"]
    TEST --> RESULT["Record result and conditions"]
    AUTH --> RESULT
    RESULT --> LEDGER["Update evidence and decision ledgers"]
```

## Sources

- [Package bibliography](09-bibliography.md); verify the linked source record before relying on current or external claims.
