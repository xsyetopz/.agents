# PCSX2 CLI and automation

## Authority and syntax

Use the current official CLI page first, then the parser source for the exact pinned build when behavior differs:

- Official CLI: <https://pcsx2.net/docs/advanced/cli>
- Official source: <https://github.com/PCSX2/pcsx2>

Documented syntax:

```text
pcsx2-qt.exe [parameters] [--] [boot filename]
```

The option terminator `--` is not a help prefix. It ends option parsing so a boot filename beginning with a hyphen is treated as a filename. PCSX2's documented switches below use one leading hyphen. Do not substitute guessed GNU-style forms.

## Documented option inventory

| Option | Argument | Operational meaning |
| --- | --- | --- |
| `-help` | none | Print supported command-line options for that executable. Use only when inspecting a specific installed build. |
| `-version` | none | Print version information and exit. |
| `-batch` | none | Exit PCSX2 when the VM shuts down. |
| `-nogui` | none | Hide the main window and imply batch mode; not a guarantee of displayless rendering. |
| `-portable` | none | Use portable mode and override `-datapath`. |
| `-datapath` | path | Use a specified data directory. Prefer this for isolated automation. |
| `-elf` | file | Boot a PS2 ELF. |
| `-gameargs` | string | Pass arguments to the ELF/game. Preserve it as one process argument. |
| `-disc` | path | Override the disc source while booting another target such as an ELF. |
| `-logfile` | path | Write logging to the specified file. |
| `-bios` | none | Boot the BIOS/system menu. |
| `-fastboot` | none | Skip the BIOS boot sequence. |
| `-slowboot` | none | Use the full BIOS boot sequence. |
| `-state` | index | Load a save-state slot. |
| `-statefile` | filename | Load a specific save-state file. |
| `-fullscreen` | none | Start fullscreen. |
| `-nofullscreen` | none | Prevent fullscreen startup. |
| `-bigpicture` | none | Start the fullscreen/big-picture UI. |
| `-earlyconsolelog` | none | Open console logging early in startup where supported. |
| `-testconfig` | none | Test configuration loading and exit. |
| `-setupwizard` | none | Run the setup wizard. |
| `-debugger` | none | Open the debugger. |
| `-turbo` | none | Start in turbo mode. |
| `-unlimited` | none | Remove the normal speed limiter. |
| `-raintegration` | none | Enable the documented RetroAchievements integration mode. |

Use `scripts/build_command.py` rather than transcribing this table into ad hoc shell code.

## Safe launch patterns

Interactive disc image:

```text
pcsx2-qt.exe -- /absolute/path/game.iso
```

Disposable no-main-window test with explicit data and log paths:

```text
pcsx2-qt.exe -batch -nogui -datapath /tmp/pcsx2-case -logfile /tmp/pcsx2-case/emulog.txt -- /fixtures/game.iso
```

ELF with a separate disc source:

```text
pcsx2-qt.exe -batch -datapath /tmp/pcsx2-case -elf /fixtures/test.elf -disc /fixtures/game.iso
```

Validate an isolated configuration without booting a game:

```text
pcsx2-qt.exe -datapath /tmp/pcsx2-case -testconfig
```

## Isolation procedure

1. Create a fresh writable directory outside the user's normal PCSX2 data directory.
2. Copy only the minimum authorized fixtures: configuration, BIOS, memory card, patch, and input artifacts required by the case.
3. Hash copied fixtures and retain the originals unchanged.
4. Launch with `-datapath <directory>`. Do not combine it with `-portable`; portable mode takes precedence.
5. Use `-logfile` inside the case directory and archive the exact command.
6. Treat files created during the run as outputs, not as trusted future inputs, until reviewed.
7. Delete or archive the disposable directory according to the user's retention requirement.

## No-GUI and CI reality

`-nogui` removes the main PCSX2 window and implies exit-on-shutdown behavior. It does not promise that Qt, the renderer, audio, controller backends, or the host graphics stack can initialize without a session. For CI:

1. Identify the OS, package, display server, GPU access, and chosen renderer.
2. Validate one short boot in the same runner image before scaling the test matrix.
3. Provide a real display, virtual display, or supported software-rendering path as required by that platform.
4. Set an external timeout and terminate the entire process tree on hangs.
5. Preserve the log and crash artifacts even when the process does not exit normally.

Do not label a command “headless” merely because it contains `-nogui`.

## Process-control rules

- Pass arguments as an array from scripts; do not build an unquoted shell string.
- Put `--` immediately before a positional boot path.
- Preserve `-gameargs` as one argument unless the installed build's parser proves otherwise.
- Set an external timeout; PCSX2 has no documented generic timeout flag.
- Capture stdout/stderr and `-logfile` separately when diagnosing startup.
- Record exit code, signal, wall time, and whether VM shutdown or host termination ended the run.
- Never infer pass/fail solely from process exit; use a game-specific checkpoint or artifact.
