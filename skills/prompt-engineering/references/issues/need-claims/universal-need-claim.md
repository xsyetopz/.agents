# Universal Need Claim Without Evidence

**Merged from**: `need-claim-as-premise`, `universal-need-claim-before-role-trace`, `universal-script-need-claim`, `script-necessity-claim-before-trace`
**Category**: `need-claims`

## Trigger patterns

- Use when: the agent answers a challenge by declaring what "nobody needs" before tracing the artifact, command, or workflow.
- Use when: the agent repeats or adopts a "nobody needs this" claim about an artifact before tracing its observed role, reach, and replacement cost.
- Use when: the agent answers a script role challenge with a blanket claim that nobody needs the script.
- Use when: the agent says a script or command is unnecessary before tracing what it does and who depends on it.

## Bad forms — what this looks like

- ❌ `"Nobody needs this."`
- ❌ `"This is not needed here."`
- ❌ `"I'll remove it."`
- ❌ `"It just does prose."`
- ❌ `"This class of artifact should not exist" before tracing the local artifact.`
- ❌ `"I'll remove its references" before knowing which references are live.`

## Required behavior

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record inputs, outputs, writes, exit behavior, ownership, and reach.
Answer the role question with observed facts first.
Separate these questions: what it does, who uses it, whether the role belongs, and whether this artifact is the right implementati
Recommend deletion only after the trace proves the behavior is unwanted or already covered by a smaller existing route.
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record inputs, outputs, writes, exit behavior, ownership, and reach.
```

## Acceptance checks

- - Need claims do not appear before artifact tracing. - Deletion promises do not appear before caller, output, write, ownership, and reach accounting. - Final reports distinguish user complaint, observed behavior, changed artifacts, command evidence, and remaining unverified claim. - Rejected behavior is not recreated under another filename, command, CI job, install action, or generated artifact.
- Before echoing or making a need claim, the agent can name the artifact, callers, inputs, outputs, exits, user reach, covered claim, duplicate coverage, and uncovered behavior after removal.
- - No script is called unnecessary before role tracing. - Role answers distinguish observed behavior from the edit that follows. - Prose-only automation is not recreated under a different command name. - Final reports state whether the script had install reach, runtime reach, or only local maintenance reach.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
