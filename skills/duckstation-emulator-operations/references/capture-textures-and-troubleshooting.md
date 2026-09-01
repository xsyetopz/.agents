# DuckStation capture, textures, and troubleshooting

Primary references:

- Logging wiki: <https://github.com/stenzek/duckstation/wiki/Enabling-Logging>
- Texture replacement wiki: <https://github.com/stenzek/duckstation/wiki/Texture-Replacement>
- Resource overrides wiki: <https://github.com/stenzek/duckstation/wiki/Resource-Overrides>
- Repository/README: <https://github.com/stenzek/duckstation>

## Evidence-first diagnosis

1. Record exact build, host, BIOS, game revision/hash, settings, and checkpoint.
2. Preserve one reproduction with the user's current settings.
3. Reproduce from a disposable portable profile with defaults.
4. Verify image format and track layout.
5. Disable cheats, textures, overlays, runahead, rewind, and nondefault enhancements.
6. Change one likely causal category at a time.
7. For regressions, find a known-good/known-bad build pair.

## Logging

Current documented GUI flow uses advanced settings to choose log level and output destination, including system console and file output. Menu labels can evolve; confirm them in the pinned build.

For diagnosis:

- use a debug-level log only for the shortest reproduction needed;
- enable early console output with `-earlyconsole` when diagnosing startup on a supported platform;
- preserve startup through failure with timestamps;
- record the active portable/normal data root;
- disable verbose logging after the run because it can affect timing and expose paths;
- redact private paths/account data without removing relevant warnings.

## Screenshots and media capture

- Capture the smallest sequence showing the expected and actual behavior.
- Record renderer, internal resolution, aspect ratio, post-processing, PGXP, and whether output is an emulator capture or host screen recording.
- Media capture availability and codecs can depend on platform, package, and build. Inspect the pinned build instead of assuming a fixed encoder set.
- For timing issues, retain original frame cadence where practical and include the input timeline.

## Texture dumping and replacement

Texture replacement is an enhancement workflow, not a clean compatibility baseline.

1. Confirm the exact game serial/revision and use an isolated portable profile.
2. Enable texture dumping only for the bounded scene needed.
3. Record relevant dump settings and prevent unbounded disk growth.
4. Hash dumped files and preserve naming/layout metadata.
5. Create replacements without embedding content the user lacks rights to redistribute.
6. Enable replacement loading and test one asset class at a time.
7. Compare against a disabled-replacement baseline.
8. Record VRAM/disk/performance impact and mipmap/alpha/color-space behavior.
9. Package only original or properly licensed replacement assets.

Texture naming and cache behavior are version-sensitive; follow the current wiki/source for the pinned build.

## Resource overrides

Resource overrides can change fonts, icons, shaders, or other frontend/runtime resources depending on current support. Keep overrides in a disposable profile, document every file and hash, and remove them before reporting a baseline defect. Never replace signed/application resources in place when the supported data-directory override mechanism can be used.

## Crash and hang triage

- Distinguish guest crash, emulation stop, frontend crash, renderer/device loss, deadlock, and external timeout.
- Preserve exit code/signal, console output, DuckStation log, OS crash report, and last checkpoint.
- Record whether emulation, audio, rendering, UI, or the entire process stopped.
- Re-test without third-party overlays, injection tools, texture packs, cheats, and advanced timing features.
- Re-test with defaults before blaming a driver or game image.

## Issue-report bundle

Include only authorized data:

- concise expected/actual behavior and exact steps;
- exact DuckStation version/commit and package;
- host OS/CPU/GPU/driver/display stack;
- BIOS region/version/hash, never the BIOS file;
- game serial/region/revision/image hash, never the image;
- settings diff, cheats, textures, and enhancements;
- logs, screenshots, minimal video, crash report, or debugger evidence;
- known-good/bad builds for regressions;
- result from a clean disposable portable profile.

Review current project issue/support policy and obtain explicit authorization before uploading anything.
