# Sublime Text package platform and architecture

Verified against official Sublime Text documentation on 2026-09-01. Sublime Text 4 build 4200 was the current stable download. The API documentation can include annotations for later development builds; target the package's declared minimum and guard newer APIs deliberately.

## Package model

Sublime packages are resource trees under `Packages/<PackageName>/` or packed `.sublime-package` archives. Typical resources include:

- Python modules loaded as plugins.
- `.sublime-settings` defaults.
- `.sublime-commands`, `.sublime-menu`, `.sublime-keymap`, `.sublime-mousemap`.
- `.sublime-syntax`, `.tmLanguage`, `.sublime-completions`, `.sublime-snippet`.
- `.sublime-build`, `.sublime-project`, selectors and contexts.
- `.sublime-theme`, `.sublime-color-scheme`, icons/images.
- `messages.json` and install/upgrade message files.
- Python dependency metadata and optional `.no-sublime-package`.

Use resource APIs such as `load_resource`, `load_binary_resource`, `find_resources`, and `decode_value` rather than direct filesystem paths. Packed packages may have no ordinary directory path.

## Python environment and compatibility

Sublime Text 4 introduced a Python 3.8 API environment while retaining compatibility mechanisms for older packages. Determine the selected environment from package metadata and runtime behavior.

- Do not import unsupported third-party modules merely because they exist in the developer's Python.
- The embedded Python environment is separate from system Python.
- For stable builds supporting Python 3.8, select it with a repository-root `.python-version` containing `3.8`; absence historically selected the legacy 3.3 environment. Verify newer build behavior before adopting the Python 3.14 environment documented for build 4205 and later.
- Guard newer API by minimum build or capability when supporting older builds.
- Keep ST3 compatibility only when it is an explicit support contract; it can require syntax, API, and dependency constraints.
- Use `sublime.version()`, `platform()`, `arch()`, and `channel()` only for real compatibility branches.

## Plugin lifecycle

- Module import happens before ordinary API readiness. Only the limited functions documented for import time are safe.
- Put API initialization in module-level `plugin_loaded()`.
- Use `plugin_unloaded()` to cancel timers/tasks, close resources, remove temporary state, and invalidate caches.
- Sublime reloads plugin modules during development and package updates. Code must tolerate reload without duplicate registrations, stale class references, or orphan workers.
- Avoid background threads retaining old module objects after reload.

## Commands and listeners

- `ApplicationCommand`: application-wide action.
- `WindowCommand`: action owned by a window.
- `TextCommand`: buffer mutation using `run(edit, ...)`.
- Command class names map from `CamelCaseCommand` to `snake_case`; treat command names as public IDs.
- Use `is_enabled`, `is_visible`, `description`, and input handlers for context-aware UX without heavy work.
- `EventListener` receives global events; `ViewEventListener` narrows ownership to a view; `TextChangeListener` handles text-change streams.
- Keep callbacks fast, avoid recursive edits, and understand sync versus async event variants.

## Threading and async work

The API is documented as thread-safe, but application state can change concurrently.

- Use `sublime.set_timeout` for main-loop scheduling and `set_timeout_async` for worker-thread tasks.
- Capture stable IDs/data, not long-lived assumptions about active window/view/selection.
- Revalidate `view.is_valid()`/window association and changed content before applying asynchronous results.
- Use TextCommands for edits. Do not retain `Edit` objects beyond the command call.
- Bound subprocess/network work, support cancellation where possible, and avoid blocking event callbacks.

## Settings and state

- Load package defaults with `sublime.load_settings` and listen for changes with namespaced callbacks.
- Separate default, user, project, syntax, view, and session scopes.
- Do not overwrite user settings files programmatically unless the feature explicitly owns a setting and migration is authorized.
- Store secrets outside plain settings/project files; Sublime has no universal package secret store, so define a safe external/OS-specific strategy when credentials are unavoidable.
- Remove change listeners and clear temporary state on unload.

## Syntax, selectors, completions, and UI

- Use `.sublime-syntax` YAML and test prototype/context transitions, recursion, embeddings, captures, and performance.
- Follow scope naming conventions so themes, selectors, symbol indexing, and completions interoperate.
- Prefer `CompletionItem`/`CompletionList` on supported builds for structured asynchronous completions.
- Use phantoms, popups, sheets, quick panels, and input handlers according to native UX.
- minihtml is a constrained HTML/CSS environment, not a browser. Escape untrusted text, validate links/events, use theme variables, and support DPI/accessibility.
- Keep keybindings contextual and avoid overriding common defaults without user choice.

## Official sources

- <https://www.sublimetext.com/docs/api_reference.html>
- <https://www.sublimetext.com/docs/packages.html>
- <https://www.sublimetext.com/docs/api_environments.html>
- <https://www.sublimetext.com/docs/porting_guide.html>
- <https://www.sublimetext.com/docs/syntax.html>
- <https://www.sublimetext.com/docs/scope_naming.html>
- <https://www.sublimetext.com/docs/minihtml.html>
- <https://www.sublimetext.com/docs/key_bindings.html>
- <https://www.sublimetext.com/>
