# Multi-editor extension architecture plan

## Outcome

- User workflow:
- Target users/editors:
- Explicitly excluded editors:
- Required operating systems/architectures:
- Minimum editor versions:

## Capability map

| Capability | Portable core/protocol | JetBrains | VS Code | Zed | Neovim | Eclipse | Sublime | Degradation decision |
|---|---|---|---|---|---|---|---|---|
| Language intelligence |  |  |  |  |  |  |  |  |
| Debugging |  |  |  |  |  |  |  |  |
| Syntax/grammar |  |  |  |  |  |  |  |  |
| Commands/settings |  |  |  |  |  |  |  |  |
| Native UI |  |  |  |  |  |  |  |  |
| Remote/web |  |  |  |  |  |  |  |  |

## Shared core

- Language/runtime:
- Public API or protocol version:
- Capability negotiation:
- Cancellation/progress:
- Logging and redaction:
- Process ownership/restart:
- Binary distribution/update:
- Offline/proxy behavior:

## Per-editor adapters

For each editor record:

- Manifest and extension ID.
- Activation and disposal owner.
- Workspace/project/root mapping.
- Trust/permission checks.
- URI/filesystem abstraction.
- Commands, settings, UI, storage, and secrets.
- Protocol transport and executable resolver.
- Minimum/current-version tests.
- Packaging/registry/signing owner.

## Public contracts and migration

- Existing IDs/settings/commands/state:
- Compatibility window:
- Unsupported features:
- State import/export:
- Telemetry/privacy changes:
- Rollback:

## Validation matrix

- Shared core tests:
- Protocol conformance:
- Editor adapter tests:
- OS/architecture:
- Remote/web/trust:
- Clean installation/upgrade:
- Performance/resource limits:
- Release evidence:

## Authorization boundary

- Local artifacts allowed:
- External repositories/registries:
- Publisher identities:
- Signing secrets:
- Production promotion approval:
