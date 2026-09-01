# PCSX2 source builds and versioning

Official sources:

- Repository: <https://github.com/PCSX2/pcsx2>
- Latest release/update: <https://github.com/PCSX2/pcsx2/releases/latest>
- Build documentation: <https://pcsx2.net/docs/development/building>
- Website documentation: <https://pcsx2.net/docs>

## Current version snapshot

As of September 1, 2026, the latest PCSX2 release/update version is **v2.9.9**, released August 31, 2026. Use v2.9.9 when a task asks for the latest version at this snapshot. Re-check the official latest-release endpoint for later work instead of assuming this value remains current.

Always capture the executable's actual `-version` output in test evidence. Do not infer the running version from an old download name, an updater's previous-version field, or a remembered stable release.

## Choose the build path

Use an official binary when the task is operation, configuration, or ordinary reproduction. Build from source when the task requires an exact commit, local instrumentation, a regression bisect, or validating a source change.

Before building, record:

- requested commit/tag and why;
- supported host OS/architecture;
- compiler and build-system versions required by that revision;
- optional components and packaging target;
- dependency source and whether network fetches are permitted;
- expected validation target.

Build instructions and dependencies change. Read the documentation and repository files at the pinned commit; do not copy a command from a different branch or assume a current package layout applies to an older revision.

## Source-build workflow

1. Start from the official repository and verify the requested revision.
2. Read the root contribution/build instructions and platform-specific files at that revision.
3. Configure a separate build directory with an explicit build type.
4. Preserve the complete configure command, compiler identity, dependency revisions, and generated build metadata.
5. Build only the smallest required target first.
6. Run the repository's required unit/static checks for the changed surface.
7. Launch against an isolated PCSX2 data directory; never point an untrusted or instrumented build at the user's normal state first.
8. Record the source commit in every test artifact and issue report.

## Stable, nightly, and local builds

- **Stable:** useful for user-facing baseline and supported release behavior.
- **Nightly/development:** useful for checking current fixes, but pin the exact build rather than writing only “nightly.”
- **Local source build:** useful for bisecting or instrumentation; document toolchain and local diff.

Package behavior can differ across Windows archives/installers, Linux AppImage/Flatpak/distribution packages, and macOS bundles. Resolve executable names, permissions, sandboxed filesystem access, data paths, graphics access, and bundled capture libraries for the actual package.

## Regression build discipline

1. Keep the toolchain and build options fixed across commits when possible.
2. Clean only when evidence suggests stale artifacts; otherwise preserve efficient incremental builds.
3. Do not mix configuration/data directories between builds unless that sharing is part of the test.
4. Keep save states with their producing build.
5. Re-test the final adjacent good/bad commits using a clean build and identical runtime fixtures.
6. Inspect the boundary commit before claiming root cause.

## Local modifications

- Keep instrumentation minimal and reviewable.
- Record a patch/diff and whether it changes timing, memory layout, logging, optimization, or renderer behavior.
- Compare an unmodified build from the same commit.
- Do not redistribute unofficial binaries without reviewing PCSX2's current license obligations and third-party dependency notices.
- Never bundle BIOS or game content.
