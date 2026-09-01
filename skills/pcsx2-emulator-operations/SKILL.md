---
name: pcsx2-emulator-operations
description: Operate and investigate PCSX2 for PlayStation 2 emulation. Use for GUI, exact CLI and no-GUI launches, isolated game testing, debugger or PNACH-assisted runtime analysis, captures, troubleshooting, and source builds; not for standalone static decompilation or PlayStation 1 emulation.
---

## Start with evidence

1. Identify the requested outcome: interactive play, configuration, repeatable test, regression bisect, capture, debugger session, patch experiment, issue report, or source build.
2. Record the platform, PCSX2 executable/package, exact version or commit, installation mode, and whether the run may touch the user's existing data directory.
3. Establish the game identity before changing settings: title, region, serial, revision, media format, and a locally computed hash when reproducibility matters.
4. Establish legal provenance. PCSX2 does not ship a PlayStation 2 BIOS; use only a BIOS and game media the user is authorized to dump and use. Never retrieve or redistribute copyrighted firmware or game content.
5. Locate the active PCSX2 data directory and inventory relevant settings, per-game overrides, memory cards, save states, patches, cheats, logs, screenshots, and dumps. Back up or copy mutable state before testing.
6. For automation, choose an isolated data path or disposable portable copy. Never use the user's primary memory cards, save states, or configuration as test fixtures.
7. Treat the documented CLI and the source for the exact installed build as authoritative. PCSX2 options use a single leading hyphen. Never invent `--help`, `--headless`, `--config`, or similarly guessed switches, and do not run help probes as a substitute for reading the documented interface.
8. Distinguish `-nogui` from a truly displayless process: it hides the main window and implies batch mode, but emulation and rendering can still require a graphics/display backend.

## Workflow

1. Choose one route and read only its referenced guide before acting:
   - GUI setup, folders, BIOS, controllers, memory cards, per-game settings: `references/gui-data-and-configuration.md`
   - Exact CLI, no-GUI launches, isolation, and automation: `references/cli-and-automation.md`
   - Deterministic game tests, regression checks, and test matrices: `references/testing-and-reproducibility.md`
   - Debugger-assisted reverse engineering, symbols, memory inspection, and PNACH work: `references/debugging-reverse-engineering-and-patches.md`
   - Logs, screenshots, video, GS dumps, diagnosis, and issue evidence: `references/capture-artifacts-and-troubleshooting.md`
   - Building PCSX2, pinning revisions, packaging differences, and version-sensitive behavior: `references/build-source-and-versioning.md`
2. Create a session record from `assets/emulator-session-plan.md` for any test, investigation, or report that must be repeatable.
3. Prefer GUI configuration for one-off interactive use and exact CLI launches for repeatable runs. Keep global settings, per-game settings, command-line overrides, and temporary experiments separate in the record.
4. Generate automation commands with `scripts/build_command.py`; it emits documented options, inserts `--` before a positional boot path, rejects contradictory combinations, and never starts PCSX2.
5. Pin the emulator build, BIOS identity, game identity, data directory, renderer, CPU mode, speed controls, patches/cheats, memory-card or save-state fixture, input sequence, and expected checkpoint.
6. Establish a clean baseline before enabling enhancements, patches, cheats, widescreen fixes, texture replacements, overclocking, frame-rate changes, or debugger mutations.
7. For reverse engineering, keep static-analysis addresses and runtime PCSX2 addresses explicitly mapped. Use the emulator debugger and dumps as dynamic evidence; do not present emulator observations as a complete decompilation workflow.
8. Capture the smallest artifacts that prove the result: command, configuration delta, hashes, log excerpt, screenshot/video, debugger observation, GS dump, or good/bad revision pair.
9. Restore or discard isolated state after the run. Do not silently promote a test setting, patch, memory card, or save state into the user's normal setup.

## Validation

1. Run `python3 scripts/test_build_command.py` from this skill directory.
2. Run the repository skill-structure validator when available and require the folder name, frontmatter name, and four OWO sections to pass.
3. For a generated command, inspect the rendered argument order and confirm every emitted emulator switch appears in `references/cli-and-automation.md` for the pinned build.
4. For an operational task, reproduce the expected checkpoint from a clean isolated data directory or explain why isolation is impossible.
5. For a regression claim, verify at least one known-good and one known-bad build with the same BIOS, game image, settings, fixtures, and input sequence.
6. For a patch or debugger claim, preserve the original value, runtime address space, trigger condition, observed result, and rollback path.
7. For an issue report, confirm that logs and dumps correspond to the failing run and contain no private paths, account data, copyrighted content, or unrelated user state beyond what the user approved.

## Boundaries

- Do not download, request, extract, or distribute BIOS files, game images, keys, decrypted assets, proprietary symbols, or copyrighted code without authorization and a lawful basis.
- Do not claim `-nogui` is equivalent to headless/displayless operation. If CI has no display or GPU, explicitly provide and validate the platform-specific virtual-display or software-rendering setup.
- Do not guess CLI flags or carry options over from another emulator. If the installed version differs from the referenced interface, inspect that version's official documentation or source before constructing a command.
- Do not use save states as durable cross-version fixtures. Prefer in-game saves or memory-card copies for long-lived tests; save states are build-sensitive and must remain pinned to their producing version.
- Do not alter the user's normal configuration, memory cards, saves, patches, or game files when an isolated data directory or copied fixture can satisfy the task.
- Do not enable patches, cheats, enhancements, speed modes, or nondefault timing for a baseline unless the test explicitly targets them.
- Do not conflate PCSX2's experimental PlayStation 1 mode with supported PlayStation 2 operation.
- Do not publish issue reports, upload dumps, modify upstream repositories, or perform other hosted writes without explicit user authorization.
