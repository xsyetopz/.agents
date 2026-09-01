# PCSX2 testing and reproducibility

## Define a testable claim

Replace “the game works” with one observable claim, for example:

- reaches a named screen within a bounded time;
- renders a specified frame without a known corruption;
- produces expected register or memory state after a deterministic trigger;
- maintains frame time or emulated speed within a stated tolerance;
- does not crash across a fixed workload;
- reproduces in build B and not in build A.

Record the oracle in `assets/emulator-session-plan.md` before running the test.

## Pin the complete environment

At minimum pin:

- PCSX2 version/channel/commit and package origin;
- OS, architecture, display stack, GPU, and driver;
- BIOS region/version/hash;
- game title, serial, region, revision, format, and hash;
- global and per-game configuration;
- renderer, adapter, CPU mode, timing, and speed controls;
- active patches, cheats, fixes, and enhancements;
- memory-card or save-state fixture and hash;
- controller/input source and event sequence;
- boot mode, timeout, checkpoint, repetitions, and tolerance.

“Latest nightly” is not a pin. Resolve it to a build identifier or source commit at test time.

## Baseline procedure

1. Create an isolated data directory with `-datapath`.
2. Populate only the authorized, hashed fixtures needed by the case.
3. Validate configuration loading with `-testconfig` when appropriate.
4. Start with default emulation behavior and no cheats or optional patches.
5. Run a short smoke boot and verify log/artifact collection.
6. Execute the defined workload and evaluate the declared oracle.
7. Repeat enough times to distinguish deterministic failure from intermittent host noise.
8. Archive command, configuration, hashes, logs, result, and deviations together.

## State-fixture hierarchy

Prefer entry points in this order:

1. Normal boot plus deterministic input.
2. Copied in-game save on a copied memory card.
3. A save state produced by and pinned to the exact tested build.
4. Debugger mutation or patched entry point, clearly labeled as a synthetic test.

Save states can encode emulator implementation details and should not be the sole evidence for cross-version compatibility.

## Regression bisect

1. Prove the issue on a known-bad build and absence on a known-good build.
2. Run both with identical immutable fixtures and configuration.
3. Prefer official revisioned builds or build exact commits from source.
4. Test the midpoint and retain the result bundle for every boundary-changing revision.
5. Re-test the final adjacent good/bad pair at least once.
6. Report the first bad commit/build as evidence, not proof of root cause; inspect the change before attributing causality.

## Performance tests

- Warm caches consistently or explicitly measure cold start.
- Separate host frame time, emulated speed, and game-internal timing.
- Disable turbo and unlimited modes unless they are the subject of the test.
- Keep window/fullscreen, vsync, renderer, resolution, audio synchronization, and host power state fixed.
- Report distributions or repeated samples rather than one instantaneous counter.
- Do not compare different scenes, save points, patches, or input paths.

## Test matrix discipline

Start with the smallest discriminating matrix. Expand one dimension at a time:

1. build/version;
2. renderer/backend;
3. hardware adapter/driver;
4. CPU mode or timing setting;
5. game revision/region;
6. enhancement or patch.

Do not multiply every setting combination before identifying which dimension changes the result.

## Result classifications

- **Pass:** the declared oracle was met under the pinned environment.
- **Fail:** the declared oracle was not met and evidence is complete.
- **Inconclusive:** contamination, nondeterminism, missing artifacts, timeout ambiguity, or an unpinned dependency prevents a claim.

Never convert an inconclusive run into a pass because PCSX2 exited normally.
