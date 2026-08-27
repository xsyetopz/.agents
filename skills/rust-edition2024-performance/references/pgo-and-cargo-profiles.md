# PGO and Cargo profile tuning

Tune Cargo profiles as a measured deployment decision. The root workspace manifest owns `[profile]`; the consuming workspace profile comes from that manifest rather than dependency manifests. Compare the resulting release artifact, startup, throughput, tail latency, memory, binary size, build time, and debug/incident requirements. [EXAMPLE: RUST-TECH-CARGO-PROFILE] [EXAMPLE: RUST-TECH-PGO-BOLT]

## PGO workflow

Use the same compiler, target, non-PGO `RUSTFLAGS`, feature set, and representative workload for both sides of the comparison. Use absolute profile paths and keep stale profile data out of the training directory. [EXAMPLE: RUST-TECH-PGO-BOLT]

<!-- [EXAMPLE: RUST-TECH-PGO-BOLT] -->
```bash
rm -rf /tmp/project-pgo
RUSTFLAGS="-Cprofile-generate=/tmp/project-pgo" \
  cargo build --release --target=x86_64-unknown-linux-gnu
# Run the instrumented target binary repeatedly with representative traffic.
llvm-profdata merge -o /tmp/project-pgo/merged.profdata /tmp/project-pgo
RUSTFLAGS="-Cprofile-use=/tmp/project-pgo/merged.profdata -Cllvm-args=-pgo-warn-missing-function" \
  cargo build --release --target=x86_64-unknown-linux-gnu
```

Replace the example target and binary invocation with the repository's supported target. The instrumentation build is not the candidate; benchmark the profile-use build against the ordinary release build. Keep profile artifacts out of source control unless the repository explicitly owns a reproducible target-specific pipeline. [EXAMPLE: RUST-TECH-PGO-BOLT]

## Profile choices

Evaluate `opt-level`, `lto`, `codegen-units`, `panic`, `strip`, `debug`, `incremental`, and target CPU/features one at a time or in a named candidate profile. LTO and fewer codegen units can improve generated code but lengthen builds; `panic = "abort"` changes failure behavior; `target-cpu=native` can make artifacts nonportable. [EXAMPLE: RUST-TECH-CARGO-PROFILE] [EXAMPLE: RUST-TECH-PORTABLE-FALLBACK]

## Optional post-link layout

BOLT is a separate, post-link binary optimization/layout tool, not a Cargo or rustc guarantee. Consider it only when the exact target, linker/debug information, LLVM/BOLT version, and deployment pipeline are supported and reproducible. Train it with representative traffic, compare the final BOLT artifact with the same non-BOLT release/PGO artifact on a holdout workload, and gate startup/throughput/tails, RSS, binary size, and correctness. Keep a portable non-BOLT artifact and document rollback; never add a generic BOLT command to a stable Rust workflow without verifying support. [EXAMPLE: RUST-TECH-PGO-BOLT]

## Source locations

- Rust PGO procedure: `https://doc.rust-lang.org/rustc/profile-guided-optimization.html`
- Cargo profile settings and precedence: `https://doc.rust-lang.org/cargo/reference/profiles.html`
- LLVM BOLT build/availability context: `https://llvm.org/docs/AdvancedBuilds.html#bolt`
