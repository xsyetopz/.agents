---
name: jetbrains-plugin-development
description: Build, migrate, test, verify, sign, and publish plugins for IntelliJ Platform IDEs using the current Gradle 2.x toolchain and supported platform APIs. Use for IntelliJ IDEA, Android Studio, PyCharm, WebStorm, Rider, CLion, GoLand, RubyMine, RustRover, DataGrip, and other IntelliJ-based products; not for VS Code or Eclipse extensions.
---

# JetBrains Plugin Development

Develop against the repository's declared IntelliJ Platform baseline and product matrix. Prefer supported public APIs, declarative registrations, lazy services, lifecycle-bound coroutine scopes, and verification across every advertised IDE build.

## Start with evidence

1. Inspect `gradle.properties`, `settings.gradle.kts`, `build.gradle.kts`, version catalogs, `src/main/resources/META-INF/plugin.xml`, module descriptors, tests, CI, signing configuration, and release automation.
2. Identify target products, minimum and maximum build branches, Java/Kotlin levels, IntelliJ Platform Gradle Plugin version, bundled and Marketplace dependencies, Dynamic Plugin support, and Marketplace channel strategy.
3. Preserve an existing compatible architecture. Do not migrate Gradle 1.x, split modules, modularize the plugin, widen IDE compatibility, or remove an `until-build` boundary unless the request includes that change.
4. Read only the references needed:
   - [Platform and architecture](references/platform-and-architecture.md) for project setup, descriptors, APIs, threading, services, persistence, UI, and compatibility.
   - [Testing and quality](references/testing-and-quality.md) for fixtures, integration tests, Plugin Verifier, inspections, performance, and leak prevention.
   - [Packaging and release](references/packaging-and-release.md) for archives, signing, Marketplace publishing, channels, credentials, and release gates.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before scaffolding or borrowing a pattern from an existing plugin.

## Workflow

- Use IntelliJ Platform Gradle Plugin 2.x for current projects; treat 1.x as migration-only legacy.
- Keep compile-time platform/plugin dependencies and runtime declarations in `plugin.xml` or module descriptors consistent.
- Depend on the narrowest platform module and product-specific plugins required by actual API use.
- Never use implementation/internal APIs or reflection into platform details unless the user explicitly accepts unsupported coupling.
- Keep expensive work off the event dispatch thread. Respect read/write actions, smart/dumb mode, cancellation, disposal, project lifetime, and plugin unload.
- Prefer application/project services with constructor-injected `CoroutineScope` for background lifetimes. Dispose listeners, message-bus connections, alarms, executors, UI resources, and native/process resources.
- Keep actions lightweight in `update()`, use dumb-aware declarations only when behavior is genuinely index-independent, and localize visible strings.
- Treat PSI, VFS, documents, indexes, and write commands as platform-owned models with explicit access constraints; do not retain invalid PSI or project objects beyond their lifetime.
- Follow existing UI technology. Use Kotlin UI DSL for settings-style forms where appropriate, Swing/platform components for general controls, and platform icons/colors/fonts for theme and accessibility support.
- Preserve settings and serialized-state compatibility unless a migration is authorized and tested.

### Templates

Use [the Kotlin/Gradle starter](assets/plugin-template/) as an adaptation source, not a fixed-version generator. Replace every `__PLACEHOLDER__`, select real platform/plugin versions, add only required dependencies/extensions, and retain repository-native structure when editing an existing project.

## Validation

Run focused tests, project tests, `verifyPluginProjectConfiguration`, `verifyPluginStructure`, `verifyPlugin`, and `buildPlugin` as applicable. Inspect and install the built archive in a clean development IDE. Do not claim compatibility from compilation alone.

Report targeted IDEs/builds, changed descriptors and source paths, commands and results, verifier warnings, unsupported APIs, compatibility gaps, and any Marketplace or credential step not executed.

## Boundaries

- Publishing, Marketplace mutations, certificate creation, secret configuration, and release promotion require explicit authorization.
- Do not add compatibility shims for IDE branches outside the declared support matrix.
- When the request expands into cross-editor architecture or shared protocol design, make that decision from current platform capabilities and repository evidence. Never stop to locate or install a companion skill.
