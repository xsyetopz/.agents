# Zed extension platform and architecture

Verified against Zed documentation and the published Rust API on 2026-09-01. `zed_extension_api` 0.7.0 was the latest crate documentation found. Re-check the crate and Zed docs before raising the API or using newly added capabilities.

## Manifest and structure

Every extension has `extension.toml` at its root with stable identity and metadata such as `id`, `name`, `description`, `version`, `schema_version`, authors, and repository.

Optional content includes:

- `languages/<language>/config.toml` and Tree-sitter query files.
- Grammar declarations in `extension.toml`.
- Language-server declarations and Rust implementation.
- Debug-adapter and locator declarations, required configuration schemas, and Rust implementation.
- `themes/*.json`, `icon_themes/*.json`, and `icons/` assets.
- `snippets/*.json`.
- `Cargo.toml` and `src/lib.rs` only when procedural functionality is required.

Keep IDs consistent across manifest tables, language metadata, queries, snippets, server/adapter callbacks, and registry entries.

## Rust and WebAssembly

- Procedural code is a `cdylib` using `zed_extension_api` and is compiled to `wasm32-wasip2`.
- Register one extension implementation through `zed::register_extension!`.
- WASM is sandboxed and differs from native execution. Do not assume arbitrary filesystem, sockets, environment, threads, dynamic libraries, or process behavior.
- Use `zed::current_platform()` for operating system and architecture.
- Use `Worktree` APIs to read workspace text, discover binaries, and obtain shell environment.
- Use supported download, GitHub-release, npm, and process APIs rather than native substitutes.
- Keep mutable extension state small and safe across repeated callbacks. Return actionable errors without leaking paths, tokens, or source contents.

## Language extensions

- Every supported language has a directory and `config.toml` containing the exact language name, grammar, suffixes, comments, and optional language behavior.
- Declare a grammar for every language submitted to the registry. Pin grammar repository and revision according to the manifest contract.
- Keep highlight, injection, outline, bracket, text-object, indentation, runnable/task, and override queries compatible with the grammar node types.
- Prefer small query fixtures that cover nested syntax, errors, injections, comments/strings, and large-file behavior.
- Do not claim a dialect unrelated to the primary language merely to broaden discovery.

## Language servers

- Declare server ID/name and exact language names in `extension.toml`.
- Implement the current `Extension` trait methods required to resolve server commands, arguments, environment, initialization options, and workspace configuration.
- Prefer a user-installed binary when policy supports it; otherwise download an upstream release through supported APIs.
- Do not bundle language-server executables in registry extensions.
- Select assets by current platform/architecture, use exact release assets, avoid mutable download URLs, and surface installation status.
- Bound retries and downloads. Preserve offline behavior and do not repeatedly fetch on every callback.
- Treat workspace settings and project toolchains as untrusted inputs to command construction.

## Debugger extensions

- Declare each debug adapter and mandatory configuration schema.
- Implement binary resolution and scenario conversion against the current Rust API.
- Debug locators may translate Zed tasks into debug scenarios and can be shared across adapters.
- Do not bundle debug adapters; find or download them through supported APIs.
- Validate executable, cwd, arguments, environment, and user-provided adapter paths.

## Themes, icon themes, and snippets

- Theme and icon-theme extensions should remain category-pure for registry submission.
- Validate files against the current schema URLs declared by Zed documentation.
- Use semantic/theme variables consistently and verify light, dark, high-contrast, inactive, diagnostic, git, terminal, and syntax states where supported.
- Keep SVG/icon assets minimal, licensed, and free of unsafe external references.
- Scope language snippets to language names; use global scope only for genuinely universal snippets.

## Deprecated/transitional capabilities

- New agent-server and slash-command extension submissions are deprecated; use the current ACP registry path for agent servers.
- MCP server extensions are expected to give way to the MCP registry. Check current policy before creating or publishing one.
- Do not infer unsupported arbitrary UI contribution or command APIs from other editors.

## Official sources

- <https://zed.dev/docs/extensions>
- <https://zed.dev/docs/extensions/developing-extensions>
- <https://zed.dev/docs/extensions/languages>
- <https://zed.dev/docs/extensions/debugger-extensions>
- <https://zed.dev/docs/extensions/themes>
- <https://zed.dev/docs/extensions/icon-themes>
- <https://zed.dev/docs/extensions/snippets>
- <https://docs.rs/zed_extension_api/latest/zed_extension_api/>
- <https://docs.rs/zed_extension_api/latest/zed_extension_api/trait.Extension.html>
