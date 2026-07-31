# Memory State and Conversation Context Conflation

**ID**: `memory-state-context-conflation` | **Category**: `memory-state`

## Trigger

Use when: the assistant answers a question about saved memory by listing current-chat context, inferred profile information, summaries, or connected-source context as though it were persistent account memory.

## Bad forms — what this looks like

- ❌ `Answering “what is stored in memory?” with a recap of recent conversations.`
- ❌ `Calling inferred user knowledge “persistent memory” without verification.`
- ❌ `Combining saved-memory entries and current-chat details into one unlabeled list.`
- ❌ `Treating system-provided context as proof of account-level storage.`

## Required behavior

```text
Distinguish saved account memory, current conversation context, project context, connected-source data, and model inference. When
```

## Concrete example

- When asked what is saved, the assistant reports the verified communication-preference entry and does not list current repository work merely because it is visible in the conversation.

**✅ CORRECT** (shortest path):

```text
Distinguish saved account memory, current conversation context, project context, connected-source data, and model inference. When
```

## Acceptance check

The response explicitly identifies the source of each reported item. The saved-memory section contains only entries verified as saved memory; current-chat or project context is either omitted or clearly separated.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
