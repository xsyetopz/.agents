# IntelliJ Platform and architecture

Verified against JetBrains documentation available on 2026-09-01. Re-check the SDK docs, target product release notes, and API change lists before changing a version-sensitive contract.

## Current baseline

- Current projects use IntelliJ Platform Gradle Plugin 2.x. The 1.x Gradle plugin is no longer actively developed.
- JetBrains documentation available on the verification date covers IntelliJ Platform 2026.2. Target the repository's declared branch rather than automatically raising it.
- The Gradle plugin selects platform artifacts, JetBrains Runtime, test framework, verification, signing, and publishing tasks. Pin versions through the repository's established catalog or properties.
- Match the Java language/toolchain and Kotlin plugin to the target platform. Do not infer them from the developer machine.

## Project surfaces

Inspect and keep synchronized:

- `settings.gradle.kts`: repositories and IntelliJ Platform settings plugin.
- Root/module `build.gradle.kts`: platform, plugins, test framework, instrumentation, verification, signing, and publishing.
- `gradle.properties` or version catalog: plugin version, platform type/version, since/until builds, channels, and feature flags.
- `META-INF/plugin.xml`: identity, vendor, dependencies, extensions, actions, listeners, resource bundle, and compatibility.
- Optional module descriptors for modular plugins. Modular plugins are experimental; use only when already adopted or explicitly requested.
- Icons, descriptions, change notes, searchable options, localization bundles, and legal files.

Keep one canonical source for values patched by Gradle. Avoid maintaining the same version, compatibility range, description, or change notes independently in several files.

## Compatibility and dependencies

- `since-build` and `until-build` use real IntelliJ build branches. Never invent branch/build values.
- Omitting `until-build` declares open-ended compatibility and can expose users to unverified future IDEs. Make that a conscious policy decision.
- Declare the appropriate platform module dependency; new plugins should not rely on legacy implicit IntelliJ IDEA-only loading.
- Add bundled or third-party plugin dependencies to Gradle for compilation and to runtime descriptors for loading.
- Optional dependencies need code paths that remain absent until the dependency is available.
- Verify dependencies against every product advertised. An API present in IntelliJ IDEA may be absent in another product.
- Use the IntelliJ Platform Explorer, extension-point lists, bundled descriptors, and current source to find supported registrations and examples.

## Public API discipline

- Prefer documented OpenAPI classes and extension points.
- Treat `@ApiStatus.Experimental` as a compatibility risk, `@ScheduledForRemoval` as migration work, and `@Internal` or implementation packages as unsupported.
- Avoid service lookup in constructors when it creates initialization cycles. Keep constructors cheap.
- Prefer extension points and services over classloader tricks, reflection, global singletons, or replacing platform implementations.
- Record why unsupported API use is unavoidable, which IDE builds are tested, and how breakage will be detected.

## Lifetimes, threading, and cancellation

- UI callbacks generally run on the event dispatch thread; keep them short.
- Use background dispatchers/tasks for blocking I/O and CPU work. Re-enter the correct platform context for model or UI mutation.
- Respect read/write actions and write-command requirements. Avoid long read actions that starve writes.
- Account for dumb mode when indexes are unavailable.
- Prefer constructor-injected service coroutine scopes. Service scopes are canceled with application/project and plugin lifetimes.
- Propagate cancellation and use platform progress/cancellation mechanisms for user-visible long work.
- Tie listeners and resources to a `Disposable`, message-bus connection, service scope, project, editor, or tool-window lifetime.
- Dynamic unload requires no leaked threads, classloader references, static project state, undisposed UI, or persistent callbacks.

## Platform models and UI

- PSI is a semantic model, not durable storage. Re-resolve smart pointers or identifiers and check validity.
- Keep documents and PSI synchronized through supported APIs and commands.
- Use VFS and indexing APIs instead of raw polling or untracked caches.
- Use `PersistentStateComponent` or current storage APIs for settings; store credentials through password-safe APIs.
- Register actions declaratively and keep `update()` cheap.
- Use Kotlin UI DSL for settings-style forms and platform Swing components for general UI.
- Follow platform icons, theme colors, spacing, accessibility, keyboard navigation, high contrast, and localization.

## Official sources

- <https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin.html>
- <https://plugins.jetbrains.com/docs/intellij/configuring-gradle.html>
- <https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html>
- <https://plugins.jetbrains.com/docs/intellij/plugin-compatibility.html>
- <https://plugins.jetbrains.com/docs/intellij/build-number-ranges.html>
- <https://plugins.jetbrains.com/docs/intellij/threading-model.html>
- <https://plugins.jetbrains.com/docs/intellij/coroutine-scopes.html>
- <https://plugins.jetbrains.com/docs/intellij/services.html>
- <https://plugins.jetbrains.com/docs/intellij/kotlin-ui-dsl-version-2.html>
- <https://plugins.jetbrains.com/docs/intellij/api-changes-list.html>
