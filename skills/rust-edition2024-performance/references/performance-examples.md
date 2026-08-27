# Rust performance example map

This reference is the auditable example contract for the nine optimization-order items. Each stable ID has both exact-label **GOOD** and **RED** blocks. RED is an anti-pattern, not executable advice. Benchmark the representative release artifact, retain repeated raw trials and a holdout, and gate correctness before performance.

## Optimization-order map

| Item | Stable example ID | Primary decision |
| ---: | --- | --- |
| 1 | `RUST-OPT-01` | Remove unnecessary work and repeated computation |
| 2 | `RUST-OPT-02` | Remove allocations, clones, formatting, boxing, and dynamic dispatch |
| 3 | `RUST-OPT-03` | Improve measured layout and locality |
| 4 | `RUST-OPT-04` | Reduce copies and bounds checks with safe slices/iterators first |
| 5 | `RUST-OPT-05` | Reduce synchronization/queue contention with ownership and bounds |
| 6 | `RUST-OPT-06` | Specialize common cases and isolate cold/error paths |
| 7 | `RUST-OPT-07` | Batch stages/I/O/messages while preserving contracts |
| 8 | `RUST-OPT-08` | Tune Cargo profiles/PGO/BOLT only with artifact and holdout evidence |
| 9 | `RUST-OPT-09` | Use pooling/arenas/unsafe/SIMD/FFI only with proofs and fallbacks |

## Reference-technique coverage

Every technique in the six listed references is either shown by the mapped pair or grouped under that named pair. The ID is the auditable join key.

| Source reference | Technique or caveat | Example ID |
| --- | --- | --- |
| `benchmarking-and-profiling.md` | Micro versus macro boundary; realistic sizes/branches/alignment/cache/ownership; black-box limits | `RUST-OPT-01` |
| `benchmarking-and-profiling.md` | Repeated trials, p50/p95/p99/spread, throughput/errors/CPU/RSS/allocations/copies/limiting signal | `RUST-OPT-01` |
| `benchmarking-and-profiling.md` | Criterion/profiler/tracing/tool selection and dedicated-runner regression gate | `RUST-OPT-08` |
| `benchmarking-and-profiling.md` | `black_box` limits, hardware counters, `perf`/flamegraph availability, and compiler/vectorizer evidence | `RUST-OPT-04`, `RUST-OPT-09` |
| `benchmarking-and-profiling.md` | Durable write/flush primitives, batch sizes, sequential/random access | `RUST-OPT-07` |
| `concurrency-numa.md` | Worker saturation, async task versus worker parallelism, queues, locks, allocator/remote-memory signals | `RUST-OPT-05` |
| `concurrency-numa.md` | Ownership partitioning, sharding, bounded queues, backpressure, cancellation, fairness, shutdown, panic propagation | `RUST-OPT-05` |
| `concurrency-numa.md` | Atomic happens-before proof and ordering; affinity/NUMA/first-touch; pinned/unpinned and single-thread controls | `RUST-OPT-05`, `RUST-OPT-09` |
| `concurrency-numa.md` | Batching filesystem/durable storage without weakening flush/order/failure semantics | `RUST-OPT-07` |
| `dirty-optimization-patterns.md` | Scratch reuse, manual fusion, capacity-aware buffers, common paths, data-oriented layout, sharding, batching | `RUST-OPT-02`, `RUST-OPT-03`, `RUST-OPT-05`, `RUST-OPT-06`, `RUST-OPT-07` |
| `dirty-optimization-patterns.md` | `PERF:` reason, `SAFETY:` proof, readable fallback, preserve errors/durability/cancellation/observability | `RUST-OPT-09` |
| `hotpath-optimization.md` | Remove repeated computation/parsing/formatting/virtual dispatch/duplicate validation | `RUST-OPT-01`, `RUST-OPT-02` |
| `hotpath-optimization.md` | Borrowing, moving, preallocation, capacity distribution, RSS/retention | `RUST-OPT-02` |
| `hotpath-optimization.md` | Contiguous/packed layout, SoA rationale, construction cost, cache misses | `RUST-OPT-03` |
| `hotpath-optimization.md` | Borrow/move pipeline stages, copy traffic, pooling retention | `RUST-OPT-04` |
| `hotpath-optimization.md` | SIMD remarks/assembly, alignment/aliasing/remainders/dispatch/scalar fallback/code size/i-cache | `RUST-OPT-09` |
| `hotpath-optimization.md` | Cold errors/diagnostics/metrics/rare formats; overflow/alignment/endian/UTF-8/drop/panic/error tests | `RUST-OPT-06`, `RUST-OPT-09` |
| `pgo-and-cargo-profiles.md` | Root workspace profile ownership and precedence | `RUST-OPT-08` |
| `pgo-and-cargo-profiles.md` | Same compiler/target/features/workload; instrument/train/use; artifact comparison and holdout | `RUST-OPT-08` |
| `pgo-and-cargo-profiles.md` | Absolute profile paths, stale-profile exclusion, and keeping training artifacts out of source control | `RUST-OPT-08` |
| `pgo-and-cargo-profiles.md` | `opt-level`, LTO, codegen units, panic, strip, debug, incremental, target CPU/features tradeoffs | `RUST-OPT-08` |
| `pgo-and-cargo-profiles.md` | BOLT as optional supported post-link experiment, portable rollback artifact | `RUST-OPT-08` |
| `unsafe-ffi-simd.md` | Pointer/provenance/alignment/init/bounds/aliasing/lifetime/ownership/thread/ABI proof | `RUST-OPT-09` |
| `unsafe-ffi-simd.md` | Boundary validation, small unsafe region, malformed/edge/panic/cross-platform tests | `RUST-OPT-09` |
| `unsafe-ffi-simd.md` | Generated behavior/benchmark; CPU feature dispatch and portable fallback | `RUST-OPT-09` |
| `unsafe-ffi-simd.md` | FFI conversion/copy/allocation/synchronization/call cost and ABI ownership | `RUST-OPT-09` |

## Named technique coverage

| Stable technique ID | Source references | Required GOOD tokens |
| --- | --- | --- |
| `RUST-TECH-PROFILER` | `benchmarking-and-profiling.md` | `perf stat`, `Criterion`, `black_box` |
| `RUST-TECH-MACRO-ALLOC` | `benchmarking-and-profiling.md`, `hotpath-optimization.md` | `macro`, `allocations`, `p99` |
| `RUST-TECH-LAYOUT` | `hotpath-optimization.md`, `dirty-optimization-patterns.md` | `label`, `locality`, `behavior` |
| `RUST-TECH-COPY-ALLOC` | `hotpath-optimization.md`, `dirty-optimization-patterns.md` | `borrow`, `reserve`, `rss` |
| `RUST-TECH-ATOMIC-LOCK` | `concurrency-numa.md` | `Atomic`, `Ordering`, `contention`, `async` |
| `RUST-TECH-NUMA` | `concurrency-numa.md` | `NUMA`, `affinity`, `p99` |
| `RUST-TECH-CARGO-PROFILE` | `pgo-and-cargo-profiles.md` | `workspace`, `opt-level`, `profile.release` |
| `RUST-TECH-PGO-BOLT` | `pgo-and-cargo-profiles.md` | `profile-use`, `BOLT`, `holdout` |
| `RUST-TECH-SIMD-UNSAFE-FFI` | `unsafe-ffi-simd.md`, `hotpath-optimization.md` | `unsafe`, `simd`, `abi` |
| `RUST-TECH-PIPELINE-IO` | `concurrency-numa.md`, `benchmarking-and-profiling.md` | `batch`, `flush`, `durability`, `p99` |
| `RUST-TECH-ERROR-EDGES` | `benchmarking-and-profiling.md`, `hotpath-optimization.md`, `dirty-optimization-patterns.md` | `malformed`, `zero`, `MAX_SIZE` |
| `RUST-TECH-VECTORIZER` | `hotpath-optimization.md`, `unsafe-ffi-simd.md` | `vectorize`, `remainder`, `i-cache` |
| `RUST-TECH-LAYOUT-EDGES` | `hotpath-optimization.md` | `label`, `zero`, `max_label` |
| `RUST-TECH-UNSAFE-INPUTS` | `unsafe-ffi-simd.md` | `malformed`, `len == 0`, `MAX` |
| `RUST-TECH-UNSAFE-CONCURRENCY` | `unsafe-ffi-simd.md`, `concurrency-numa.md` | `Arc`, `catch_unwind`, `thread` |
| `RUST-TECH-UNWIND-PORTABILITY` | `unsafe-ffi-simd.md`, `hotpath-optimization.md` | `catch_unwind`, `cfg`, `fallback` |
| `RUST-TECH-PORTABLE-FALLBACK` | `unsafe-ffi-simd.md`, `pgo-and-cargo-profiles.md` | `is_x86_feature_detected`, `fallback`, `cfg` |

## Paired examples

<a id="rust-opt-01"></a>
<!-- [EXAMPLE: RUST-OPT-01] -->
### `RUST-OPT-01` — remove repeated work

#### GOOD

```diff
--- a/src/parse.rs
+++ b/src/parse.rs
@@
-let normalized = normalize(input);
-let result = parse(normalized);
+let result = parse_normalized(input); // measured: one normalization pass
```

#### RED

```diff
--- a/src/parse.rs
+++ b/src/parse.rs
@@
+let result = parse(normalize(normalize(input))); // repeated work without evidence
```

<a id="rust-opt-02"></a>
<!-- [EXAMPLE: RUST-OPT-02] -->
### `RUST-OPT-02` — allocations and ownership

#### GOOD

```diff
--- a/src/format.rs
+++ b/src/format.rs
@@
-for row in rows.iter() { emit_label(row.label.clone()); }
+for row in rows { emit_label(row.label); } // emit_label(String) caller contract is unchanged
```

#### RED

```diff
--- a/src/format.rs
+++ b/src/format.rs
@@
+for row in rows.iter() { emit_label(row.label.clone()); } // same emit_label(String), needless clone
```

<a id="rust-opt-03"></a>
<!-- [EXAMPLE: RUST-OPT-03] -->
### `RUST-OPT-03` — layout and locality

#### GOOD

```diff
--- a/src/points.rs
+++ b/src/points.rs
@@
-struct Point { x: f32, y: f32, label: String }
+struct Point { x: f32, y: f32, label: String } // public value shape and label behavior remain available
+struct PointColumns { x: Vec<f32>, y: Vec<f32>, label: Vec<String> }
+impl PointColumns {
+    fn at(&self, i: usize) -> Point { Point { x: self.x[i], y: self.y[i], label: self.label[i].clone() } }
+    fn labels(&self) -> impl Iterator<Item = &str> { self.label.iter().map(String::as_str) }
+} // x/y traversal changes layout; Point fields, labels, order, and reconstruction stay intact
```

#### RED

```diff
--- a/src/points.rs
+++ b/src/points.rs
@@
+struct Point { x: f32, y: f32, label: String } // pointer-heavy stride for a numeric traversal
```

<a id="rust-opt-04"></a>
<!-- [EXAMPLE: RUST-OPT-04] -->
### `RUST-OPT-04` — safe copies and bounds

#### GOOD

```diff
--- a/src/sum.rs
+++ b/src/sum.rs
@@
-let bytes = input.to_vec();
-for i in 0..bytes.len() { total += bytes[i]; }
+for &byte in input { total += byte; } // safe slice iteration; no copy
```

#### RED

```diff
--- a/src/sum.rs
+++ b/src/sum.rs
@@
+unsafe { total += *input.get_unchecked(i); } // no residual cost or invariant proof
```

<a id="rust-opt-05"></a>
<!-- [EXAMPLE: RUST-OPT-05] -->
### `RUST-OPT-05` — bounded coordination

#### GOOD

```diff
--- a/src/queue.rs
+++ b/src/queue.rs
@@
-let (tx, rx) = unbounded();
+let (tx, rx) = bounded(1024); // preserves backpressure and cancellation policy
```

#### RED

```diff
--- a/src/queue.rs
+++ b/src/queue.rs
@@
+let (tx, rx) = unbounded(); // throughput-only change; queue/RSS/tail behavior unknown
```

<a id="rust-opt-06"></a>
<!-- [EXAMPLE: RUST-OPT-06] -->
### `RUST-OPT-06` — common and cold paths

#### GOOD

```diff
--- a/src/decode.rs
+++ b/src/decode.rs
@@
+if let Some(value) = decode_common(bytes) { return Ok(value); }
+decode_rare_with_diagnostics(bytes)
```

#### RED

```diff
--- a/src/decode.rs
+++ b/src/decode.rs
@@
+decode_common(bytes).unwrap_or_default() // hides malformed-input/error semantics
```

<a id="rust-opt-07"></a>
<!-- [EXAMPLE: RUST-OPT-07] -->
### `RUST-OPT-07` — batching with durability

#### GOOD

```diff
--- a/src/writer.rs
+++ b/src/writer.rs
@@
+writer.write_batch(batch)?;
+writer.flush_and_confirm()?; // ordering/durability boundary retained
```

#### RED

```diff
--- a/src/writer.rs
+++ b/src/writer.rs
@@
+writer.buffer_forever(item); // unbounded retention and no flush/failure contract
```

<a id="rust-opt-08"></a>
<!-- [EXAMPLE: RUST-OPT-08] -->
### `RUST-OPT-08` — profile/PGO evidence

#### GOOD

```diff
--- a/perf/decision.md
+++ b/perf/decision.md
@@
+compare --release-artifact release --candidate pgo --target=same --workload=representative --trials=5 --holdout=fixtures/holdout --correctness-first
+rollback_if --metric=p99 --metric=RSS --metric=binary-size --holdout
```

#### RED

```diff
--- a/perf/decision.md
+++ b/perf/decision.md
@@
+cargo build --release --features=pgo --target-cpu=native; compare --fastest-micro-only --no-holdout
```

<a id="rust-opt-09"></a>
<!-- [EXAMPLE: RUST-OPT-09] -->
### `RUST-OPT-09` — unsafe/SIMD/FFI proof

#### GOOD

```diff
--- a/src/simd.rs
+++ b/src/simd.rs
@@
+unsafe extern "C" {
+    fn simd_kernel(input: *const u8, len: usize, output: *mut u8) -> usize;
+}
+fn encode(input: &[u8]) -> Vec<u8> {
+    let mut output = vec![0; input.len()];
+    #[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
+    fn avx2_available() -> bool { is_x86_feature_detected!("avx2") }
+    #[cfg(not(any(target_arch = "x86", target_arch = "x86_64")))]
+    fn avx2_available() -> bool { false }
+    if avx2_available() {
+        // SAFETY: input/output are valid for their lengths, non-aliasing, and borrowed for this call; the C ABI writes only output bytes.
+        let written = unsafe { simd_kernel(input.as_ptr(), input.len(), output.as_mut_ptr()) };
+        output.truncate(written.min(output.len()));
+        return output;
+    }
+    scalar(input)
+}
```

#### RED

```diff
--- a/src/simd.rs
+++ b/src/simd.rs
@@
+unsafe { simd_kernel(ptr, len) } // no alignment, aliasing, ABI, feature, or fallback proof
```

## Caveats

Async tasks overlap waits but do not create CPU parallelism. NUMA/affinity is topology-specific. `unsafe`, SIMD, FFI, allocators, unchecked indexing, PGO, BOLT, target CPU, and panic/profile choices affect safety, portability, build/debug behavior, or failure semantics. Keep safe validation, scalar/portable fallbacks, backpressure, and macro correctness gates.

## Named technique pairs

The following named pairs are the concrete coverage targets in the table above. Each pair keeps the mechanism small while making the required evidence and semantic caveat visible.

<!-- [EXAMPLE: RUST-TECH-PROFILER] -->
### `RUST-TECH-PROFILER` — profiler and hardware counters

#### GOOD

```diff
--- a/perf/capture.sh
+++ b/perf/capture.sh
@@
+cargo bench --bench parser # Criterion harness; the benchmark defines its own release-equivalent profile
+perf stat -e cycles,instructions,cache-misses ./target/release/server
--- a/benches/parser.rs
+++ b/benches/parser.rs
@@
+use criterion::Criterion;
+use std::hint::black_box;
+let mut criterion = Criterion::default();
+criterion.bench_function("parser", |b| b.iter(|| black_box(input)));
```

#### RED

```diff
--- a/perf/capture.sh
+++ b/perf/capture.sh
@@
+time cargo run --example parser # one wall-clock sample, no counters or release artifact
```

<!-- [EXAMPLE: RUST-TECH-MACRO-ALLOC] -->
### `RUST-TECH-MACRO-ALLOC` — representative benchmark and allocations

#### GOOD

```diff
--- a/perf/gate.sh
+++ b/perf/gate.sh
@@
+load --release --workload=fixtures/representative --mix=representative --warmup 30s --trials 5 --holdout fixtures/holdout
+allocations=$(measure --metric=allocations); p99=$(measure --metric=p99); record_results --p50 --p95 --p99 --throughput --errors --allocations --RSS --CPU
```

#### RED

```diff
--- a/perf/gate.sh
+++ b/perf/gate.sh
@@
+criterion --bench tiny_input # micro-only result; no macro workload, allocation, or holdout gate
```

<!-- [EXAMPLE: RUST-TECH-LAYOUT] -->
### `RUST-TECH-LAYOUT` — layout while preserving behavior

#### GOOD

```diff
--- a/src/points.rs
+++ b/src/points.rs
@@
-struct Point { x: f32, y: f32, label: String }
+struct PointColumns { x: Vec<f32>, y: Vec<f32>, label: Vec<String> }
+let locality = dense_column_traversal(&points.x); let behavior = points.label.clone();
+fn label<'a>(p: &'a PointColumns, i: usize) -> &'a str { &p.label[i] } // label behavior retained
```

#### RED

```diff
--- a/src/points.rs
+++ b/src/points.rs
@@
+struct PointColumns { x: Vec<f32>, y: Vec<f32> } // drops labels while claiming locality
```

<!-- [EXAMPLE: RUST-TECH-COPY-ALLOC] -->
### `RUST-TECH-COPY-ALLOC` — copies, allocator, and retention

#### GOOD

```diff
--- a/src/encode.rs
+++ b/src/encode.rs
@@
-let copy = bytes.to_vec();
+let mut out = Vec::with_capacity(measured_capacity);
+let borrowed = bytes; out.reserve(measured_capacity);
+let rss = measure_rss(); encode_into(&mut out, borrowed);
```

#### RED

```diff
--- a/src/encode.rs
+++ b/src/encode.rs
@@
+let mut pool = Vec::with_capacity(usize::MAX); // allocator/RSS cost hidden by fewer allocations
+pool.extend_from_slice(bytes);
```

<!-- [EXAMPLE: RUST-TECH-ATOMIC-LOCK] -->
### `RUST-TECH-ATOMIC-LOCK` — contention and memory ordering

#### GOOD

```diff
--- a/src/counter.rs
+++ b/src/counter.rs
@@
+let guard = lock.lock().unwrap();
+let counter = AtomicU64::new(0); let contention = measure_contention(&lock);
+let async_contention = measure_async_contention();
+counter.fetch_add(1, Ordering::Relaxed); // Ordering follows the happens-before proof
```

#### RED

```diff
--- a/src/counter.rs
+++ b/src/counter.rs
@@
+counter.fetch_add(1, Ordering::Relaxed); // weaker ordering chosen from throughput alone
+spawn_many_tasks_without_bound(); // async task count is not CPU parallelism
```

<!-- [EXAMPLE: RUST-TECH-NUMA] -->
### `RUST-TECH-NUMA` — topology-specific placement

#### GOOD

```diff
--- a/perf/numa.md
+++ b/perf/numa.md
@@
+NUMA=production; affinity="pinned,unpinned"; compare --first-touch --affinity="$affinity"
+record --remote-memory --migration --fairness --single-thread --p99 --rss --holdout=fixtures/holdout
```

#### RED

```diff
--- a/src/runtime.rs
+++ b/src/runtime.rs
@@
+pin_threads_to_node(0); // portable default changed without host evidence or rollback
```

<!-- [EXAMPLE: RUST-TECH-CARGO-PROFILE] -->
### `RUST-TECH-CARGO-PROFILE` — workspace profile precedence

#### GOOD

```diff
--- a/Cargo.toml
+++ b/Cargo.toml
@@
+[workspace]
+members = ["app"]
+[profile.release]
+opt-level = 3
+lto = "thin"
```

#### RED

```diff
--- a/dependency/Cargo.toml
+++ b/dependency/Cargo.toml
@@
+[profile.release]
+opt-level = 3 # dependency manifest cannot own the consuming workspace profile
```

<!-- [EXAMPLE: RUST-TECH-PGO-BOLT] -->
### `RUST-TECH-PGO-BOLT` — PGO and post-link comparison

#### GOOD

```diff
--- a/perf/pgo.sh
+++ b/perf/pgo.sh
@@
+profile_use=profile-use; RUSTFLAGS="-C${profile_use}=/abs/merged.profdata" cargo build --release
+bolt optimize --data=representative.fdata target/release/app -o target/release/app-bolt
+run --holdout fixtures/holdout release/PGO/BOLT; retain portable rollback artifact
```

#### RED

```diff
--- a/perf/pgo.sh
+++ b/perf/pgo.sh
@@
+target-cpu=native cargo build --release # no profile training, artifact comparison, holdout, or portability check
```

<!-- [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI] -->
### `RUST-TECH-SIMD-UNSAFE-FFI` — costs, proof, and fallback

#### GOOD

```diff
--- a/src/kernel.rs
+++ b/src/kernel.rs
@@
+unsafe extern "C" {
+    fn ffi_simd(input: *const u8, len: usize, output: *mut u8) -> usize;
+}
+fn encode(input: &[u8]) -> Vec<u8> {
+    let mut output = vec![0; input.len()];
+    let abi_contract: &str = "C";
+    let lifetime = input;
+    debug_assert_eq!(abi_contract, "C");
+    #[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
+    fn avx2_available() -> bool { is_x86_feature_detected!("avx2") }
+    #[cfg(not(any(target_arch = "x86", target_arch = "x86_64")))]
+    fn avx2_available() -> bool { false }
+    if avx2_available() {
+        // SAFETY: input/output are valid for their lengths, non-aliasing, and borrowed for this call; the C ABI writes only output bytes.
+        let written = unsafe { ffi_simd(lifetime.as_ptr(), lifetime.len(), output.as_mut_ptr()) };
+        output.truncate(written.min(output.len()));
+        return output; // SIMD/FFI conversion and call cost are measured against the scalar path.
+    }
+    scalar_encode(input) // portable fallback owns the returned buffer
+}
```

#### RED

```diff
--- a/src/kernel.rs
+++ b/src/kernel.rs
@@
+unsafe { simd_kernel(ptr, len) } // no provenance, alignment, ABI, feature, or scalar proof
```

<!-- [EXAMPLE: RUST-TECH-PIPELINE-IO] -->
### `RUST-TECH-PIPELINE-IO` — pipeline and durable I/O batching

#### GOOD

```diff
--- a/src/pipeline.rs
+++ b/src/pipeline.rs
@@
+for batch in batches(input, 64) { // batch size is part of the durability experiment
+    write_batch(batch)?;
+    let durability = flush_and_confirm()?; let p99 = completion_p99(); record("p99", p99, durability);
+}
```

#### RED

```diff
--- a/src/pipeline.rs
+++ b/src/pipeline.rs
@@
+buffer_all(input); // removes intermediate writes by removing bounded memory/durability semantics
```

<!-- [EXAMPLE: RUST-TECH-ERROR-EDGES] -->
### `RUST-TECH-ERROR-EDGES` — semantic/error edge cases

#### GOOD

```diff
--- a/tests/decoder.rs
+++ b/tests/decoder.rs
@@
+let zero = vec![];
+for input in [malformed(), zero, vec![0; MAX_SIZE]] {
+    assert_error_or_valid_result_without_panic(decode(input));
+}
```

#### RED

```diff
--- a/tests/decoder.rs
+++ b/tests/decoder.rs
@@
+assert!(decode(sample()).is_ok()); // only happy-path behavior is checked
```

<!-- [EXAMPLE: RUST-TECH-VECTORIZER] -->
### `RUST-TECH-VECTORIZER` — compiler evidence and remainder path

#### GOOD

```diff
--- a/perf/vectorize.sh
+++ b/perf/vectorize.sh
@@
+vectorize_remarks=vectorize; RUSTFLAGS="-C llvm-args=-pass-remarks=loop-vectorize" cargo build --release
+report --remainder-path --code-size --i-cache target/release/app
```

#### RED

```diff
--- a/perf/vectorize.sh
+++ b/perf/vectorize.sh
@@
+cargo build --release # assumes vectorization without compiler remarks or remainder evidence
```

<!-- [EXAMPLE: RUST-TECH-LAYOUT-EDGES] -->
### `RUST-TECH-LAYOUT-EDGES` — layout edge behavior

#### GOOD

```diff
--- a/tests/points.rs
+++ b/tests/points.rs
@@
+let zero = 0; assert_eq!(columns.at(zero).label, "");
+assert_eq!(columns.at(columns.len() - 1).label, max_label);
+let behavior = columns.at(zero); let max = max_label; // zero/max layout edges retain label behavior
```

#### RED

```diff
--- a/tests/points.rs
+++ b/tests/points.rs
@@
+assert!(columns.x.len() > 0); // no zero/max or label behavior check
```

<!-- [EXAMPLE: RUST-TECH-UNSAFE-INPUTS] -->
### `RUST-TECH-UNSAFE-INPUTS` — malformed and boundary inputs

#### GOOD

```diff
--- a/src/ffi.rs
+++ b/src/ffi.rs
@@
+validate(malformed, 0, MAX)?;
+if len == 0 || len > MAX { return Err(InputError::Bounds); }
+unsafe { call_checked(ptr, len) }
```

#### RED

```diff
--- a/src/ffi.rs
+++ b/src/ffi.rs
@@
+unsafe { call_checked(ptr, len) } // malformed, zero, and MAX inputs reach the raw call
```

<!-- [EXAMPLE: RUST-TECH-UNSAFE-CONCURRENCY] -->
### `RUST-TECH-UNSAFE-CONCURRENCY` — concurrent access and unwind

#### GOOD

```diff
--- a/tests/ffi.rs
+++ b/tests/ffi.rs
@@
+let shared = Arc::new(buffer);
+let result = thread::spawn({ let shared = Arc::clone(&shared); move || catch_unwind(|| use_shared(&shared)) }).join();
+assert!(result.is_ok());
```

#### RED

```diff
--- a/tests/ffi.rs
+++ b/tests/ffi.rs
@@
+thread::spawn(|| unsafe { use_shared(&GLOBAL) }); // shared access and unwind are uncontrolled
```

<!-- [EXAMPLE: RUST-TECH-UNWIND-PORTABILITY] -->
### `RUST-TECH-UNWIND-PORTABILITY` — unwind and platform fallback

#### GOOD

```diff
--- a/src/dispatch.rs
+++ b/src/dispatch.rs
@@
+let result = catch_unwind(|| dispatch(input));
+#[cfg(any(target_arch = "x86_64", target_arch = "aarch64"))] fn fallback() { portable_path(); }
+// panic/unwind is contained and every supported target has a fallback
```

#### RED

```diff
--- a/src/dispatch.rs
+++ b/src/dispatch.rs
@@
+unsafe { arch_only_path(input) }; // no catch_unwind or cross-platform fallback
```

<!-- [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK] -->
### `RUST-TECH-PORTABLE-FALLBACK` — runtime CPU dispatch

#### GOOD

```diff
--- a/src/kernel.rs
+++ b/src/kernel.rs
@@
+#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
+fn avx2_available() -> bool { is_x86_feature_detected!("avx2") }
+#[cfg(not(any(target_arch = "x86", target_arch = "x86_64")))]
+fn avx2_available() -> bool { false }
+if avx2_available() { avx2_path(input) } else { fallback(input) }
+fn fallback(input: &[u8]) { scalar_path(input); }
```

#### RED

```diff
--- a/src/kernel.rs
+++ b/src/kernel.rs
@@
+avx2_path(input); // assumes one CPU and has no fallback
```
