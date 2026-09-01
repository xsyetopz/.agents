# Sublime Text package testing and quality

## Test layers

1. Pure Python tests outside Sublime for parsing, transformation, state, command construction, and protocols.
2. Sublime API integration tests for commands, views, settings, resources, events, and lifecycle.
3. Syntax/completion/theme fixture checks.
4. Clean-profile manual or automated smoke tests.
5. Packaged `.sublime-package` install/update/reload tests.

Keep Sublime-dependent code behind small adapters so most logic can run under ordinary Python matching the embedded environment.

## Clean environment

- Use `subl --safe-mode` for a sandboxed clean environment where appropriate.
- Prefer a disposable/portable data directory or test installation when package placement and restart behavior must be controlled.
- Do not copy test packages into the user's real `Packages/User` without authorization.
- Disable unrelated packages and use fixture projects/files.
- Capture console output and build/version/platform information.

The CLI supports `--command`, new windows, projects, safe mode, version output, and other platform-dependent options. Check `subl --help` on the tested installation rather than assuming every flag.

## Lifecycle cases

- Cold startup and `plugin_loaded()` initialization.
- Package reload after Python/resource changes.
- `plugin_unloaded()` cleanup with pending async work.
- Multiple windows and project changes.
- Views closed while callbacks are queued.
- Package disabled/enabled and application restart.
- Upgrade with old settings/state and removed resources.

## Command/listener cases

- Correct command name conversion and command-palette/menu/keymap wiring.
- `is_enabled`/`is_visible` and contexts for valid/invalid views.
- TextCommand edits across multiple selections and read-only/scratch/large views.
- Event ordering, duplicate listeners after reload, async callback state changes.
- Input handler validation, back navigation, cancellation, and event metadata.
- No accidental recursion from edits triggered inside modification listeners.

## Resource and syntax tests

- Load every referenced resource through Sublime's resource API.
- Validate JSON/YAML syntax and platform-specific keymap/menu variants.
- Ensure package name and `Packages/<name>/...` references match exactly.
- Test syntax scopes on representative, nested, incomplete, and adversarial files.
- Test completions with selectors, inhibition flags, commit characters, snippets, and asynchronous refresh where used.
- Exercise minihtml in light/dark themes, high DPI, long/untrusted text, keyboard navigation, and link callbacks.

## Performance and concurrency

- Avoid synchronous `load_resource` of large files in hot callbacks; resource loading is synchronous.
- Measure whole-buffer operations on large files.
- Debounce selection/modified events and narrow listener applicability.
- Ensure workers do not call stale views after reload/close.
- Bound quick-panel/completion/result sizes and cancel obsolete work.
- Check process handles, temp files, threads, timers, settings listeners, and phantoms on unload.

## Security

- Treat project settings, build variables, file paths, file contents, and URLs as untrusted.
- Avoid shell command strings; use structured process APIs or carefully validated argument lists in chosen subprocess library.
- Escape minihtml content and validate navigation targets.
- Never log credentials, access tokens, private file content, or full environment dumps.
- Review bundled Python dependencies/native binaries and update channels.

## Official sources

- <https://www.sublimetext.com/docs/api_reference.html>
- <https://www.sublimetext.com/docs/command_line.html>
- <https://www.sublimetext.com/docs/safe_mode.html>
- <https://www.sublimetext.com/docs/syntax.html>
- <https://www.sublimetext.com/docs/minihtml.html>
