# Sublime Text package packaging and release

## Package forms

- Development packages are commonly unpacked under `Packages/`.
- Installed packages may be ZIP-compatible `.sublime-package` archives.
- Add `.no-sublime-package` only when files must remain unpacked, typically executables or shared libraries.
- Do not assume a resource has a filesystem path when packed.

Inspect the final archive for Python modules, resource files, messages, license, dependencies, and unexpected development content.

## Package Control expectations

Package Control's default channel indexes packages and resolves releases from repository tags or explicitly hosted package metadata.

- Search for existing packages before creating a duplicate public listing.
- Use a stable package name compatible with filesystem and Python package rules.
- Public GitHub/Bitbucket hosting normally uses one package at repository root.
- New releases use semantic version tags; branch-based releases are deprecated for new submissions.
- Remove `.pyc`, generated `package-metadata.json`, local caches, and invalid cross-platform filenames.
- Hosted package/repository metadata must use HTTPS.
- Run current ChannelRepositoryTools/default-channel validation before submitting metadata.

Package Control documentation contains historical ST3 terminology in places; verify current channel schemas and accepted release rules before publication.

## Dependencies and native files

- Declare Package Control dependencies using its current dependency model and compatible Python environment.
- Avoid vendoring common dependencies when Package Control provides a supported package, but do not migrate existing dependency ownership without need.
- Native binaries require platform/architecture-specific releases, licenses, safe extraction, and unpacked-package behavior.
- Never ship locally compiled binaries without reproducible source/provenance and target-platform tests.

## Install and upgrade messages

- Use `messages.json` and versioned message files for important installation or migration information.
- Keep messages concise and actionable; do not show routine release advertising.
- Ensure referenced message versions match real release transitions.
- Preserve settings and command/resource aliases only for the explicitly supported migration window.

## Release gate

1. Run pure Python and Sublime integration tests against supported builds/platforms.
2. Reload/disable/enable and restart the package in a clean profile.
3. Validate syntaxes, resources, menus, keymaps, settings, messages, and dependencies.
4. Build/inspect the `.sublime-package` or repository contents.
5. Test installation and upgrade from the previous public version.
6. Validate Package Control metadata/channel tests.
7. Review license, changelog, version tag, and rollback plan.

## Publication boundary

Creating tags/releases, uploading packages, opening a Package Control channel PR, changing hosted repositories, renaming/removing a listing, and transferring ownership are external writes requiring explicit authorization.

## Official sources

- <https://www.sublimetext.com/docs/packages.html>
- <https://packagecontrol.io/docs/submitting_a_package>
- <https://packagecontrol.io/docs/creating_package_files>
- <https://packagecontrol.io/docs/dependencies>
- <https://packagecontrol.io/docs/messaging>
- <https://packagecontrol.io/docs/channels_and_repositories>
