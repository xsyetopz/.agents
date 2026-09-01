# PCSX2 debugging, reverse engineering, and patches

Official references:

- Debugger: <https://pcsx2.net/docs/advanced/debugger>
- Writing patches: <https://pcsx2.net/docs/advanced/writing-patches>

## Scope

PCSX2 can provide dynamic evidence for lawful compatibility research, game testing, modding, bug diagnosis, and decompilation projects: disassembly, registers, memory, symbols, breakpoints, runtime mutations, and dumps. A static decompiler, source reconstruction project, asset pipeline, and build-matching process remain separate. Never imply that an emulator debugger automatically produces a correct decompilation.

## Debugger workflow

1. Pin the PCSX2 build, game revision/hash, BIOS, and test state.
2. Enable the debugger through the documented GUI/configuration path or launch with `-debugger` where supported.
3. Select the correct processor context:
   - R5900 / Emotion Engine (EE) for primary PS2 code;
   - R3000 / IOP for I/O processor code.
4. Establish module and ELF load addresses before mapping static symbols.
5. Import or define symbols only from authorized project artifacts and verify a few known functions/data objects against runtime behavior.
6. Set the smallest breakpoint or watchpoint that can falsify the hypothesis.
7. Record trigger conditions, thread/processor context, registers, memory, call path, and relevant instructions before mutation.
8. Change one register, byte range, instruction, or function behavior at a time.
9. Re-run from a clean checkpoint to distinguish persistent behavior from debugger contamination.

## Address mapping

Always label addresses with their domain:

- disc/image file offset;
- ELF virtual address;
- EE virtual/physical address;
- IOP address;
- host process address;
- GS-local or other device memory when applicable.

Record the transformation between domains. Do not paste a host pointer into a static project as though it were a PS2 virtual address. Account for overlays, relocations, dynamically loaded modules, and revision differences.

## Evidence useful to decompilation

- observed function entry/return and caller/callee relationships;
- live argument and return registers;
- stack-frame and global-data behavior;
- branch outcomes under controlled inputs;
- memory layouts, object lifetimes, and state transitions;
- timing or coprocessor behavior not obvious from static code;
- imported symbols and labels validated against execution.

For each observation, retain the game hash, checkpoint, address domain, trigger, and PCSX2 build. One execution path does not prove behavior for all inputs.

## PNACH patches and cheats

Keep baseline fixes, optional enhancements, and cheats distinct:

- built-in/game-index patches may supply compatibility or quality-of-life behavior;
- the patches location is used for patch files and built-in patch archives according to current PCSX2 packaging;
- the cheats location is for user cheat behavior;
- PNACH identity is tied to game serial and ELF CRC, so confirm both before applying a patch.

Patch procedure:

1. Reproduce without the patch.
2. Record the original bytes/value and exact address domain.
3. Generate or edit the PNACH through documented PCSX2 tooling or a reviewed text file.
4. Enable it only for the intended game identity.
5. Confirm the log reports the expected patch and no unintended patch set.
6. Re-run the same oracle and check adjacent behavior for regressions.
7. Retain a rollback: disable/remove the patch and restore the original fixture.

Never use a patch to conceal a baseline emulator regression. Label experimental patches and avoid distributing copyrighted replacement content.

## Function stubbing and runtime mutation

Function stubbing and direct memory/register edits are high-contamination techniques. Use them only to isolate causality:

1. capture the unmodified failing run;
2. state the predicted result of the mutation;
3. apply one reversible mutation;
4. observe both expected and unexpected effects;
5. restart from a clean state and repeat;
6. remove the mutation before drawing a baseline compatibility conclusion.

## Safety

- Debug only software and systems the user is authorized to inspect.
- Do not extract or distribute proprietary code, BIOS content, protected assets, secrets, or private online-service data.
- Avoid networked or anti-cheat environments unless the user has explicit authorization and the risk is understood.
- Keep research notes and symbols revision-specific; do not assume addresses transfer between regional or revision variants.
