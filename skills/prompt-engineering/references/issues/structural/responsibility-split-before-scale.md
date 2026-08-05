# Responsibility Split Before Scale

**ID**: `responsibility-split-before-scale` | **Category**: `structural`

## Trigger

Use when: the agent keeps adding behavior to already-large modules, CLIs, renderers, generators, or config files during a broad expansion instead of first separating responsibilities.

## Bad forms — what this looks like

- ❌ `Adding more renderer logic to an already oversized CLI file.`
- ❌ `Combining comparison, design, migration, and validation in one edit loop.`
- ❌ `Using one core module for parsing, rendering, file IO, validation, and reporting.`
- ❌ `Deferring the split until after another broad feature pass.`

## Required behavior

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

## Concrete example

- A template generator CLI already contains parsing and rendering, and the agent adds multiple language presets there instead of splitting renderer ownership.

**✅ CORRECT** (shortest path):

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

## Acceptance check

New broad-scope behavior lands in a file whose responsibility is named and bounded, or the agent reports that a split is needed before more implementation. Large multipurpose files are not expanded further without explicit authorization and a stated reason.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
