# Zed extension testing and quality

Zed extensions do not expose the same comprehensive extension-host test harness as some older editors. Use layered deterministic checks plus an actual Dev Extension installation.

## Static and Rust checks

- Parse and validate `extension.toml`, language `config.toml`, JSON assets, and configuration schemas.
- Run `cargo fmt --check`, `cargo clippy` with repository policy, and `cargo test` for pure Rust logic.
- Build the `wasm32-wasip2` target with the pinned toolchain/API.
- Keep binary asset-selection, version parsing, command construction, and settings transformations in pure testable functions.
- Verify no unsupported native dependencies enter the WASM dependency graph.

## Grammar and query fixtures

For every language/grammar change, include representative files covering:

- Top-level and nested constructs.
- Incomplete/error syntax.
- Comments, strings, escapes, heredocs/templates, and interpolation.
- Embedded/injected languages.
- Outline names and ranges.
- Brackets, indentation, text objects, runnables, and overrides when provided.
- Path suffix and first-line detection.
- Large or adversarial nesting where regex/query cost can grow.

Check query captures against the exact pinned grammar revision. A query that references missing nodes should fail validation rather than silently losing features.

## Language-server and debugger cases

- Supported OS/architecture mapping and unsupported-platform errors.
- User-installed binary discovery and shell environment.
- Latest/pinned release selection, prerelease policy, missing assets, and network failure.
- Download/extraction destination, executable marking, version upgrades, and stale installation recovery.
- Workspace settings, initialization options, command arguments, environment, and path quoting.
- Multiple worktrees and project roots.
- Cancellation/retry behavior and bounded installation-status updates.
- Debug schema validation, user-provided adapter paths, locator output, and malformed task definitions.

## Dev Extension smoke tests

1. Install Rust through `rustup` when procedural code exists and ensure `wasm32-wasip2` is available.
2. Install the repository with `zed: install dev extension`.
3. Confirm the extension is shown as a dev override when a published version exists.
4. Open representative files and exercise every declared capability.
5. Review `Zed.log` with `zed: open log`.
6. Relaunch from a terminal with `zed --foreground` when Rust output or startup diagnostics are needed.
7. Remove/reinstall the dev extension to catch state and artifact assumptions.

Use clean sample worktrees and avoid relying on globally installed servers unless that is one explicit test case.

## Performance and security

- Keep grammar/query scope precise and avoid pathological regular expressions.
- Cache release checks and downloaded tools responsibly; do not perform network work for unrelated files.
- Validate archive type and expected asset names. Prefer upstream release sources and immutable tags.
- Do not execute a workspace file merely because it matches a server/adapter name.
- Avoid logging source content, environment secrets, access tokens, or full private paths.
- Verify theme/icon assets and repository dependencies have compatible licenses.

## Official sources

- <https://zed.dev/docs/extensions/developing-extensions>
- <https://zed.dev/docs/extensions/languages>
- <https://zed.dev/docs/extensions/debugger-extensions>
- <https://docs.rs/zed_extension_api/latest/zed_extension_api/>
