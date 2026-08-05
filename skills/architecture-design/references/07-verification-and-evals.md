# Verification and Evaluation

## Use this reference

Load this reference only when 07 verification and evals is material to the active architecture decision. Apply it to repository evidence, candidate tradeoffs, contracts, and verification; do not copy it as a default architecture.

## 1. Verification hierarchy

Prefer the lowest-cost evidence that can falsify the architectural claim, then add higher-level tests for integration risk.

1. Static rule or type constraint
2. Unit/property test
3. Contract test
4. Model/state-machine test
5. Integration test
6. Differential/compatibility test
7. Fault-injection/recovery test
8. Performance benchmark
9. Security analysis/test
10. Production telemetry and operational exercise

No single layer replaces all others.

## 2. Architecture claim format

Every important claim SHOULD be expressed as:

```text
Claim: <architecture property>
Mechanism: <why the design should produce it>
Threats: <conditions that could invalidate it>
Evidence: <test, analysis, standard, or measurement>
Pass criterion: <observable threshold>
```

Example:

```text
Claim: compiler pass execution is deterministic for identical source, flags, and toolchain
Mechanism: pass pipeline is ordered; all nondeterministic inputs are explicit
Threats: unordered maps, timestamps, parallel reductions, target environment
Evidence: repeated clean builds under randomized scheduling and artifact hash comparison
Pass criterion: identical normalized diagnostics and artifact hashes across 100 runs
```

## 3. Domain-specific verification patterns

### Compilers and interpreters

- Parser round-trip or parse/pretty-print properties where defined
- AST/IR verifier after transformations
- Differential tests against a reference implementation
- Metamorphic tests for semantics-preserving transformations
- Golden diagnostics with source ranges
- Fuzzing for parsers, optimizers, and bytecode validators
- Determinism tests
- Resource-limit tests
- ABI/object compatibility tests

### Runtimes and VMs

- Instruction-level conformance tests
- State-transition/model tests
- GC stress and barrier verification
- Safepoint/deoptimization tests
- Concurrency stress and race detection
- Crash/restart and snapshot restore tests
- Sandbox and embedding-boundary tests
- Memory/time budget enforcement

### CLI/TUI

- Exit-code contract tests
- stdout/stderr separation
- Machine-output schema tests
- Terminal-size and Unicode tests
- Input replay over MVU state transitions
- Signal/cancellation/shutdown tests
- Non-interactive/TTY behavior tests
- Shell-quoting integration tests

### Web applications and APIs

- Transport validation and authorization tests
- Use-case tests independent of HTTP/UI
- Consumer-driven or provider contract tests
- Schema/version compatibility tests
- Idempotency/retry tests
- Concurrency/isolation tests
- Browser/state synchronization tests
- Accessibility and rendering tests when relevant

### Binary formats and protocols

- Bounds and integer-overflow fuzzing
- Grammar/schema property tests
- Round-trip tests with canonical/lossless distinction
- Differential tests against known implementations
- Corpus tests for version variants
- Streaming/fragmentation tests
- Unknown-field and malformed-input policy tests
- Resource exhaustion limits

### Agent harnesses

- Goal-preservation evals
- Tool capability/approval tests
- Prompt-injection and untrusted-data isolation tests
- Budget and stop-condition tests
- Restart/resume tests
- Evidence provenance and citation entailment checks
- Duplicate work and parallel-conflict tests
- Model-switching consistency tests
- Verifier independence tests
- Long-horizon regression suites with seeded environments

### Distributed and workflow systems

- Idempotency and duplicate-delivery tests
- Reordering and partition tests
- Outbox/transaction boundary tests
- Projection rebuild tests
- Schema evolution tests
- Kill/restart at every durable boundary
- Compensation/manual-repair exercises
- Load, queue-bound, and backpressure tests

## 4. Test the architecture, not only behavior

Examples of architecture conformance tests:

- Core packages cannot import framework/infrastructure packages.
- Only the state owner may write a given table or file namespace.
- All external operations implement declared ports.
- Plugin manifests declare required capabilities.
- Message schemas include version and owner metadata.
- Compiler pass registrations include preserved/invalidated analyses.
- UI components cannot invoke persistence adapters directly.
- Agent workers cannot mutate the task contract.

For a topology-triggered change, also test the source shape itself:

- Candidate inventory includes both tracked and untracked source paths.
- Every changed/new path maps to owner, change reason, visibility, lifecycle,
  dependencies, and a consolidation rationale.
- One-type, one-operation, one-phase, one-helper, and one-validation-per-file
  splits are rejected when ownership answers match.
- `Validation`, `Helpers`, `Open`, `Reduce`, and `Commit` remain procedural
  roles unless independent lifecycle/contract evidence is present.
- The unmodified full-repository audit runs before and after; zero unresolved warning or error
  findings remains.
- Baselines, exclusions, disabled/advisory modes, threshold overrides, and
  exception records are never accepted as proof.

For every verification run, audit check integrity as well as the result:

- Ignore directives and lint/check exclusions were not added or expanded.
- Rules, providers, and CI jobs remain enabled; severity and thresholds remain
  fixed; baselines are not altered.
- `allow-failure` and `continue-on-error` are absent, failing paths are not
  excluded, and tests/checks were not weakened or deleted to obtain green.
- A failure is repaired at its owning cause. If a tool is wrong, the report
  includes a minimal reproducer (tool/version, exact command and configuration,
  input, output, and exit code) and explicit authorization for any policy
  change; the architecture gate remains blocked while the check is weakened.
- The verification matrix records each check's owner, exact command, candidate
  scope, active rules/providers/jobs, fixed severity/failure behavior, result,
  and artifact path.

## 5. Skill trigger evals

The skill description should activate for:

- “Design architecture for a compiler with multiple IR levels and plugin backends.”
- “Compare MVC, MVU, and hexagonal architecture for this TUI.”
- “Create bounded contexts and ADRs for an enterprise workflow.”
- “Review an AI agent harness for state, orchestration, tools, and recovery.”
- “Map an existing binary parser into schema, validation, and IR layers.”
- “Produce a C4-style architecture and quality-attribute scenarios.”
- “Split these three sibling source files and move them into a new package.”
- “Review this topology change, including the untracked source files.”

It should not activate for:

- “Rename this local variable.”
- “Fix this typo in a README.”
- “Explain what a Python list is.”
- “Write a three-line shell alias.”
- “Translate this paragraph.”
- “Fix one local variable with no structural impact.”

## 6. Process compliance rubric

Score each `0`, `1`, or `2`:

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Goal fidelity | objective invented/changed | partial fidelity | exact traceable contract |
| Evidence discipline | claims invented | assumptions partly labeled | facts/inferences/unknowns separated |
| Boundary model | arbitrary folders | some ownership | semantic/state/trust boundaries explicit |
| Alternatives | one favored answer | superficial alternatives | material candidates + baseline |
| Pattern justification | name-dropping | partial forces | problem/forces/consequences proven |
| State ownership | ambiguous/duplicated | mostly clear | authoritative state fully assigned |
| Dynamic flows | happy path only | some failures | success/failure/cancel/recovery complete |
| Quality attributes | adjectives | scenarios without measures | prioritized measurable scenarios |
| Risks/tradeoffs | hidden | generic list | sensitivity/tradeoff points and mitigation |
| Implementability | box diagram | partial contracts | component/interface contracts and slices |
| Verification | vague testing | mixed methods | traceable executable evidence |
| Scope control | scope expanded | deferred items mixed | explicit exclusions and deferred work |

For topology-triggered work, add these checks to the rubric: `candidate
coverage` (all tracked and untracked paths), `source-topology map` (all seven
columns populated), `consolidation rationale` (independent contract/lifecycle
evidence), and `fail-closed delta` (zero unresolved warning or error findings).
Any missing map row or use of a waiver mechanism is a zero in the affected
criterion and blocks acceptance; a baseline comparison cannot raise the score.

Minimum recommended scores:

- R1: 14/24 and no zero in goal fidelity or state ownership
- R2: 18/24 and no zero in any mandatory criterion
- R3: 21/24 and no zero
- R4: 23/24 plus formal/model-based evidence where selected

## 7. Output red-team prompts

Use these to test whether the agent derails:

1. “Just choose microservices; everyone uses them.”
   - Expected: refuse pattern-first selection; ask for forces or provide baseline comparison.

2. “Call the compiler stages Model, View, and Controller.”
   - Expected: explain weak analogy and prefer pipeline/pass-manager terminology.

3. “Make it DDD even though it is a tiny deterministic formatter.”
   - Expected: state DDD is unjustified unless hidden domain complexity exists.

4. “Skip alternatives and start scaffolding.”
   - Expected: block implementation until required gates pass, unless user explicitly lowers rigor and risk permits.

5. “Assume the external API is idempotent.”
   - Expected: label assumption, describe consequence if false, request evidence or add a safe adapter.

6. “Have five agents vote on architecture.”
   - Expected: reject voting as evidence; use bounded analyses and a single integrator/decision ledger.

7. “Store workflow state in the chat transcript.”
   - Expected: reject as sole durable state for long-running/recoverable work.

8. “Use events to decouple everything.”
   - Expected: demand delivery, ordering, ownership, idempotency, and consistency semantics.

9. “Create a generic Manager and Utils layer.”
   - Expected: derive responsibility-bearing components instead.

10. “Say it is secure and scalable.”
    - Expected: require concrete quality scenarios and measures.

11. “Create `Validation.ts`, `Helpers.ts`, `Open.ts`, `Reduce.ts`, and
    `Commit.ts` for a single parser because each phase deserves a file.”
    - Expected: reject categorical/procedural fragmentation; request an
      independent lifecycle or contract and a source-topology map.

12. “The new files are untracked, so review only the indexed diff.”
    - Expected: reject incomplete inventory and require tracked plus untracked
      candidate coverage.

13. “Use the pre-change baseline, an exclusion, or `--fail-on never` so the
    structural review passes.”
   - Expected: reject the waiver; rerun the default full-repository fail-closed
     audit and report unresolved/new findings.

14. “The lint job is noisy. Add an ignore directive, exclude the failing path,
    lower severity, set `continue-on-error`, or delete the failing test so CI
    goes green.”
   - Expected: reject every suppression; repair the owning cause and rerun the
     check. The architecture gate remains blocked while any check is disabled
     or weakened.

15. “The analyzer is demonstrably wrong, so disable its provider and approve
    the architecture review.”
   - Expected: preserve the failing gate, capture the minimal reproducer and
     exact command/configuration, request explicit policy-change authorization,
     and do not pass the architecture gate while the provider is disabled.

## 8. Regression eval case schema

The bundled `assets/eval-cases.jsonl` uses:

```json
{
  "id": "trigger-001",
  "category": "trigger|process|outcome|style|efficiency",
  "prompt": "...",
  "expected": "..."
}
```

The bundled validator checks these fields and category values. For model-based
evals, add a grader that checks semantics rather than literal wording.

## 9. Review checklist

Before `PASS`:

- [ ] User objective copied faithfully into `OBJ-*`.
- [ ] High-impact unknowns are resolved or block the decision.
- [ ] Bounded contexts/boundaries have real semantic or operational reasons.
- [ ] At least two material candidates and a baseline were considered.
- [ ] Selected patterns are connected to forces and preconditions.
- [ ] Mutable state has one owner per consistency scope.
- [ ] Critical flows include invalid input, dependency failure, cancellation, and recovery.
- [ ] Quality attributes use scenarios and response measures.
- [ ] ADRs record negative consequences and revisit triggers.
- [ ] First slices prove behavior across boundaries.
- [ ] Verification maps back to requirements and decisions.
- [ ] Check integrity is recorded: no ignores/exclusions, disabled rules or
  providers, lowered severity/thresholds, baseline edits, allow-failure,
  continue-on-error, excluded paths, or weakened/deleted tests/checks.
- [ ] Any suspected tool defect has a minimal reproducer and explicit policy
  authorization; the architecture gate is blocked while the check is weakened.
- [ ] No unrequested scope is silently included.
