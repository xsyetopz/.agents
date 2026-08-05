# Agents Universal Surface Overstatement

**ID**: `agents-universal-surface-overstatement` | **Category**: `naming-invention`

## Trigger

Use when: the agent turns `.agents/` compatibility into a claim that `.agents/` is the canonical source or root for every generated tool surface.

## Bad forms — what this looks like

- ❌ "`.agents/` is the canonical source of everything."
- ❌ "`.codex/` and `.claude/` are just projections."
- ❌ "The universal intent always flows from `.agents/`."
- ❌ "Generate everything under `.agents/` first."

## Required behavior

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

## Concrete example

- The agent said `.agents/` is the universal source/runtime surface and `.codex/` and `.claude/` are generated projections.

**✅ CORRECT** (shortest path):

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

## Acceptance check

The agent describes placement per artifact class: universal-compatible hooks, skills, and scripts may live in `.agents/` or be symlinked with tool paths as required; tool-specific artifacts stay under their native tool surface.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
