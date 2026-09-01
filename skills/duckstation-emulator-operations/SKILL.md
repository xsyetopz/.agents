---
name: duckstation-emulator-operations
description: Operate and investigate DuckStation for PlayStation emulation. Use for desktop/fullscreen UI, exact CLI and no-GUI launches, portable game testing, integrated or GDB-assisted runtime analysis, textures, captures, troubleshooting, and source builds; not for standalone static decompilation or PlayStation 2 emulation.
---

## Start with evidence

1. Identify the requested outcome: interactive play, configuration, repeatable test, regression check, capture, integrated/remote debugger session, texture experiment, issue report, or source build.
2. Record the platform, DuckStation executable/package, exact release/preview version or commit, and whether the run may touch the user's existing data directory.
3. Establish game identity before changing settings: title, region, serial, revision, image format, track layout, and a local hash when reproducibility matters.
4. Establish legal provenance. DuckStation requires a BIOS dumped from the user's own console and authorized game media. Never retrieve or redistribute copyrighted firmware, game images, keys, protected assets, or proprietary code.
5. Resolve the active DuckStation data directory and inventory global and per-game settings, memory cards, save states, cheats, texture replacements, logs, screenshots, videos, and debugger settings. Back up or copy mutable state before testing.
6. For automation, use a disposable copied installation containing `portable.txt` beside the executable, or another platform-isolated user environment. DuckStation does not document a general `-datapath` option; never invent one.
7. Treat the current command-line wiki and parser source for the exact installed build as authoritative. Options use a single leading hyphen. Never invent `--help`, `--headless`, `--config`, `--datapath`, or switches borrowed from another emulator.
8. Distinguish `-nogui` from displayless/headless execution: it disables the main window and exits on shutdown, but Qt, rendering, audio, and host display/GPU backends may still need initialization.

## Workflow

1. Choose one route and read only its referenced guide before acting:
   - Desktop/fullscreen UI, data directories, BIOS, controllers, memory cards, and per-game settings: `references/gui-data-and-configuration.md`
   - Exact CLI, no-GUI launches, portable isolation, and automation: `references/cli-and-automation.md`
   - Deterministic game tests, regression checks, and test matrices: `references/testing-and-reproducibility.md`
   - Integrated/remote debugging, GDB, PCDrv, runtime evidence, and reverse-engineering support: `references/debugging-and-reverse-engineering.md`
   - Logging, screenshots, media capture, texture dumps/replacements, crash evidence, and issue reports: `references/capture-textures-and-troubleshooting.md`
   - Building DuckStation, pinning revisions, packaging, source licensing, and version-sensitive behavior: `references/build-source-and-versioning.md`
2. Create a session record from `assets/emulator-session-plan.md` for any test, investigation, or report that must be repeated.
3. Prefer GUI configuration for one-off interactive use and exact CLI launches for controlled runs. Keep global settings, per-game overrides, command-line behavior, and temporary debugger changes separate.
4. Generate commands with `scripts/build_command.py`; it emits documented options, inserts `--` before a positional boot path, rejects contradictory combinations, and never executes DuckStation.
5. Pin the emulator build, BIOS identity, game identity, portable data root, renderer, CPU mode, enhancements, cheats, memory-card/save-state fixture, input sequence, and expected checkpoint.
6. Establish a clean baseline before enabling enhancements, cheats, overclocking, runahead/rewind, texture replacement, PGXP options, debugging facilities, or runtime mutations.
7. For reverse engineering, map executable/file offsets and console runtime addresses explicitly. Use DuckStation's integrated or remote debugger as dynamic evidence, not as a replacement for a controlled static decompilation project.
8. Capture the smallest artifacts proving the result: exact command, configuration delta, hashes, log excerpt, screenshot/video, texture dump, debugger observation, or good/bad revision pair.
9. Restore or discard the disposable portable copy after the run. Do not silently copy test state into the user's normal data directory.

## Validation

1. Run `python3 scripts/test_build_command.py` from this skill directory.
2. Run the repository skill-structure validator when available and require the folder name, frontmatter name, and four OWO sections to pass.
3. Inspect every generated command and confirm each emulator switch appears in `references/cli-and-automation.md` for the pinned build.
4. Reproduce operational acceptance from a clean disposable portable copy or explain why that isolation is impossible.
5. For a regression, verify at least one known-good and one known-bad build using identical BIOS, game media, settings, fixtures, and input.
6. For debugger or reverse-engineering claims, record address domain, trigger, register/memory evidence, source build, and rollback.
7. For reports or shared artifacts, inspect for copyrighted content, private paths, account data, credentials, and unrelated user state before requesting authorization to upload.

## Boundaries

- Do not download, request, extract, or distribute BIOS files, game images, keys, protected assets, proprietary symbols, or copyrighted code without authorization and a lawful basis.
- Do not claim `-nogui` is true headless/displayless mode. Explicitly validate any virtual display, GPU passthrough, or software-rendering arrangement used in CI.
- Do not guess command-line switches or use options from a different emulator. Inspect the exact DuckStation version's official wiki/source if the documented interface and installed build differ.
- Do not use save states as durable cross-version fixtures. Prefer copied memory cards and in-game saves for long-lived tests; pin save states to the producing build.
- Do not modify the user's normal settings, cards, saves, cheats, textures, or game files when a copied portable installation can satisfy the task.
- Do not enable enhancements, cheats, runahead, rewind, overclocking, texture replacement, or debugger mutations in a baseline unless explicitly under test.
- Do not package, redistribute, or publish modified DuckStation builds without reviewing the repository's current license and third-party notices; its source distribution terms are not the same as this skill's license.
- Do not publish reports, upload logs/captures, modify upstream repositories, or perform other hosted writes without explicit user authorization.
