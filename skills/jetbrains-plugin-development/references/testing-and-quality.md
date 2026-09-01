# IntelliJ plugin testing and quality

## Test layers

Use the cheapest layer that exercises the real contract:

1. Pure Kotlin/Java tests for platform-independent logic.
2. Light platform tests for PSI, actions, inspections, references, completion, and services that can reuse fixtures.
3. Heavy tests only when a fresh project/application state is required.
4. Integration API tests for complete-product behavior.
5. UI tests for workflows that cannot be asserted through supported APIs.
6. Plugin Verifier and clean-install smoke tests for packaging and compatibility.

Platform tests use real implementations for many services. Do not mock platform models when a fixture gives a more meaningful oracle.

## Fixture practices

- Select the narrowest fixture/base class matching the feature.
- Assert behavior, diagnostics, navigation, edits, or presentation rather than implementation details.
- Use stable markers and fixture APIs instead of filesystem sleeps or arbitrary UI delays.
- Restore registries, extension registrations, services, settings, system properties, and temporary files.
- Ensure `super.tearDown()` runs in a `finally` block when overriding teardown.
- Test cancellation, project close, plugin unload, dumb mode, read-only files, malformed input, and absent optional dependencies when relevant.

## Feature-specific checks

- Actions: visibility/enabled state by place and context, dumb mode, update performance, invocation side effects.
- PSI/inspections: parse errors, incomplete code, injected languages, modules, libraries, and quick-fix write commands.
- Completion/navigation: indexing state, cancellation, no duplicate results, and result ordering only when contractual.
- Tool windows/editors: disposal, reopening, project close, theme changes, keyboard and accessibility behavior.
- Settings: defaults, round trip, old-state migration, invalid state, and project/application scope.
- Processes/network: command construction, environment, cancellation, timeouts, output limits, proxy, credentials, and offline failure.

## Verification and matrix

Use repository-configured equivalents of `test`, `verifyPluginProjectConfiguration`, `verifyPluginStructure`, `verifyPlugin`, `buildPlugin`, and integration-test tasks.

- Test the minimum supported IDE branch and newest declared branch.
- Test each distinct product dependency surface.
- Include EAP only when early compatibility is intentional.
- Separate source compatibility, binary verification, installation, startup, and feature behavior in reports.
- Do not suppress invalid ranges, missing dependencies, internal APIs, scheduled removals, or binary incompatibility merely to pass CI.

## Performance and leaks

- Profile startup and action `update()` hot paths before optimizing.
- Avoid whole-project scans, synchronous I/O, repeated PSI traversal, and unbounded caches.
- Use modification trackers and cached-value infrastructure.
- Check repeated project open/close and dynamic unload for leaked classloaders, threads, listeners, editors, UI, and coroutines.
- Keep logs actionable and free of source contents, credentials, tokens, and high-frequency noise.

## Official sources

- <https://plugins.jetbrains.com/docs/intellij/testing-overview.html>
- <https://plugins.jetbrains.com/docs/intellij/light-and-heavy-tests.html>
- <https://plugins.jetbrains.com/docs/intellij/testing-faq.html>
- <https://plugins.jetbrains.com/docs/intellij/integration-tests.html>
- <https://plugins.jetbrains.com/docs/intellij/integration-tests-intro.html>
- <https://plugins.jetbrains.com/docs/intellij/integration-tests-ui.html>
- <https://plugins.jetbrains.com/docs/intellij/verifying-plugin-compatibility.html>
- <https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin-tasks.html>
- <https://plugins.jetbrains.com/docs/intellij/dynamic-plugins.html>
