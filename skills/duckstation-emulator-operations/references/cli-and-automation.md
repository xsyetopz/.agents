# DuckStation CLI and automation

## Authority and syntax

Use the official command-line wiki, then inspect the parser source for the exact pinned revision when behavior differs:

- Command-line wiki: <https://github.com/stenzek/duckstation/wiki/Command-Line-Arguments>
- Current Qt parser source: <https://github.com/stenzek/duckstation/blob/master/src/duckstation-qt/qthost.cpp>
- Official repository: <https://github.com/stenzek/duckstation>

Documented syntax:

```text
duckstation-qt [parameters] [--] [boot filename]
```

The exact executable suffix varies by platform/package. The `--` token ends option parsing; it is not the prefix used by DuckStation's documented options. Do not translate single-hyphen options into guessed double-hyphen forms.

## Documented option inventory

| Option | Argument | Operational meaning |
| --- | --- | --- |
| `-help` | none | Print supported command-line options for the installed executable. Use only for exact-version inspection. |
| `-version` | none | Print version information and exit. |
| `-batch` | none | Exit when emulation stops instead of returning to the UI. |
| `-fastboot` | none | Skip the BIOS boot animation/sequence. |
| `-slowboot` | none | Use the full BIOS boot sequence. |
| `-bios` | none | Boot the BIOS/system menu. |
| `-resume` | none | Resume the most recent state according to current DuckStation behavior. |
| `-state` | index | Load a save-state slot. |
| `-statefile` | filename | Load a specific save-state file. |
| `-exe` | filename | Boot a PS-X executable directly. |
| `-fullscreen` | none | Start fullscreen. |
| `-nofullscreen` | none | Prevent fullscreen startup. |
| `-nogui` | none | Disable the main window and exit on shutdown; not a displayless guarantee. |
| `-bigpicture` | none | Start the fullscreen/TV-oriented UI. |
| `-earlyconsole` | none | Open/attach console logging early where supported. |
| `--` | none | Stop option parsing; remaining token is the boot filename. |

There is no documented general `-datapath`, `--headless`, generic timeout, or arbitrary config-file switch. Do not invent one.

## Safe launch patterns

Interactive image boot:

```text
duckstation-qt -- /absolute/path/game.cue
```

No-main-window batch boot from a disposable portable copy:

```text
/tmp/duckstation-case/duckstation-qt -batch -nogui -- /fixtures/game.cue
```

Direct PS-X executable boot:

```text
duckstation-qt -batch -exe /fixtures/test.exe
```

Specific state file:

```text
duckstation-qt -batch -statefile /fixtures/checkpoint.sav
```

Use `scripts/build_command.py` to construct these forms without executing them.

## Portable isolation

DuckStation's desktop builds support portable mode by placing an empty `portable.txt` beside the executable. There is no documented CLI data-path override, so use this one obvious automation pattern:

1. Copy an official DuckStation package into a fresh writable case directory.
2. Create `portable.txt` next to that copied executable.
3. Start the copied executable once if required to create the data tree, then stop it.
4. Copy only the minimum authorized BIOS, settings, memory card, state, cheat, or texture fixture into the portable data tree.
5. Hash all fixtures and leave originals untouched.
6. Run the copied executable by absolute path and archive its exact version/commit.
7. Collect logs and outputs from the copied portable tree.
8. Delete or archive the whole case directory after review.

Do not create `portable.txt` in the user's normal installation unless they explicitly want to convert that installation's storage behavior.

## No-GUI and CI reality

`-nogui` suppresses the primary frontend window and arranges exit when emulation stops. It does not prove that Qt, graphics, audio, input, or the selected renderer can initialize without a desktop session. For CI:

1. Use the same package and runner image intended for the suite.
2. Validate a short smoke boot with the selected display/GPU arrangement.
3. Supply a real display, virtual display, GPU passthrough, or supported software path as platform requirements dictate.
4. Apply an external timeout and terminate the complete process tree on hangs.
5. Preserve early console output, the DuckStation log, and crash artifacts.

Call this “no-GUI” unless the complete host arrangement has been proven displayless.

## Process-control rules

- Pass arguments as an array rather than concatenating an unquoted shell command.
- Insert `--` immediately before a positional image path.
- Do not combine `-fastboot` and `-slowboot`, or `-fullscreen` and `-nofullscreen`.
- Keep `-state` and `-statefile` mutually exclusive in automation.
- Set timeout and retry behavior in the harness; DuckStation has no documented generic timeout switch.
- Record process exit code/signal and distinguish guest shutdown from forced host termination.
- Evaluate a game-specific oracle; a zero exit code is not proof that gameplay or rendering is correct.
