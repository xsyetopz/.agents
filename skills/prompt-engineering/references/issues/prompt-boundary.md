# Prompt Boundary Cases

**Category:** `prompt-boundary`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="full-source-application-downgrade"></a>

## full-source-application-downgrade

**ID**: `full-source-application-downgrade` | **Category**: `prompt-boundary`

### Trigger

Use when: the agent is told to fully apply a named prompt guide, issue corpus, spec, policy, or source, but treats it as optional inspiration or applies only visible concepts.

### Observed failure

- ❌ `I applied some concepts from the guide.`
- ❌ `I mostly followed it.`
- ❌ `I used the spirit of the prompt guide.`
- ❌ `The visible concepts are covered.`
- ❌ `Full application is approximated by these rules.`
- ❌ `Completing a subset and calling it done.`

### Required behavior

```text
Treat explicit words such as "full", "fully", "literal", "complete", and "according to the guide" as hard scope constraints.
Read the named source before acting.
Extract the source's required structure, target surfaces, stop rules, output contract, and acceptance criteria.
Map each required source element to the exact artifact category the user requested.
Do not replace source requirements with familiar concepts, summaries, or partial approximations.
```

### Example

- A prompt guide defines Role, Personality, Goal, Success criteria, Constraints, Output, and Stop rules; the agent copies only outcome-first and validation language.

**✅ CORRECT** (shortest path):

```text
Treat explicit words such as "full", "fully", "literal", "complete", and "according to the guide" as hard scope constraints.
Read the named source before acting.
Extract the source's required structure, target surfaces, stop rules, output contract, and acceptance criteria.
```

### Acceptance check

Before reporting completion, the agent can point to every required element from the named source and show where it was applied, intentionally not applicable, or blocked. No completion claim uses partial-application language when the user requested full application.

<a id="named-readme-workflow-bypass"></a>

## named-readme-workflow-bypass

**ID**: `named-readme-workflow-bypass` | **Category**: `prompt-boundary`

### Trigger

Use when: the user names a README, template, generator workflow, or external guide as the authority, but the agent inspects unrelated files, copies or hand-rolls scaffold, runs unrelated checks, or substitutes its own workflow instead of following the named source literally.

### Observed failure

- ❌ `Reading template internals after being told to read only README.md.`
- ❌ `Manually creating a scaffold when the README documents a generator command.`
- ❌ `Running checks in the template repo when the user asked to use the workflow on a different repo.`
- ❌ `Treating 'use this README' as permission to copy files.`
- ❌ `Treating a correction as permission to start writing files.`

### Required behavior

```text
When the user names a README or guide, read that source before inspecting adjacent files unless the source itself directs further
Respect explicit bounds such as "read only the README", "do not copy files", or "use the generator workflow".
Identify the authoritative workflow described by the source before acting.
Preserve the requested artifact category: generator workflow means run the generator, not hand-roll equivalent files; read means r
Do not run extra checks, create files, or inspect generated output unless the user asked or the documented workflow requires it fo
```

### Example

- User points to a Rust template README for workspace setup; the agent inspects template Cargo files instead of reading the README.

**✅ CORRECT** (shortest path):

```text
When the user names a README or guide, read that source before inspecting adjacent files unless the source itself directs further
Respect explicit bounds such as "read only the README", "do not copy files", or "use the generator workflow".
Identify the authoritative workflow described by the source before acting.
```

### Acceptance check

The action trace starts with the named source, not adjacent artifacts. Every command or edit is either directly requested by the user or required by the named workflow for the target repo. No copied template files, manual scaffold, unrelated validation, or internal-template inspection appears when the user constrained the source to the README.

<a id="native-workflow-bypass"></a>

## native-workflow-bypass

**ID**: `native-workflow-bypass` | **Category**: `prompt-boundary`

### Trigger

Use when: the user requires a host application’s native goal, task, job, workflow, or orchestration feature, but the assistant substitutes an implicit standalone prompt, direct implementation, or its own workflow.

### Observed failure

- ❌ `Telling an agent to review and execute work without instructing it to create a native goal.`
- ❌ `Replacing a named task system with a prose checklist.`
- ❌ `Executing phases directly when the user required separate native goals.`
- ❌ `Treating equivalent task wording as equivalent lifecycle behavior.`

### Required behavior

```text
Treat the named native mechanism as part of the artifact contract. Draft instructions that explicitly create or invoke that mechan
```

### Example

- The user requires the CLI’s native goal feature. The instruction tells the agent to call that feature with the approved goal text rather than merely carrying out the text as an ordinary prompt.

**✅ CORRECT** (shortest path):

```text
Treat the named native mechanism as part of the artifact contract. Draft instructions that explicitly create or invoke that mechan
```

### Acceptance check

The resulting instruction names and uses the required native workflow operation. Execution reports show that work ran inside the requested goal or task lifecycle, and no later phase began outside its own approved native goal.

<a id="prompt-boundary-and-intent-interpretation"></a>

## prompt-boundary-and-intent-interpretation

**ID**: `prompt-boundary-and-intent-interpretation` | **Category**: `prompt-boundary`

### Trigger

Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

#### Assumption Over Prompt ```diff - The assistant substitutes inferred intent for literal user text

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

### Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
