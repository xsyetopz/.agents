# Rust 1.98 and Edition 2024 contract

Keep the minimum compiler version, edition, target triples, and stable/nightly policy separate and explicit. `edition = "2024"` selects language semantics; it does not set an MSRV. Check the workspace root and package manifests, CI toolchain files, `rust-toolchain.toml`, Cargo config, and deployment target before changing any of them.

Use a stable compiler by default. A target feature, `-C target-cpu`, `RUSTFLAGS`, allocator choice, or unstable intrinsic belongs to a target-specific performance decision with a portability owner and a fallback path where the project supports multiple target classes.

## Source locations

- Rust editions/compiler flag: `https://doc.rust-lang.org/rustc/command-line-arguments.html#--edition-specify-the-edition-to-use`
- Rust 2024 Edition Guide: `https://doc.rust-lang.org/edition-guide/rust-2024/`
- Rust release notes: `https://doc.rust-lang.org/releases.html`
