# Generic Implementation Bucket Tree

**ID**: `generic-implementation-bucket-tree` | **Category**: `abstract-reframing`

## Trigger

Use when: the agent organizes `src/` around generic software buckets instead of the product's domain-specific source responsibilities.

## Bad forms — what this looks like

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

## Concrete example

- The agent proposed `src/install`, `src/render`, `src/codex`, `src/catalog`, `src/validation`, and `src/manifest`. The user rejected it as a terrible structure.

**✅ CORRECT** (shortest path):

```text
When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. sha
```

## Acceptance check

Each `src/` child has a one-sentence domain responsibility and names what humans author there or what code owns there. If it cannot, it is not proposed.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
