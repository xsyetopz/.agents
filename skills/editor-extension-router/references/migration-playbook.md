# Editor extension migration playbook

## Inventory before mapping

Capture the source extension's public contract:

- Extension/package ID, publisher/vendor, version, license, registry ownership.
- Commands, menus, keybindings, views, settings, contexts, filetypes/languages, snippets, themes.
- Persisted global/workspace/project state and secrets.
- Activation triggers and background processes.
- Language/debugger protocol and binaries.
- Workspace/project semantics, trust, remote/web behavior.
- Telemetry/privacy/support URLs.
- Supported editor versions, operating systems, and architectures.

Classify each feature as portable, adaptable, degraded, unsupported, or intentionally omitted.

## Map concepts, not APIs

Examples:

- VS Code command contribution maps to JetBrains action or Eclipse command/handler, not to a direct method translation.
- JetBrains PSI inspection maps poorly to a syntax-only Sublime/Zed package; consider LSP diagnostics/code actions.
- Neovim autocmd maps to host lifecycle/document events with different ordering and ownership.
- Eclipse workspace resource delta is not equivalent to raw filesystem watching.
- Sublime Text selector scopes and TextMate scopes can seed VS Code grammars, but settings and completion APIs remain separate.
- Zed WASM extensions cannot receive arbitrary native capabilities available to local Python/Lua/JVM/Node extensions.

## Preserve user contracts deliberately

- Reuse IDs only within the same registry/ownership contract.
- Map setting names/defaults and document differences.
- Provide import/migration for user state only when authorized and technically safe.
- Keep old commands/settings as temporary aliases only within an explicit deprecation window.
- Do not copy credentials between editors automatically.
- Preserve file formats/protocols when they are editor-independent.

## Feasibility gates

Stop or redesign when the target lacks:

- Required UI/contribution surface.
- Required process/filesystem/network capability.
- Workspace trust or permission model necessary for safe execution.
- Registry acceptance for the extension category/license/binary model.
- Stable API at the target version floor.
- Test infrastructure for the promised compatibility.

## Incremental migration

1. Extract and test portable core/protocol behavior without changing the source extension.
2. Create the target manifest and minimal activation/lifecycle adapter.
3. Implement one vertical user workflow end to end.
4. Add configuration/state mapping and failure UX.
5. Add target-native features rather than cloning source-editor UI mechanically.
6. Run target minimum/current and packaging tests.
7. Publish only after identity, support, telemetry, migration, and rollback decisions are approved.

## Shared-server migration

When moving analysis/debug behavior to LSP/DAP/CLI:

- Freeze existing behavior with fixtures.
- Define protocol and capability version.
- Keep source extension on the new core/server before building additional clients when feasible.
- Compare diagnostics, edits, navigation, cancellation, and performance.
- Preserve local fallback or coordinate server/client releases.
- Treat server downloads and executable trust separately for each editor.

## Completion criteria

- The target extension provides documented equivalent or intentionally degraded behavior.
- Unsupported features are explicit.
- Public settings/commands/state have a migration decision.
- Security and permissions are adapted to the target.
- Minimum/current target versions pass behavior and packaging tests.
- Registry identity, license, support ownership, and release authorization are settled.
