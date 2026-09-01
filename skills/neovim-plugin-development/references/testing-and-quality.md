# Neovim plugin testing and quality

## Isolated test environment

Run tests outside the developer's real configuration:

- Use `nvim --headless` with `--clean` or `-u` pointing to a minimal test init.
- Set temporary `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME`.
- Build a controlled runtimepath containing the plugin and explicit test dependencies only.
- Disable swap/backup/shada or redirect them into the fixture when they are irrelevant.
- Pin the tested Neovim binary/version in CI.

## Test layers

1. Pure Lua tests for parsing, merging, protocol, command construction, and state transitions.
2. Headless API tests for buffers, windows, commands, mappings, autocmds, extmarks, diagnostics, and lifecycle.
3. LSP/RPC/process integration tests with deterministic fake servers/processes.
4. Tree-sitter query fixtures using exact parser revisions.
5. Interactive smoke tests only for behavior that cannot be observed headlessly.

Plenary can provide a Busted-style harness, but it is a third-party choice rather than a Neovim requirement. Preserve the repository's existing test framework and account for async handles that can keep headless instances alive.

## Core behavior cases

- Module import is side-effect safe and idempotent where expected.
- `setup()` defaults, partial config, invalid config, repeated calls, and migration behavior.
- Commands: arguments, ranges, bang, completion, invalid buffers, cancellation, and errors.
- Mappings: `<Plug>` availability, buffer scope, no overwrite of user mappings, cleanup.
- Autocmds: duplicate setup, group ownership, buffer deletion, rapid event sequences.
- UI: user-closes-window behavior, focus restoration, scratch-buffer cleanup, multi-window/tab behavior.
- Async: cancellation, timeout, process failure, partial output, invalidated buffers, pending timers/handles.
- LSP: root changes, multiple clients, attach/detach, capability absence, server restart, diagnostics cleanup.
- Persistence: corrupt/old state, atomic writes, concurrent updates, path portability.

## Version matrix

- Test the minimum supported release.
- Test current stable, which was 0.12.5 on the verification date.
- Optionally test nightly as an allowed-failure early-warning job; never make nightly behavior the stable contract.
- Read every release's `:help news-*` and `:help deprecated` between the floor and current stable.
- Avoid version-string branching when feature detection is reliable and semantically equivalent.

## Health checks

`lua/<plugin>/health.lua` should diagnose actionable environmental conditions:

- Neovim version and required feature availability.
- Required and optional executables/providers.
- Configuration conflicts or invalid options.
- Parser/server/plugin dependencies.
- Writable cache/data paths and platform limitations.

Health checks should not perform destructive actions, install dependencies, expose secrets, or fail because optional enhancements are absent.

## Performance and leaks

- Measure startup with controlled repeated runs before changing lazy architecture.
- Profile callback frequency and large-buffer/project behavior.
- Avoid whole-buffer copies, repeated full scans, unbounded extmarks/diagnostics, and synchronous filesystem/process work.
- Ensure headless tests exit; lingering uv handles, jobs, channels, or timers indicate lifecycle defects.
- Bound logs and never include source content, environment secrets, or authentication tokens by default.

## Documentation checks

- Run `:helptags` on `doc/` and check duplicate/missing tags.
- Verify examples with the declared minimum version.
- Keep Lua annotations and help signatures aligned with implementation.
- Document defaults, side effects, external dependencies, public events, and compatibility policy.

## Official sources

- <https://neovim.io/doc/user/lua-plugin/>
- <https://neovim.io/doc/user/starting/>
- <https://neovim.io/doc/user/api/>
- <https://neovim.io/doc/user/health/>
- <https://github.com/nvim-lua/plenary.nvim>
