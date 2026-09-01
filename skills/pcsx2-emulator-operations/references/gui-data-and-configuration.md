# PCSX2 GUI, data, and configuration

## First-run sequence

1. Install an official stable or nightly package appropriate to the platform.
2. Start the setup wizard and select a legally dumped PlayStation 2 BIOS.
3. Confirm the active data directory before importing memory cards, patches, covers, or per-game settings.
4. Add game directories or open a single authorized image.
5. Configure and test controllers before changing emulation settings.
6. Boot one title with defaults and create a baseline session record.

Official guides:

- Installation and running: <https://pcsx2.net/docs/setup/installation>
- BIOS dumping: <https://pcsx2.net/docs/setup/bios>
- Controllers: <https://pcsx2.net/docs/post-installation/controllers>
- Memory cards: <https://pcsx2.net/docs/post-installation/memory-cards>
- General troubleshooting: <https://pcsx2.net/docs/troubleshooting/general-issues>

## Data ownership

Treat these classes independently:

- global configuration;
- per-game configuration;
- BIOS inventory;
- memory cards and in-game saves;
- emulator save states;
- patches and cheats;
- screenshots, video, logs, and GS dumps;
- covers, cache, and transient data.

Before a destructive or diagnostic change, use the GUI's data-folder action where available, record the resolved directory, and copy the affected files. A portable installation is useful for a self-contained manual lab; `-datapath` is preferable for explicit automated isolation.

## Configuration order

Use one obvious order so causal evidence remains clear:

1. Reset the title to global defaults or record every existing override.
2. Verify BIOS and media identity.
3. Reproduce with default CPU timing and renderer settings.
4. Change one category at a time: renderer, blending/accuracy, CPU mode, timing, audio, input, then enhancements.
5. Prefer a per-game override for title-specific fixes.
6. Annotate every nondefault setting in the session plan.
7. Remove experimental changes after the test or retain them only in the isolated profile.

## BIOS and media

- PCSX2 does not include a BIOS. The user must dump one from hardware they own and comply with applicable law.
- Record BIOS region/version and SHA-256 without publishing the BIOS.
- Keep original disc images read-only during tests.
- Use the game's Properties verification tools where available to validate track/layout integrity.
- Record serial, region, revision, and image hash because different revisions can require different expectations or patches.

## Controllers

- Confirm device identity and host-level input before remapping.
- Keep automatic mapping results separate from manual corrections.
- Record dead zones, sensitivity, pressure behavior, multitap, and device subtype when relevant.
- For repeatable tests, use a deterministic input source and document how it reaches PCSX2; do not assume a physical controller sequence is frame-stable.

## Memory cards and save states

- Copy memory-card fixtures before every automated or destructive run.
- Prefer in-game saves on copied memory cards for long-lived regression entry points.
- Use save states only with the exact producing PCSX2 build and settings unless compatibility has been demonstrated.
- Never overwrite the user's only copy of a save.
- Record card format, slot, game serial, source, and hash.

## Enhancements and per-game fixes

Resolution scaling, deinterlacing, widescreen patches, texture changes, frame-rate patches, cheats, overclocking, cycle changes, and speed controls can invalidate a baseline. Enable them only after default reproduction, one category at a time, and store title-specific changes as per-game configuration where possible.
