# Responsibility Split Before Scale

**ID**: `responsibility-split-before-scale` | **Category**: `structural`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent keeps adding behavior to already-large modules, CLIs, renderers, generators, or config files during a broad expansion instead of first separating responsibilities.

## Observed failure

- ❌ `Adding more renderer logic to an already oversized CLI file.`
- ❌ `Combining comparison, design, migration, and validation in one edit loop.`
- ❌ `Using one core module for parsing, rendering, file IO, validation, and reporting.`
- ❌ `Deferring the split until after another broad feature pass.`

## Required behavior

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

## Example

- A template generator CLI already contains parsing and rendering, and the agent adds multiple language presets there instead of splitting renderer ownership.

**✅ CORRECT** (shortest path):

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

## Acceptance check

New broad-scope behavior lands in a file whose responsibility is named and bounded, or the agent reports that a split is needed before more implementation. Large multipurpose files are not expanded further without explicit authorization and a stated reason.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
