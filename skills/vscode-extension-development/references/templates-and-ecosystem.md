# VS Code templates and ecosystem examples

Verified 2026-09-01. Prefer official samples for API shape and active production extensions for scale/lifecycle evidence. Review licenses before adapting code.

## Official starters

- `microsoft/vscode-extension-samples`: focused samples for contribution points, tests, web extensions, LSP, DAP, webviews, authentication, notebooks, virtual documents, and remote/web behavior.
- `microsoft/vscode-generator-code`: current `yo code` scaffolds and manifest/build conventions.
- `microsoft/vscode-languageserver-node`: LSP client/server libraries and examples.
- `microsoft/vscode-test-cli`, `microsoft/vscode-test-web`, and `microsoft/vscode-test`: official test harnesses.
- `microsoft/vscode-vsce`: packaging/publishing implementation and file inclusion rules.

Do not use the deprecated VS Code Webview UI Toolkit samples as a new UI foundation.

## Production extensions

- `microsoft/vscode-eslint`: LSP client/server split, workspace trust, multi-root configuration, server lifecycle, and large-workspace concerns.
- `microsoft/vscode-python`: large extension decomposition, experiments, telemetry, environment discovery, remote/web boundaries, and integration tests.
- `microsoft/vscode-jupyter`: notebooks, webviews, kernels, remote resources, data science UI, and broad test matrices.
- `gitkraken/vscode-gitlens`: desktop/web environment abstraction, large command/view surface, webviews, Git process ownership, and explicit repository AGENTS.md guidance.
- `prettier/prettier-vscode`: formatter provider, workspace dependency resolution, trust, configuration, and virtual workspaces.
- `vadimcn/codelldb`: native debugger packaging and DAP/platform asset complexity.
- `xsyetopz/versionlens-redux`: Bun-only command surface, isolated installs, Biome configuration, strict layered TypeScript configs, `Bun.build` with a disposable check mode, Bun unit tests, and VSCE packaging. Its Rust/N-API core and virtual `#vscode-host` adapter solve project-specific boundaries; copy them only when the target has the same needs.

## What to extract

- One official sample per API surface, not a combined sample dump.
- Manifest contribution and activation boundaries.
- Host abstraction patterns from extensions that genuinely support desktop and web.
- Protocol/process supervision from maintained LSP/DAP clients.
- Test profile isolation and packaged VSIX checks.

## Avoid copying

- Publisher IDs, telemetry keys, experiments, branding, generated schemas, bundled licenses, or registry automation.
- Private/proposed VS Code APIs used under special agreements.
- Legacy webpack/gulp scaffolds when the target uses the Bun 1.4.0 baseline.
- Deprecated webview toolkit components.

## Repositories

- <https://github.com/microsoft/vscode-extension-samples>
- <https://github.com/microsoft/vscode-generator-code>
- <https://github.com/microsoft/vscode-languageserver-node>
- <https://github.com/microsoft/vscode-test-cli>
- <https://github.com/microsoft/vscode-test-web>
- <https://github.com/microsoft/vscode-test>
- <https://github.com/microsoft/vscode-vsce>
- <https://github.com/microsoft/vscode-eslint>
- <https://github.com/microsoft/vscode-python>
- <https://github.com/microsoft/vscode-jupyter>
- <https://github.com/gitkraken/vscode-gitlens>
- <https://github.com/prettier/prettier-vscode>
- <https://github.com/vadimcn/codelldb>
- <https://github.com/xsyetopz/versionlens-redux>
