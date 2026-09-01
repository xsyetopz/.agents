# Unsafe, FFI, SIMD, and layout-sensitive optimization

Reach for these only after representative profiling shows that a safe design has a material residual cost. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI]

## Required proof and checks

- State the safety invariant beside each unsafe operation: pointer provenance, validity, alignment, initialized range, bounds, aliasing/mutability, lifetime, ownership/deallocation allocator, thread access, and ABI/calling convention as applicable. [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI]
- Keep safe validation at the boundary and make the unsafe region as small as possible. Test malformed input, zero/empty/maximum sizes, alignment edges, overflow, aliasing, concurrent access, panic/unwind, and cross-platform behavior. [EXAMPLE: RUST-TECH-UNSAFE-INPUTS] [EXAMPLE: RUST-TECH-UNSAFE-CONCURRENCY] [EXAMPLE: RUST-TECH-UNWIND-PORTABILITY]
- Verify generated behavior or benchmark before assuming manual loops, `#[inline]`, `MaybeUninit`, unchecked indexing, raw pointers, or intrinsics are faster. [EXAMPLE: RUST-TECH-VECTORIZER] [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI]
- Gate CPU features at runtime or use a target-specific deployment artifact. Preserve a supported fallback where portability is required. [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK]
- For FFI, measure conversion, copying, allocation, synchronization, and call costs; ABI correctness and ownership rules are mandatory even if the call is cold. [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI] [EXAMPLE: RUST-TECH-COPY-ALLOC]

`SAFETY:` documents why an operation is valid; `PERF:` documents why it remains necessary. Neither comment substitutes for a test or proof. [EXAMPLE: RUST-TECH-SIMD-UNSAFE-FFI] [EXAMPLE: RUST-TECH-UNSAFE-INPUTS]
