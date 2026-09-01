# DuckStation debugging and reverse-engineering support

Primary sources:

- Repository/README: <https://github.com/stenzek/duckstation>
- Current settings/source tree: <https://github.com/stenzek/duckstation/tree/master/src>

## Scope

DuckStation provides integrated and remote debugging facilities useful for lawful compatibility work, homebrew testing, bug diagnosis, and decompilation research. It can supply runtime disassembly, registers, memory, breakpoints, symbols, TTY output, and controlled execution evidence. Static analysis, matching source reconstruction, asset analysis, and build tooling remain separate disciplines.

## Evidence setup

1. Pin DuckStation version/commit, BIOS, game or PS-X EXE hash, and portable data root.
2. Establish the executable's load address, module boundaries, and runtime checkpoint.
3. Use a copy of every memory-card/state fixture.
4. Enable only the minimum debugger features needed.
5. Record all settings that can change execution, especially CPU mode, overclock, cheats, PGXP, runahead, and rewind.

## Integrated debugger workflow

1. Open the debugger through the documented UI for the pinned build.
2. Verify the current program counter against known boot/module code.
3. Import or define only authorized symbols and validate a few known labels against runtime behavior.
4. Set the narrowest breakpoint or watchpoint that can falsify the hypothesis.
5. Capture pre-trigger registers, memory, call context, and relevant instructions.
6. Trigger using a repeatable input/workload.
7. Capture post-trigger state and unexpected side effects.
8. Restart from a clean checkpoint before repeating or applying a mutation.

## Remote GDB workflow

Current DuckStation source exposes GDB-server settings including enablement and port. These interfaces are version-sensitive; verify the exact build's settings/source rather than assuming a fixed menu path or port.

1. Bind to loopback by default and choose an unused local port.
2. Do not expose a debugger endpoint to an untrusted network.
3. Start DuckStation with the intended game/EXE and clean checkpoint.
4. Connect a GDB client configured for the emulated MIPS target and the exact executable/symbol set.
5. Verify target architecture, byte order, register mapping, and one known symbol before trusting breakpoints.
6. Record server settings, client version, symbol file/hash, breakpoint commands, and observed state.
7. Disable the server after the session.

Debugger protocol support can evolve. Treat the current source and a successful capability handshake as the oracle, not a remembered command list.

## Address domains

Label every address as one of:

- image/file offset;
- PS-X EXE virtual address;
- emulated CPU virtual/physical address;
- scratchpad, BIOS, or device address;
- host-process pointer.

Document transformations and account for overlays, dynamically loaded code, regional revisions, and executable differences. Never import a host pointer into a static project as a console address.

## PCDrv and TTY

DuckStation source includes PCDrv and TTY-related debugging controls. These are especially useful for authorized homebrew/test executables:

- use PCDrv only with a dedicated host directory containing non-sensitive fixtures;
- treat guest-controlled paths and filenames as untrusted;
- keep host write access read-only where possible;
- capture TTY output with timestamps and the exact executable hash;
- do not expose private source trees or credentials through a shared host path.

Verify setting names and behavior against the pinned source revision before enabling them.

## Dynamic evidence for decompilation

Useful observations include:

- live argument/return registers and stack usage;
- branch decisions under controlled inputs;
- object layouts and state transitions;
- caller/callee relationships and indirect targets;
- DMA/device interaction and timing-sensitive behavior;
- runtime validation of imported symbols.

Record the trigger, address domain, game revision/hash, emulator build, and whether any cheat, patch, or mutation was active. One observed path does not prove all possible behavior.

## Runtime mutation safety

1. Capture an unmodified baseline.
2. State a falsifiable prediction.
3. Change one register, memory range, instruction, or breakpoint action.
4. Observe expected and unintended effects.
5. restart from a clean state and repeat.
6. Remove the mutation before making compatibility claims.

Do not use debugging facilities to bypass access controls, attack services, extract protected content, or inspect software without authorization.
