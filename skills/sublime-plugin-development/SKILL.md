---
name: sublime-plugin-development
description: Build, migrate, test, package, and publish Sublime Text 4 packages and Python plugins. Use for sublime and sublime_plugin APIs, commands, listeners, settings, menus, keymaps, syntax definitions, completions, minihtml, themes, build systems, Package Control metadata, and .sublime-package distribution.
---

# Sublime Plugin Development

Develop against the package's declared Sublime Text build/Python API environment. Keep import-time behavior minimal, use the command/event lifecycle correctly, preserve resource names and settings, and test in a clean Sublime profile across supported platforms.

## Start with evidence

1. Inspect Python modules, `.sublime-settings`, commands, menus, keymaps, mousemaps, completions, syntax/theme/color-scheme files, build systems, minihtml, messages, dependencies, tests, CI, and Package Control metadata.
2. Identify minimum Sublime build, Python API environment, supported platforms/architectures, package format, native dependencies, Package Control release strategy, and Sublime Text 3 compatibility if any.
3. Preserve package/resource names and user settings. Do not add legacy ST3 compatibility or change Python environments unless requested.
4. Load relevant references:
   - [Platform and architecture](references/platform-and-architecture.md) for package layout, lifecycle, commands/listeners, threading, resources, settings, syntax, completions, and minihtml.
   - [Testing and quality](references/testing-and-quality.md) for pure Python tests, clean-profile integration, reload behavior, UI/resource checks, performance, and security.
   - [Packaging and release](references/packaging-and-release.md) for `.sublime-package`, dependencies, Package Control submission, tags, messages, and release gates.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before adapting command, listener, syntax, LSP, or Package Control patterns.

## Implementation contract

- Treat current stable and the declared minimum build separately. Sublime Text 4 stable was build 4200 on 2026-09-01; verify APIs by build annotations and runtime capability.
- Do not call ordinary API functions during module import. Use `plugin_loaded()` after the API is ready and `plugin_unloaded()` for cleanup.
- Choose `ApplicationCommand`, `WindowCommand`, or `TextCommand` according to ownership; text mutations belong in a `TextCommand` with its `Edit` token.
- Keep event listeners fast. Defer blocking work with async scheduling or worker threads, then re-check view/window validity before applying results.
- Use settings/resources through Sublime APIs and `Packages/<name>/...` paths; do not assume packages are unpacked on disk.
- Keep command names, setting keys, contexts, selectors, scopes, syntaxes, and resource paths stable after publication.
- Sanitize minihtml and navigation callbacks; treat file/project/settings contents as untrusted.
- Avoid broad event listeners, repeated whole-buffer reads, synchronous resource/network work, and global mutable state without reload cleanup.
- Support multiple windows, transient/clone sheets, unsaved views, and package reload.

## Validation boundary

Run Python formatting/lint/unit tests, syntax/schema checks, package/resource load checks, integration smoke tests in a safe or disposable profile, package reload tests, supported build/platform tests, and packaged archive inspection. Validate Package Control metadata without publishing.

Report minimum/current builds, Python environment, commands/listeners/resources changed, tests, package contents, compatibility caveats, and publication actions not performed.

## Templates

Use [the Python package starter](assets/package-template/) as an adaptation source. Replace package/command/settings names, choose the actual Python API environment, and remove example resources that the package does not use.

## Boundaries

- Package Control PRs, tags/releases, hosted package uploads, and channel/repository mutation require explicit authorization.
- Do not add `.no-sublime-package`, binary dependencies, or manual hosting unless the package actually requires unpacked/native artifacts.
- Route cross-editor or shared language-server design to `$editor-extension-router`.
