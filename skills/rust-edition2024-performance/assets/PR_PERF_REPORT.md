# Controlled empirical evidence report

<!-- GENERATED FILE. Regenerate with scripts/generate_skill_reports.py. -->

> Generated for `rust-edition2024-performance`. Use this shared report shape for the skill.

## Decision summary

- Decision:
- Evidence status:
- Acceptance result:

## Fixed scope and hypothesis

- Scope and acceptance boundary:
- Hypothesis and mechanism:
- Preserved semantic, safety, compatibility, and resource contracts:

## Baseline/control

- Baseline revision/artifact:
- Control configuration and comparison:
- Baseline selection rationale:

## Environment

- Runtime/compiler/tool versions:
- OS, CPU, container/cgroup, memory, affinity/NUMA, and deployment topology:
- Repository revision, flags, dependency/lockfile state, and relevant configuration:

## Workload/cases

- Representative workload matrix (input/payload distribution, access pattern, concurrency, cache state, errors/retries, downstream behavior):
- Warm-up/cold-start treatment and duration:
- Holdout workload/cases not used for tuning:

## Intervention

- Changed paths and owning decision:
- Exact commands/configuration used:
- Safety/ownership/lifetime/backpressure/durability invariants:

## Metrics/results

Rust-specific metrics: allocations/copies, lock/cache/syscall signals, RSS, binary size/i-cache, target CPU/NUMA.

| Scope | Case | Trial | Before/control | After/candidate | Delta | Raw result/variation | Command or artifact |
|---|---|---:|---:|---:|---:|---|---|
| Micro |  | 1 |  |  |  |  |  |
| Macro |  | 1 |  |  |  |  |  |
| Holdout |  | 1 |  |  |  |  |  |

- Report repeated independent raw trials, distributions/spread, throughput, p50/p95/p99, errors/timeouts, CPU, memory, and bottleneck-specific signals as applicable.

## Semantic/correctness gates

- Tests, type/build checks, replay/output comparison, and invariant checks:
- Error, ordering, cancellation, ownership/lifetime, portability, and security results:

## Threats to validity

- Runner noise, workload representativeness, holdout limits, profiler/measurement bias:
- Unseen behavior, environment drift, model/runtime specificity, and remaining confounders:

## Reproduction commands

```text
# Pin environment and run the baseline/control:
# Pin environment and run the candidate/intervention:
# Run semantic/correctness gates and holdout:
```

## Decision/rollback

- Decision and acceptance rule:
- Rollback condition and preserved baseline/artifact:
- Baseline refresh or follow-up review path:

## Unresolved risks

-
