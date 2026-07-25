# Architecture fitness rules

Use this reference when selecting boundaries, evaluating a structural proposal,
or planning a migration. These rules operationalize the core contract; they do
not replace language and toolchain requirements.

## Contents

- Ownership and cohesion review; coupling limits; public-surface budget
- Architecture selection; shared-code admission; monolith and fragmentation
- Directory/package promotion; composition roots; generated/vendor boundaries
- Migration gates; fitness functions; exception requirements

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
8. Who reviews an exception or cross-boundary change?

If these answers cannot be stated without listing unrelated concepts, split the
unit. If multiple units have the same answers and only forward calls,
consolidate them.

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
that repeats an ancestor owner for review. Make a finding a hard gate only when
the toolchain or repository policy explicitly requires it. Count
source/header/test/declaration/platform representations of one unit once.

Extract the repeated owner into a durable directory/module/package and keep a
one- or two-token leaf. A resulting single-file owner directory is valid when it
carries package/module identity, visibility, routing, public path, or an
established extraction boundary; a wrapper directory that only disguises one
trivial file is not. Do not mechanically split declaration-matching CamelCase or
PascalCase names. See `naming.md` for authority and language-specific rules.

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

- baseline the build/tests and capture known failures;
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
composition changed.

## 12. Fitness functions

Prefer automated checks that fail on drift:

- dependency-cycle detection;
- forbidden-import rules and module visibility;
- public API/export baselines;
- workspace/project-reference constraints;
- package-content inspection;
- generated-output freshness;
- source/test ownership mapping;
- line, naming, bucket, and flat-cluster heuristics;
- binary size, compile-time, or layering budgets when architecture depends on them.

Run `scripts/audit_architecture.py` as one input. It cannot prove semantic
cohesion or dependency direction.

## 13. Exception requirements

Accept an exception only if it identifies the rule, exact scope, reason, owner,
compensating control, and review/removal condition. Examples include generated
bindings, framework-mandated paths, cohesive parsers/state machines, C/C++
single-header distribution, migrations, fixtures, or compatibility surfaces
with a real deprecation contract.

Reject blanket exceptions and rationales consisting only of "legacy,"
"temporary," "framework," "performance," or "enterprise standard."

Record naming exceptions in `.architecture-enforcement.json` with one exact
repository-root-relative `path` and the fields `rule`, `reason`, `owner`,
`control`, and `review`. Globs are forbidden. Keep accepted exceptions visible
in audit output; they waive only the named rule at the exact path and cannot
serve as full-repository acceptance proof for excluded content.

Classify generated, vendor, schema-derived, migration, snapshot, fixture, or
framework-owned trees with an exact `artifact_exemptions` record containing
`class`, `path`, `reason`, `owner`, `control`, and `review`. A suggestive
directory name is not provenance. Reject overlapping, stale, wildcard, or
control-free artifact records.
