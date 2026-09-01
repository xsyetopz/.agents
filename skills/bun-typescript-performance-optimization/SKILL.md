---
name: bun-typescript-performance-optimization
description: Profile, review, or optimize Bun 1.4+ JavaScript or TypeScript 7+ applications using measured hot-path, allocation, Bun-native API, server/CLI, bundling, benchmark, CPU/heap-profile, and regression-gate evidence.
---

# Bun and TypeScript Performance Optimization

## Start with evidence

Bun 1.4.0 or newer; ECMAScript 2025 language baseline; TypeScript 7.0 or newer. This skill targets Bun runtime behavior, not browser-only or Node-only projects.

Set the user-visible performance objective, workload, compatibility contract, and acceptance metric before changing code. Safe local profiling, edits, and validation may proceed. Deployment, hosted, destructive, or costly changes require explicit authorization. Report changed paths, commands, measurements, preserved contracts, and unresolved runtime evidence.

## Workflow

1. Confirm Bun is the runtime/toolchain being optimized and identify deployment topology, TypeScript version, `tsconfig.json`, package-manager policy, CPU/NUMA visibility, and existing benchmark, profiler, and CI performance gates.
2. Keep the language contract explicit: Bun >=1.4, TypeScript >=7.0, and ES2025 for `target`/`lib` unless repository requirements intentionally differ. Read `references/typescript-es2025-contract.md` before changing compiler settings.
3. Establish a reproducible baseline for the user-visible objective: throughput, p50/p95/p99 latency, startup, memory/GC, CPU, or cost. Keep a **microbenchmark** for one local mechanism separate from a **representative application/load benchmark** for acceptance; the latter must include realistic payload distributions, concurrency, cache state, error mix, downstream waits, and a holdout case.
4. Find real or structurally credible hot paths. Run `scripts/scan_bun_hotpaths.py <repo>` as a search aid, then confirm with CPU/heap profiles, benchmark frequency, request volume, payload size, allocation evidence, or system-level saturation evidence.
5. Run `scripts/audit_bun_project.py <repo>` to inspect package/runtime pins and TypeScript/Bun configuration.
6. Load `references/benchmarking-and-profiling.md` for the micro/macro boundary, JSC warm-up/profile realism, profiler selection, memory accounting, and regression-gate design. Use `mitata` for focused comparisons and `bombardier`, `oha`, or another generator that demonstrably does not bottleneck `Bun.serve()`.
7. Prefer removing work and crossing fewer abstraction/runtime boundaries. When a Bun-native API can replace a dependency or Node compatibility path, read `references/bun-native-performance.md` before rewriting. For loops, object shapes, buffers, strings, JSON, collections, promises, and server paths, read `references/js-ts-hotpaths.md`.
8. Before tuning concurrency, workers, process count, affinity, or NUMA placement, read `references/concurrency-and-locality.md` and `references/system-performance.md`. Establish saturation or contention and measure one topology change at a time; keep tail latency, memory, and downstream capacity within the stated budgets.
9. Treat runtime warm-up, build caching, and PGO as separate mechanisms. Bun 1.4 exposes CPU/heap profile flags, but a warmed JavaScriptCore process is not build PGO. Read `references/system-performance.md` before proposing a compiler/native-extension PGO flow.
10. Apply the largest behavior-preserving batch supported by evidence, then run tests, type checking, builds, representative benchmarks, and any repository regression gate. Return `assets/PR_PERF_REPORT.md` when a structured PR/performance report is requested.

For the numbered optimization order and all listed performance references, use the mechanically mapped [GOOD/RED performance examples](references/performance-examples.md); each item links to a stable `BUN-OPT-*` example ID and each grouped technique links to a named `BUN-TECH-*` pair. RED marks a contrast; GOOD is the optimization pattern. For evidence transfer limits, read the package-local [prior-art protocol](references/prior-art-protocol.md).

### Optimization order

1. Eliminate unnecessary requests, parsing, serialization, copies, dependency work, and repeated initialization. ([BUN-OPT-01](references/performance-examples.md#bun-opt-01)) [EXAMPLE: BUN-OPT-01]
2. Remove hot-path allocations: temporary arrays/objects, spread copies, repeated encoders/decoders, interpolation, regex construction, closure creation, and avoidable Promise choreography. ([BUN-OPT-02](references/performance-examples.md#bun-opt-02)) [EXAMPLE: BUN-OPT-02]
3. Keep object shapes stable and data representations simple; avoid polymorphic property patterns in inner loops. ([BUN-OPT-03](references/performance-examples.md#bun-opt-03)) [EXAMPLE: BUN-OPT-03]
4. Prefer typed arrays, `ArrayBuffer`/views, streaming, and Bun-native byte/file/network primitives when they eliminate copies and conversions without extending lifetimes or buffering unexpectedly. ([BUN-OPT-04](references/performance-examples.md#bun-opt-04)) [EXAMPLE: BUN-OPT-04]
5. Improve locality: process contiguous data in order, fuse only the passes that remove material intermediates, and keep payload representation stable through the dominant path. ([BUN-OPT-05](references/performance-examples.md#bun-opt-05)) [EXAMPLE: BUN-OPT-05]
6. Batch I/O, logging, database/network operations, and cross-thread/process work. Bound concurrency to measured downstream capacity, not core count alone. ([BUN-OPT-06](references/performance-examples.md#bun-opt-06)) [EXAMPLE: BUN-OPT-06]
7. For fixed HTTP responses, prefer `Bun.serve({ routes })` static `Response` values when semantics permit; for small immutable assets compare startup-buffered `new Response(await Bun.file(path).bytes())` with `new Response(Bun.file(path))`/directory routes for larger or changing files. Production HTML imports should be prebuilt, not bundled per request. ([BUN-OPT-07](references/performance-examples.md#bun-opt-07)) [EXAMPLE: BUN-OPT-07]
8. Replace compatibility/dependency layers with Bun-native APIs when semantics match and measurement supports the change. ([BUN-OPT-08](references/performance-examples.md#bun-opt-08)) [EXAMPLE: BUN-OPT-08]
9. Specialize common cases and separate cold validation/error/reporting paths. ([BUN-OPT-09](references/performance-examples.md#bun-opt-09)) [EXAMPLE: BUN-OPT-09]
10. Tune bundling/minification/splitting, workers, process concurrency, affinity/NUMA, or a supported deployment PGO flow only after application-level waste is addressed. ([BUN-OPT-10](references/performance-examples.md#bun-opt-10)) [EXAMPLE: BUN-OPT-10]

## Validation

- **Micro:** isolate a local operation, use realistic type/branch mixes, warm up explicitly, report distribution and allocation effects, and use it to reject or support a hypothesis—not to certify the service.
- **Macro:** exercise the built application through its real protocol and topology with an external load generator, fixed duration, steady-state warm-up, realistic operation/payload distributions, downstream behavior, and p50/p95/p99, throughput, errors, CPU, RSS, JS heap, native heap, and queue/backpressure signals. Make this the merge gate.
- Record independent trials and noise; select results from the stated aggregation rule rather than the fastest run. A microbenchmark can train an unrealistically monomorphic JSC profile, just as managed-runtime literature documents for JVMs, so validate every hot-path win in application context.

For intentionally non-idiomatic optimizations, read `references/dirty-optimization-patterns.md`. For current version-sensitive source locations, read `references/source-index.md`.

## Boundaries

- Bun executes TypeScript by transpiling it; TypeScript's compiler remains a separate type-checking/tooling concern. A successful `bun run` is not a substitute for TypeScript 7 type checking.
- TypeScript 7 uses the native Go compiler line. Preserve repository invocation conventions (`tsc`/tool wrappers) rather than assuming old compiler internals.
- For TypeScript 6+ and 7+, Bun documents that `compilerOptions.types` no longer implicitly discovers all `@types`; Bun projects generally need `"types": ["bun"]` with `@types/bun` installed.
- Bun's generic docs often recommend `ESNext`; this skill intentionally uses ES2025 as a fixed reproducible language baseline. Keep that baseline explicit instead of adopting floating `ESNext`.
- A Bun-native API needs workload evidence. Benchmark the actual operation and payload distribution.
- `Promise.all` increases concurrency, not CPU parallelism. It can increase memory pressure or overload downstream services.
- Array spread, object spread, destructuring, and chained array combinators can allocate/copy. They are review signals, not automatic bugs.
- JavaScriptCore optimization depends on runtime shapes and observed types. Avoid speculative micro-optimizations without profiling.
- Keep hot objects shape-stable: initialize fields consistently, avoid changing property presence/value kinds, and avoid mixing unrelated record shapes or numeric/string types in one hot call site. This is a JSC hypothesis to verify, not a promise of a particular inline-cache behavior.
- Distinguish Bun's JavaScript heap from native memory: use `heapStats()`, `Bun.gc()`/heap snapshots for JS retention, `Bun.unsafe.mimallocDump()` for native allocator state, and RSS for the process-level outcome. A smaller JS heap can coexist with higher native memory or retained buffers.
- `Uint8Array`/`ArrayBuffer` views can remove byte copies only when ownership, mutation, detachment, and lifetime are proven. A view that prolongs a large backing buffer can worsen RSS.
- `Bun.serve` static routes, `Bun.file`, streaming, and backpressure have different memory/I/O behavior; benchmark route dispatch and the deployed server, not only a handler function.
- A load generator slower than the server under test reports the generator's ceiling, not the server's.
- A microbenchmark may validate a local hypothesis while worsening production due to JSC profile pollution, GC, queueing, cache behavior, or I/O. Keep the representative macrobenchmark as the acceptance gate.
- NUMA and CPU-affinity changes are deployment-specific. Use them only when the host topology is visible and relevant, and revalidate after container, allocator, or process-count changes.

### Optimization comments

When a performance rewrite intentionally reduces readability, depends on a stable object shape/buffer lifetime, reuses mutable storage, relies on byte-level aliasing/view semantics, or duplicates a specialized hot path, add a short `PERF:` comment stating the measured/structural reason and the invariant future edits must preserve.
