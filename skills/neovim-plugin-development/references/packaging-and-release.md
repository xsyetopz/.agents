# Neovim plugin packaging and release

## Repository contract

A distributable Neovim plugin is normally a version-controlled directory with runtime files at repository root. Keep installation independent of a particular manager.

Recommended release surfaces when applicable:

- `README.md` with installation-neutral examples and minimum Neovim version.
- `doc/<plugin>.txt` with help tags and complete public API.
- `LICENSE` and notices for bundled grammars/assets.
- Semantic tags/releases and concise changes/migrations.
- Optional rockspec only when LuaRocks packaging is supported and tested.

Do not commit generated help tags when repository convention regenerates them, and do not omit them when the target distribution requires them.

## Package-manager neutrality

- The plugin should work when cloned under `pack/*/start/*`, added to runtimepath, or installed by a manager.
- Do not inspect manager internals to decide whether the plugin is loaded.
- Document optional dependency ordering using ordinary runtime requirements first, then manager examples if requested.
- Keep build steps explicit for generated parsers/native components; pure-Lua plugins should not invent a build phase.
- Neovim's built-in `vim.pack` in 0.12 does not make third-party manager metadata a plugin requirement.

## Release gate

1. Run formatting, lint/type checks, unit/headless tests, and version matrix.
2. Run `:helptags`, `:checkhealth`, and clean-install smoke tests.
3. Verify no user paths, local configuration, caches, test artifacts, or secrets are included.
4. Check public module names, commands, mappings, events, highlight groups, and config migration notes.
5. Confirm dependency versions/licenses and external binary policy.
6. Create immutable version tags only after the release commit is final.

## Compatibility and versioning

- State a minimum Neovim version in one canonical place and keep CI/docs aligned.
- Use semantic versioning when public APIs/configuration are versioned; explain intentional deviations.
- Treat renamed modules/options/commands as breaking unless aliases are retained by explicit support policy.
- Do not keep indefinite shims without a removal contract.
- Avoid tagging the same version to different commits.

## LuaRocks and native artifacts

- Add a rockspec only if users or dependencies need LuaRocks resolution.
- Pin source/tag and declare Lua/Neovim/native dependencies accurately.
- Test installation in an isolated tree.
- For native binaries, publish per-platform artifacts with checksums and a clear source-build fallback or unsupported-platform error.
- Do not download/execute binaries automatically without an explicit plugin feature and security review.

## Publication boundary

Git tags, GitHub/GitLab releases, package-manager registry changes, generated binary uploads, and ownership transfers are external writes requiring explicit authorization. Local release notes and artifacts may be prepared without publishing.

## Official sources

- <https://neovim.io/doc/user/pack/>
- <https://neovim.io/doc/user/lua-plugin/>
- <https://neovim.io/doc/user/helphelp/>
- <https://github.com/neovim/neovim/releases>
- <https://luarocks.org/>
