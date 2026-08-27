# Representative measurement, profiling, and regression gates

## Establish the workload

Benchmark an observable user or system outcome. Record input size and distribution, sequential/random access, hit/miss/error mix, concurrency, cancellation/retry behavior, startup/warm-up state, downstream dependency state, and correctness checks. Separate service time from queueing and I/O wait when possible. [EXAMPLE: RUST-TECH-MACRO-ALLOC] [EXAMPLE: RUST-TECH-ERROR-EDGES]

Use a release-equivalent profile with enough debug information for the selected profiler. Collect repeated independent trials; report distributions (p50/p95/p99 and spread), throughput, errors, CPU, RSS, allocation/copy evidence, and the relevant limiting signal (cache misses, lock contention, syscalls, disk latency, or queue delay). A benchmark that only reports one duration cannot establish a regression. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-MACRO-ALLOC]

## Two non-interchangeable benchmark layers

### Microbenchmark: local mechanism

Use Criterion or the repository's existing harness for a focused operation: parsing, a layout/traversal choice, a clone/copy, an allocator path, a lock, or a SIMD kernel. Use `black_box` to block invalid constant folding, but keep realistic sizes, branch mixes, alignment, cache state, and ownership behavior. Warm caches/allocators deliberately or report cold and warm cases separately. Measure allocation/copy count and retained memory alongside time. A microbenchmark is evidence for a hypothesis, not a proxy for the whole service. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-COPY-ALLOC]

### Macrobenchmark: application/pipeline acceptance

Exercise the real release artifact through its protocol or pipeline. Fix the workload mix, input-size distribution, sequential/random access, concurrency, queue limits, downstream behavior, cache state, retries, batch sizes, and durability contract. Run a steady-state window after startup/warm-up, repeat independent trials on the same target topology, and retain a holdout workload. Gate correctness/errors first, then approved budgets for throughput, p50/p95/p99, CPU, RSS, allocations, binary size/i-cache, and queue/lock/I/O behavior. [EXAMPLE: RUST-TECH-MACRO-ALLOC] [EXAMPLE: RUST-TECH-PIPELINE-IO]

Use history to prioritize expensive benchmarks only as triage: arXiv:2211.13525 reports that a simple performance-change-history strategy can beat more complex prioritizers, but history cannot expose novel paths. arXiv:2501.12878 supports stability-based repetition budgets, while warning that the stability metric is project/language-specific. Keep full representative and holdout runs for final decisions. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-MACRO-ALLOC]

For durable writes, benchmark actual write/flush primitives across multiple batch sizes and sequential/random patterns on the target filesystem/device. Throughput can improve while p99 completion latency worsens; pick the batch size from the durability and latency contract. [EXAMPLE: RUST-TECH-PIPELINE-IO]

## Tool selection

- Use Criterion or the repository's existing harness for statistically repeated microbenchmarks; use `black_box` to avoid invalid constant folding, not to make the input representative. [EXAMPLE: RUST-TECH-PROFILER]
- On Linux, correlate a CPU profile with `perf stat`/`perf record` only when available and permitted. On macOS/Windows, use the platform profiler or flamegraph-compatible capture the repository already supports. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK]
- Measure allocations with the existing allocator instrumentation or a compatible tool. Verify retained memory separately from allocation rate. [EXAMPLE: RUST-TECH-COPY-ALLOC]
- Use tracing/metrics for async queueing, wakeups, request latency, and downstream waits; pair CPU samples with wait metrics to reveal waiting. [EXAMPLE: RUST-TECH-ATOMIC-LOCK]
- For hardware-counter sampling or low-overhead PGO-like profiles, treat arXiv:1411.6361 as platform/toolchain-dependent evidence: validate counter availability, symbolization, and compiler integration before using it, and describe it as complementary to rustc's supported instrumentation PGO. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-PGO-BOLT]

## Regression gates

1. Keep micro and macro workloads separate, each with fixed command, input fixture/seed, warm-up, duration, and sample count. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-MACRO-ALLOC]
2. Run the regression gate on a dedicated or controlled runner when latency is a merge condition; shared CI needs a tolerant advisory/scheduled check because noisy tails create false claims. [EXAMPLE: RUST-TECH-MACRO-ALLOC]
3. Capture the compiler version, target, `RUSTFLAGS`, profile, CPU feature policy, and container/affinity limits as part of the baseline. [EXAMPLE: RUST-TECH-CARGO-PROFILE] [EXAMPLE: RUST-TECH-NUMA]
4. Set budgets after measuring natural variance. Update a baseline only through a reviewed, explicit change; require review after a candidate exceeds its budget. Thresholds should be wider than runner noise but narrower than the regression that matters. [EXAMPLE: RUST-TECH-MACRO-ALLOC]
5. Gate behavior/errors first, then user-relevant latency/throughput and resource budgets. Keep functional coverage as a separate acceptance gate alongside benchmarks. [EXAMPLE: RUST-TECH-ERROR-EDGES]

## Source locations

- Cargo profiles: `https://doc.rust-lang.org/cargo/reference/profiles.html`
- Microbenchmark/application comparison: `https://arxiv.org/abs/2212.09515`
- Stability-based repetition budgets: `https://arxiv.org/abs/2501.12878`
- Historical prioritization: `https://arxiv.org/abs/2211.13525`
- Hardware-counter PGO-like sampling (platform/toolchain dependent): `https://arxiv.org/abs/1411.6361`
