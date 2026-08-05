# Bare Renderer Snapshot As Product Goal

**ID**: `bare-renderer-snapshot-as-product-goal` | **Category**: `docs-orbit`

## Trigger

Use when: the agent treats the current minimal renderer output as the intended product instead of a temporary lifecycle exercise.

## Bad forms — what this looks like

- ❌ "The product is just `.codex/config.toml`."
- ❌ `"No hooks, skills, MCP, or templates because the current renderer does not emit them."`
- ❌ `"The current minimal output is the product boundary."`
- ❌ `"Adding real generated files is scope creep."`

## Required behavior

```text
Describe the goal as a control plane for admitted generated surfaces.
Treat the current renderer output as smoke-test content, not destination scope.
Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented.
Require source routing, renderer support, manifest ownership, removal behavior, and dogfood evidence before each surface is genera
```

## Concrete example

- Goal wording implied the current `.codex/config.toml` renderer snapshot was the product boundary.

**✅ CORRECT** (shortest path):

```text
Describe the goal as a control plane for admitted generated surfaces.
Treat the current renderer output as smoke-test content, not destination scope.
Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented.
```

## Acceptance check

Goal and product docs name the intended generated-surface framework and distinguish unimplemented admitted-surface backlog from rejected scope.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
