# Zed templates and ecosystem examples

Verified 2026-09-01. The public registry is the most useful current corpus because every accepted extension reflects category, license, manifest, and submodule review. Inspect the latest commit and registry policy before adapting a pattern.

## Primary sources

- `zed-industries/zed`: extension documentation, built-in language definitions, schemas, Rust host implementation, and packaging tests.
- `zed-industries/extensions`: registry metadata, submodules, validation scripts, and accepted extension inventory.
- `zed-industries/zed_extension_api`: Rust/WASM API source and examples.

## Representative extensions

- `zed-extensions/lua`, `zed-extensions/zig`, `zed-extensions/svelte`, `zed-extensions/vue`: maintained language + grammar + LSP patterns.
- `zed-extensions/harper`: one LSP applied to many exact Zed language names.
- `zed-extensions/beancount`: PATH-first server discovery plus user binary path/arguments/environment settings.
- `zed-extensions/odin`: language, Tree-sitter, LSP, and debugger declaration in one language-focused package.
- `zed-extensions/leptos`: injection/query-focused extension layered onto an existing language.
- `zed-extensions/golangci-lint`: tool-as-language-server integration and configuration tradeoffs.

## What to extract

- Exact manifest/category patterns from recently accepted extensions.
- Current `CommandSettings` handling for path, arguments, and environment.
- Platform/architecture mapping and immutable release asset selection.
- Query organization and language-name alignment.
- Registry tests such as manifest/license/package validation.

## Avoid copying

- Old `zed_extension_api` versions or deprecated agent/slash/MCP patterns.
- Another extension's grammar revision, server asset names, license, IDs, language lists, or download logic without verifying upstream.
- Ad hoc settings fields when current structured binary settings cover the need.

## Repositories

- <https://github.com/zed-industries/zed>
- <https://github.com/zed-industries/extensions>
- <https://github.com/zed-industries/zed_extension_api>
- <https://github.com/zed-extensions/lua>
- <https://github.com/zed-extensions/zig>
- <https://github.com/zed-extensions/svelte>
- <https://github.com/zed-extensions/vue>
- <https://github.com/zed-extensions/harper>
- <https://github.com/zed-extensions/beancount>
- <https://github.com/zed-extensions/odin>
- <https://github.com/zed-extensions/leptos>
- <https://github.com/zed-extensions/golangci-lint>
