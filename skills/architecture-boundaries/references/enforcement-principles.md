# Architecture fitness rules

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against authority sources (see `enforcement-sources.md`) is required.

Use this reference when selecting boundaries, evaluating a structural proposal,
or planning a migration. These rules operationalize the core contract; they do
not replace language and toolchain requirements.

## Contents

- Ownership and cohesion review; source-topology gate; coupling limits;
  public-surface budget
- Architecture selection; shared-code admission; monolith and fragmentation
- Directory/package promotion; composition roots; generated/vendor boundaries
- Migration gates; fail-closed fitness functions; quality-attribute gates;
  non-waiver requirements

## 1. Ownership test

For every repository, deployable, package, module, target, directory, and
substantial file, answer:

1. What durable product, domain, platform, or pipeline capability does it own?
2. Which changes belong here, and which explicitly do not?
3. What is its supported public surface?
4. Which dependencies may it consume?
5. Which consumers may depend on it?
6. Where are its unit, contract, integration, and architecture tests?
7. Which manifest/build target enforces the boundary?
8. Who reviews a cross-boundary change or artifact-provenance record?

If these answers cannot be stated without listing unrelated concepts, split the
unit. If multiple units have the same answers and only forward calls,
consolidate them.

## 1a. Source-topology and decomposition gate

This gate is mandatory when a change creates, splits, merges, moves, or renames
three or more sibling source files, or changes package/module/directory/export
topology. Enumerate the candidate working tree from both version-control views:

```bash
git diff --name-status
git ls-files --others --exclude-standard
```

The second command is required; untracked source is part of the candidate and
must not be omitted because it is absent from the index. For every changed or
new source unit, record a row containing:

| Path | Owner | Change reason | Visibility | Lifecycle | Dependencies | Consolidation rationale |
| --- | --- | --- | --- | --- | --- | --- |

The owner is the nearest durable capability, not a filename category. The
consolidation rationale must explain why the unit cannot remain with that
owner. A row with no independent contract, lifecycle, dependency boundary,
visibility boundary, or failure policy is a finding, not an architecture
decision.

Do not decompose by syntax or procedure: one type, operation, phase, helper,
or validation rule per file is forbidden when the units share an owner, change
reason, visibility, lifecycle, dependency set, or test contract. `Validation`,
`Helpers`, `Open`, `Reduce`, and `Commit` describe procedural roles in a flow;
they are not durable owners. Keep them separate only with evidence of an
independent lifecycle or contract and a source-topology row that proves it.

The topology map is a gate, not a suggestion. A missing rationale, unexplained
categorical file, or any warning or error finding blocks acceptance. A
pre-change audit provides diagnostic context only; it cannot waive an existing
finding.

## 2. Cohesion review heuristic

When evidence is incomplete, use a 0-2 score on each axis as a comparative
conversation aid. These weights are a local judgment, not an industry
standard, and never establish acceptance by themselves:

| Axis | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Change | unrelated change reasons | sometimes changes together | one durable reason to change |
| Concept | category or convenience | related vocabulary | one recognizable capability |
| Dependency | disjoint collaborators | partially shared graph | same local dependency set |
| Lifecycle | unrelated construction/replacement | coupled in some modes | created, deployed, and replaced together |
| Test | unrelated fixture universes | shared harness only | one owned behavior contract |

Use the result to choose the next evidence: inspect imports, public surface,
change history, lifecycle, and test ownership before preserving, splitting, or
consolidating. Generated/data-oriented units require artifact provenance, not a
better score. Never use the score to justify an illegal dependency or
contractual break.

## 3. Coupling limits

Treat these as architectural defects:

- a package depends on another package's private path;
- a domain module imports a database, web framework, UI toolkit, OS API, or
vendor SDK directly without owning that adapter role;
- a shared module imports one of its consumers;
- a public facade exposes internal transport/persistence types;
- package cycles require initialization-order knowledge;
- test fixtures become a production dependency;
- build metadata declares a boundary that source imports bypass;
- one feature change routinely touches three or more unrelated top-level layers
or repositories.

Prefer compile-time/module-system enforcement. Where the ecosystem lacks it,
add architecture tests, linter rules, build queries, or CI scripts.

## 4. Public-surface budget

Public APIs create long-term change cost. For every new export, public header,
package-visible type, endpoint, plugin contract, or cross-package event, require:

- a named consumer;
- semantics independent of the current implementation;
- versioning/compatibility expectations;
- error and lifecycle behavior;
- a contract test when the boundary is consequential.

Default to private. Do not re-export internals "for convenience." Do not leak
ORM entities, framework request objects, generated clients, or vendor SDK types
across domain boundaries.

## 5. Architecture selection gates

### Modular monolith

Choose when one deployment and transaction boundary is operationally
sufficient. Require feature/domain modules, restricted internal imports,
explicit composition, and data ownership. Do not let modules become naming-only
folders over a shared global model.

### Layered

Choose when policy, orchestration, and technical integration have distinct
change rates. Require inward dependency direction. Reject a layer when
it only forwards calls or renames data.

### Ports and adapters

Choose at unstable I/O or vendor boundaries. The inward owner defines the port
around required capability, not around the vendor API. Do not create an
interface for every class.

### Pipeline/data-oriented

Choose when transformations, stages, scheduling, memory layout, or throughput
dominate. Make data ownership, mutability, backpressure, stage contracts, and
failure propagation explicit. Do not force controller/service/repository layers
onto it.

### Plugin

Choose when extensions must be independently discovered, versioned, enabled,
replaced, or isolated. Define host/plugin direction, compatibility negotiation,
lifecycle, capabilities, resource limits, and failure containment.

### Service boundary

Require at least one operational justification: independent deployment cadence,
scaling profile, failure domain, security/compliance boundary, data
sovereignty, team ownership with operational autonomy, or technology
constraint. Also require observable network contracts, timeouts, retries
idempotency policy, versioning, and data ownership. Otherwise retain an
enforced in-process module.

## 6. Shared-code admission

A shared package is admitted only when all are true:

1. two or more real consumers have identical semantics;
2. the abstraction has a stable capability name independent of consumers;
3. it has a named owner and release/change policy;
4. dependencies point away from consumers;
5. it does not become a channel for domain models to leak;
6. tests prove its own contract;
7. extraction reduces total coupling rather than only duplicate lines.

Prefer local duplication when semantics or change cadence may diverge. A third
copy is a review trigger, not automatic permission to create `shared/`.

## 7. Detecting monoliths and fragmentation

Signs of an accidental monolith:

- multiple independent public APIs or error taxonomies;
- section banners functioning as virtual files;
- unrelated imports grouped by region;
- distinct state/lifecycle machinery;
- separate fixture universes;
- frequent merge conflicts from unrelated changes;
- one edit requires navigating distant, independent regions.

Signs of microfile confetti:

- forwarding and imports dominate behavior;
- most abstractions have one implementation and no policy seam;
- names differ only by `Base`, `Impl`, `Default`, `Manager`, or `Helper`;
- a single operation requires opening many files across categorical folders;
- visibility is widened solely to support splitting;
- files cannot be named by a durable responsibility.

Split the first by responsibility. Consolidate the second into the nearest owner.

## 8. Directory and package promotion

Promote a flat cluster when it has a durable owner and one or more of:

- three or more implementation files with a repeated owner prefix;
- private subcomponents or adapters;
- owned fixtures, tests, generated support, or platform variants;
- a stable facade;
- an enforceable dependency or visibility boundary.

Promote a directory to a package/project/target only when independent
visibility, dependencies, build configuration, reuse, deployment, or ownership
justify the additional graph node. Do not package every directory.

### Filename fitness

Classify authored, generated/vendor/schema-derived, migration, snapshot/fixture,
and reserved artifacts before evaluation. For authored separator-delimited
leaves, remove only active-toolchain test, declaration, generated-companion, and
platform markers. Flag three or more remaining semantic tokens, three or more
sibling logical units sharing a semantic leading token, and a multi-token leaf
that repeats an ancestor owner for review. Count source/header/test/declaration/
platform representations of one unit once. These heuristics do not replace the
source-topology gate; an inventory label cannot be used as an acceptance waiver,
and no threshold override may lower the required review.

Extract the repeated owner into a durable directory/module/package and keep a
one- or two-token leaf. A resulting single-file owner directory is valid when it
carries package/module identity, visibility, routing, public path, or an
established extraction boundary; a wrapper directory that only disguises one
trivial file is not. Do not mechanically split declaration-matching CamelCase or
PascalCase names. See `enforcement-naming.md` for authority and language-specific rules.

## 9. Composition-root rules

Executable entrypoints may:

- read process arguments and environment;
- load and validate configuration;
- construct concrete adapters;
- connect implementations to inward-owned ports;
- start lifecycle and register shutdown;
- delegate to application orchestration.

They must not own business policy, persistence queries, protocol parsing beyond
bootstrap, or reusable algorithms. A growing composition root is evidence of
missing application or platform ownership.

## 10. Generated and vendor boundaries

Generated or vendor code must have:

- an identifiable source or upstream version;
- a deterministic regeneration/acquisition command;
- a segregated path or unmistakable marker;
- a policy for commit versus build-time generation;
- a stale/diff check where committed;
- adapters preventing generated/vendor types from becoming domain contracts.

Never manually patch generated output as the durable fix. Change the schema,
generator, template, patch pipeline, or adapter.

## 11. Migration gates

Before moving code:

- capture pre-change build/test/audit results for diagnosis; do not treat a
  baseline or known failure list as acceptance or a waiver;
- inventory public paths, manifests, build targets, exports, reflection/config
references, code generation, CI filters, and documentation;
- define allowed dependency edges and the target tree;
- choose compatibility policy: atomic consumer update, versioned transition, or
contractual shim with removal condition;
- detect case-only rename and platform path hazards.

During migration:

- move one owner at a time;
- keep path-only and semantic changes separate when practical;
- use compiler/symbol-aware moves;
- validate each changed boundary;
- do not add permanent barrels or aliases to conceal incomplete work.

After migration:

- compare dependency graph to the target;
- verify public API/ABI and package contents;
- remove obsolete paths, targets, aliases, shims, and empty directories;
- run architecture checks, full tests, packaging, and runtime smoke where
  composition changed;
- rerun the unmodified full-repository audit with tracked and untracked
  candidate files included; reject any new unresolved structural finding.

## 12. Fitness functions

Prefer automated checks that fail on drift:

- dependency-cycle detection;
- forbidden-import rules and module visibility;
- public API/export comparisons (diagnostic compatibility evidence, never a
  baseline acceptance waiver);
- workspace/project-reference constraints;
- package-content inspection;
- generated-output freshness;
- source/test ownership mapping;
- line, naming, bucket, and flat-cluster heuristics;
- binary size, compile-time, or layering budgets when architecture depends on them.

Run the target repository's native architecture checks as one input. They cannot prove semantic
cohesion or dependency direction.

## 13. Non-waiver requirements

The audit exposes no baseline, path exclusion, disabled/inventory-only gate,
advisory severity, threshold override, or naming-exception waiver. The required
acceptance run always uses fixed thresholds, full Git-visible scope (tracked
plus non-ignored untracked files), and failure on every warning or error.

If the repository has generated, vendor, schema-derived, migration, snapshot,
fixture, or framework-owned paths, record their provenance and regeneration
control separately. Exact metadata may help the audit classify the artifact,
but an artifact record is not permission to ignore new topology findings. A
stale, overlapping, wildcard, or control-free record is itself a finding.

## 14. Quality-attribute scenarios and gates

Architecture is a response to measurable forces, not a collection of nouns.
Write scenarios before selecting a pattern or boundary. Use this form:

```text
Stimulus: <request, fault, deploy, load, threat, or change>
Context: <normal/peak/failure state, trust zone, data class, version>
Response: <observable behavior and owner>
Target: <latency, throughput, availability, RTO/RPO, error budget, or deadline>
Proof: <test, load run, threat check, telemetry, rehearsal, or review>
```

### Reliability and resilience

Require explicit failure domains, deadlines, cancellation, retry and
idempotency policy, backpressure, overload behavior, recovery, and data
consistency. Define RTO/RPO or availability targets when the system is
operationally significant. Test dependency loss, partial writes, duplicate
delivery, stale reads, restart, deploy rollback, and exhausted capacity.

Do not add retries without a bounded deadline, jitter/backoff, duplicate
semantics, and a decision about which layer owns retry. Do not call a system
resilient because it has a circuit breaker; prove recovery and user-visible
behavior.

### Security and privacy

Map trust boundaries, principals, assets, data classifications, and threat
assumptions. Assign ownership for authentication, authorization, validation,
secrets, key rotation, audit trails, dependency provenance, and incident
response. Minimize data movement and retention. Keep identity and policy types
out of adapters that should not own access decisions.

Verify least privilege, fail-closed behavior, input/output validation, secure
defaults, dependency and artifact scanning, secret absence, and relevant abuse
cases. Treat public APIs, plugins, FFI, generated clients, and message brokers
as attack surfaces.

### Performance and capacity

State workload shape, latency percentiles, throughput, concurrency, memory,
storage, network, startup, and cost budgets that influence architecture. Model
capacity and contention before introducing caches, queues, batching, pools,
lock-free structures, or a new service.

Measure the production-shaped path with representative data and failure states.
Document cache invalidation, freshness, eviction, hot keys, queue limits, and
degradation. A faster microbenchmark does not prove a faster system boundary.

### Operability

Every deployable and consequential async boundary needs an operating owner,
structured logs, metrics, traces/correlation, health/readiness semantics,
alerts, dashboards, rollout/rollback, and a runbook. Define SLOs, error-budget
policy, and what happens when telemetry is unavailable. Keep diagnostic context
at translation and process boundaries without leaking secrets or payloads.

### Compatibility and evolution

For every API, ABI, schema, event, database, generated client, or configuration
contract, define producer/consumer ownership, compatibility direction,
versioning, deprecation, migration, and rollback. Test old/new combinations
when rolling upgrades or mixed versions are possible. Treat serialized names,
error codes, metrics, and environment variables as public contracts when
external consumers depend on them.

### Delivery and supply chain

Require a reproducible dependency resolution policy, authoritative manifests,
lockfile scope, build inputs, generated-output provenance, artifact identity,
and environment parity. Verify that committed generated output is fresh and
that deployment artifacts can be traced to source and tool versions. Keep build
and package boundaries consistent with source visibility.

### Cost and sustainability

Assess compute, storage, network, licensing, energy, and operator time when
they materially constrain the design. Assign an owner and a measurement method;
avoid speculative optimization or sustainability claims without a workload
model. Prefer deletion, bounded retention, right-sized capacity, and simpler
operations when they satisfy the scenario.

### Safety, compliance, and accessibility

For regulated, safety-relevant, or user-facing systems, identify applicable
hazards, controls, evidence retention, auditability, data residency, recovery,
and human-impact constraints. Assign review ownership and preserve traceability
from requirement to implementation and test. For UI and client architecture,
include input modality, assistive technology, localization, privacy, and reduced
motion or resource constraints in the scenarios; defer component-level rules to
the platform design system when one exists.

### Acceptance rule

An attribute is architecturally addressed only when the scenario has an owner,
a target, a design invariant, and executable or independently reviewable proof.
Record unknown targets as risks; do not silently substitute a pattern or a
folder structure for missing requirements.

## Sources

- Architecture source map (see `enforcement-sources.md`); verify the linked source record before relying on current or external claims.
