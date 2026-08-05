# Pattern-Fill Architecture

**ID**: `pattern-fill-architecture` | **Category**: `abstract-reframing`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent fills a product or repository architecture with familiar scaffolding terms instead of staying inside the user's stated constraints.

## Observed failure

- ❌ `"v1"`
- ❌ `"first implementation slice"`
- ❌ `"default profile"`
- ❌ `"power profile"`
- ❌ `"dogfood.yaml"`
- ❌ `"crates are the natural place"`

## Required behavior

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

## Example

The agent completes an architecture from common repo patterns after the user has already corrected the frame

**✅ CORRECT** (shortest path):

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

## Acceptance check

After a correction, the next architecture answer lists only user-stated directories, observed repository facts, and explicitly labelled open questions or proposals. No familiar scaffold term appears unless the response ties it directly to a user statement or current file evidence.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
