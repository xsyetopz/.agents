# Cross-editor repositories and reusable cores

Verified 2026-09-01. Use these repositories to study boundaries and integration tests. Do not assume their licenses, protocols, release models, or architecture fit the target project.

## Shared protocol/tooling sources

- `microsoft/vscode-languageserver-node`: canonical TypeScript LSP client/server libraries and sample split.
- `eclipse-lsp4e/lsp4e`: Eclipse LSP/DAP adapter and integration examples.
- `neovim/nvim-lspconfig`: Neovim server configuration corpus and current core-LSP transition.
- `zed-industries/zed` plus `zed-industries/extensions`: Zed host and registry LSP/DAP integration.
- `rust-lang/rust-analyzer`: substantial LSP server used by many editors, with protocol extensions and editor clients.
- `clangd/clangd`: C/C++ language server with broad client interoperability.
- `microsoft/pyright`, `redhat-developer/yaml-language-server`, `taplo/taplo`: language servers with multiple editor integrations.
- `microsoft/debug-adapter-protocol` and `microsoft/vscode-debugadapter-node`: DAP specification, libraries, and examples.

## Multi-editor products

- `sourcegraph/cody`: multi-editor clients sharing service/domain behavior; inspect current repository topology and product licensing.
- `TabbyML/tabby`: server plus several editor clients and protocol integration.
- `continue-revolution/continue`: multi-editor adapters, shared core, web UI, configuration, and model/provider boundaries.
- `editorconfig/editorconfig-core-*` plus editor plugins: example of a small portable specification/core with thin host integration.

## Evaluation questions

- Is the shared boundary a stable standard protocol or project-private RPC?
- Can clients and server update independently through capability/version negotiation?
- Which host concepts leak into the core?
- How are binaries located, downloaded, verified, upgraded, and stopped?
- How are workspace trust, remote/web execution, secrets, telemetry, and user consent adapted?
- Which tests are protocol-wide and which remain editor-specific?
- Does the license permit the intended reuse, linking, distribution, and commercial model?

## Repositories

- https://github.com/microsoft/vscode-languageserver-node
- https://github.com/eclipse-lsp4e/lsp4e
- https://github.com/neovim/nvim-lspconfig
- https://github.com/zed-industries/zed
- https://github.com/zed-industries/extensions
- https://github.com/rust-lang/rust-analyzer
- https://github.com/clangd/clangd
- https://github.com/microsoft/pyright
- https://github.com/redhat-developer/yaml-language-server
- https://github.com/tamasfe/taplo
- https://github.com/microsoft/debug-adapter-protocol
- https://github.com/microsoft/vscode-debugadapter-node
- https://github.com/sourcegraph/cody
- https://github.com/TabbyML/tabby
- https://github.com/continuedev/continue
- https://github.com/editorconfig
