# Memory Scope Pollution

**ID**: `memory-scope-pollution` | **Category**: `memory-state`

## Trigger

Use when: the assistant saves or proposes saving project-specific, task-specific, account, hardware, repository, path, or personal facts as persistent memory instead of limiting memory to stable communication preferences explicitly requested by the user.

## Bad forms — what this looks like

- ❌ `Saving repository names, paths, branches, or implementation decisions as user memory.`
- ❌ `Saving hardware inventories, subscriptions, identities, or account details as communication preferences.`
- ❌ `Treating a long project recap as permission to create persistent memory.`
- ❌ `Inferring and saving preferences without an explicit memory request.`

## Required behavior

```text
Save memory only when the user explicitly asks. Limit saved content to stable preferences about how the assistant should communica
```

## Concrete example

- A user asks the assistant to remember that replies should be concise and evidence-first. The saved entry contains that communication preference only, not the repository, hardware, or project details discussed nearby.

**✅ CORRECT** (shortest path):

```text
Save memory only when the user explicitly asks. Limit saved content to stable preferences about how the assistant should communica
```

## Acceptance check

A memory audit shows only explicitly requested, stable communication preferences. No project-specific, task-specific, path, hardware, subscription, identity, or other personal facts appear in saved memory.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
