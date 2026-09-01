---
name: vscode-extension-development
description: Build, migrate, test, secure, package, and publish Visual Studio Code extensions for desktop, remote, and web extension hosts. Use for VS Code Extension API, contribution points, language servers, debug adapters, webviews, Marketplace/VSIX release, and Open VSX compatibility; not for Visual Studio IDE extensions.
---

# VS Code Extension Development

Develop to the extension's declared `engines.vscode` floor and host matrix, not merely the newest local VS Code. Prefer declarative contribution points, lazy activation, capability-aware behavior, web-safe abstractions where required, and behavior tests in representative extension hosts.

## Start with evidence

1. Inspect `package.json`, lockfile, TypeScript/build config, `src/extension.*`, browser entrypoint, language-client/server packages, webviews, `.vscodeignore`, tests, CI, telemetry/privacy code, and publishing workflows.
2. Identify minimum VS Code version, desktop/web support, local/remote execution preference, Workspace Trust and virtual-workspace behavior, proposed API use, target registries, and update compatibility.
3. Preserve the repository's package manager, bundler, module format, and extension-host architecture unless migration is requested. For a new scaffold, use the maintained Bun 1.4.0 and Biome 2.5.10 baseline in this skill's template.
4. Load only relevant references:
   - [Platform and architecture](references/platform-and-architecture.md) for manifests, activation, hosts, remote/web support, APIs, language features, webviews, trust, and lifecycle.
   - [Testing and quality](references/testing-and-quality.md) for unit, extension-host, browser, integration, performance, and security testing.
   - [Packaging and release](references/packaging-and-release.md) for bundling, VSIX inspection, Marketplace/Open VSX publication, signing/provenance, and CI.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before scaffolding or adapting an open-source extension pattern.

## Workflow

- Keep `engines.vscode` aligned with the oldest API actually used. Do not raise it solely because the latest stable is available.
- Prefer `contributes` declarations over activation-time registration where a contribution point exists.
- Activate only when needed. Dispose commands, providers, watchers, terminals, clients, webview resources, and event subscriptions through `context.subscriptions` or explicit lifecycle owners.
- Keep extension-host callbacks responsive. Bound filesystem scans, debounce events, propagate cancellation, and avoid synchronous child processes or network work.
- Treat workspace content, settings, task/debug inputs, binaries, and dependency resolution as untrusted until Workspace Trust policy permits execution.
- Use `vscode.Uri`, `workspace.fs`, document selectors, and host capabilities instead of assuming local filesystem paths.
- Separate UI and workspace responsibilities when remote execution requires it; set `extensionKind` only from actual capability/location needs.
- For web extensions, provide a `browser` entrypoint, bundle for web workers, and avoid Node-only APIs unless isolated behind a desktop path.
- For webviews, use restrictive CSP, nonces, `asWebviewUri`, minimal `localResourceRoots`, validated message schemas, and no unsanitized HTML.
- Use stable APIs for Marketplace releases. Proposed APIs are Insiders-only development surfaces and must not silently become stable dependencies.
- For new scaffolds, pin `packageManager` to `bun@1.4.0`, commit `bun.lock`, use only Bun commands, and pin `@biomejs/biome` plus its configuration schema to `2.5.10`. Do not introduce npm, pnpm, Yarn, or a second lockfile.
- Use `Bun.build` for the template's desktop and browser bundles, externalize `vscode`, and keep the extension runtime TypeScript configuration separate from build tooling and tests. Adopt a different pipeline only when repository evidence or required compatibility justifies it.

### Templates

Use [the Bun desktop-and-web TypeScript starter](assets/extension-template/) as an adaptation source. It pins Bun 1.4.0 and Biome 2.5.10 and follows the strict TypeScript/build/test shape used by `xsyetopz/versionlens-redux`. Resolve all `__PLACEHOLDER__` values before running it; remove the browser entrypoint when web support is not required.

## Validation

Run Biome's non-mutating check, TypeScript typechecks, focused Bun tests, a clean `Bun.build` check, extension-host tests through the repository's current VS Code test tooling, web-host tests when a browser entrypoint exists, packaging with `vsce package`, and archive inspection. Test minimum and current supported VS Code versions plus relevant local/remote/web and trusted/untrusted modes. Use Biome's write mode only for an explicit fix or formatting operation.

Report host matrix, `engines.vscode`, changed contribution points and activation paths, checks, packaged contents, trust/web limitations, proposed API use, and any registry mutation not performed.

## Boundaries

- Publishing, publisher creation, PAT use, registry deletion/unpublish, and production rollout require explicit authorization.
- Do not widen to Cursor, VSCodium, code-server, or Open VSX unless compatibility is requested and verified.
- When the request expands into platform selection or shared multi-editor design, make that decision from current platform capabilities and repository evidence. Never stop to locate or install a companion skill.
