# Deliberately non-idiomatic Rust optimizations

Use a non-idiomatic form only with a measured reason and a local invariant. Examples: reusable scratch storage, manual loop fusion, capacity-aware buffers, specialized common paths, data-oriented layout, sharded state, explicit batching, and a narrowly scoped unsafe primitive. [EXAMPLE: RUST-TECH-COPY-ALLOC] [EXAMPLE: RUST-TECH-LAYOUT] [EXAMPLE: RUST-TECH-ATOMIC-LOCK] [EXAMPLE: RUST-TECH-PIPELINE-IO]

Place `PERF:` beside the optimization with the workload/metric and preserve a `SAFETY:` proof where unsafe applies. Keep a readable reference or slow path when rare inputs, portability, or error semantics need it. [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI] [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK] Do not remove checks, durability, cancellation, panic/error handling, or observability merely to improve a benchmark. [EXAMPLE: RUST-TECH-ERROR-EDGES] [EXAMPLE: RUST-TECH-PIPELINE-IO]
