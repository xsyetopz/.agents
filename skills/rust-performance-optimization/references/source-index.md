# Source index

Use primary documentation for version-sensitive claims; verify the selected
target/toolchain before enabling platform-specific optimization.

## Official sources

- Rust 1.98.0 release (current latest as of 2026-08-27): <https://blog.rust-lang.org/releases/latest/>
- Edition 2024 guide: <https://doc.rust-lang.org/edition-guide/rust-2024/>
- Cargo profiles: <https://doc.rust-lang.org/cargo/reference/profiles.html>
- Cargo `rust-version`: <https://doc.rust-lang.org/cargo/reference/rust-version.html>
- Rust instrumentation PGO: <https://doc.rust-lang.org/rustc/profile-guided-optimization.html>
- Rust codegen options: <https://doc.rust-lang.org/rustc/codegen-options/index.html>
- `std::hint::black_box`: <https://doc.rust-lang.org/std/hint/fn.black_box.html>
- LLVM BOLT availability/build context: <https://llvm.org/docs/AdvancedBuilds.html#bolt>

## Relevant prior art

- arXiv:2605.23570, *Misleading Microbenchmarks on the Java Virtual Machines* — managed-runtime profile-realism warning; JVM evidence only, useful as a boundary reminder for any JIT comparison: <https://arxiv.org/abs/2605.23570>
- arXiv:2212.09515, *Using Microbenchmark Suites to Detect Application Performance Changes* — micro suites can detect changes but can produce false positives: <https://arxiv.org/abs/2212.09515>
- arXiv:2501.12878, *μOpTime* — stability-based repetition budgets, with language/project-specific metric choice: <https://arxiv.org/abs/2501.12878>
- arXiv:2211.13525, *Evaluating Search-Based Software Microbenchmark Prioritization* — simple history can prioritize efficiently, but cannot cover novel paths: <https://arxiv.org/abs/2211.13525>
- arXiv:1411.6361, *Hardware Counted Profile-Guided Optimization* — low-overhead hardware-counter sampling is promising but platform/toolchain dependent: <https://arxiv.org/abs/1411.6361>
- arXiv:1810.05600, *Compact NUMA-Aware Locks* — local handoff can help under contention; validate fairness, migration, and single-thread impact: <https://arxiv.org/abs/1810.05600>
- arXiv:2002.07515, *Characterizing Synchronous Writes in Stable Memory Devices* — evaluate throughput and latency across batch sizes and sequential/random patterns: <https://arxiv.org/abs/2002.07515>
- arXiv:2212.06321, *Data Layout from a Type-Theoretic Perspective* — make representation/layout and access-pattern rationale explicit: <https://arxiv.org/abs/2212.06321>
