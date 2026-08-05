# Architecture Design Workflow

## Use this reference

Load this reference only when workflow is material to the active architecture decision. Apply it to repository evidence, candidate tradeoffs, contracts, and verification; do not copy it as a default architecture.

The complete 11-phase architecture design procedure. Load when the agent
needs the full step-by-step methodology.

## Phase 0 - Task contract

Extract without embellishment:

- Objective
- Deliverable
- In-scope domains and components
- Explicit constraints
- Explicit exclusions
- Compatibility requirements
- Required rigor and evidence level
- Definition of done

Assign stable identifiers: `OBJ-*`, `REQ-*`, `CON-*`, `EXC-*`, `QA-*`.

**Gate G0 - Goal integrity:** The proposed work can be traced to the user's
request. No invented objective is present.

## Phase 0a - Candidate tree and topology trigger

Treat these as architecture work even when the author calls them a mechanical
refactor: creating, splitting, merging, moving, or renaming three or more
sibling source files, or changing package/module/export/directory topology.
Enumerate the candidate working tree before reading only the indexed diff:

```bash
git status --short
git diff --name-status
git ls-files --others --exclude-standard
```

The untracked-source listing is mandatory. New files are candidate architecture
whether or not they are staged. For repository-affecting work, run the
architecture-enforce capability preflight and full audit before editing and
again after editing:

```bash
python3 skills/architecture-enforce/scripts/providers.py capabilities --root <repo> --format json
python3 skills/architecture-enforce/scripts/audit_architecture.py <repo> --format json
```

The audit exposes one policy: full filesystem scope, fixed thresholds, and
failure on every warning or error. It has no downgrade or waiver mode. Record
commands, scope, provider status, findings, and exit codes. A failed or blocked
preflight/audit stops the design until the owning issue is resolved.

## Phase 1 - Evidence and uncertainty

Inspect available code, documentation, schemas, logs, tests, standards, and
runtime behavior before inferring architecture. Prefer primary sources and
executable evidence.

Classify every material statement as:

- `FACT` - directly observed or sourced
- `USER` - asserted by the user
- `INFERRED` - reasoned from evidence
- `ASSUMED` - provisional and testable
- `UNKNOWN` - not established

For each assumption, record the consequence if false.

**Gate G1 - Evidence sufficiency:** No high-impact decision depends on an
unlabeled or untestable assumption.

## Phase 1a - Source-topology gate

For a topology trigger, create a source-topology table before proposing a tree
and update it after the design is implemented. Include every changed or newly
created source path, including untracked paths:

| Path | Owner | Change reason | Visibility | Lifecycle | Dependencies | Consolidation rationale |
| --- | --- | --- | --- | --- | --- | --- |

The owner must be a durable capability or boundary, not a syntax category. A
row is incomplete without a concrete reason the unit cannot be consolidated
into its nearest owner. Reject one-type, one-operation, one-phase,
one-helper, and one-validation-per-file plans when the units share owner,
change reason, visibility, lifecycle, dependency set, or test contract.
`Validation`, `Helpers`, `Open`, `Reduce`, and `Commit` are procedural roles;
they are not durable owners unless an independent lifecycle, contract,
visibility/dependency boundary, or failure policy is proven.

**Gate G1a - Topology coherence:** Every candidate source path is mapped, every
split has a consolidation rationale, and zero unresolved warning or error findings
remains. Existing findings stay visible with a disposition; a pre-change
result is comparison context, not a baseline waiver.

## Phase 2 - Domain and boundary model

Identify:

1. The problem domain and subdomains.
2. The semantic core: concepts, invariants, state, transitions, and
   authoritative vocabulary.
3. System boundary and external actors.
4. Bounded contexts or equivalent semantic boundaries.
5. Inputs, outputs, commands, events, queries, and side effects.
6. Ownership of mutable state.
7. Trust, privilege, deployment, and failure boundaries.

Use DDD terms only when they clarify the domain. Otherwise use plain boundary,
module, state, and contract language.

**Gate G2 - Boundary coherence:** Every major responsibility has one primary
owner; cross-boundary interactions have explicit contracts.

## Phase 3 - Architectural forces

Create concrete quality-attribute scenarios using
`source -> stimulus -> environment -> artifact -> response -> measure`.

At minimum consider: correctness, modifiability, testability, performance,
reliability, security, observability, portability, operability, and human
reviewability. Mark non-applicable attributes explicitly.

## Phase 4 - Candidate generation

Generate at least two materially different candidates unless only one is
physically or contractually possible. Candidates MUST differ in responsibility
allocation, control flow, state ownership, or dependency direction - not merely
framework choice.

For each candidate provide: structural style, state owner, control authority,
dependency direction, I/O model, failure/cancellation behavior, extension
mechanism, benefits, liabilities, validation evidence needed.

**Gate G3 - Alternatives:** At least two credible candidates and one explicit
"do less" candidate, or a justified impossibility statement. The do-less
candidate is a comparison, not a passing baseline and cannot waive a topology
or audit finding.

## Phase 5 - Pattern decision

Select patterns only after the forces are explicit. A selected pattern MUST
include: problem it solves, preconditions, forces balanced, responsibilities
allocated, invariants protected, consequences, failure modes introduced, reasons
alternatives lost, exit criteria for replacement.

Use the matrix in `references/04-decision-procedure.md`.

## Phase 6 - Structural and behavioral specification

Produce the minimum complete set of views:

1. **Semantic view** - domain concepts, invariants, state ownership.
2. **Static view** - systems, containers/modules, components, dependencies.
3. **Dynamic view** - command/query/event flow for critical scenarios.
4. **Data view** - schemas, lifetimes, consistency, serialization, migration.
5. **Runtime view** - processes, threads/tasks, scheduling, cancellation, backpressure.
6. **Deployment view** - trust zones, persistence, external services, recovery.

**Gate G4 - Flow completeness:** Critical paths include success, invalid input,
dependency failure, timeout/cancellation, retry/recovery, and partial completion.

## Phase 7 - Contracts and invariants

For every major component define: purpose, inputs/outputs, pre/postconditions,
invariants, owned state/lifetime, dependencies/forbidden dependencies, error
taxonomy, concurrency model, idempotency/replay, observability signals, security
assumptions, test seam.

No component may be described solely by a vague noun such as `manager`,
`service`, `handler`, `engine`, or `utils`.

## Phase 8 - Tradeoff and risk review

Run a lightweight ATAM-style review: rank quality scenarios, identify sensitivity
and tradeoff points, identify risks/non-risks, identify unverified architectural
assumptions, record mitigation and validation experiments.

**Gate G5 - Quality fit:** The selected design demonstrably addresses the
highest-ranked quality scenarios and exposes its tradeoffs.

## Phase 9 - Decision records and implementation slices

Write an ADR for every architecturally significant decision. Plan vertical
slices that prove architecture: one real input, semantic validation, one state
transition, one side effect through a port, one observable output, one failure
path, one automated test. Do not turn each step into a file by default: keep
validation, helpers, open/reduce/commit phases, and one-off types with the
nearest durable owner unless the source-topology map proves independent
contracts and lifecycles.

**Gate G6 - Implementability:** Interfaces, ownership, dependency rules, and
first slices are specific enough to implement without inventing architecture
during coding.

## Phase 10 - Verification

Define tests at the correct level: invariant/property tests, contract tests,
golden/snapshot tests, differential tests, state-machine tests, fault-injection
tests, performance budgets, security tests, architecture conformance checks.

Audit the integrity of every check before accepting its result. Do not add or
expand ignore directives or lint/check exclusions; disable rules, providers,
or jobs; lower severity or thresholds; alter baselines; add `allow-failure` or
`continue-on-error`; exclude failing paths; or weaken/delete tests/checks to
make the result green. Fix failures at the owning cause. If a tool is wrong,
preserve the failure and record a minimal reproducer (tool/version, exact
command/configuration, input, output, exit code) while requesting explicit
policy-change authorization; the architecture gate remains blocked while that
check is disabled or weakened.

**Gate G7 - Verifiability:** Each critical requirement maps to an executable
test, inspection, analysis, or monitored measure.

## Phase 11 - Final consistency pass

1. Re-read the user's objective and exclusions.
2. Verify traceability from objective to tests.
3. Search for invented facts and unlabeled assumptions.
4. Search for pattern names unsupported by forces.
5. Search for orphan components and duplicate state owners.
6. Search for missing failure, cancellation, migration, and rollback paths.
7. Verify the source-topology map covers tracked and untracked candidate files.
8. Audit the check configuration and CI diff for ignore/exclusion directives,
   disabled rules/providers/jobs, severity or threshold changes, baseline edits,
   allow-failure/continue-on-error, excluded paths, and weakened/deleted tests.
   Any such suppression is a blocking finding.
9. Run the unmodified architecture-enforce preflight and full audit again when
   repository files changed. Acceptance requires zero unresolved warning or
   error findings.
10. Run bundled validators when applicable and record exact commands, scopes,
    active checks, exit codes, and artifact paths.
