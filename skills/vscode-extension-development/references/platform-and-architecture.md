# VS Code platform and architecture

Verified against official VS Code documentation on 2026-09-01. VS Code 1.135, released 2026-08-26, was the latest stable release. Use the repository's `engines.vscode` as the compatibility contract and re-check current API documentation before introducing new APIs.

## Manifest and entrypoints

`package.json` controls identity, engine range, categories, activation, entrypoints, capabilities, contributions, dependencies, extension kind, preview flags, and Marketplace presentation.

- `main`: Node.js desktop/remote extension-host entrypoint.
- `browser`: browser/web-worker entrypoint for vscode.dev and web extension hosts.
- `contributes`: commands, configuration, languages, grammars, views, menus, keybindings, debuggers, tasks, notebooks, authentication, themes, snippets, walkthroughs, and other static contributions.
- `activationEvents`: explicit events are still relevant for compatibility and non-contribution activation. Since VS Code 1.74, contributed commands and language declarations do not require redundant matching activation events.
- `engines.vscode`: oldest supported API contract; use a real semver range and test the floor.

Keep command IDs, configuration IDs, view IDs, language IDs, and context keys stable once published. Treat changes as migrations affecting users, keybindings, settings sync, and dependent extensions.

## Bun and TypeScript baseline for new scaffolds

The bundled starter intentionally follows the local `xsyetopz/versionlens-redux` development shape:

- Pin Bun with `packageManager: "bun@1.4.0"` and `.bun-version`; use `bun install --frozen-lockfile` in validation and CI after committing `bun.lock`.
- Use `bunfig.toml` with the isolated linker. Do not add npm, pnpm, Yarn, or their lockfiles.
- Bundle with `Bun.build`, using `format: "cjs"`, `target: "node"` for the desktop entrypoint, `target: "browser"` for the web entrypoint, and `external: ["vscode"]` for both.
- Keep a strict shared `tsconfig.base.json`. The VersionLens-derived settings include ES2022, CommonJS, bundler resolution, forced module detection, `.ts` import support, `noEmit`, `strict`, exact optional properties, unchecked indexed-access protection, side-effect import checking, override/return checks, unused-code checks, and erasable TypeScript syntax.
- Give extension source an explicit `types` set containing `bun`, `node`, and `vscode`, plus `rootDir`, `outDir`, and a local build-info path. Typecheck tests separately so test files do not weaken or distort the extension-host project.

`erasableSyntaxOnly` requires a supporting TypeScript release. Keep it when using the template's pinned compiler; remove or revise it only as part of an intentional compiler compatibility change. TypeScript settings do not change the actual Node APIs available in the supported VS Code host, so avoid calling APIs merely because a newer `@types/node` exposes them.

For code that needs a highly mockable VS Code boundary, VersionLens uses a package import such as `#vscode-host` and a Bun build plugin that rewrites the virtual module to real `vscode` exports. Adopt that extra indirection only when tests or host isolation need it; direct `import * as vscode from "vscode"` remains clearer for a small extension.

## Extension hosts and placement

VS Code can run extensions in local Node, remote Node, and web worker hosts. Placement depends on available hosts, entrypoints, installation location, capability, and `extensionKind` preference.

- Workspace extensions run near workspace contents, including remote hosts.
- UI extensions prefer the local/UI side when they need local devices, credentials, or low-latency UI resources.
- Web extensions run in a browser worker and cannot assume Node built-ins, unrestricted processes, or local disk paths.
- Do not force `extensionKind` without a measured requirement; incorrect placement breaks remote and web scenarios.
- Use `vscode.env.remoteName`, URI schemes, and capabilities only where behavior genuinely differs.

## Activation and lifetime

- Keep module import side effects small; heavy initialization belongs after activation and behind feature demand.
- Register disposables in `context.subscriptions`.
- Cache only bounded data keyed by stable identities and invalidate on workspace/configuration/document changes.
- Stop language clients, child processes, servers, file watchers, timers, and telemetry on deactivation or owning-resource disposal.
- Use cancellation tokens and avoid orphan promises. Catch and surface expected failures without crashing the extension host.
- Avoid activating for every workspace when a narrower document selector, command, view, or URI event works.

## Workspace Trust and virtual workspaces

Declare `capabilities.untrustedWorkspaces` accurately:

- `true` only when all functionality is safe without executing or trusting workspace-controlled content.
- `false` when the extension cannot operate safely in Restricted Mode; provide a user-facing reason.
- `limited` when safe features remain available. Gate risky behavior on `workspace.isTrusted` and restrict security-sensitive settings.

Threat-model workspace settings, executable paths, project dependencies, config files, tasks, debug configurations, shell arguments, and generated commands. Avoid shell interpolation; use argument arrays and validate paths.

Declare `virtualWorkspaces` support according to actual use of `workspace.fs` and URI-aware APIs. Features that require local processes or native paths should degrade clearly rather than corrupt remote resources.

## API and feature architecture

- Prefer VS Code APIs and contribution points over DOM/private workbench access.
- Use `DocumentSelector` narrowly to avoid unintended providers.
- Language features can be direct providers or LSP. Choose LSP for cross-editor/server reuse and project-scale semantic analysis; choose direct providers for small VS Code-specific features.
- Debug adapters should follow DAP and separate adapter transport/process lifecycle from VS Code UI integration.
- Use tasks and terminals through their APIs instead of private terminal internals.
- Store secrets in `ExtensionContext.secrets`; use global/workspace state only for non-secret JSON-serializable state.
- Localize user-visible manifest and runtime strings where the product requires it.

## Webviews

- Use webviews only when native views, trees, quick picks, input boxes, or editors cannot satisfy the UX.
- Apply CSP with a nonce for scripts; disallow broad remote sources.
- Convert local resources with `asWebviewUri` and minimize `localResourceRoots`.
- Validate every message at both boundaries and model it as a versioned protocol.
- Sanitize untrusted text, avoid `innerHTML`, preserve state deliberately, and dispose listeners.
- Support themes, high contrast, keyboard navigation, screen readers, zoom, and reduced motion.

## Proposed APIs

Proposed APIs require Insiders/development configuration and cannot be published as ordinary stable Marketplace dependencies. Keep proposal names explicit, pin the development environment, provide a stable fallback when required, and remove stale proposal declarations as APIs stabilize or change.

## Official sources

- <https://code.visualstudio.com/api/references/extension-manifest>
- <https://code.visualstudio.com/api/references/vscode-api>
- <https://code.visualstudio.com/api/references/contribution-points>
- <https://code.visualstudio.com/api/references/activation-events>
- <https://code.visualstudio.com/api/advanced-topics/extension-host>
- <https://code.visualstudio.com/api/extension-guides/web-extensions>
- <https://code.visualstudio.com/api/extension-guides/workspace-trust>
- <https://code.visualstudio.com/api/extension-guides/virtual-workspaces>
- <https://code.visualstudio.com/api/extension-guides/webview>
- <https://code.visualstudio.com/api/advanced-topics/using-proposed-api>
- <https://code.visualstudio.com/updates>
- <https://bun.sh/docs/bundler>
- <https://bun.sh/docs/typescript>
