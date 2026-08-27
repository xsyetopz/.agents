# Rust hot paths: work, allocations, copies, and layout

Start with a profile or representative benchmark, then trace the bytes and ownership changes through the hot operation. [EXAMPLE: RUST-TECH-PROFILER] [EXAMPLE: RUST-TECH-COPY-ALLOC]

- Replace repeated computation, parsing, formatting, virtual dispatch, and duplicated validation only when the semantic contract remains intact. [EXAMPLE: RUST-OPT-01] [EXAMPLE: RUST-TECH-ERROR-EDGES]
- Prefer borrowing `&[T]`, `&str`, and views over cloning or rebuilding collections when lifetime/ownership permits. Move ownership when the caller no longer needs the value. [EXAMPLE: RUST-OPT-02] [EXAMPLE: RUST-TECH-COPY-ALLOC]
- Preallocate only from a measured capacity distribution; over-reserving can increase RSS and worsen locality. [EXAMPLE: RUST-TECH-COPY-ALLOC]
- Favor contiguous vectors, packed/compact fields, predictable iteration, and data partitioning when access is dense and cache misses show up. State the representation/access-pattern/locality rationale before converting an aggregate to structure-of-arrays or another layout; measure both the hot traversal and the construction/conversion cost. arXiv:2212.06321 supports treating layout as an explicit representation choice, not a style rule. [EXAMPLE: RUST-TECH-LAYOUT] [EXAMPLE: RUST-TECH-LAYOUT-EDGES]
- Compare allocator behavior and copy traffic, not only allocation counts: `reserve` from measured distributions, borrow or move through pipeline stages, reuse buffers only across proven ownership boundaries, and verify that pooling does not retain oversized memory. [EXAMPLE: RUST-TECH-COPY-ALLOC]
- For vectorization/SIMD, inspect compiler/vectorizer remarks or generated assembly, check alignment/aliasing/remainder paths and runtime CPU-feature dispatch, and retain a scalar fallback when artifacts serve multiple CPU classes. Measure code size and i-cache effects in the macro workload. [EXAMPLE: RUST-TECH-VECTORIZER] [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK]
- Keep cold errors, diagnostics, metrics, and rare format variants out of a dominant loop where that does not weaken observability or required checking. [EXAMPLE: RUST-OPT-06] [EXAMPLE: RUST-TECH-ERROR-EDGES]
- Test overflow, alignment, endian, UTF-8, aliasing, drop, panic, and error behavior after a data-representation rewrite. [EXAMPLE: RUST-TECH-LAYOUT-EDGES] [EXAMPLE: RUST-TECH-UNSAFE-INPUTS] [EXAMPLE: RUST-TECH-UNWIND-PORTABILITY]

A smaller allocation count, fewer clones, or a more manual loop is evidence to investigate—not proof of an end-to-end win. [EXAMPLE: RUST-TECH-COPY-ALLOC] [EXAMPLE: RUST-TECH-MACRO-ALLOC]
