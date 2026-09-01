# Sublime Text templates and ecosystem examples

Verified 2026-09-01. Sublime packages vary from declarative resource sets to large asynchronous Python applications. Review package and dependency licenses before adapting code.

## Primary sources

- `sublimehq/Packages`: syntaxes and resources shipped with Sublime Text; main follows the dev channel, so use release tags for stable-build compatibility.
- `SublimeText/PackageDev`: syntax/schema support and commands for developing Sublime resource files.
- `sublimehq/package_control`: package loading, dependency/download/update behavior, channels, tests, and cross-platform concerns.

## Production packages

- `sublimelsp/LSP`: large plugin lifecycle, sessions, asynchronous requests, views/listeners, diagnostics, completions, tests, and package dependencies.
- `SublimeText/LaTeXTools`: mature multi-module command/listener package with external tools and cross-platform behavior.
- `SublimeText/Origami`: window/layout commands and native UI integration.
- `SublimeText/TrailingSpaces`: smaller command/listener/settings package useful for focused lifecycle patterns.
- `randy3k/Terminus`: process/terminal emulation, platform differences, keymaps, and resource packaging.
- `jisaacks/GitGutter`: view lifecycle, regions, subprocess Git integration, and debouncing.

## What to extract

- `plugin_loaded`/`plugin_unloaded` ownership and reload safety.
- Command/listener decomposition and module naming.
- Resource-path access that works from packed packages.
- Structured settings/defaults and change-listener cleanup.
- Clean profile, syntax, and package tests.
- Platform/architecture release metadata and Package Control messages.

## Avoid copying

- Package names, command IDs, settings, icons, messages, or Package Control metadata.
- Compatibility branches for unsupported Sublime builds.
- Private helper modules or vendored dependencies without license review.
- Direct filesystem assumptions from packages requiring `.no-sublime-package` unless the new package has the same need.

## Repositories

- <https://github.com/sublimehq/Packages>
- <https://github.com/SublimeText/PackageDev>
- <https://github.com/sublimehq/package_control>
- <https://github.com/sublimelsp/LSP>
- <https://github.com/SublimeText/LaTeXTools>
- <https://github.com/SublimeText/Origami>
- <https://github.com/SublimeText/TrailingSpaces>
- <https://github.com/randy3k/Terminus>
- <https://github.com/jisaacks/GitGutter>
