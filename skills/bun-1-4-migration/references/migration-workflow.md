# Migration workflow

## Inventory

Inspect active ownership before editing:

- Bun version pins in tool managers, CI actions, images, deployment configuration, and documentation that controls setup.
- `package.json`, `bunfig.toml`, `bun.lock`, `bun.lockb`, competing lockfiles, workspace files, overrides, catalogs, patches, and linker settings.
- Package-manager and runtime commands in scripts, CI, containers, hooks, task runners, and deployment files.
- Test, build, typecheck, lint, format, framework, loader, plugin, and native-addon requirements.
- Existing `biome.json` or `biome.jsonc`, the installed Biome version, and current ESLint or Prettier behavior.

Ignore keyword matches in history, examples, fixtures, generated output, and vendored code unless they affect current execution.

## Migration ledger

For each active surface, record:

1. Current owner and consumers.
2. Bun replacement and whether it is required or conditional.
3. Focused compatibility check.
4. Removal or retention decision.
5. Evidence and unresolved blocker.

## Order

1. Update active Bun pins to the repository's chosen 1.4+ policy.
2. Run `bun install`; inspect the resulting dependency and workspace state.
3. Convert frozen installs to `bun ci`, script execution to `bun run`, and one-shot CLIs to `bunx`.
4. Update CI, containers, deployment, hooks, and active setup documentation.
5. Apply the Biome create-or-version-only rule when Biome setup is in scope.
6. Migrate conditional runtime, test, bundler, lint, format, or library slices separately.
7. Remove old lockfiles and dependencies only after the replacement passes.
8. Run the audit and all applicable repository checks.

Do not hand-edit `bun.lock`. Fix undeclared dependencies instead of preserving accidental hoisting. Keep an explicit linker setting only when repository behavior requires it.

## Evidence gate

At minimum, capture `bun --version`, install status, changed dependency state, and every applicable typecheck, lint, test, build, and production smoke check. A successful install alone does not prove runtime, test-runner, or bundler compatibility.

If Bun, network access, credentials, services, or a required platform is unavailable, stop the affected migration slice and mark its evidence `UNVERIFIED`.
