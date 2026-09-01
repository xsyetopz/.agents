# IntelliJ Platform plugin starter

Adapt rather than copy blindly:

1. Replace every `__PLACEHOLDER__`.
2. Resolve current released Gradle, Kotlin, platform, and Java versions against the target IDE.
3. Add only required platform/plugin dependencies and extension registrations.
4. Generate a Gradle wrapper with the version supported by the selected IntelliJ Platform Gradle Plugin.
5. Run tests, project/structure verification, Plugin Verifier, and `buildPlugin`.

The example action is intentionally small. Delete it when the requested plugin does not expose an action.
