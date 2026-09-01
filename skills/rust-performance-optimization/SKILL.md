---
name: rust-performance-optimization
description: Profile, review, or optimize Rust 1.98+ Edition 2024 code using measured hot-path, allocation, data-layout, concurrency, PGO, SIMD, FFI, benchmark, Cargo-profile, and regression-gate evidence.
---

# Rust Performance Optimization

## Start with evidence

Rust 1.98.0 or newer; Rust Edition 2024; stable toolchain by default. Optional profiling tools may be platform-specific.

Set the user-visible performance objective, workload, compatibility contract, safety invariants, and acceptance metric before changing code. Safe local profiling, edits, and validation may proceed. Deployment, hosted, destructive, or costly changes require explicit authorization. Report changed paths, commands, measurements, preserved contracts, and unresolved toolchain or runtime evidence.

## Workflow

1. Establish the repository's MSRV, edition, target triples, correctness constraints, deployment topology, CPU/NUMA visibility, and existing benchmark, profiler, and CI performance gates. Keep MSRV at or below the stated 1.98.0 baseline unless the repository explicitly changes it.
2. Define the user-visible objective and a representative workload matrix before rewriting: throughput, p50/p95/p99 latency, startup, allocation/RSS, CPU, or cost; realistic input shape and size, concurrency, cache state, error mix, and a holdout case. Keep a local **microbenchmark** separate from the representative application/pipeline **macrobenchmark**; only the latter is the end-to-end acceptance boundary.
3. Find actual or structurally credible hot paths. Run `scripts/scan_rust_hotpaths.py <repo>` as a search aid, then confirm with profiles, benchmarks, call frequency, data volume, allocation evidence, or system-level saturation evidence.
4. Run `scripts/audit_cargo_perf.py <repo>` to inspect `Cargo.toml` release/bench profiles and reproducibility problems.
5. For benchmark design, profiler choice, representative macro measurement, PGO, concurrency, NUMA, and regression gates, read `references/benchmarking-and-profiling.md`. Preserve representative inputs and separate throughput, latency distributions, allocation/copy, memory, binary-size/i-cache, and energy effects.
6. For loop/data-layout rewrites, read `references/hotpath-optimization.md`. Prefer eliminating work, allocations, copies, indirection, synchronization, parsing, and cache misses before low-level instruction tricks.
7. Before changing native interfaces, `unsafe`, raw pointers, custom allocators, SIMD, or layout-sensitive code, read `references/unsafe-ffi-simd.md`. Use `scripts/check_unsafe_justifications.py <repo>` after introducing or touching unsafe code.
8. Before changing worker topology, affinity, or NUMA policy, read `references/concurrency-numa.md`; before Cargo profile, PGO, or post-link layout changes, read `references/pgo-and-cargo-profiles.md`. Apply the largest safe batch of measurable improvements, make one topology or PGO decision at a time, then compare the optimized release artifact against the baseline under the same representative and holdout workloads.
9. Run repository tests, relevant microbenchmarks, representative macrobenchmarks, target-specific builds, and any established regression gate. Return a concise performance report using `assets/PR_PERF_REPORT.md` when the user asks for a PR/report artifact.

For intentionally non-idiomatic optimizations and their tradeoffs, read `references/dirty-optimization-patterns.md`. For Rust 1.98+/Edition 2024 language and toolchain facts, read `references/rust-version-contract.md`. For current version-sensitive source locations, read `references/source-index.md`.
For the numbered optimization order and all listed performance references, use the mechanically mapped [GOOD/RED performance examples](references/performance-examples.md); each item links to a stable `RUST-OPT-*` example ID and each grouped technique links to a named `RUST-TECH-*` pair. RED marks a contrast; GOOD is the optimization pattern. For evidence transfer limits, read the package-local [prior-art protocol](references/prior-art-protocol.md).

### Optimization order

1. Remove unnecessary work and repeated computation. ([RUST-OPT-01](references/performance-examples.md#rust-opt-01)) [EXAMPLE: RUST-OPT-01]
2. Remove allocations, clones, temporary collections, formatting, boxing, and dynamic dispatch from hot paths. ([RUST-OPT-02](references/performance-examples.md#rust-opt-02)) [EXAMPLE: RUST-OPT-02]
3. Improve data layout and locality; favor contiguous storage, compact representations, and one-pass traversal when measured access patterns justify them. ([RUST-OPT-03](references/performance-examples.md#rust-opt-03)) [EXAMPLE: RUST-OPT-03]
4. Reduce copies and bounds checks with iterators/slices first, indexing/unchecked access only when evidence justifies it. ([RUST-OPT-04](references/performance-examples.md#rust-opt-04)) [EXAMPLE: RUST-OPT-04]
5. Reduce synchronization, queueing, and atomic contention; shard or batch before reaching for weaker memory ordering, more threads, affinity, or NUMA policy. ([RUST-OPT-05](references/performance-examples.md#rust-opt-05)) [EXAMPLE: RUST-OPT-05]
6. Specialize common cases and move cold/error paths out of hot loops. ([RUST-OPT-06](references/performance-examples.md#rust-opt-06)) [EXAMPLE: RUST-OPT-06]
7. Batch pipeline stages, filesystem/network/database I/O, flushes, and cross-thread messages while preserving ordering, durability, cancellation, fairness, and bounded memory. ([RUST-OPT-07](references/performance-examples.md#rust-opt-07)) [EXAMPLE: RUST-OPT-07]
8. Tune Cargo release settings and use instrumentation PGO only with compatible tooling, representative profile training, release-artifact comparison, and a holdout workload. Consider BOLT only as an optional target/toolchain-specific post-link experiment when its support is verified. ([RUST-OPT-08](references/performance-examples.md#rust-opt-08)) [EXAMPLE: RUST-OPT-08]
9. Use pooling, arenas, custom allocation, SIMD, intrinsics, raw pointers, or FFI-specific tricks only with benchmark evidence and explicit safety invariants. Check vectorization reports/assembly and guard CPU features with a portable fallback. ([RUST-OPT-09](references/performance-examples.md#rust-opt-09)) [EXAMPLE: RUST-OPT-09]

## Validation

- **Micro:** isolate one local mechanism, use `black_box` for optimizer control, warm up caches/allocators as appropriate, and report distributions plus allocation/copy effects. Use it to support or reject a hypothesis; representative inputs remain the macrobenchmark's responsibility.
- **Macro:** exercise the real binary/pipeline with representative input-size and access-pattern distributions, concurrency, downstream behavior, cache state, I/O, and batching. Use repeated steady-state trials and a holdout workload; make throughput, p50/p95/p99, errors, CPU, RSS, allocations, binary size/i-cache indicators, and queue/lock/I/O signals the acceptance evidence.
- Set regression thresholds only after measuring runner noise; preserve raw trials and environment metadata. Gate correctness/errors first, then user-visible latency/throughput and resource budgets. Require macro evidence for an end-to-end performance decision.

## Boundaries

- `unsafe` does not make code faster by itself. It only enables operations whose safety proof is no longer compiler-enforced.
- `#[inline]` and `#[inline(always)]` are hints, not guarantees; code-size growth can make instruction-cache behavior worse.
- Vectorization/SIMD is an architecture and data-shape decision: verify alignment, aliasing, remainder handling, CPU feature dispatch, generated code, and scalar fallback. Faster inner-loop instructions can lose at the macro level through code size, i-cache pressure, or dispatch overhead.
- Iterator code is not inherently slower than manual loops; inspect generated behavior or benchmark before replacing it.
- `clone()` can be cheap or expensive depending on the type. Treat it as a review signal, not proof of an allocation.
- Treat allocator choice, reserve sizes, ownership moves, serialization, and buffer copies as measurable costs; fewer allocations can still increase RSS or retention.
- Bounds-check removal is often already achieved by idiomatic slice iteration. Introduce unchecked indexing only when a measured residual cost and nearby safety proof justify it.
- `release` defaults are not universally optimal. LTO, codegen-units, panic strategy, target CPU, PGO, and debug info affect portability, build time, binary size, and debuggability.
- `black_box` prevents some optimizer assumptions; it does not make an invalid benchmark representative.
- Edition 2024 is a language-edition contract, not an MSRV. Keep both explicit.
- Rust 1.98 adds stable features but does not justify using nightly-only intrinsics or flags in a stable-targeted repository.
- More threads can worsen tail latency through allocator, lock, cache, or remote-memory contention. Treat CPU affinity and NUMA placement as deployment-specific experiments, not universal defaults.
- NUMA wins must be checked for lock fairness, thread migration, remote-memory traffic, and single-thread performance; a contended benchmark alone is insufficient.
- A microbenchmark can validate a local hypothesis while worsening end-to-end behavior. Use the representative macrobenchmark and holdout workload as the acceptance boundary.

### Unsafe comments

Every newly introduced raw-pointer dereference, unchecked indexing, `get_unchecked`, `unwrap_unchecked`, transmute, mutable static access, manual allocation/deallocation, `unsafe impl`, or nontrivial `unsafe` block must have a nearby `SAFETY:` comment stating the invariant that makes the operation valid. Add a `PERF:` note when the unsafe operation exists specifically for a measured performance reason.
