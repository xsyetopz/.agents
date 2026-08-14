# Need Claims Cases

**Category:** `need-claims`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="universal-need-claim"></a>

## universal-need-claim

**ID**: `universal-need-claim`

**Merged from**: `need-claim-as-premise`, `universal-need-claim-before-role-trace`, `universal-script-need-claim`, `script-necessity-claim-before-trace`
**Category**: `need-claims`

### Trigger

- Use when: the agent answers a challenge by declaring what "nobody needs" before tracing the artifact, command, or workflow.
- Use when: the agent repeats or adopts a "nobody needs this" claim about an artifact before tracing its observed role, reach, and replacement cost.
- Use when: the agent answers a script role challenge with a blanket claim that nobody needs the script.
- Use when: the agent says a script or command is unnecessary before tracing what it does and who depends on it.

### Observed failure

- ❌ `"Nobody needs this."`
- ❌ `"This is not needed here."`
- ❌ `"I'll remove it."`
- ❌ `"It just does prose."`
- ❌ `"This class of artifact should not exist" before tracing the local artifact.`
- ❌ `"I'll remove its references" before knowing which references are live.`

### Required behavior

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record inputs, outputs, writes, exit behavior, ownership, and reach.
Answer the role question with observed facts first.
Separate these questions: what it does, who uses it, whether the role belongs, and whether this artifact is the right implementati
Recommend deletion only after the trace proves the behavior is unwanted or already covered by a smaller existing route.
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Inspect the artifact before naming its role.
Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces.
Record inputs, outputs, writes, exit behavior, ownership, and reach.
```

### Acceptance check

- - Need claims do not appear before artifact tracing. - Deletion promises do not appear before caller, output, write, ownership, and reach accounting. - Final reports distinguish user complaint, observed behavior, changed artifacts, command evidence, and remaining unverified claim. - Rejected behavior is not recreated under another filename, command, CI job, install action, or generated artifact.
- Before echoing or making a need claim, the agent can name the artifact, callers, inputs, outputs, exits, user reach, covered claim, duplicate coverage, and uncovered behavior after removal.
- - No script is called unnecessary before role tracing. - Role answers distinguish observed behavior from the edit that follows. - Prose-only automation is not recreated under a different command name. - Final reports state whether the script had install reach, runtime reach, or only local maintenance reach.

<a id="utility-verdict-skip"></a>

## utility-verdict-skip

**ID**: `utility-verdict-skip`

**Merged from**: `utility-verdict-before-inventory`, `script-challenge-to-unsupported-purpose-verdict`, `script-purpose-assertion-without-trace`, `single-script-challenge-to-category-verdict`
**Category**: `need-claims`

### Trigger

- Use when: the agent declares that nobody needs a script, command, CI job, package task, generator, or helper before inventorying its role.
- Use when: the agent answers a script challenge by declaring what the script is for and what should happen to it before tracing the script.
- Use when: the agent asserts what a script is "only" for from a user challenge, then promises deletion or cleanup before tracing the script.
- Use when: the agent treats one challenged script as evidence that a whole script category, command family, verifier layer, or maintenance route should be removed.

### Observed failure

- ❌ `"Nobody needs this."`
- ❌ `"This is just a prose script."`
- ❌ `"I'll remove it and its references."`
- ❌ `"This command is unnecessary" before tracing callers.`
- ❌ `"A script like this is not needed here" before inventorying project role.`
- ❌ `"I'll replace it with a cleaner command" before showing what behavior must survive.`
- ❌ `"I'll remove it."`
- ❌ `"It just polices prose."`
- ❌ `"I'll remove the script and its references."`
- ❌ `"A script like this should not exist."`

### Required behavior

```text
Before any utility verdict, inventory:
command entrypoints
direct callers
package, CI, install, release, smoke, and maintenance reach
files read
files written
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before any utility verdict, inventory:
command entrypoints
direct callers
```

### Acceptance check

- Every utility verdict is preceded by an artifact inventory. The final action names the observed behavior being removed, preserved, narrowed, or replaced.
- Before stating a purpose verdict or removal plan, the agent can name the exact script, aliases, callers, inputs, reads, writes, deletes, outputs, exit behavior, user-file reach, supported claim, lost coverage, and authorization for the proposed action.
- - Script-role answers name observed callers and outputs. - Removal commits do not leave stale command references. - Documentation-only gates are not recreated under another script or installer action. - Final explanations separate "what it did" from "what changed."
