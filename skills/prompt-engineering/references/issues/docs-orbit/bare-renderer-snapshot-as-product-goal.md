# Bare Renderer Snapshot As Product Goal

**ID**: `bare-renderer-snapshot-as-product-goal` | **Category**: `docs-orbit`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent treats the current minimal renderer output as the intended product instead of a temporary lifecycle exercise.

## Observed failure

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

## Example

- Goal wording implied the current `.codex/config.toml` renderer snapshot was the product boundary.

**✅ CORRECT** (shortest path):

```text
Describe the goal as a control plane for admitted generated surfaces.
Treat the current renderer output as smoke-test content, not destination scope.
Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented.
```

## Acceptance check

Goal and product docs name the intended generated-surface framework and distinguish unimplemented admitted-surface backlog from rejected scope.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
