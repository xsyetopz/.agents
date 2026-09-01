---
name: neovim-plugin-development
description: Build, migrate, test, profile, document, and release Neovim plugins using supported Lua/Vim APIs and runtime conventions. Use for Lua plugins, remote providers, runtime files, LSP, Tree-sitter queries, commands, mappings, health checks, help docs, package-manager compatibility, and Neovim version migrations; not for Vim-only plugins unless compatibility is requested.
---

# Neovim Plugin Development

Develop to the plugin's declared minimum Neovim version and test against current stable. Follow runtimepath conventions, keep startup files minimal, expose composable Lua APIs and `<Plug>` mappings, own resources by buffer/window/tab/client scope, and avoid depending on a specific plugin manager unless integration is requested.

## Start with evidence

1. Inspect plugin layout, `lua/`, `plugin/`, `autoload/`, `ftplugin/`, `after/`, `queries/`, `doc/`, health modules, tests, minimal init, CI, release tags, rockspecs, and package-manager metadata.
2. Identify minimum Neovim version, Lua/Vimscript support, setup contract, lazy-loading assumptions, external tools/providers, LSP/Tree-sitter use, and supported operating systems.
3. Preserve public module names, commands, mappings, autocmd events, highlight groups, options, and serialized state unless a migration is authorized.
4. Load only relevant references:
   - [Platform and architecture](references/platform-and-architecture.md) for runtime layout, Lua APIs, configuration, lifecycle, UI, LSP, Tree-sitter, and compatibility.
   - [Testing and quality](references/testing-and-quality.md) for headless tests, minimal environments, fixtures, async behavior, performance, and health checks.
   - [Packaging and release](references/packaging-and-release.md) for help tags, repository layout, versioning, package-manager neutrality, luarocks, and releases.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before selecting modules, tests, health checks, or CI patterns.

## Workflow

- Use documented `vim.*` and API functions available at the declared floor. Check `:help deprecated` and release news before adopting or removing APIs.
- Keep `plugin/*.lua` startup work limited to guards, commands, lightweight autocmds, and user-facing entrypoints. Defer heavy modules until invoked.
- A `setup()` function is optional, not mandatory. If present, make it predictable, validate configuration, merge defaults without mutating caller tables, and avoid requiring users to call it for basic runtime files unless necessary.
- Use augroups and clear only the plugin's own autocmds. Use buffer-local commands, keymaps, and options for buffer-owned behavior.
- Provide `<Plug>` mappings or callable functions; do not overwrite user mappings by default.
- Schedule API mutations from fast/textlocked callbacks when required. Bound asynchronous jobs, timers, handles, and RPC clients and close them on teardown.
- Use `vim.system`/supported process APIs according to the minimum version; pass argument arrays, handle cancellation/timeouts, and avoid shell interpolation.
- Keep LSP integrations compatible with current core defaults and configuration APIs; do not duplicate defaults or require `nvim-lspconfig` unless that is an explicit dependency.
- Treat Tree-sitter integration as version-sensitive and validate queries against pinned/current parsers.
- Add `lua/<plugin>/health.lua` for meaningful environment/configuration diagnostics.

### Templates

Use [the Lua runtimepath starter](assets/plugin-template/) as an adaptation source. It includes a lazy command entrypoint, configuration module, health check, help file, minimal test init, and headless smoke test without requiring a plugin manager.

## Validation

Run formatting/lint/type checks established by the repository, pure Lua tests, headless Neovim tests with a minimal isolated XDG environment, help-tag validation, `:checkhealth`, minimum/current stable matrix tests, and focused startup/performance checks.

Report minimum/current versions, public API changes, runtime files, commands/mappings/autocmds, tests, deprecated API findings, package-manager assumptions, and release actions not performed.

## Boundaries

- Do not install plugins into the user's real config or mutate public repositories/releases without authorization.
- Do not add compatibility for Vim or older Neovim releases outside the declared support scope.
- When the request expands into cross-editor architecture or shared protocol design, make that decision from current platform capabilities and repository evidence. Never stop to locate or install a companion skill.
