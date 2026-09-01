---
name: editor-extension-router
description: Select and coordinate the correct development workflow for JetBrains, VS Code, Zed, Neovim, Eclipse, or Sublime editor extensions. Use for platform choice, feasibility, multi-editor architecture, shared LSP/DAP/core design, migration, or requests that mention editor plugins without naming one; route single-platform implementation to the dedicated skill.
---

# Editor Extension Router

Choose platforms from required capabilities, runtime constraints, target users, distribution, security, and maintenance cost. Do not select an editor solely because its extension language matches the existing codebase.

## Routing workflow

1. Establish whether the user named a target editor. If yes, preserve that decision and route directly unless the requested capability is unsupported.
2. If no platform is fixed, identify required capabilities: language intelligence, syntax/grammar, debugger, commands, settings, editor UI, project/workspace model, remote/web support, native process access, themes/snippets, marketplace, and supported operating systems.
3. Inspect existing assets: LSP/DAP servers, Tree-sitter/TextMate grammars, shared protocol/core libraries, packaging, licenses, telemetry, native binaries, and release infrastructure.
4. Read [the platform matrix](references/platform-matrix.md) and recommend the narrowest viable platform set with explicit exclusions and uncertainty.
5. For multi-editor work, read [cross-editor architecture](references/cross-editor-architecture.md). Separate reusable protocol/domain cores from thin host adapters without forcing lowest-common-denominator UX.
6. For an existing extension port or migration, read [migration playbook](references/migration-playbook.md). Inventory user-visible and persistent contracts before mapping APIs.
7. Read [cross-editor repositories](references/templates-and-ecosystem.md) when selecting a shared LSP, DAP, grammar, protocol, or monorepo pattern. Treat repositories as evidence, not copy sources.
8. Route implementation:
   - `$jetbrains-plugin-development`
   - `$vscode-extension-development`
   - `$zed-extension-development`
   - `$neovim-plugin-development`
   - `$eclipse-plugin-development`
   - `$sublime-plugin-development`

## Decision contract

- Distinguish declarative packages from procedural extensions. A syntax/theme/snippet package may need no host runtime.
- Prefer LSP for reusable language intelligence and DAP for reusable debugging when their protocols cover the required behavior.
- Keep host-native UX, configuration, storage, security, and lifecycle in platform adapters.
- Do not claim one extension artifact runs across editors; each platform has different manifests, APIs, sandboxing, packaging, and registry policy.
- Treat remote/web execution, workspace trust, binary download/execution, and credential storage as first-class design constraints.
- Budget testing and release work per platform. Shared code reduces domain duplication but does not remove host integration matrices.
- Re-check current official documentation before version-sensitive recommendations.

## Output

Return:

- Recommended platform(s) and why.
- Required capabilities and any unsupported/degraded behavior.
- Shared-core/protocol boundary and per-editor adapters.
- Runtime/build/packaging implications.
- Security and permission differences.
- Test and release matrix.
- Migration/public-contract risks.
- The dedicated skill(s) to use next.

For a new multi-editor effort, copy and complete [the architecture plan template](assets/multi-editor-plan.md) before scaffolding adapters.

## Boundaries

- Do not scaffold all platforms when the user asked for one.
- Do not publish, reserve namespaces, create publisher accounts, or mutate registries without explicit authorization.
- Surface unresolved product, compatibility, and licensing choices before implementation.
