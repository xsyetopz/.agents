# DuckStation GUI, data, and configuration

Official repository and user documentation:

- Repository/README: <https://github.com/stenzek/duckstation>
- Wiki: <https://github.com/stenzek/duckstation/wiki>

## Frontends

DuckStation's desktop application provides a Qt desktop frontend and a fullscreen/TV-oriented interface. Use the desktop GUI for setup, library maintenance, per-game properties, debugging, and detailed diagnosis. Use the fullscreen UI for controller-driven operation after the baseline is configured.

## First-run sequence

1. Install an official stable or preview package for the platform.
2. Add a legally dumped PlayStation BIOS and record its region/version/hash.
3. Confirm the active data directory before importing saves, states, cheats, textures, or covers.
4. Add authorized game directories or open a single image.
5. Configure and test the controller.
6. Boot one game with defaults and record a baseline before enabling enhancements.

## Data directories

Current documented defaults include:

- Windows: the DuckStation directory under the user's local application-data location; older installs can retain a Documents-based directory.
- Linux: `$XDG_DATA_HOME/duckstation` or `~/.local/share/duckstation` when `XDG_DATA_HOME` is unset.
- macOS: `~/Library/Application Support/DuckStation`.
- Portable desktop install: data beside the application when `portable.txt` exists next to the executable.

Use **Tools > Open Data Directory** where available to resolve the actual active location. Never infer it solely from the OS because upgrades and portable installs can change the result.

## Data classes

Treat independently:

- global settings;
- per-game settings;
- BIOS inventory;
- memory cards and in-game saves;
- emulator save states;
- cheats and patches;
- screenshots and media captures;
- texture dumps and replacements;
- logs, cache, covers, and transient data.

Copy mutable fixtures before testing. Avoid synchronizing an active data tree while DuckStation is running.

## Configuration order

1. Record or reset per-game overrides.
2. Verify BIOS and image identity/track layout.
3. Reproduce using defaults.
4. Change one category at a time: renderer/display, CPU execution, timing/audio, input, then enhancements.
5. Store title-specific behavior in per-game settings.
6. Record each nondefault option in the session plan.
7. Restore the clean profile after experiments.

## BIOS and media

- DuckStation does not ship a BIOS. Use a BIOS dumped from hardware the user owns in accordance with applicable law.
- Record BIOS region/version and SHA-256, but never publish the file.
- Keep source images read-only.
- Prefer cue/bin or another format preserving track layout when the game depends on multiple tracks; verify the actual format support of the pinned build.
- Record game serial, region, revision, and image hash.

## Memory cards and save states

- Copy memory cards before tests and destructive operations.
- Prefer in-game saves on copied cards as durable cross-version checkpoints.
- Keep per-game/shared-card behavior explicit; changing card topology can alter the test.
- Pin save states to the exact build that created them unless compatibility is demonstrated.
- Never overwrite the user's only save or card.

## Enhancements

Internal resolution, PGXP options, texture filtering, widescreen behavior, overclocking, runahead, rewind, cheats, and texture replacement can alter compatibility and timing. Establish a default baseline, then enable one category at a time. Do not describe an enhanced result as default emulation behavior.

## Platform boundaries

Desktop Windows, Linux, and macOS packages do not necessarily share paths, graphics backends, permissions, capture codecs, or controller behavior. Android has a separate application lifecycle and storage/UI model; inspect its current official instructions rather than applying desktop steps unchanged.
