# DuckStation testing and reproducibility

## Define an observable oracle

Use a bounded claim such as:

- reaches a named screen within a stated time;
- renders a specified scene without the target artifact;
- produces expected register/memory state after a controlled trigger;
- boots a PS-X EXE and reaches a known symbol;
- remains within a declared frame-time or emulated-speed tolerance;
- fails in one pinned build and passes in another.

Write the oracle before running the test.

## Pin the environment

Record:

- DuckStation version/channel/commit and package origin;
- OS, architecture, display stack, GPU, and driver;
- BIOS region/version/hash;
- game serial, region, revision, image format/track layout, and hash;
- global and per-game settings;
- renderer, resolution, CPU mode/overclock, PGXP, timing, and audio settings;
- cheats, runahead/rewind, texture replacement, and enhancements;
- memory-card/save-state fixture and hash;
- input source/sequence;
- boot mode, timeout, checkpoint, repetition count, and tolerance.

Resolve “current preview” to an exact version or commit. It is not a reproducible identifier by itself.

## Baseline procedure

1. Create a copied disposable installation with `portable.txt` next to its executable.
2. Add only the authorized, hashed fixtures needed by the test.
3. Configure logging and perform a short smoke boot.
4. Start with default emulation behavior and no cheats, texture replacement, runahead, rewind, or overclock.
5. Execute the fixed workload and evaluate the declared oracle.
6. Repeat enough times to detect intermittent host or timing noise.
7. Archive the executable/build identity, portable settings, command, fixture hashes, logs, and result together.

## Checkpoint hierarchy

Prefer:

1. normal boot plus deterministic input;
2. copied in-game save on a copied memory card;
3. save state pinned to the exact producing DuckStation build;
4. direct PS-X EXE boot for a purpose-built authorized test program;
5. debugger mutation, clearly labeled as synthetic.

Do not use a state from an unrelated build as the only evidence for a regression.

## Regression procedure

1. Confirm a known-bad and known-good build under identical portable fixtures.
2. Preserve separate data roots or reset the same immutable fixture between every run.
3. Test midpoint revisions using official artifacts where available or source builds from exact commits.
4. Re-test the final adjacent good/bad pair.
5. Inspect the boundary change before attributing root cause.
6. Report the first-bad revision as a localization result, not automatic proof that every change in it is causal.

## Performance and latency

- Keep renderer, display mode, vsync, resolution, audio synchronization, CPU overclock, runahead, rewind, and host power state fixed.
- Separate host frame time, emulated speed, guest frame rate, and input latency.
- Use the same game scene and deterministic input.
- Warm caches consistently or label cold-start measurements.
- Report repeated samples and tolerance, not a single overlay reading.
- Runahead and rewind affect CPU/memory load and must be disabled unless explicitly tested.

## Matrix expansion

Expand one dimension only after a minimal reproduction:

1. emulator revision;
2. renderer/backend and GPU driver;
3. CPU execution mode or overclock;
4. game revision/region/image layout;
5. enhancement, PGXP, or texture replacement;
6. input/controller path.

Avoid a combinatorial settings sweep that cannot explain which variable changed the outcome.

## Classify results

- **Pass:** oracle met with complete pinned evidence.
- **Fail:** oracle not met and the failure evidence is complete.
- **Inconclusive:** timeout ambiguity, fixture contamination, nondeterminism, unpinned build, or missing artifacts prevents a claim.

Normal process exit alone does not establish a pass.
