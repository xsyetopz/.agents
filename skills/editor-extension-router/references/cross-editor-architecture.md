# Cross-editor extension architecture

## Separate portable and host-owned concerns

Good shared candidates:

- Language Server Protocol server.
- Debug Adapter Protocol server.
- CLI or daemon with a versioned JSON/RPC protocol.
- Parsers, analyzers, formatters, linters, domain models, and transformation libraries.
- Shared test corpora and protocol conformance fixtures.
- Grammar source generators when each host emits/validates its own artifact.

Keep platform-specific:

- Manifest/contribution registration.
- Activation and disposal lifecycle.
- Workspace/project/root discovery and trust.
- Commands, menus, keybindings, views, settings, notifications, and accessibility.
- URI/filesystem abstractions and remote placement.
- Secret storage, telemetry consent, logs, and update policy.
- Package/registry metadata and signing.

## Adapter boundary

Define a small host adapter around capabilities rather than editor names leaking through the core:

- Workspace folders and document snapshots.
- Cancellation and progress.
- Configuration retrieval and change events.
- Logging/telemetry sink.
- UI prompts and notifications.
- Process/binary resolver.
- Secret/token provider.
- Persistent non-secret state.

The shared core should not accept raw JetBrains `Project`, VS Code `TextDocument`, Neovim buffer IDs, Eclipse `IResource`, Sublime `View`, or Zed `Worktree` objects. Convert at the adapter boundary into versioned domain values.

## Protocol design

- Version every out-of-process protocol.
- Negotiate capabilities and preserve backward compatibility across independently updated clients/servers.
- Use structured messages, bounded payloads, cancellation IDs, timeouts, and explicit error classes.
- Avoid sending complete workspaces or documents when incremental changes suffice.
- Redact secrets and user content from diagnostics by default.
- Define ownership of process startup, restart, crash backoff, updates, and shutdown for each host.

## LSP architecture

- Keep server behavior standard where possible and isolate editor-specific custom requests.
- Each client adapter maps settings, initialization options, workspace folders, commands, progress, and middleware.
- Test protocol behavior independently, then test each host's lifecycle and UI mapping.
- Do not assume all clients expose the same proposed LSP methods or dynamic-registration behavior.
- Use semantic tokens, inlay hints, code actions, workspace edits, and file operations only for clients in the support matrix.

## DAP architecture

- Keep adapter launch/transport independent of host UI.
- Define platform-specific discovery and executable resolution in clients where necessary.
- Test attach/launch, cancellation, terminal requests, path mapping, source requests, reverse requests, and adapter crashes.
- Preserve configuration names and schemas per host even when they map to one domain model.

## Grammar strategy

- Do not present TextMate and Tree-sitter artifacts as interchangeable.
- Keep shared language fixtures and a canonical language specification.
- Generate artifacts only when the generator is deterministic and host output remains reviewable.
- Test scopes/captures in each host because theme/query conventions differ.
- JetBrains PSI and Eclipse model frameworks require separate semantic implementations unless delegated to LSP.

## Binary distribution

Choose one explicit model:

1. Require a user-installed executable.
2. Download immutable upstream release assets.
3. Bundle per-platform binaries when registry rules allow it.
4. Run a separately installed service.

For every model define supported OS/architecture, version pin/update, checksums/signatures, proxy/offline behavior, executable permissions, quarantine/notarization, cache location, cleanup, and consent/trust.

Registry policies differ: Zed currently disallows bundling language servers/debug adapters; VS Code web cannot execute native binaries; packed Sublime resources can require `.no-sublime-package`; JVM platforms have their own native-library/classloader constraints.

## Repository topology

Use a monorepo when shared code and synchronized releases materially benefit from one CI graph. Use separate repos when registries require it, release cadence/ownership differs, or language/tooling boundaries make coupling costly.

Possible monorepo shape:

```text
core/
protocol/
server/
editors/
  jetbrains/
  vscode/
  zed/
  neovim/
  eclipse/
  sublime/
fixtures/
```

Do not impose this structure on an established repository without an authorized migration.

## Testing matrix

- Core unit/property tests.
- Protocol conformance and golden fixtures.
- Server integration tests.
- One adapter suite per editor and minimum/current version.
- OS/architecture cases driven by native behavior.
- Remote/web/trust modes where claimed.
- Packaging and clean-install/upgrade tests for each registry.
- End-to-end representative workflows without requiring every cross-product combination.

## Release coordination

- Independent adapter versions reduce lockstep releases but require protocol negotiation.
- Lockstep releases simplify compatibility but increase blast radius and registry coordination.
- Record minimum server/protocol versions in each extension.
- Publish server binaries before clients that require them, or bundle a compatible fallback where allowed.
- Keep rollback paths for each registry and avoid simultaneous irreversible migrations.
