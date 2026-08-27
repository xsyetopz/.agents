# Failure Modes and Anti-Patterns

## Contents

- [1. Pattern-first architecture](#1-pattern-first-architecture)
- [2. Three-box MVC cargo cult](#2-three-box-mvc-cargo-cult)
- [3. Anemic domain plus "service" sprawl](#3-anemic-domain-plus-service-sprawl)
- [4. Domain layer contaminated by infrastructure](#4-domain-layer-contaminated-by-infrastructure)
- [5. Bounded contexts as folder names](#5-bounded-contexts-as-folder-names)
- [6. Aggregate per table](#6-aggregate-per-table)
- [7. Controller/application-service god object](#7-controllerapplication-service-god-object)
- [8. Generic repository and CRUD abstraction](#8-generic-repository-and-crud-abstraction)
- [9. Event soup](#9-event-soup)
- [10. False decoupling through a bus](#10-false-decoupling-through-a-bus)
- [11. Hidden duplicate state](#11-hidden-duplicate-state)
- [12. Mutable shared blackboard without provenance](#12-mutable-shared-blackboard-without-provenance)
- [13. Agent voting as verification](#13-agent-voting-as-verification)
- [14. Prompt as durable workflow state](#14-prompt-as-durable-workflow-state)
- [15. Unbounded autonomous loop](#15-unbounded-autonomous-loop)
- [16. Multi-agent decomposition by persona](#16-multi-agent-decomposition-by-persona)
- [17. Pipeline with ambient state](#17-pipeline-with-ambient-state)
- [18. IR proliferation](#18-ir-proliferation)
- [19. Parser doing semantic and business work](#19-parser-doing-semantic-and-business-work)
- [20. Lossless and canonical round-trip conflated](#20-lossless-and-canonical-round-trip-conflated)
- [21. TUI state in widgets](#21-tui-state-in-widgets)
- [22. CLI transport mixed with domain logic](#22-cli-transport-mixed-with-domain-logic)
- [23. Framework-shaped architecture](#23-framework-shaped-architecture)
- [24. Premature microservices](#24-premature-microservices)
- [25. Shared database as integration contract](#25-shared-database-as-integration-contract)
- [26. Happy-path-only sequence diagram](#26-happy-path-only-sequence-diagram)
- [27. Quality adjectives without scenarios](#27-quality-adjectives-without-scenarios)
- [28. Architecture as folder tree](#28-architecture-as-folder-tree)
- [29. Abstract factory explosion](#29-abstract-factory-explosion)
- [30. "Future-proof" without threshold](#30-future-proof-without-threshold)
- [31. Architecture decision without negative consequences](#31-architecture-decision-without-negative-consequences)
- [32. Validation theatre](#32-validation-theatre)
- [33. One-file-per-role decomposition](#33-one-file-per-role-decomposition)
- [34. Indexed-diff topology blindness](#34-indexed-diff-topology-blindness)
- [35. Waiver or social-approval acceptance](#35-waiver-or-social-approval-acceptance)
- [36. Check suppression as a fix](#36-check-suppression-as-a-fix)
- [37. Tool-defect authorization shortcut](#37-tool-defect-authorization-shortcut)
- [Sources](#sources)

> Locally authored guidance, not a primary source or generated snapshot; source gap: live verification of standards, provider behavior, and other current claims against the bibliography (see `design-09-bibliography.md`) is required before relying on them.

## 1. Pattern-first architecture

**Symptom:** "Use MVC/microservices/event sourcing/DDD" appears before requirements and forces.

**Why it fails:** The design optimizes for a label rather than the system.

**Correction:** Return to task contract, state/control ownership, and quality scenarios. Generate a simpler baseline.

## 2. Three-box MVC cargo cult

**Symptom:** Any data structure becomes Model, any output becomes View, and all remaining code becomes Controller.

**Why it fails:** The names provide no predictive power about dependencies, observation, state transitions, or testing.

**Correction:** Use the dominant form: pipeline, abstract machine, state machine, dataflow, application service, parser-validator, or scheduler-executor.

## 3. Anemic domain plus "service" sprawl

**Symptom:** Domain objects are data bags; all rules live in generic services.

**Why it fails:** Invariants have no clear owner and behavior fragments across orchestration code.

**Correction:** Place behavior with the semantic object/aggregate/value when it protects its invariants; retain application coordination outside.

## 4. Domain layer contaminated by infrastructure

**Symptom:** HTTP requests, ORM entities, widgets, tool APIs, file handles, or model-provider types appear in domain rules.

**Why it fails:** Technology mechanics become semantic dependencies and make tests/migration harder.

**Correction:** Translate at adapters; define purpose-oriented ports; preserve framework-free domain values where justified.

## 5. Bounded contexts as folder names

**Symptom:** Every feature directory is declared a bounded context.

**Why it fails:** No distinct language/model/ownership boundary exists.

**Correction:** Require semantic divergence, ownership, integration, or lifecycle evidence. Use modules when a bounded context is unnecessary.

## 6. Aggregate per table

**Symptom:** Persistence schema determines aggregate boundaries.

**Why it fails:** Transactional invariants and consistency scope are ignored.

**Correction:** Derive aggregates from rules that must remain consistent in one transaction; use references/events/workflows across aggregates.

## 7. Controller/application-service god object

**Symptom:** One coordinator validates, calculates, persists, formats, retries, and emits events.

**Why it fails:** Control authority, semantic policy, and infrastructure become inseparable.

**Correction:** Retain use-case sequencing but delegate invariant-bearing behavior, effects, and projections through explicit contracts.

## 8. Generic repository and CRUD abstraction

**Symptom:** `Repository<T>` exposes all storage operations uniformly.

**Why it fails:** Domain retrieval semantics, performance, and consistency are hidden; invalid operations are easy.

**Correction:** Use intention-revealing ports such as `LoadRunCheckpoint`, `FindModuleByCanonicalName`, or `AppendEventsAtExpectedVersion`.

## 9. Event soup

**Symptom:** Every internal action is broadcast; ownership and semantics are unclear.

**Why it fails:** Ordering, duplication, consistency, and debugging costs explode.

**Correction:** Distinguish domain events, integration events, notifications, commands, and queries. Prefer direct calls within one ownership boundary.

## 10. False decoupling through a bus

**Symptom:** Producer and consumer remain semantically and operationally coupled but communicate through a broker.

**Why it fails:** The coupling becomes less visible while failure modes increase.

**Correction:** Specify schema ownership, delivery, timing, and independent evolution. Remove the bus if no real temporal/deployment decoupling exists.

## 11. Hidden duplicate state

**Symptom:** UI, cache, database, prompt, workflow history, and in-memory objects all claim current truth.

**Why it fails:** Reconciliation and recovery are undefined.

**Correction:** Declare one authority and classify all other forms as projections, caches, checkpoints, or replicas with consistency rules.

## 12. Mutable shared blackboard without provenance

**Symptom:** Agents or analyzers write free-form conclusions to shared state.

**Why it fails:** Claims overwrite each other, evidence disappears, and consensus is mistaken for truth.

**Correction:** Use typed entries with provenance, append-only evidence where possible, conflict resolution, and one integration authority.

## 13. Agent voting as verification

**Symptom:** Multiple agents vote on a technical claim.

**Why it fails:** Correlated models can repeat the same error; independent evidence comes from distinct sources or controlled tests.

**Correction:** Assign distinct methods: source inspection, execution, formal reasoning, adversarial review. Resolve through evidence.

## 14. Prompt as durable workflow state

**Symptom:** Long-running progress exists only in conversation history or compacted summaries.

**Why it fails:** State can be lost, distorted, or unversioned; recovery and audit are weak.

**Correction:** Persist explicit task graph, checkpoints, artifacts, evidence IDs, budgets, and terminal states.

## 15. Unbounded autonomous loop

**Symptom:** "Continue until done" with no budget, stop condition, or verifier.

**Why it fails:** Thrashing, repeated tool use, cost growth, and scope drift.

**Correction:** Define maximum steps/time/tokens, progress criteria, retry budgets, escalation, and verifier-controlled completion.

## 16. Multi-agent decomposition by persona

**Symptom:** "Architect, coder, reviewer" roles operate without bounded artifacts or independent evidence.

**Why it fails:** Work overlaps; the reviewer sees the same assumptions; responsibility is vague.

**Correction:** Decompose by falsifiable questions and artifact ownership: evidence collector, candidate analyst, threat reviewer, test designer, integrator.

## 17. Pipeline with ambient state

**Symptom:** Compiler/data stages mutate global context not represented in inputs/outputs.

**Why it fails:** Ordering and caching become implicit; parallelism and testing break.

**Correction:** Make required state explicit, declare preserved/invalidated analyses, and isolate unavoidable global services.

## 18. IR proliferation

**Symptom:** Many intermediate representations exist because "compilers have IRs."

**Why it fails:** Conversion cost and semantic loss exceed benefit.

**Correction:** Each IR must preserve a distinct abstraction level or enable named analyses/targets. Record invariants and lowering proof obligations.

## 19. Parser doing semantic and business work

**Symptom:** Binary/text parser allocates domain resources, changes persistence, or applies high-level policy during decoding.

**Why it fails:** Untrusted input crosses trust boundaries before validation; errors become entangled.

**Correction:** Stage framing, structural parse, semantic validation, normalization, then domain action.

## 20. Lossless and canonical round-trip conflated

**Symptom:** Serializer tests expect byte-identical output when the format allows equivalent representations, or lose unknown data when exact preservation is required.

**Why it fails:** Compatibility promises are ambiguous.

**Correction:** Declare one policy: semantic round-trip, canonical encoding, or lossless preservation. Test accordingly.

## 21. TUI state in widgets

**Symptom:** Widget tree contains the only authoritative state.

**Why it fails:** Replay, deterministic testing, resize handling, and recovery become difficult.

**Correction:** Use an explicit model and reducer/update loop; widgets render projections.

## 22. CLI transport mixed with domain logic

**Symptom:** Argument parsing functions perform domain operations and print directly.

**Why it fails:** Alternate interfaces and machine-readable output are hard; tests require process execution.

**Correction:** Parse to typed command, invoke application operation, format typed result.

## 23. Framework-shaped architecture

**Symptom:** Components mirror framework concepts regardless of domain.

**Why it fails:** Framework upgrades or replacements become architectural rewrites.

**Correction:** Treat framework as adapter or explicit constraint. Use its inversion only where measured value exceeds coupling.

## 24. Premature microservices

**Symptom:** Deployment boundaries are created before semantic ownership and consistency are understood.

**Why it fails:** Distributed transactions, latency, schemas, and operations appear without compensating benefits.

**Correction:** Start with modular boundaries; split only on explicit ownership, scaling, trust, failure, or release-cadence forces.

## 25. Shared database as integration contract

**Symptom:** Multiple contexts/services edit the same tables directly.

**Why it fails:** Ownership and semantic versioning are impossible to enforce.

**Correction:** Assign table/schema ownership and integrate through published contracts; use migration/replication deliberately.

## 26. Happy-path-only sequence diagram

**Symptom:** Dynamic view ends after success.

**Why it fails:** Timeouts, retries, cancellation, partial completion, and recovery remain architecture-by-accident.

**Correction:** Add invalid input, dependency failure, timeout/cancel, duplicate/replay, and restart paths.

## 27. Quality adjectives without scenarios

**Symptom:** "Scalable, secure, maintainable" with no workload, threat, maintenance, or operational measure.

**Why it fails:** No decision can be evaluated and no test can pass.

**Correction:** Use source/stimulus/environment/artifact/response/measure.

## 28. Architecture as folder tree

**Symptom:** Deliverable contains directory names and interfaces but no behavior or consequences.

**Why it fails:** The difficult decisions remain deferred to implementation.

**Correction:** Add state ownership, contracts, critical flows, quality scenarios, ADRs, and vertical slices.

## 29. Abstract factory explosion

**Symptom:** Interfaces are created for every class before a second implementation or test seam exists.

**Why it fails:** Indirection and navigation costs rise without reducing risk.

**Correction:** Abstract at volatile effects, published extension points, or meaningful policy seams.

## 30. "Future-proof" without threshold

**Symptom:** Complexity is justified by hypothetical scale or future clients.

**Why it fails:** Current costs are real; future benefit is unfalsifiable.

**Correction:** Record explicit evolution triggers and use a reversible baseline.

## 31. Architecture decision without negative consequences

**Symptom:** ADR lists only benefits.

**Why it fails:** It is advocacy, not a decision record.

**Correction:** Record costs, operational burden, migration, failure modes, and revisit triggers.

## 32. Validation theatre

**Symptom:** A validator checks headings but not substantive claims, yet is treated as proof.

**Why it fails:** Form compliance masks semantic defects.

**Correction:** Combine static checks with executable tests, adversarial scenarios, and expert review. Treat bundled scripts as minimum lint only.

## 33. One-file-per-role decomposition

**Symptom:** A proposed tree creates `Validation`, `Helpers`, `Open`, `Reduce`,
`Commit`, `Types`, or `Operations` files/directories solely because each name
sounds like a responsibility.

**Why it fails:** Procedural steps and syntax categories become durable owners
without independent state, lifecycle, contract, visibility, dependency, or
failure semantics. The result is microfile confetti and hidden coupling.

**Correction:** Treat those names as procedural roles. Keep them with the
nearest durable owner unless a source-topology map proves an independent
lifecycle and contract. Reject one-type, one-operation, one-phase,
one-helper, and one-validation-per-file plans when ownership answers match.

## 34. Indexed-diff topology blindness

**Symptom:** The design reviews only `git diff` or tracked files while newly
created source files remain untracked and absent from the architecture map.

**Why it fails:** The candidate tree is incomplete; a split can pass review by
leaving its most consequential files outside the apparent change set.

**Correction:** Enumerate `git status --short`, `git diff --name-status`, and
`git ls-files --others --exclude-standard`. Map every changed and untracked
source path to owner, change reason, visibility, lifecycle, dependencies, and
consolidation rationale.

## 35. Waiver or social-approval acceptance

**Symptom:** A baseline, path exclusion, disabled/advisory mode, threshold
override, exception record, urgency, reassurance, or praise is presented as a
passing architecture result.

**Why it fails:** The finding remains unresolved; only the evidence surface or
the gate has been weakened. Conversation cannot establish ownership,
dependency direction, or structural correctness.

**Correction:** Use the unmodified full-repository fail-closed audit before and
after repository edits. A pre-change result is comparison context, not a
waiver baseline. Acceptance requires the topology map and zero unresolved warning or error
findings; report a blocker when that evidence is unavailable.

## 36. Check suppression as a fix

**Symptom:** A lint/check failure is made green by adding an ignore or exclude,
disabling a rule/provider/job, lowering severity, changing a baseline, adding
`allow-failure` or `continue-on-error`, excluding the failing path, or weakening
or deleting the test/check.

**Why it fails:** The owning defect remains and the verification contract no
longer measures the architecture claim. A green result obtained through a
suppression is not evidence.

**Correction:** Repair the owning cause and rerun the check. If the tool is
wrong, preserve the failed gate, capture a minimal reproducer (tool/version,
exact command/configuration, input, output, exit code), and obtain explicit
policy-change authorization. Keep acceptance blocked while the check is
disabled or weakened.

## 37. Tool-defect authorization shortcut

**Symptom:** An agent claims an analyzer is incorrect and silently disables its
provider or marks the job advisory so architecture review can pass.

**Why it fails:** The claim is untestable, the failure surface is hidden, and
the gate can no longer detect the risk.

**Correction:** Report the exact reproducer and environment, keep the original
check enabled and failing, and request a separately recorded policy change.
No conversational approval or local config edit authorizes a passing gate.

## Sources

- Package bibliography (see `design-09-bibliography.md`); verify the linked source record before relying on current or external claims.
