# PCSX2 capture, artifacts, and troubleshooting

Official references:

- General issues: <https://pcsx2.net/docs/troubleshooting/general-issues>
- Diagnosing problems: <https://pcsx2.net/docs/troubleshooting/diagnosing-problems>
- GS dump runner: <https://pcsx2.net/docs/advanced/gs-dump-runner>

## Evidence-first diagnosis

1. Record the exact failing build, host, BIOS, game revision/hash, settings, and checkpoint.
2. Reproduce once with existing settings and preserve the artifacts.
3. Reproduce from an isolated default configuration.
4. Verify the disc image/track layout through PCSX2's game-properties verification where available.
5. Change one likely causal category at a time.
6. If it is a regression, find a known-good/known-bad pair before broad setting experiments.

## Logs

- Enable file logging through the documented Tools action or launch with `-logfile <path>`.
- Default installations commonly place emulator logs under the active data directory, including `logs/emulog.txt`; resolve the actual path for the pinned package rather than assuming it.
- Capture startup through failure, including timestamps and the command/configuration used.
- Do not reboot another title before collecting volatile or overwritten evidence.
- Redact private filesystem names and account identifiers, but do not remove warnings or context needed to understand the failure.

## Screenshots and video

- Capture the smallest sequence that shows the checkpoint and defect.
- Record renderer, internal resolution, aspect ratio, deinterlacing, post-processing, and whether the image came from PCSX2 capture or host screen capture.
- Video-capture support can depend on package-provided FFmpeg libraries and the PCSX2 build; verify the installed build rather than assuming codecs or menu entries.
- For timing bugs, include an input timeline and avoid re-encoding that destroys frame cadence when practical.

## GS dumps

A GS dump records graphics-synthesizer activity for focused rendering reproduction. Current documented capture paths include the Tools action and the Shift+F8 shortcut for a single-frame dump, with output normally under the active data directory's `snaps` area.

Procedure:

1. Reproduce at the exact bad frame with a clean baseline.
2. Capture the smallest useful GS dump; large or long dumps can be costly and may contain game-derived data.
3. Record PCSX2 build, renderer, game serial/revision/hash, settings, and screenshot of expected versus actual output.
4. Replay with the official GS dump runner on the same build first.
5. Change one renderer/accuracy setting at a time during replay.
6. Treat successful replay on another build as evidence, not proof that full-game execution is fixed.
7. Review content and obtain authorization before uploading; dumps can include copyrighted game data.

## Crash and hang triage

- Distinguish guest crash, VM shutdown, frontend crash, renderer/device loss, deadlock, and external timeout.
- Preserve exit code/signal, stdout/stderr, emulator log, OS crash report, and the last known checkpoint.
- For hangs, record whether emulated time, audio, rendering, UI, or the whole process stopped.
- Re-test without third-party overlays, injection tools, custom texture packs, cheats, or patches.
- Re-test a default renderer/configuration before attributing a host driver issue.

## Issue-report bundle

Include only authorized evidence:

- concise title and expected/actual result;
- exact reproduction steps;
- PCSX2 version/build or commit;
- host OS/CPU/GPU/driver/display stack;
- BIOS region/version/hash, never the BIOS file;
- game serial/region/revision/hash, never the game image;
- settings diff and active patches;
- logs, screenshots, minimal video, crash report, or GS dump as appropriate;
- known-good and known-bad builds for regressions;
- whether a clean isolated configuration reproduces.

Do not upload or publish the bundle without explicit authorization.
