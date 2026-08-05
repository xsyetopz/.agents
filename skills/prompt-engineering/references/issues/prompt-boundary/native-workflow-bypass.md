# Native Workflow Bypass

**ID**: `native-workflow-bypass` | **Category**: `prompt-boundary`

## Trigger

Use when: the user requires a host application’s native goal, task, job, workflow, or orchestration feature, but the assistant substitutes an implicit standalone prompt, direct implementation, or its own workflow.

## Bad forms — what this looks like

- ❌ `Telling an agent to review and execute work without instructing it to create a native goal.`
- ❌ `Replacing a named task system with a prose checklist.`
- ❌ `Executing phases directly when the user required separate native goals.`
- ❌ `Treating equivalent task wording as equivalent lifecycle behavior.`

## Required behavior

```text
Treat the named native mechanism as part of the artifact contract. Draft instructions that explicitly create or invoke that mechan
```

## Concrete example

- The user requires the CLI’s native goal feature. The instruction tells the agent to call that feature with the approved goal text rather than merely carrying out the text as an ordinary prompt.

**✅ CORRECT** (shortest path):

```text
Treat the named native mechanism as part of the artifact contract. Draft instructions that explicitly create or invoke that mechan
```

## Acceptance check

The resulting instruction names and uses the required native workflow operation. Execution reports show that work ran inside the requested goal or task lifecycle, and no later phase began outside its own approved native goal.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
