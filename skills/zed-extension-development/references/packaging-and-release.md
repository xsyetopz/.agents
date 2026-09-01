# Zed extension packaging and release

## Registry prerequisites

Before publication, determine the current category rules:

- Language extensions support the primary language and related dialects, declare grammars, and may include related LSP/debug/snippet support.
- LSP-only and debugger-only extensions use descriptive IDs and do not bundle executables.
- Theme, icon-theme, and snippet-only extensions remain focused on that content type.
- New agent-server and slash-command extension submissions are not accepted.
- MCP server extension policy is transitional; verify the MCP registry direction.
- The repository must use a license accepted by Zed's current publishing rules.

Review the current prerequisite and license pages rather than copying an old accepted-license list.

## Version synchronization

Keep these identical for a release:

- `extension.toml` version.
- Cargo package version when Rust exists.
- Top-level registry `extensions.toml` entry.
- Submodule commit containing that version.
- Release/tag metadata used for external binaries, when applicable.

Never move a published semantic version to different contents.

## Publication model

Zed registry publication is performed through a pull request to `zed-industries/extensions`:

1. Extension source is publicly available.
2. The registry adds it as an HTTPS Git submodule under `extensions/<extension-id>`.
3. The submodule commit is reachable from a branch.
4. Top-level `extensions.toml` records the extension ID, submodule, optional path, and version.
5. Registry files are sorted with the repository's current `pnpm sort-extensions` command.
6. Maintainers review and merge the PR, after which packaging/publication occurs.

Opening the PR, changing the submodule, or updating the public registry is an external write requiring explicit authorization.

## Release gate

- Validate manifest/schema/assets and run Rust/WASM checks.
- Install and exercise the exact commit as a Dev Extension.
- Confirm supported platforms and external binary asset mapping.
- Review repository/license metadata and category prerequisites.
- Check version consistency and registry path.
- Ensure no binary, secret, build output, cache, or unrelated content is committed.
- Prepare concise user-facing changes and migration notes.

## Updates and maintenance

- Publish source changes first, then update the registry submodule and version in a separate authorized PR.
- Update PRs follow the current registry review and response-time rules.
- Keep upstream language servers/debug adapters maintained and update download logic when release asset naming changes.
- Test Zed/API upgrades before raising `zed_extension_api`.
- If an extension is no longer maintainable, coordinate transfer or removal through current registry policy rather than abandoning mutable download endpoints.

## Official sources

- <https://zed.dev/docs/extensions/publishing/overview>
- <https://zed.dev/docs/extensions/publishing/prerequisites>
- <https://zed.dev/docs/extensions/publishing/license-requirements>
- <https://zed.dev/docs/extensions/publishing/publishing-guide>
- <https://zed.dev/docs/extensions/publishing/updating-and-maintenance>
- <https://github.com/zed-industries/extensions>
