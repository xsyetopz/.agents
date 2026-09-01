# Representative measurement, profiling, and regression gates

## Establish the workload

Write the benchmark around an observable outcome, not an implementation detail. Record the operation mix, input-size distribution, sequential/random key or file-access mix, concurrency, think time, cache state, failure/retry behavior, downstream dependencies, payload encoding, and correctness checks. Split client-observed latency from server service time and queue time where possible. [EXAMPLE: BUN-TECH-WORKLOAD-MIX]

Run enough warm-up to reach the intended steady state, then collect repeated independent process trials. Keep cold-start/startup results separate from warm steady-state results. Report median and spread (IQR/MAD or confidence interval where appropriate) as well as p50/p95/p99, throughput, error count/rate, CPU, RSS, JavaScript-heap measurements, native-heap measurements, and one bottleneck-specific signal such as GC, queue delay, open connections, or bytes copied. Re-run an unexpected result before changing code; do not publish the best run. [EXAMPLE: BUN-TECH-TRIALS] [EXAMPLE: BUN-TECH-COLD-STEADY]

## Two non-interchangeable benchmark layers

### Microbenchmark: local mechanism

Use `mitata` or the repository's existing harness to compare one operation: parsing, a loop, a byte conversion, route selection, serialization, or allocation pattern. Pin the input and consume the result so the benchmark cannot be optimized away. Include representative small/medium/large inputs and the type/branch mix seen by the application; warm up the same function before measuring and record the Bun version and command. Measure allocation and retained-memory effects separately from elapsed time. A micro result supports a local hypothesis only. [EXAMPLE: BUN-TECH-MICRO] [EXAMPLE: BUN-TECH-WORKLOAD-MIX]

### Macro/load benchmark: application acceptance

Drive the built server/CLI through its real protocol and deployment shape. Pin the operation and payload distributions, concurrency, duration, cache state, downstream fakes or services, error/retry mix, CPU/memory limits, and load-generator capacity. Use a fixed-duration steady-state window after warm-up, repeated independent trials, and a holdout trace or workload that was not used to tune the change. Gate on correctness/errors first, then approved budgets for throughput, p50/p95/p99, CPU, RSS/heap, and queue/backpressure. If the candidate wins only in the micro suite, keep the application result as the decision. [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-ERROR-MIX]

Managed-runtime caution: arXiv:2605.23570 demonstrates the problem on JVMs—isolated tests can train unrealistic branch/type profiles despite careful harnessing. The runtime is different, so apply its narrower lesson to Bun rather than transferring JVM measurements to JSC; apply the narrower lesson to Bun by mixing realistic types/branches and requiring application-context validation. arXiv:2212.09515 likewise found optimized micro suites can detect application changes while producing frequent false positives, so they are not complete proxies. arXiv:2501.12878 supports stability-based repetition budgets, but choose the stability metric for this project/runtime and retain a full macro gate. [EXAMPLE: BUN-TECH-WORKLOAD-MIX] [EXAMPLE: BUN-TECH-TRIALS]

For synchronous/durable writes, measure the exact file system, device class, flush primitive, write sizes, and sequential/random pattern. A larger batch can increase throughput while worsening per-operation tail latency; choose from the required latency and failure-safety contract rather than throughput alone. [EXAMPLE: BUN-TECH-DURABLE-IO]

## Bun tools

Use Bun 1.4+'s built-in profiles around a workload that lasts long enough to produce useful samples. [EXAMPLE: BUN-TECH-PROFILER] `--cpu-prof` writes a Chrome/DevTools `.cpuprofile`; `--cpu-prof-md` writes a grep/LLM-friendly profile. `--heap-prof`/`--heap-prof-md` write an exit-time heap profile; allocation sampling intervals require a different profiler because these heap flags provide no such intervals in JavaScriptCore.

<!-- [EXAMPLE: BUN-TECH-PROFILER] -->
```bash
mkdir -p profiles
bun --cpu-prof --cpu-prof-dir profiles ./src/server.ts
bun --cpu-prof-md --cpu-prof-dir profiles ./src/server.ts
bun --heap-prof-md --heap-prof-dir profiles ./src/server.ts
```

Load CPU profile JSON in Chrome DevTools or inspect the Markdown profile. Pair baseline/candidate snapshots after equivalent workload completion, and capture application metrics too—profiles become end-to-end evidence when paired with application metrics. [EXAMPLE: BUN-TECH-PROFILER]

For memory, keep three views distinct: [EXAMPLE: BUN-TECH-PROFILER]

- JavaScript heap: `import { heapStats } from "bun:jsc"`; use `Bun.generateHeapSnapshot()` to investigate retained objects and `Bun.gc()` only as a deliberate diagnostic boundary. [EXAMPLE: BUN-TECH-PROFILER]
- Native heap: `Bun.unsafe.mimallocDump()` for non-JavaScript allocations and allocator state. [EXAMPLE: BUN-TECH-PROFILER]
- Process outcome: RSS, faults, and cgroup memory under the same workload. [EXAMPLE: BUN-TECH-PROFILER]

Interpret all three with allocation rate, buffer lifetimes, and GC pauses. A heap snapshot is not a native-heap report, and forcing GC can hide the steady-state behavior being optimized. [EXAMPLE: BUN-TECH-PROFILER]

## Regression gates

1. Keep a deterministic microbenchmark for a local mechanism and a separate macro/load scenario for the user-facing operation. [EXAMPLE: BUN-TECH-MICRO] [EXAMPLE: BUN-TECH-MACRO-GATE]
2. Pin benchmark inputs, command, runtime version, CPU/container allocation, warm-up, duration, and sample count in the existing test/CI surface. [EXAMPLE: BUN-TECH-TRIALS] [EXAMPLE: BUN-TECH-COLD-STEADY]
3. Gate on a tolerant, reviewed budget only after observing noise on that runner. Prefer p95/p99 and error budgets for services, plus throughput/CPU/RSS/heap where those are the constraint. Set the threshold wider than normal variance but narrower than the regression that matters; state the number of trials and decision rule. [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-TRIALS]
4. Make a baseline update an explicit reviewed change. Retry a noisy run and inspect host/load changes before accepting a regression or moving the threshold. [EXAMPLE: BUN-TECH-TRIALS]
5. Run fragile latency thresholds on a reproducible scheduled or dedicated runner; expose that result to review instead of using shared, variable CI as a required merge gate. [EXAMPLE: BUN-TECH-MACRO-GATE]

## Source locations

- Bun benchmarking, heap distinctions, and CPU/heap flags: `https://bun.com/docs/project/benchmarking`
- Bun 1.4 release context: `https://bun.com/blog/bun-v1.4`
- Microbenchmark/application comparison: `https://arxiv.org/abs/2212.09515`
- Managed-runtime profile realism caveat (JVM evidence; apply cautiously to JSC): `https://arxiv.org/abs/2605.23570`
- Stability-based repetition budgets: `https://arxiv.org/abs/2501.12878`
- Historical prioritization: `https://arxiv.org/abs/2211.13525`
