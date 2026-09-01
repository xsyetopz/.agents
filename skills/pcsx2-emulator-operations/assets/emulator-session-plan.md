# PCSX2 session plan

## Objective

- Question or acceptance condition:
- Route: interactive / automated test / regression / capture / debugger / patch / build
- Authorized mutations and external writes:

## Runtime identity

- Date and operator:
- OS, architecture, display server, and container/VM:
- GPU and driver:
- PCSX2 version, channel, package, and source commit:
- Executable path and command:
- Data directory or disposable portable root:

## Console and game identity

- BIOS region, version, and SHA-256:
- Game title, region, serial, and revision:
- Media path/type and SHA-256:
- Track/layout verification result:
- ELF or module identity when applicable:

## Configuration

- Global configuration snapshot or diff:
- Per-game configuration snapshot or diff:
- Renderer, adapter, resolution, and presentation mode:
- CPU mode, cycle rate/skip, frame pacing, and speed mode:
- Patches, cheats, widescreen fixes, texture changes, and enhancements:
- Controller mapping and input source:
- Memory-card fixture and hash:
- Save-state producer version and slot/file, if used:

## Procedure and oracle

- Boot mode: fast / slow / BIOS / disc / ELF / state
- Deterministic input sequence or workload:
- Timeout and checkpoint:
- Expected visual, audio, memory, register, log, or performance result:
- Repetitions and tolerance:

## Runtime investigation

- EE/IOP address space and module/load mapping:
- Static-analysis address or file offset:
- Runtime address and symbol:
- Breakpoint/watchpoint and trigger:
- Registers/memory before and after:
- Hypothesis and falsifying observation:
- Patch or mutation and rollback:

## Evidence and result

- Exit status and duration:
- Log path and relevant timestamps:
- Screenshot/video path:
- GS dump path and renderer used to replay it:
- Configuration and command archive:
- Result: pass / fail / inconclusive
- Deviations, contamination, and follow-up:
