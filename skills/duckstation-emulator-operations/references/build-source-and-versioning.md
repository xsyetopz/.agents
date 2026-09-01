# DuckStation source builds and versioning

Primary source:

- Repository, README, license, and platform build instructions: <https://github.com/stenzek/duckstation>

## Choose the build path

Use an official stable or preview package for ordinary operation and user-facing reproduction. Build from source for exact-commit tests, instrumentation, regression bisection, or validating a code change.

Before building, record:

- exact commit/tag and purpose;
- host OS/architecture and supported compiler/toolchain;
- CMake/preset/dependency requirements at that revision;
- frontend and packaging target;
- whether dependency downloads are authorized;
- smallest build and validation target that proves the outcome.

DuckStation's build commands and dependencies change. Read the README and checked-in build files at the pinned revision. Do not paste current commands into an old revision or assume one platform's dependencies apply to another.

## Source-build workflow

1. Use the official repository and verify the requested revision.
2. Read the revision's README, license, dependency, and platform build sections.
3. Configure a separate build directory/preset with explicit build type and architecture.
4. Preserve configure command, compiler identity, SDK/dependency revisions, and local options.
5. Build the smallest required desktop target first.
6. Run the repository's required checks for the changed surface.
7. Copy the resulting application into a disposable directory and enable portable mode with `portable.txt` for runtime tests.
8. Record source commit and local diff with every artifact.

## Releases and previews

- **Stable:** preferred user-facing baseline.
- **Preview/development:** useful for current fixes; resolve it to an exact build/commit.
- **Local build:** appropriate for bisecting/instrumentation; preserve toolchain and diff.

Windows, Linux, and macOS packages can differ in executable location, runtime libraries, Qt packaging, graphics backends, permissions, capture support, and data-directory behavior. Validate the actual artifact rather than treating builds as interchangeable.

## Regression builds

1. Hold toolchain/build options fixed across commits when feasible.
2. Use separate portable data roots or reset an immutable fixture for each run.
3. Keep save states paired with their producing build.
4. Re-test the final adjacent good/bad revisions using clean builds.
5. Inspect the first-bad change before claiming root cause.
6. Distinguish a source regression from a packaging, dependency, driver, or stale-data difference.

## Licensing and redistribution

The DuckStation repository currently publishes source under project-specific terms identified in its license file and README, including noncommercial/no-derivatives constraints in current releases. Treat those current repository files as authoritative because terms can change.

- Do not copy DuckStation source into this skill.
- Do not distribute modified source or binaries, preconfigured packages, or derivative releases without a license review.
- Preserve required notices for any authorized redistribution.
- Review third-party dependency and resource licenses independently.
- Never bundle BIOS files, game images, saves containing copyrighted content, or protected assets.

Local building and testing authorization does not automatically authorize redistribution.
