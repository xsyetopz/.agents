# Scratch Space Overdesign

**ID**: `scratch-space-overdesign` | **Category**: `naming-invention`

## Trigger

Use when: the agent predesigns internal layout for gitignored build or scratch directories without a real command lifecycle owning that layout.

## Bad forms — what this looks like

- ❌ `.build/previews/`
- ❌ `.build/targets/`
- ❌ `.build/eval-runs/`
- ❌ `"logs" as a proposed tree item without retention rules.`
- ❌ `Naming scratch children from lifecycle nouns before command behavior exists.`

## Required behavior

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

## Concrete example

- The agent proposed `.build/previews`, `.build/targets`, and `.build/eval-runs` without showing the commands that produce or consume those paths.

**✅ CORRECT** (shortest path):

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

## Acceptance check

Every scratch subdirectory in a proposal has an owning command, producer, consumer, retention rule, and cleanup behavior. Otherwise only the scratch root is named.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
