# Appeasement Loop

**Merged from**: `appeasement-edit-before-role-answer`, `role-challenge-appeasement-loop`, `role-label-to-file-plan`
**Category**: `artifact-role-confusion`

## Trigger patterns

- Use when: the agent answers an artifact-role question with agreement and an edit promise before stating what the artifact actually does.
- Use when: the agent answers "why does this artifact exist?" by agreeing, labeling the artifact, claiming nobody needs it, and promising an edit before tracing behavior.
- Use when: the agent accepts a negative role label for an artifact and answers with a file plan before tracing the artifact.

## Bad forms — what this looks like

- ❌ `"I'll remove it."`
- ❌ `"Agreed, this is unnecessary."`
- ❌ `"Nobody needs this."`
- ❌ `"It just polices prose."`
- ❌ `"I'll remove the file and references."`
- ❌ `"A script like this is not needed here."`
- ❌ `"This is just prose tooling."`
- ❌ `"That file is bloat."`
- ❌ `"The script is unnecessary."`
- ❌ `"I'll remove the file and its references" before checking references.`

## Required behavior

```text
When a user challenges why an artifact exists:
locate the exact artifact and likely aliases
read it before naming its role
trace direct references and command paths
identify reads, writes, generated output, exit behavior, and user-file reach
name the current claim or workflow it supports
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When a user challenges why an artifact exists:
locate the exact artifact and likely aliases
read it before naming its role
```

## Acceptance checks

- The first response to an artifact-role question contains role and reach facts before any edit promise. If facts are not known yet, the agent says what it will inspect, not what it will delete.
- For any challenged artifact, the agent first reports observed behavior and reach. Only then may it propose deletion, retention, relocation, or replacement.
- Before giving a file plan, the agent can state the exact artifact, aliases, callers, reads, writes, outputs, exits, user-file reach, supported claim, uncovered claim after removal, and whether the user explicitly requested the operation.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
