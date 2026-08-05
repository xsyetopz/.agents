# Complaint as Authorization

**Merged from**: `complaint-is-not-authorization`, `complaint-mirroring-into-commitment`, `criticism-to-action-shortcut`
**Category**: `complaint-mirroring`

## Trigger patterns

- Use when: the agent treats a user's frustrated complaint as approval, evidence, or a product decision.
- Use when: the agent repeats the user's critical framing as an implementation commitment before checking facts, ownership, references, or product behavior.
- Use when: the agent responds to a user's criticism by immediately promising a deletion, rewrite, rename, or cleanup before inspecting the artifact's role.

## Bad forms — what this looks like

- ❌ `"I'll remove it."`
- ❌ `"I'll delete the references."`
- ❌ `"Nobody needs this."`
- ❌ `"That is just prose."`
- ❌ `"We should stop using that."`
- ❌ `"I'll replace it with the normal one."`
- ❌ `"Understood, I'll clean it up" when no concrete cleanup was requested.`

## Required behavior

```text
When a user complaint names or implies an artifact:
identify the exact target before promising an action
separate the user's judgment from observed facts
trace callers, readers, writers, outputs, ownership, and installed reach when the target is executable or generated
state what is proven, unproven, or wrong
ask for a choice when several remedies are possible and none was explicitly requested
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When a user complaint names or implies an artifact:
identify the exact target before promising an action
separate the user's judgment from observed facts
```

## Acceptance checks

- The first answer to a frustrated artifact complaint separates complaint, fact, and authorization. File changes follow an explicit request or a traced single correct fix.
- - The response starts from evidence, not mirrored phrasing. - Edit commitments name the observed input, output, owner, and install reach. - No file is promised for removal until references and behavior are checked. - Issue reports generalize the behavior without copying hook noise or transcript fragments.
- - A criticized artifact is traced before deletion, replacement, or reference cleanup. - The response states what is known from files or commands and what remains unknown. - Cleanup edits are limited to the behavior the user actually requested. - Similar artifacts are not changed by analogy without their own source check.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
