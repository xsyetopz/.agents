# Agents Universal Surface Overstatement

**ID**: `agents-universal-surface-overstatement` | **Category**: `naming-invention`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent turns `.agents/` compatibility into a claim that `.agents/` is the canonical source or root for every generated tool surface.

## Observed failure

- ❌ "`.agents/` is the canonical source of everything."
- ❌ "`.codex/` and `.claude/` are just projections."
- ❌ "The universal intent always flows from `.agents/`."
- ❌ "Generate everything under `.agents/` first."

## Required behavior

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

## Example

- The agent said `.agents/` is the universal source/runtime surface and `.codex/` and `.claude/` are generated projections.

**✅ CORRECT** (shortest path):

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

## Acceptance check

The agent describes placement per artifact class: universal-compatible hooks, skills, and scripts may live in `.agents/` or be symlinked with tool paths as required; tool-specific artifacts stay under their native tool surface.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
