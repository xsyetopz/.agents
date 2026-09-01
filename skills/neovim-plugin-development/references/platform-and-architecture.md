# Neovim plugin platform and architecture

Verified against Neovim documentation and releases on 2026-09-01. Neovim 0.12.5 was the latest stable release; 0.13 was development-only. Use the plugin's declared minimum version and review `:help news-0.12` plus `:help deprecated` before version-sensitive changes.

## Runtime layout

Neovim discovers plugin content through `runtimepath` and packages. There is no required plugin manifest.

- `plugin/*.lua` or `.vim`: sourced during startup after user configuration; keep lightweight.
- `lua/<module>/`: Lua modules loaded by `require()`.
- `autoload/`: Vimscript autoload functions when needed for Vimscript/public compatibility.
- `ftplugin/<filetype>.*`: buffer-local filetype behavior.
- `after/`: overrides/additions loaded after ordinary runtime files; use sparingly.
- `queries/<language>/*.scm`: Tree-sitter queries.
- `syntax/`, `indent/`, `compiler/`, `ftdetect/`, `colors/`, `keymap/`: standard runtime integrations.
- `doc/*.txt`: Vim help documents; generate tags with `:helptags`.
- `lua/<plugin>/health.lua`: discovered by `:checkhealth`.

Do not require one package manager. A repository-root plugin should work when placed on runtimepath or under `pack/*/start/*`.

## Public API design

- Use one stable top-level Lua module and focused submodules.
- Return a module table; avoid writing unrelated globals.
- Document functions, options, commands, mappings, events, and highlight groups as public or internal.
- Keep configuration defaults immutable. Deep-copy or construct merged state where nested tables matter.
- Validate types and important invariants with `vim.validate()` or equivalent behavior supported at the minimum version.
- Report unknown configuration fields through clear errors or health checks according to compatibility policy.
- Avoid implicit setup side effects at module import.

## Startup and lazy behavior

- Use a `vim.g.loaded_<name>` guard in startup/ftplugin files when duplicate sourcing is possible.
- Startup files may define commands/autocmds that require implementation modules only when invoked.
- Do not inspect the entire workspace, spawn jobs, initialize LSP clients, or create UI during startup without a feature trigger.
- A plugin manager's lazy-loading spec is consumer configuration, not the plugin's core architecture.
- Neovim 0.12 includes `vim.pack`, but plugins should remain runtimepath-compatible unless explicitly built around that manager.

## Commands, mappings, autocmds, and options

- Create user commands with explicit argument, range, bang, completion, and buffer scope.
- Offer functions or `<Plug>(PluginAction)` mappings; leave user-facing key choices to users unless the plugin's UX contract explicitly includes defaults.
- Use a named augroup and delete/clear only resources owned by that group.
- Prefer `FileType` and buffer-local behavior over scanning all buffers.
- Set options with correct global/local scope and preserve user values when behavior is temporary.
- Namespace extmarks, highlights, diagnostics, and decorations so cleanup is exact.

## Events, async work, and lifecycle

- API callbacks can run under textlock or fast-event restrictions. Use `vim.schedule()`/`vim.schedule_wrap()` before forbidden mutations.
- Prefer current `vim.uv` naming when the minimum version supports it; retain `vim.loop` only for declared older compatibility.
- Close timers, pipes, TCP handles, jobs, channels, and watchers on completion, buffer deletion, client stop, or plugin teardown.
- Use bounded queues and debounce/coalesce rapid events.
- Check buffer/window validity immediately before mutation; IDs can become invalid between async steps.
- Use `vim.system()` where available for structured process invocation, timeout, text output, and cancellation. Avoid shell strings.

## UI and state

- Use scratch buffers with deliberate `buftype`, `bufhidden`, `swapfile`, modifiability, filetype, and cleanup.
- Keep window creation/restoration robust when users close or move windows.
- Store plugin metadata in namespaced buffer/window variables or module-owned weak/bounded tables.
- Use `vim.ui.select`, `vim.ui.input`, notifications, quickfix/location lists, floating windows, extmarks, or in-process LSP actions according to composability.
- Define highlight groups with `default=true` and link to semantic groups so colorschemes can override them.

## LSP

- Core Neovim provides an LSP client; servers remain external.
- Current 0.12 APIs include `vim.lsp.config`-style configuration and expanded defaults. Check the minimum version before using them.
- Avoid resetting global handlers/keymaps or duplicating defaults.
- Scope clients by root and filetype, support multiple clients, honor capabilities, and clean diagnostics/state on detach.
- Treat server settings, root detection, command, and environment as public compatibility surfaces.

## Tree-sitter

- Neovim documents Tree-sitter integration as experimental/version-sensitive.
- Keep query captures conventional and narrowly scoped.
- Use `; extends` only when intentionally extending inherited queries.
- Validate parser ABI/revision and changed node names.
- Avoid reading undocumented metadata shapes; use current range/query APIs.

## Official sources

- <https://neovim.io/doc/user/lua-plugin/>
- <https://neovim.io/doc/user/lua-guide/>
- <https://neovim.io/doc/user/api/>
- <https://neovim.io/doc/user/pack/>
- <https://neovim.io/doc/user/health/>
- <https://neovim.io/doc/user/lsp/>
- <https://neovim.io/doc/user/treesitter/>
- <https://neovim.io/doc/user/deprecated/>
- <https://neovim.io/doc/user/news-0.12/>
- <https://github.com/neovim/neovim/releases>
