---
name: bun-1-4-migration
description: Migrate JavaScript and TypeScript repositories to Bun 1.4+, or initialize Biome 2.5.9 in a new Bun project, with evidence-gated tool replacements.
---

# Bun 1.4 Migration

Consolidate a repository on Bun 1.4+ without trading correctness for tool reduction.

## Use this skill

- Upgrade active Bun pins from 1.3 to 1.4+, consolidate package management on Bun, or update JavaScript/TypeScript CI, containers, scripts, and lockfiles.
- Evaluate replacing Node.js, Deno, Jest, Vitest, Vite, webpack, esbuild, ESLint, Prettier, script runners, or redundant runtime libraries.
- Initialize Biome 2.5.9 in a new Bun project that has no Biome configuration, or bump an existing Biome configuration without overwriting it.
- Do not use for other new-project setup, a generic dependency upgrade, or a replacement that lacks repository-specific compatibility evidence.
- Redirect general CI design to `/skill:git-ci-cd`, architecture changes to `/skill:software-architecture`, and obsolete compatibility cleanup after migration to `/skill:no-legacy-cleanup`.

## Rules

- Inspect active configuration and consumers before editing. Exclude history, fixtures, examples, generated output, and vendored files unless they control current behavior.
- Upgrade every active development, CI, container, and deployment pin that sets Bun below 1.4. Preserve exact or floating version policy already owned by the repository.
- Use one package manager after migration. Generate `bun.lock` with Bun; never hand-edit lockfile format or delete the prior lockfile before install and dependency checks pass.
- Treat package-manager commands and direct script-runner replacements as mandatory consolidation. Treat runtime, test-runner, bundler, database, networking, and framework replacements as conditional.
- Keep a tool when required behavior is not reproduced. Record the blocker instead of adding a shim or claiming an equivalent migration.
- Remove dependencies and configuration only after focused checks prove the Bun path. Preserve TypeScript typechecking and declaration generation when required.
- For a new project without `biome.json` or `biome.jsonc`, install `@biomejs/biome@2.5.9` and create `biome.json` from the package template without the `react` domain.
- If a Biome configuration exists, preserve it and change only the package version and any existing schema URL to 2.5.9. Do not replace, normalize, or complete the configuration from the template.
- Do not invent custom schema files or custom generated files as outputs. `biome.json` is allowed as an established Biome configuration format; otherwise use only established repository-owned formats and canonical inputs.

## Steps

1. Read repository instructions and inspect versions, lockfiles, `package.json`, workspaces, Bun configuration, CI, containers, deployment files, and active documentation.
2. Build a migration ledger from the [workflow](references/migration-workflow.md) and [replacement matrix](references/replacement-matrix.md). Mark each change required, conditional, retained, or blocked.
3. Upgrade Bun pins, run `bun install` to create or migrate `bun.lock`, verify the dependency graph, then convert installs, script execution, CI, and containers to Bun.
4. Apply the [Biome 2.5.9 baseline](references/biome-2-5.md) when initializing a new Bun project or updating an existing Biome setup.
5. Migrate conditional runtime, test, bundler, lint, format, or library slices one at a time. Run focused checks before removing each old tool or dependency.
6. Remove stale active lockfiles, commands, pins, dependencies, and configuration. Run the repository checks and the final-state audit, then inspect the diff for unsupported cleanup.

## Resources

- Start with the [reference router](references/index.md).
- Use the [migration workflow](references/migration-workflow.md) for ordering and evidence, the [replacement matrix](references/replacement-matrix.md) for keep-or-replace decisions, and the [Biome 2.5.9 baseline](references/biome-2-5.md) for configuration creation or version-only updates.

## Verify

- Done means Bun reports `>=1.4.0`, `bun.lock` is present, active package management and automation use Bun, Biome changes follow the create-or-version-only rule, retained tools have named compatibility reasons, and applicable install, typecheck, lint, test, and build checks pass.
- Run `python3 scripts/check.py` from this package. Run `python3 scripts/audit_bun14.py /path/to/repository` against the migrated repository, then run its native Bun checks. The audit checks common active paths; it does not replace the migration ledger or repository-specific search.
- Record changed pins, removed and retained tools, commands, exit statuses, and unresolved blockers. Mark unavailable Bun, network, install, runtime, or external compatibility evidence `UNVERIFIED`.
