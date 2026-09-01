# VS Code desktop-and-web extension starter

This starter is intentionally pinned to Bun 1.4.0 and Biome 2.5.10 and follows the Bun/build/TypeScript shape used in `xsyetopz/versionlens-redux`.

1. Replace every `__PLACEHOLDER__`. Match `@types/node` to the Node runtime in the oldest supported VS Code host and `@types/vscode` to `engines.vscode`.
2. Run `bun install` with Bun 1.4.0 and commit the generated `bun.lock`. Do not create npm, pnpm, or Yarn lockfiles.
3. Keep the `browser` entrypoint only when web support is required and tested; otherwise remove `browser.ts`, the manifest field, and its build target.
4. Add contribution points before adding activation-time registration.
5. Replace the permissive Workspace Trust and virtual-workspace declarations if actual behavior executes workspace content, assumes local paths, or otherwise cannot support them safely.
6. Use `bun run check` for the non-mutating local/CI gate and `bun run format` only when source modification is intended.
7. Add official extension-host/browser tests, then run production builds, `bunx vsce ls --no-dependencies`, `bun run package`, and clean-profile VSIX smoke tests.
