# JetBrains templates and ecosystem examples

Verified 2026-09-01. Inspect current source and license before adapting a pattern. Do not copy implementation code or branding unless its license and attribution requirements are compatible with the target project.

## Primary templates and samples

- `JetBrains/intellij-platform-plugin-template`: current Gradle 2.x repository structure, verifier/signing/release automation, changelog and dependency update patterns.
- `JetBrains/intellij-platform-compose-plugin-template`: Compose-oriented UI experiments; verify current platform support before choosing Compose over platform Swing/UI DSL.
- `JetBrains/intellij-platform-modular-plugin-template`: experimental modular/frontend-backend structure for distributed IDE scenarios; do not adopt for an ordinary plugin.
- `JetBrains/intellij-sdk-code-samples`: focused extension-point examples for actions, inspections, services, settings, PSI, tool windows, and tests.
- `JetBrains/intellij-sdk-docs`: source of the SDK documentation and sample provenance.
- `JetBrains/intellij-platform-gradle-plugin`: authoritative task/configuration implementation when Gradle behavior is unclear.

## Large production codebases

- `JetBrains/intellij-community`: platform implementation and bundled plugins. Use public API and extension-point examples only; internal source availability does not make an API supported.
- `JetBrains/intellij-plugins`: many JetBrains-maintained language and framework plugins with multi-module structures and tests.
- `JetBrains/intellij-rust`: historical/production-scale language plugin architecture; check current ownership and API age before imitation.
- `MinecraftDev/MinecraftDev`: multi-platform IntelliJ plugin with actions, inspections, settings, build tooling, and compatibility concerns.
- `google/google-java-format` IntelliJ plugin module: compact example of integrating an external formatter and settings into the IDE.

## What to extract

- Gradle 2.x declarations and CI verification from the official template.
- The smallest extension-point sample matching the feature from SDK samples.
- Service/disposal/threading idioms from current platform code.
- Multi-module separation only when product/dependency boundaries justify it.
- Tests that assert platform behavior rather than mocked internals.

## Avoid copying

- Template version pins without checking current releases.
- Internal APIs used by bundled JetBrains code.
- Product branding, plugin IDs, certificate configuration, Marketplace workflows, or secrets.
- Old Gradle 1.x syntax and obsolete UI-test infrastructure from historical commits.

## Repositories

- https://github.com/JetBrains/intellij-platform-plugin-template
- https://github.com/JetBrains/intellij-platform-compose-plugin-template
- https://github.com/JetBrains/intellij-platform-modular-plugin-template
- https://github.com/JetBrains/intellij-sdk-code-samples
- https://github.com/JetBrains/intellij-sdk-docs
- https://github.com/JetBrains/intellij-platform-gradle-plugin
- https://github.com/JetBrains/intellij-community
- https://github.com/JetBrains/intellij-plugins
- https://github.com/JetBrains/intellij-rust
- https://github.com/MinecraftDev/MinecraftDev
- https://github.com/google/google-java-format
