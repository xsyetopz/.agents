---
name: bun-migration
description: Use this skill when migrating a JavaScript or TypeScript repository to Bun 1.4+ or initializing Biome 2.5.9 in a new Bun project; use ordinary dependency maintenance when no Bun migration is intended.
---

# Bun Migration

Move an active JavaScript or TypeScript repository to Bun 1.4+ with evidence-gated replacements and preserved behavior.

## Workflow

1. Inspect repository instructions, Bun pins, manifests, workspaces, lockfiles, Bun and Biome configuration, CI, containers, deployments, scripts, and active documentation.
2. Build a migration ledger with the direct references below; classify each tool change as required, conditional, retained, or blocked.
   - [Biome 2.5.9 baseline](references/biome-2-5.md) · [Migration workflow](references/migration-workflow.md) · [Bun 1.4 replacement matrix](references/replacement-matrix.md)
3. Upgrade every active Bun pin while preserving the repository's exact-or-floating version policy, then run `bun install` to create or migrate `bun.lock` and verify the dependency graph.
4. Consolidate installs, package scripts, CI, and containers on Bun; migrate conditional runtime, test, bundler, lint, format, database, networking, or framework slices one at a time.
5. Apply the Biome 2.5.9 baseline only for a new project without configuration; for an existing configuration, preserve content and update only the package version and existing schema URL.
6. Run `python3 scripts/audit_bun14.py /path/to/repository` plus applicable install, typecheck, lint, test, and build checks before removing old tools or lockfiles.
7. Return changed pins, removed and retained tools, commands, statuses, blockers, and unavailable network, install, runtime, or compatibility evidence as `UNVERIFIED`.

## Gotchas

- Package-manager and direct script-runner consolidation is required; runtime, test, bundler, and library replacement remains compatibility-dependent.
- Keep a tool when required behavior is not reproduced, and record the blocker instead of adding a shim.
- Generate `bun.lock` with Bun and preserve the prior lockfile until install and dependency checks pass.
- `biome.json` is an established Biome format; other outputs stay within repository-owned formats and canonical inputs.
- Route general pipeline design to `$git-ci-cd`, architecture changes to `$architecture-boundaries`, and post-migration obsolete-surface removal to `$legacy-cleanup`.
