# Zed Rust/WASM LSP starter

1. Replace placeholders and resolve the latest compatible `zed_extension_api`.
2. Prefer a user-installed server through `Worktree::which` unless managed download is required.
3. If downloading, add immutable release selection, platform/architecture mapping, extraction, caching, and failure tests.
4. Compile for `wasm32-wasip2`, install as a Dev Extension, and inspect `Zed.log`.
