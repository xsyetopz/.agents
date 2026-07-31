# Artifact Naming Without Domain Contract

**ID**: `artifact-naming-without-domain-contract` | **Category**: `naming-invention`

## Trigger

Use when: the agent invents file, schema, command, or directory names before proving the artifact has a domain role, producer, consumer, and accepted source format.

## Bad forms — what this looks like

- ❌ `render-plan.schema.json`
- ❌ `external-tool.schema.json`
- ❌ `docs-provider.schema.json`
- ❌ `"schema for runtime things"`
- ❌ `"schema for shared tools"`
- ❌ `Naming files from broad nouns such as provider, runtime, plan, catalog, or manifest without a concrete contract.`

## Required behavior

```text
Before naming a schema, command, config file, manifest, or generated artifact, the agent must identify: 1. the exact source artifa
```

## Concrete example

- The agent proposed `render-plan.schema.json` after the user asked for dry-run generated artifacts, even though the user had not named a render-plan concept.

**✅ CORRECT** (shortest path):

```text
Before naming a schema, command, config file, manifest, or generated artifact, the agent must identify: 1. the exact source artifa
```

## Acceptance check

Every proposed artifact name can be traced to user wording, current repo source, upstream format, or an explicitly marked open proposal with producer and consumer named.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
