# IntelliJ plugin packaging and release

## Release inputs

Confirm stable plugin identity, version, vendor, legal files, descriptions, icons, support links, target products/builds, dependency declarations, Marketplace channel, signing ownership, and CI secret source.

## Build and archive

- Use `buildPlugin` or the repository equivalent to produce the distributable ZIP.
- Inspect the archive for descriptors, plugin JARs, dependencies, duplicate classes, forbidden files, development artifacts, credentials, and license notices.
- Keep bundled dependencies minimal and avoid packaging platform libraries already supplied by the IDE.
- Pin Gradle wrapper, repositories, toolchain, platform version, and release commit.
- Install the built archive into a clean compatible IDE rather than testing only the development sandbox.

## Release gate

1. Run tests and integration tests.
2. Run project configuration and structure verification.
3. Run Plugin Verifier across the declared matrix.
4. Exercise installation, startup, core feature, upgrade, disable/uninstall, and dynamic unload when supported.
5. Review Marketplace text, privacy/telemetry behavior, and change notes.

## Signing and credentials

- Configure certificate chain, private key, password, and Marketplace token through approved secret providers.
- Never commit or print private keys, passwords, tokens, or decoded secret material.
- Preserve certificate continuity and document ownership/rotation outside the repository when required.
- `publishPlugin` normally invokes signing when configured, but verify the repository's task graph.

## Publishing and CI

- Marketplace publication, channel changes, paid-plugin configuration, unpublish/delete, and production promotion require explicit authorization.
- Use custom channels for staged/EAP releases when established by the project.
- Never reuse a released version or rewrite release history.
- Separate pull-request verification from protected release jobs.
- Pin CI actions/plugins, minimize permissions, and publish the same verified artifact when practical.
- Retain verifier reports, checksums, artifact metadata, and publication evidence.

## Official sources

- <https://plugins.jetbrains.com/docs/intellij/publishing-plugin.html>
- <https://plugins.jetbrains.com/docs/intellij/plugin-signing.html>
- <https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin-extension.html>
- <https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin-tasks.html>
- <https://plugins.jetbrains.com/docs/marketplace/plugin-upload.html>
