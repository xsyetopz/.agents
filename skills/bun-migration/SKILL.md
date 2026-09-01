---
name: bun-migration
description: Migrate a JavaScript or TypeScript repository from Bun 1.3.14 to Bun 1.4+ or initialize Biome 2.5.10 in a new Bun project. Use for an explicit Bun migration; not for ordinary dependency maintenance.
---

# Bun 1.3.14 to 1.4+ Migration

Move an active JavaScript or TypeScript repository from Bun 1.3.14 to Bun 1.4+ while preserving behavior, version policy, and dependency ownership.

Set the migration boundary, active pins, compatibility constraints, and completion checks. Safe local inspection, edits, installs, and validation may proceed in scope. Hosted, destructive, costly, or scope-expanding actions require authorization. Return changed pins, retained and removed tools, commands, checks, blockers, and unresolved runtime or network evidence.

## Start with evidence

1. Inspect repository instructions, Bun pins, manifests, workspaces, lockfiles, Bun and Biome configuration, CI, containers, deployments, scripts, and active documentation.

## Workflow

1. Build a migration ledger with the direct references below; classify each tool change as required, conditional, retained, or blocked.
   - [Biome 2.5.10 baseline](references/biome-2-5.md) · [Migration workflow](references/migration-workflow.md) · [Bun 1.4 replacement matrix](references/replacement-matrix.md)
   - [GOOD/RED migration examples](references/examples.md) (read before changing pins, lockfiles, or replacement ownership; RED marks a contrast, while GOOD is the migration pattern)
2. Upgrade every active Bun pin while preserving the repository's exact-or-floating version policy, then run `bun install` to create or migrate `bun.lock` and verify the dependency graph.
3. Consolidate installs, package scripts, CI, and containers on Bun; migrate conditional runtime, test, bundler, lint, format, database, networking, or framework slices one at a time.
4. Apply the Biome 2.5.10 baseline only for a new project without configuration; for an existing configuration, preserve content and update only the package version and existing schema URL.

## Validation

1. Run `python3 scripts/audit_bun14.py /path/to/repository` plus applicable install, typecheck, lint, test, and build checks before removing old tools or lockfiles.
2. Return changed pins, removed and retained tools, commands, statuses, blockers, and unavailable network, install, runtime, or compatibility evidence as `UNVERIFIED`.

## Boundaries

- Package-manager and direct script-runner consolidation is required; runtime, test, bundler, and library replacement depends on compatibility evidence.
- Retain a tool when the replacement does not reproduce required behavior, and record the blocker rather than adding a shim.
- Generate `bun.lock` with Bun and preserve the prior lockfile until install and dependency checks pass.
- `biome.json` is an established Biome format; keep other outputs within repository-owned formats and canonical inputs.
- General pipeline design, architecture changes, and post-migration obsolete-surface cleanup are separate concerns. Handle them directly when included in scope; never stop to locate or install a companion skill.
