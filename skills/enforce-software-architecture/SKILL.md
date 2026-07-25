---
name: enforce-software-architecture
description: Use this skill when designing, reviewing, refactoring, migrating, or decomposing repository architecture, packages, modules, deployables, APIs, schemas, build graphs, or cross-language boundaries. Enforce ownership, dependency direction, public contracts, quality attributes, security and reliability, naming, toolchain topology, separation of tests and benchmarks, and executable verification without inventing layers or suppressing findings.
---

# Enforce Software Architecture

Enforce architecture as an accountable system of boundaries, decisions, and
proof. Be strict about ownership, dependency direction, public contracts,
quality attributes, and operational behavior. Be adaptable about directory
shapes and implementation details when a compiler, framework, product
constraint, or measured trade-off requires another choice. Reject cargo-cult
enterprise layering, pattern name-dropping, universal layouts, and arbitrary
refactors presented as architecture.

## Trigger and scope

Apply this skill when creating, reviewing, refactoring, migrating, or
decomposing any of the following:

- repositories, monorepos, workspaces, deployables, libraries, firmware, and
  runtime processes;
- packages, crates, modules, targets, namespaces, components, bounded
  contexts, pipelines, plugins, or services;
- source, tests, APIs, schemas, events, database ownership, FFI, generated
  artifacts, CI, build graphs, deployment topology, or architecture records.

Coordinate with specialist skills rather than duplicating their contracts. For
example, preserve authentication semantics, UI design rules, Rinf boundaries,
and build-optimization measurements when those skills are active; this skill
owns the architectural boundary and integration decision.

## Non-negotiable contract

Require every changed architectural unit to have:

1. one accountable owner and one durable capability or reason to change;
2. an explicit public surface, or an intentional private status;
3. allowed dependency directions enforced by the language, build graph, or a
   tested policy;
4. owned data, lifecycle, failure, observability, and compatibility behavior;
5. tests at the boundary they claim to prove;
6. a reproducible build/package/deployment declaration;
7. a focused verification path through the real entrypoint when feasible.

Do not accept compilation, green unit tests, a diagram, or a familiar pattern
name as architecture proof by itself.

## 1. Establish context and evidence

### Mandatory audit protocol

When this skill is triggered for a repository change, the bundled checks are a
required part of the work rather than optional advice. Before editing, resolve
the repository root and run both commands below from this skill directory:

```bash
python3 scripts/architecture_tools.py capabilities --root <repo> --format json
python3 scripts/audit_architecture.py <repo> --format json
```

Run the same checks again after editing and before claiming completion. Record
the exact scope, gate, provider status, findings, and exit codes. A source read,
test run, or model-produced claim that the audit was used is not evidence that
the commands ran. If a required provider is unavailable or the bundled audit
cannot execute, report the check as blocked and do not claim architectural
acceptance.

Do not narrow, weaken, or hide the audit to make a change pass. Do not use
`--exclude`, `--fail-on never`, an external `--exceptions` file, or an edited
exception/configuration entry without explicit user approval for that exact
scope and reason. The CLI requires acknowledgement flags for scoped and
inventory-only modes; those flags are not user approval. Never add an exception,
move a file into an ignored/artifact directory, rename a finding away, or edit
the checker to suppress a finding as a workaround. Escalate a genuine contract
conflict to the user and leave the failing evidence visible.

The bundled audit rejects authored inline tests and benchmarks. Test source must
be a runner-recognized file or source set, not a block, function, annotation,
macro, or DSL embedded in production code. Generated and vendored output stays
under its existing provenance policy; it is not a loophole for authored tests.
The inline-test rule has no naming-exception escape hatch.

Before proposing a structural change:

1. Read all applicable repository instructions, ADRs, manifests, CI entrypoints,
   architecture tests, and generated-code policies.
2. Detect languages, language families, runtimes, frameworks, package/build
   managers, workspaces, generators, deployment units, and authoritative
   dependency graphs. Distinguish generators from executors and package
   managers from build tools.
3. Identify users and consumers, deployables, trust boundaries, data
   classifications, state ownership, release/team boundaries, and external
   contracts.
4. Capture quality-attribute scenarios: stimulus, context, measurable response,
   target, and verification method. Include reliability, security/privacy,
   performance/capacity, operability, compatibility, cost, and sustainability
   when material. Read `references/quality-attributes.md`.
5. Inspect representative production, test, generated, vendor, deployment, and
   tooling paths. Infer no boundary from filenames alone.
6. For source-level rules, use the strongest available syntax and graph facts:
   `ast-grep` or Tree-sitter for structural matches, language-native analyzers
   or compiler APIs for symbols/types/references, and the build/package graph
   for resolved dependencies. Treat regex or filename scans as untrusted
   inventories, never as proof of syntax, ownership, or dependency direction.
7. Run the mandatory capability preflight above and record unavailable providers
   before relying on a syntax or graph gate. Use `ast-query` for a read-only
   structural query; configure repeatable queries under `syntax_rules` in
   `.architecture-enforcement.json` without replacing bundled invariants.
8. Baseline the narrowest available build, tests, packaging, and runtime smoke
   before editing; record known failures separately.

For native repositories, classify the build stack explicitly before editing:
CMake is normally the target-model generator; Make may be the authored graph or
only a wrapper; Ninja normally executes generated input; Conan owns C/C++
dependency recipes, profiles, locks, and generated toolchain/dependency files;
and Xmake (often written XMake) can own both target modeling and execution.
Confirm the evidenced owner before touching `Makefile`, `build.ninja`, Conan
output, or generated IDE/project files. Read `references/toolchains.md`.

Rank evidence in this order:

1. compiler, runtime, platform, protocol, ABI, schema, persistence, and
   deployment contracts;
2. repository policy, ADRs, enforced build/module visibility, and CI gates;
3. current official language, framework, and toolchain guidance for pinned
   versions;
4. dominant ecosystem practice and documented organizational constraints;
5. this skill's defaults.

Label observations, inferences, trade-offs, and owner decisions. When evidence
conflicts, preserve the higher-ranked contract or obtain an explicit decision;
do not hide uncertainty behind a generic convention.

## 2. Select an enforcement profile

Choose the smallest profile that explains the real deployment and change
boundaries. Record the drivers, at least one rejected alternative, consequences,
and revisit trigger in an ADR or equivalent architecture record.

- **Modular monolith:** one deployable with capability-owned modules and
  restricted internal imports.
- **Library or SDK:** narrow stable API/ABI, versioned compatibility, package
  contents, and consumer contract tests.
- **Client, UI, or edge runtime:** platform lifecycle, state ownership,
  rendering/input boundaries, offline/failure behavior, and accessibility or
  device constraints.
- **Pipeline or data-oriented system:** explicit stages, data ownership,
  memory/layout, scheduling, throughput, backpressure, and failure propagation.
- **Plugin or extension host:** discovery, capability negotiation, lifecycle,
  version compatibility, resource limits, and failure isolation.
- **Service or distributed system:** independent deployability or scaling,
  data ownership, network contracts, timeouts, cancellation, idempotency,
  retries, observability, and failure domains.
- **Embedded, real-time, or safety-relevant system:** timing, resource,
  interrupt/concurrency, determinism, hazard, and verification budgets.
- **Polyglot workspace:** language-native module boundaries plus explicit
  contract ownership at FFI, schema, process, and generated-code edges.

Do not select microservices, CQRS, event sourcing, a service layer, or a
framework-shaped folder tree without a stated force that the simpler profile
cannot satisfy. Read `references/patterns.md` for pattern gates.

## 3. Enforce boundaries

Apply these invariants at repository, deployable, package, module, capability,
and source-unit levels:

- point policy and domain dependencies inward; adapters implement inward-owned
  ports and are composed only at entrypoints;
- forbid private-path, undeclared, cyclic, and test-support dependencies;
- make sibling capability calls use public contracts, explicit events, or one
  orchestration owner; never use barrels, service locators, reflection, or
  global registries to conceal a bad edge;
- keep public APIs, headers, exports, schemas, events, errors, configuration,
  and database views semantic and versionable; default new symbols to private;
- assign each durable data set and mutation path one owner; document consistency,
  transaction, retention, migration, and deletion behavior;
- keep composition roots thin: load/validate configuration, construct
  adapters, wire ports, start lifecycle, and delegate policy;
- isolate generated, vendored, schema-derived, migration, snapshot, and
  framework-owned artifacts with provenance and deterministic regeneration;
- treat FFI and cross-process calls as contracts with ownership for encoding,
  validation, timeout, cancellation, retries, idempotency, versioning, and
  telemetry;
- promote a directory to a package/project/target only when visibility,
  dependency, build, reuse, deployment, or ownership requires the graph node;
- admit shared code only for stable semantics, at least two real consumers, a
  named steward, independent tests, and lower total coupling than local
  duplication.

### Script and automation boundaries

Keep executable scripts as thin entrypoints. Let the entrypoint parse arguments,
load configuration, call owned modules, render results, and return an exit
status. Move discovery, policy, transformation, persistence, and formatting
into focused modules with direct tests. Do not let one script own filesystem
walking, dependency analysis, exception parsing, and CLI rendering indefinitely.
Treat a changed script above the configured review threshold as an extraction task, not
as a reason to compress code or hide logic in nested functions.

Read `references/principles.md`, `references/toolchains.md`, and
`references/languages.md` for ecosystem-specific enforcement.

## 4. Apply paradigms and patterns deliberately

Start with the language and runtime's native strengths: procedural/data-
oriented, object-oriented, functional, actor/concurrent, reactive/event-
driven, logic/rule, or metaprogramming paradigms. Preserve explicit state,
ownership, effects, scheduling, and error semantics rather than translating
every ecosystem into classes and layers.

For each selected pattern, record:

- the force or quality-attribute scenario it addresses;
- the invariant and ownership boundary it introduces;
- operational and cognitive costs, failure modes, and observability needs;
- the rejected simpler alternative;
- a focused fitness function, contract test, or runtime proof.

Read `references/patterns.md`. Combine patterns only when their boundaries are
compatible. For example, ports-and-adapters can protect a modular monolith;
an outbox can support event publication; an anti-corruption layer can protect
a bounded context during a strangler migration. Do not stack Clean, Hexagonal,
DDD, CQRS, and microservices as synonyms or create interfaces solely to match
their diagrams.

## 5. Enforce naming as a semantic contract

Apply naming authority in this order: toolchain and public contract, framework
discovery, published ecosystem guidance, one explicit repository convention,
then this skill's defaults. Apply the authority to all semantic surfaces, not
only filenames:

- packages, modules, namespaces, targets, and directories name ownership;
- types, functions, methods, values, constants, predicates, and errors name
  behavior and state precisely;
- commands, events, queries, endpoints, schemas, database objects, flags,
  environment variables, metrics, and feature switches use stable ubiquitous
  language and explicit units/semantics;
- abbreviations, boolean polarity, temporal words, and version markers remain
  consistent within a bounded context; avoid `Manager`, `Helper`, `Utils`,
  `Impl`, and `Base` when they hide capability, but permit names such as
  `Repository` or `Factory` when a real boundary and force justify them.

Classify authored, generated, vendored, schema-derived, migration,
snapshot/fixture, and reserved artifacts before applying filename rules. Treat
the scanner's token, colony, generic-bucket, and line-size findings as review
signals unless a toolchain or repository policy makes them gates. Do not cause
destructive renames merely to satisfy an arbitrary count. Read
`references/naming.md` and `references/examples.md`.

## 6. Pass production-quality gates

For every material boundary, define and verify the applicable gates:

- **Reliability:** failure domains, deadlines, retries, idempotency,
  backpressure, recovery, data consistency, and graceful degradation;
- **Security and privacy:** trust boundaries, authentication/authorization
  ownership, least privilege, validation, secrets, supply chain, auditability,
  and data minimization;
- **Performance and capacity:** workload model, latency/throughput targets,
  resource budgets, contention, caching, and scale limits;
- **Operability:** structured logs, metrics, traces, correlation, health,
  rollout/rollback, alert ownership, SLOs, and runbooks;
- **Compatibility and evolution:** API/ABI/schema/event versioning,
  deprecation, migrations, forward/backward compatibility, and consumer tests;
- **Delivery:** reproducible dependencies, hermetic or declared builds,
  generated-output freshness, artifact provenance, and environment parity;
- **Cost and sustainability:** material compute, storage, network, energy, and
  lifecycle trade-offs with an accountable owner.
- **Safety, compliance, and accessibility:** applicable hazards, controls,
  evidence retention, data residency, human-impact constraints, input
  modalities, assistive technology, and localization requirements.

Do not claim a gate passes without a measurable target and executable evidence.
Read `references/quality-attributes.md`.

## 7. Verify with fitness functions

Run the cheapest causal proof first and increase cost only as needed:

1. capability preflight, the full bundled architecture audit, formatter, manifest,
   package-content, schema, and generated-output checks;
2. compiler/type checker and focused unit/contract tests;
3. module visibility, forbidden-import, dependency-cycle, API/ABI, architecture,
   and policy checks;
4. package/workspace build, integration tests, migration checks, and security or
   supply-chain gates;
5. runtime smoke through the changed production entrypoint, then full QA.

Use `scripts/audit_architecture.py <repo>` for deterministic inventory signals,
the mandatory inline-test/benchmark gate, and configured tool-backed rules.
Filename, line-size, generic/flat-bucket, artifact, and lockfile checks are
advisory inventory; they cannot prove semantic ownership, dependency direction,
quality attributes, or runtime correctness. Inline-test findings are policy
errors and cannot be waived through naming exceptions. A required syntax rule
fails closed when its provider is missing, times out, exits unexpectedly, or
emits malformed output. Configure thresholds, provider rules, and exact
exceptions only for reviewed contracts; never use configuration to hide a
finding.
Read `references/verification.md`.

## 8. Refactor and migrate safely

1. Inventory owners, imports/includes, public surfaces, manifests, targets,
   generators, reflection/config references, CI paths, and tests.
2. Baseline behavior and record the target graph, allowed edges, compatibility
   policy, and removal condition for any transition.
3. Establish contracts before moving implementations when consumers need a
   stable seam; move one cohesive owner at a time.
4. Update declarations, imports, exports, manifests, generated inputs/outputs,
   package contents, docs, and tests atomically.
5. Keep structural and semantic changes separate when practical; never leave
   aliases, forwarding barrels, dead targets, empty owners, or migration
   tombstones without a contractual expiry.
6. Compare the final dependency/public graph to the target and run causal proof
   through the real entrypoint.

## 9. Exceptions

Accept an exception only when it records the exact rule and path/scope,
technical or contractual reason, accountable owner, compensating control, and
dated/release/upgrade/removal review trigger. Reject reasons such as
"legacy", "framework", "enterprise standard", "temporary", or "too hard" by
themselves.

Store exact machine-readable naming and artifact exceptions in
`.architecture-enforcement.json`. Keep accepted exceptions visible in audit
output; they waive only their named rule and never convert an excluded scope
into full-repository proof. Use the schema enforced by
`scripts/audit_architecture.py`.

## Required output

Report:

- detected languages, paradigms, toolchains, manifests, workspaces, deployables,
  entrypoints, and authoritative contracts;
- quality-attribute scenarios and selected enforcement profile;
- ADR decision, rejected alternative, dependency direction, ownership/data
  boundaries, public surfaces, and selected pattern invariants;
- naming authorities and changed semantic surfaces, including compatibility
  impact;
- files/packages/targets added, moved, split, consolidated, or retained;
- production-quality gates, fitness functions, focused checks, runtime proof,
  and exact outcomes, including the mandatory capability preflight and full
  architecture-audit command;
- exceptions, unresolved debt, unverified contracts, and material uncertainty.

## Resources

- `references/patterns.md`: architecture styles, design patterns, paradigm
  profiles, selection gates, and ADR template.
- `references/quality-attributes.md`: scenario format and production quality
  gates for reliability, security, performance, operability, evolution, cost,
  and sustainability.
- `references/verification.md`: executable fitness functions, proof ordering,
  and evidence reporting.
- `references/tooling.md`: fixed provider commands, syntax-rule schema, status
  handling, and evidence limits.
- `references/sources.md`: primary architecture and ecosystem authority links;
  verify versions and retrieval dates before treating guidance as a contract.
- `references/principles.md`: ownership, coupling, public-surface, migration,
  and exception rules.
- `references/languages.md`: language-family and ecosystem boundary guidance.
- `references/naming.md`: naming authorities, semantic surfaces, filenames,
  migration, and exceptions.
- `references/toolchains.md`: CMake, Make, Ninja, Xmake, Conan, build systems,
  package managers, workspaces, generated artifacts, and cross-language
  contracts.
- `references/testing.md`: idiomatic test ownership and placement.
- `references/examples.md`: accepted and rejected structures.
- `scripts/audit_architecture.py`: deterministic structural-risk scanner.
- `scripts/architecture_tools.py`: capability discovery and read-only
  ast-grep queries with strict structured-output validation.

### Agent Skills package profile

Treat an Agent Skills directory as a plugin boundary: `SKILL.md` front matter
is the trigger surface, its Markdown body is the instruction surface, and
`scripts/`, `references/`, `assets/`, and `evals/` are optional owned resources.
Do not impose a custom heading schema on the body. Validate the package with
the reference implementation:

```sh
uvx --from skills-ref agentskills validate <skill-path>
```

Keep references one level deep and relative to the skill root. Use
`evals/evals.json` for realistic prompts and expected outcomes, compare with a
no-skill or previous-version baseline, and add assertions only after observing
initial outputs. Follow the current [Agent Skills specification](https://agentskills.io/specification),
[best practices](https://agentskills.io/skill-creation/best-practices),
[description guidance](https://agentskills.io/skill-creation/optimizing-descriptions),
[evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), and
[script guidance](https://agentskills.io/skill-creation/using-scripts) as the
external contract; this skill owns repository architecture and proof, not a
replacement package format.
