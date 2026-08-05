# Consent Override

**Merged from**: `user-agency-consent-override`, `negation-is-not-consent`, `question-is-not-authorization`, `goal-prompt-misread-as-authorization`
**Category**: `scope-consent`

## Trigger patterns

- Use when: the agent overrides the user's agency or consent by turning assistant definitions, assumptions, examples, corrections, or proposals into product decisions.
- Use when: the agent treats an explicit no, missing artifact, mismatch, or denial as permission for the opposite action.
- Use when: the agent treats a user question, challenge, or complaint as permission to continue tool work.
- Use when: the user supplies, corrects, or restates goal-prompt text and the agent treats that text as permission to plan, run tools, or edit artifacts.

## Bad forms — what this looks like

- ❌ `"The cleanest shape is..."`
- ❌ `"The product becomes..."`
- ❌ `"This is a first-class..."`
- ❌ `"That means we should add..."`
- ❌ `"The correct abstraction is..."`
- ❌ `"This implies..."`
- ❌ `"So the tree should include..."`
- ❌ `"I would make this top-level..."`
- ❌ `Turning a user definition into a directory.`
- ❌ `Turning a user correction into a renamed assistant frame.`

## Required behavior

```text
When user agency or consent is material, the agent must: 1. Track five separate categories: user-stated requirement, observed repo
```

## Concrete example

The assistant receives a user question or challenge about its behavior, then continues tool calls or implementation as if the question granted permission to proceed

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When user agency or consent is material, the agent must: 1. Track five separate categories: user-stated requirement, observed repo
```

## Acceptance checks

- Before giving an architecture, plan, or file operation answer, the agent can point to each proposed item as one of: 1. directly user-stated, 2. observed in the repository, 3. verified from an external source, 4. an open question, or 5. an explicitly labelled assistant proposal. No item may move from proposal or open question into architecture, naming, generated output, or file edits until the user consents or source evidence requires it. For proposed child files under a user-approved directory, the agent must also identify the source of authority, the concrete artifact or format, the producer, the consumer, and whether the name is accepted or only proposed. If those cannot be answered, record the unresolved design question instead of inventing the file.
- A negative or absent condition produces a stop/report/clarification, not mutation of a different artifact.
- - When the user asks whether work is authorized, the agent answers directly and waits for explicit continuation before additional tool work. - When an interruption asks a question, the agent does not use tool momentum, prior goals, or a self-authored "next move" as permission to continue before answering.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
