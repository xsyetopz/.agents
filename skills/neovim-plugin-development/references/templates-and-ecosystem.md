# Neovim templates and ecosystem examples

Verified 2026-09-01. Neovim has no central plugin registry, so repository quality, maintenance, tests, documentation, and version support must be evaluated directly. Review licenses before adapting code.

## Starters and test infrastructure

- `ellisonleao/nvim-plugin-template`, `greggh/neovim-plugin-template`, and `m00qek/plugin-template.nvim`: community scaffolds with different CI/test/tooling choices; compare rather than merging all conventions.
- `nvim-lua/plenary.nvim`: commonly used Busted-style test harness and utility library.
- `nvim-lua/kickstart.nvim`: configuration teaching resource, not a plugin architecture template.

## Production plugins

- `nvim-telescope/telescope.nvim`: composable picker APIs, extensions, configuration layering, health checks, async jobs, and large test surface.
- `folke/lazy.nvim`: startup/lazy loading, spec normalization, concurrency, package management, UI, profiling, and extensive state ownership.
- `neovim/nvim-lspconfig`: runtime LSP configuration corpus and migration toward core `vim.lsp.config` APIs.
- `stevearc/conform.nvim`: formatter orchestration, async/sync execution, fallback behavior, and testable configuration.
- `lewis6991/gitsigns.nvim`: buffer attachment, jobs, extmarks, debouncing, large repositories, and lifecycle cleanup.
- `folke/which-key.nvim`: keymap discovery, plugin API/configuration, UI and health patterns.
- `nvim-treesitter/nvim-treesitter`: parser/query management and version-sensitive Tree-sitter integration.

## What to extract

- Public module and option organization.
- Buffer-scoped attachment/detachment and augroup ownership.
- Headless test setup and fixture isolation.
- Health checks that diagnose dependencies without installing them.
- Async cancellation, job cleanup, and large-buffer guards.
- Help tags, Lua annotations, semantic versioning, and deprecation policy.

## Avoid copying

- Plugin-manager-specific lazy specs into core plugin code.
- Compatibility layers for versions outside the target floor.
- Internal helper libraries or copied utilities without license review.
- Unbounded global state, startup autoloading, or benchmark claims from unrelated workloads.

## Repositories

- <https://github.com/ellisonleao/nvim-plugin-template>
- <https://github.com/greggh/neovim-plugin-template>
- <https://github.com/m00qek/plugin-template.nvim>
- <https://github.com/nvim-lua/plenary.nvim>
- <https://github.com/nvim-lua/kickstart.nvim>
- <https://github.com/nvim-telescope/telescope.nvim>
- <https://github.com/folke/lazy.nvim>
- <https://github.com/neovim/nvim-lspconfig>
- <https://github.com/stevearc/conform.nvim>
- <https://github.com/lewis6991/gitsigns.nvim>
- <https://github.com/folke/which-key.nvim>
- <https://github.com/nvim-treesitter/nvim-treesitter>
