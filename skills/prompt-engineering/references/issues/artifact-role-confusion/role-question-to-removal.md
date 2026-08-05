# Role Question → Removal Promise

**Merged from**: `role-question-evasion`, `role-challenge-to-removal-promise`, `role-question-to-unsupported-removal`, `removal-as-role-answer`, `deletion-promise-as-explanation`, `role-question-to-action-commitment`, `diagnosis-question-to-remedy`
**Category**: `artifact-role-confusion`

## Trigger patterns

- Use when: the agent answers "why does this exist?" with an edit promise instead of explaining the artifact's observed role.
- Use when: the agent answers "why does this exist?" by promising removal before tracing observed behavior.
- Use when: the agent answers "why does this exist?" by agreeing to remove the artifact before tracing its role.
- Use when: the agent answers an artifact-role question by promising removal instead of first stating what the artifact does and where it reaches.

## Bad forms — what this looks like

- ❌ `"I'll remove it."`
- ❌ `"Nobody needs this."`
- ❌ `"It just polices prose."`
- ❌ `"That script is unnecessary."`
- ❌ `"I'll remove the file and its references" before checking references.`
- ❌ `"A script like this is not needed here" before tracing behavior.`
- ❌ `"I'll remove it and its references."`
- ❌ `"It is just a prose script."`
- ❌ `"That script is not needed here."`
- ❌ `"I'll clean it up" before showing role and reach.`

## Required behavior

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record observed inputs, outputs, writes, exit behavior where applicable, ownership, and user-visible reach.
Answer the role question with observed facts first.
Separate three decisions: whether the role is real, whether the role belongs, and whether the artifact is the right implementation
Commit to deletion, movement, or reduction only after the trace proves that edit.
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record observed inputs, outputs, writes, exit behavior where applicable, ownership, and user-visible reach.
```

## Acceptance checks

- - Responses to role questions start with observed facts. - Edit promises follow a role audit, not the emotional force of the question. - Cleanup commits identify whether each touched file was live behavior or residue. - Issue reports generalize the failure without preserving hook output or transcript noise.
- - Role answers name observed inputs, outputs, callers, and install reach before promising edits. - Removal changes do not leave stale references. - Cleanup does not recreate the same behavior elsewhere. - Final reports separate "what existed" from "what changed."
- The first answer to an artifact-role question contains observed role, reach, and evidence gaps. Any edit commitment comes after that accounting.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
