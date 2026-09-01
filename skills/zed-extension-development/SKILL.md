---
name: zed-extension-development
description: Build, migrate, test, and publish Zed extensions for languages, grammars, language servers, debug adapters, themes, icon themes, snippets, and supported registry capabilities. Use for extension.toml, Rust WebAssembly extension code, Tree-sitter queries, Zed extension API, and zed-industries/extensions submissions.
---

# Zed Extension Development

Match the extension to Zed's current capability and registry rules. Most declarative language/theme/snippet extensions need no Rust; use Rust WebAssembly only for supported procedural capabilities such as language-server or debugger management.

## Start with evidence

1. Inspect `extension.toml`, `Cargo.toml`, `src/lib.rs`, `languages/`, grammars, queries, themes, icon themes, snippets, schemas, license, CI, and registry submodule metadata.
2. Identify extension category, target languages, external binaries, supported platforms, `schema_version`, `zed_extension_api` version, accepted license, and registry publication state.
3. Do not add Rust, bundle external servers/adapters, or combine categories contrary to current registry prerequisites unless the user chooses a private/local-only extension.
4. Load the relevant references:
   - [Platform and architecture](references/platform-and-architecture.md) for manifest layout, WASM constraints, languages, LSP, DAP, themes, snippets, and lifecycle.
   - [Testing and quality](references/testing-and-quality.md) for Rust/unit checks, grammar/query fixtures, dev installation, logs, platform matrix, and security.
   - [Packaging and release](references/packaging-and-release.md) for licenses, registry prerequisites, submodule publication, updates, and maintenance.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before selecting a declarative or Rust/WASM scaffold.

## Workflow

- Use `wasm32-wasip2` for procedural extensions and the latest compatible `zed_extension_api`; do not assume ordinary native Rust behavior inside WASM.
- Keep `extension.toml`, Cargo package version, registry version, and source commit synchronized.
- Prefer declarative assets when no procedural API is required.
- Do not use `std::env::var` or compile-time `cfg` as a substitute for Zed runtime platform/worktree APIs.
- Locate user-installed tools through `Worktree::which` and shell environment. Download managed binaries through supported APIs into extension-owned storage with platform/architecture selection and integrity-conscious release selection.
- Never execute workspace-controlled binaries or arguments without a clear user action and validation.
- Keep language names, grammar IDs, server IDs, adapter IDs, and manifest references exactly aligned.
- Scope Tree-sitter queries and snippets narrowly; avoid expensive broad captures and global snippets without justification.
- Treat currently deprecated agent-server and slash-command extension paths as unavailable for new registry submissions. Treat MCP server extension support as transitional and check the current MCP registry direction before implementation.

### Templates

- Use [the declarative language starter](assets/language-extension-template/) for grammar/query-only support.
- Use [the Rust LSP starter](assets/lsp-extension-template/) only when executable resolution or procedural configuration is required.

Replace placeholders and verify the latest extension API/schema before building.

## Validation

Run Rust formatting/lint/tests and WASM build when Rust exists; validate TOML/JSON/query assets; install as a Dev Extension; inspect `Zed.log` and foreground output; test all declared platforms and language files; verify registry prerequisites and version synchronization.

Report capability category, manifest/API/schema versions, supported platforms, external downloads/processes, checks, dev-install evidence, registry changes, and any publication step not performed.

## Boundaries

- Registry PRs, submodule updates, external releases, and hosted publication require explicit authorization.
- Do not promise unsupported general UI, arbitrary editor commands, or native filesystem/process access beyond the current extension API.
- When the request expands into cross-editor architecture or shared protocol design, make that decision from current platform capabilities and repository evidence. Never stop to locate or install a companion skill.
