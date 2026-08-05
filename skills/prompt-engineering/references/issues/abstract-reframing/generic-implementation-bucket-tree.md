# Generic Implementation Bucket Tree

**ID**: `generic-implementation-bucket-tree` | **Category**: `abstract-reframing`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent organizes `src/` around generic software buckets instead of the product's domain-specific source responsibilities.

## Observed failure

- ❌ `catalog/`
- ❌ `validation/`
- ❌ `manifest/`
- ❌ `render/`
- ❌ `surfaces/`
- ❌ `registry/`

## Required behavior

```text
When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. sha
```

## Example

- The agent proposed `src/install`, `src/render`, `src/codex`, `src/catalog`, `src/validation`, and `src/manifest`. The user rejected it as a terrible structure.

**✅ CORRECT** (shortest path):

```text
When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. sha
```

## Acceptance check

Each `src/` child has a one-sentence domain responsibility and names what humans author there or what code owns there. If it cannot, it is not proposed.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
