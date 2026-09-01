# System performance, topology, PGO, and regression gates on Bun

Load this before changing server concurrency, worker/process count, CPU affinity, NUMA placement, or release-build optimization policy. [EXAMPLE: BUN-TECH-BACKPRESSURE] [EXAMPLE: BUN-TECH-WORKERS] [EXAMPLE: BUN-TECH-NUMA] [EXAMPLE: BUN-TECH-PGO]

## Representative macro measurement

Treat a microbenchmark as a hypothesis test, not as an acceptance test. The macro workload must state: [EXAMPLE: BUN-TECH-MICRO] [EXAMPLE: BUN-TECH-MACRO-GATE]

- the request/operation mix, payload-size distribution, concurrency, duration, and warm/cold cache state; [EXAMPLE: BUN-TECH-WORKLOAD-MIX] [EXAMPLE: BUN-TECH-COLD-STEADY]
- the service topology: process/worker count, CPU quota and affinity, memory limit, network/database substitutes, and deployment image; [EXAMPLE: BUN-TECH-NUMA] [EXAMPLE: BUN-TECH-WORKERS]
- the measured outcomes: throughput, p50/p95/p99 latency, error/timeout rate, RSS/heap/GC, CPU, and the saturated resource; and [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-PROFILER]
- a holdout workload or trace that was not used to tune the change. [EXAMPLE: BUN-TECH-MACRO-GATE]

Run a fixed-duration steady-state trial after warm-up. Repeat enough trials to distinguish a plausible change from noise; report variation rather than selecting the best run. If the load generator cannot drive the baseline to a bottleneck, improve or distribute the generator before crediting server capacity. [EXAMPLE: BUN-TECH-COLD-STEADY] [EXAMPLE: BUN-TECH-TRIALS] [EXAMPLE: BUN-TECH-MACRO-GATE]

## Concurrency, locality, and NUMA

1. Locate the bottleneck first: event-loop CPU, allocation/GC, kernel I/O, connection pool, database, lock/queue, or downstream rate limit. [EXAMPLE: BUN-TECH-PROFILER] [EXAMPLE: BUN-TECH-BACKPRESSURE]
2. Bound in-flight work with a queue, semaphore, pool, or batching policy. Increase concurrency only while the representative macro result improves without error growth or unacceptable p99/RSS regression. [EXAMPLE: BUN-TECH-BACKPRESSURE]
3. Preserve locality by keeping a request's bytes, parsed form, and response construction in one representation and by partitioning long-lived worker state instead of sharing mutable global state. [EXAMPLE: BUN-TECH-BYTE-VIEWS] [EXAMPLE: BUN-TECH-WORKERS]
4. Treat NUMA or CPU pinning as an optional deployment experiment. Use it only when the production host exposes multiple memory nodes and profiles/counters indicate remote-memory, cross-node, or migration cost. Pin workers and their memory policy consistently, then compare the same workload against the unpinned baseline. [EXAMPLE: BUN-TECH-NUMA]
5. Re-run the full macro workload after changing process count, container CPU/memory limits, affinity, native extensions, or allocator settings; those changes can reverse an application-level result. [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-NUMA]

## PGO and warm-up

Bun application code is JIT-managed at runtime, so an in-process warm-up trial is not a profile-guided build. Record warm-up separately and compare release behavior only after reaching a stable operating state. [EXAMPLE: BUN-TECH-COLD-STEADY] [EXAMPLE: BUN-TECH-PGO]

If the deployment includes a build stage, native extension, or another compiler with a supported PGO workflow: [EXAMPLE: BUN-TECH-PGO]

1. capture profiles from a representative, privacy-safe training workload using the exact target triple and release configuration; [EXAMPLE: BUN-TECH-PGO]
2. build the optimized artifact from those profiles; [EXAMPLE: BUN-TECH-PGO]
3. compare the baseline and PGO artifacts on the representative workload and a holdout workload; and [EXAMPLE: BUN-TECH-PGO]
4. reject or retrain profiles when tail latency, memory, binary size, correctness, or holdout behavior regresses. [EXAMPLE: BUN-TECH-PGO]

Do not commit secret-bearing raw traces or claim PGO support for Bun itself without verifying the selected toolchain's current documentation. [EXAMPLE: BUN-TECH-PGO]

## Regression gates

Automate a performance gate only for a stable, material scenario. Pin the runtime, command, fixture, concurrency, CPU allocation, and acceptance statistic. Store a trusted baseline with its environment metadata, compare distributions rather than one sample, and set thresholds wider than observed noise but narrower than the regression that matters. [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-TRIALS]

A failing performance gate must retain the raw result and environment metadata, permit an explicit reviewed baseline refresh, and never silently update its baseline from the same change being evaluated. Keep correctness tests mandatory: a faster result with changed outputs, error rate, ordering, cancellation, or resource ownership is not an optimization. [EXAMPLE: BUN-TECH-MACRO-GATE] [EXAMPLE: BUN-TECH-ERROR-MIX]
