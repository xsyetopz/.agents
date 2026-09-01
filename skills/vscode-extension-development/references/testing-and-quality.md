# VS Code extension testing and quality

## Test layers

1. Pure unit tests for protocol, parsing, state, and command construction.
2. Extension-host integration tests for commands, providers, documents, workspace APIs, activation, settings, and lifecycle.
3. Language-server or debug-adapter tests independent of VS Code when protocol boundaries allow it.
4. Web extension tests in a browser host.
5. Remote/virtual workspace tests for URI and host-placement behavior.
6. Packaged VSIX clean-profile smoke tests.

Use the repository's current official tooling. VS Code documentation provides `@vscode/test-cli` for quick setup, lower-level test-electron tooling for custom runners, and `@vscode/test-web` for browser-host testing.

For the bundled starter, use `bun test` for pure TypeScript tests and import from `bun:test`. Keep VS Code host behavior out of pure units; when a unit must cross the host boundary, wrap or inject the API, or use Bun's `mock.module` with an intentionally designed adapter. Continue to use official VS Code harnesses for real activation, command, provider, desktop-host, and browser-host behavior.

The default local/CI sequence is:

1. `bun install --frozen-lockfile`
2. `bun run check:biome`
3. `bun run typecheck`
4. `bun test`
5. `bun run check:build`
6. extension-host and web-host suites required by the support matrix
7. `bun run package` and VSIX inspection

`check:biome` must be non-mutating. Reserve `bun run format` or Biome's `--write` mode for deliberate source modification. A successful Bun unit suite is not evidence that extension activation or the browser entrypoint works.

## Extension-host matrix

Choose cases from actual support claims:

- Minimum `engines.vscode` version.
- Current stable and optionally Insiders for forward detection.
- Desktop local workspace.
- Remote workspace when `extensionKind` or process placement matters.
- vscode.dev/web worker when `browser` exists.
- Trusted and untrusted workspaces.
- File, untitled, virtual, and remote URI schemes when providers claim them.

Do not claim web or remote compatibility from successful TypeScript compilation.

## Deterministic setup

- Use a temporary user-data directory and extensions directory.
- Disable unrelated extensions and avoid the developer's normal profile.
- Pin/download the tested VS Code version where the harness supports it.
- Use fixture workspaces that contain no credentials and no dependency on the developer machine.
- Bound all waits with observable events rather than sleeps.
- Capture extension-host logs, test output, and language-server/debug-adapter logs without secrets.

## Behavior cases

- Activation: no premature activation, idempotent registration, clean deactivation.
- Commands/providers: valid and invalid context, cancellation, concurrent calls, disposed documents.
- Workspace: multi-root, workspace-folder changes, configuration scope, remote/virtual URIs.
- Trust: restricted features stay unavailable; safe features remain usable; transition after trust grant works.
- Language features: incomplete syntax, large files, cancellation, incremental edits, diagnostics cleanup, server restart.
- Webviews: CSP, message validation, reload/state restore, theme/high contrast, disposal, malformed input.
- Storage: state migration, secret-storage failure, global versus workspace scope.
- Processes/network: quoting, timeouts, output limits, proxy, offline mode, trust gating, cleanup.

## Performance

- Measure activation time and avoid heavy top-level imports.
- Bundle to reduce file count and installation/activation overhead.
- Debounce file events, narrow glob/watch patterns, and avoid workspace-wide reads.
- Use incremental document state and cancellation for providers.
- Keep diagnostics, decorations, and webview messages bounded.
- Avoid retaining `TextDocument`, editor, terminal, or webview objects after disposal.

## Security review

- Validate workspace-controlled executable/configuration inputs.
- Prefer spawn argument arrays; avoid shell mode.
- Audit webview CSP, origin assumptions, links, command URIs, and message handling.
- Keep secrets in SecretStorage and redact logs/telemetry.
- Declare Workspace Trust and virtual-workspace capabilities truthfully.
- Review dependencies and bundled output, not only source `package.json`.

## Official sources

- <https://code.visualstudio.com/api/working-with-extensions/testing-extension>
- <https://code.visualstudio.com/api/working-with-extensions/continuous-integration>
- <https://code.visualstudio.com/api/extension-guides/web-extensions>
- <https://code.visualstudio.com/api/extension-guides/workspace-trust>
- <https://code.visualstudio.com/api/extension-guides/virtual-workspaces>
- <https://github.com/microsoft/vscode-test-cli>
- <https://github.com/microsoft/vscode-test-web>
- <https://bun.sh/docs/test>
