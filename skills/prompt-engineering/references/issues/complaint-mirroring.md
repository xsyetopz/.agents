# Complaint Mirroring Cases

**Category:** `complaint-mirroring`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="complaint-as-authorization"></a>

## complaint-as-authorization

**ID**: `complaint-as-authorization`

**Merged from**: `complaint-is-not-authorization`, `complaint-mirroring-into-commitment`, `criticism-to-action-shortcut`
**Category**: `complaint-mirroring`

### Trigger

- Use when: the agent treats a user's frustrated complaint as approval, evidence, or a product decision.
- Use when: the agent repeats the user's critical framing as an implementation commitment before checking facts, ownership, references, or product behavior.
- Use when: the agent responds to a user's criticism by immediately promising a deletion, rewrite, rename, or cleanup before inspecting the artifact's role.

### Observed failure

- ❌ `"I'll remove it."`
- ❌ `"I'll delete the references."`
- ❌ `"Nobody needs this."`
- ❌ `"That is just prose."`
- ❌ `"We should stop using that."`
- ❌ `"I'll replace it with the normal one."`
- ❌ `"Understood, I'll clean it up" when no concrete cleanup was requested.`

### Required behavior

```text
When a user complaint names or implies an artifact:
identify the exact target before promising an action
separate the user's judgment from observed facts
trace callers, readers, writers, outputs, ownership, and installed reach when the target is executable or generated
state what is proven, unproven, or wrong
ask for a choice when several remedies are possible and none was explicitly requested
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When a user complaint names or implies an artifact:
identify the exact target before promising an action
separate the user's judgment from observed facts
```

### Acceptance check

- The first answer to a frustrated artifact complaint separates complaint, fact, and authorization. File changes follow an explicit request or a traced single correct fix.
- - The response starts from evidence, not mirrored phrasing. - Edit commitments name the observed input, output, owner, and install reach. - No file is promised for removal until references and behavior are checked. - Issue reports generalize the behavior without copying hook noise or transcript fragments.
- - A criticized artifact is traced before deletion, replacement, or reference cleanup. - The response states what is known from files or commands and what remains unknown. - Cleanup edits are limited to the behavior the user actually requested. - Similar artifacts are not changed by analogy without their own source check.

<a id="complaint-label-as-fact"></a>

## complaint-label-as-fact

**ID**: `complaint-label-as-fact`

**Merged from**: `complaint-label-as-evidence`, `complaint-term-to-product-claim`
**Category**: `complaint-mirroring`

### Trigger

- Use when: the agent adopts a user's critical wording as a factual artifact classification before inspecting the artifact.
- Use when: the agent converts a user's complaint term into an asserted product fact, then proposes edits from that asserted fact.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

```text
Quote or paraphrase the complaint only as user input, not as artifact fact.
Inspect the artifact before naming its role.
Trace callers, commands, tests, docs, generated output, filesystem writes, install reach, and ownership.
State observed behavior before proposing edits.
Separate artifact role, defect, and patch.
If the artifact should be removed, remove stale references and replacement copies in the same change.
```

### Example

The assistant treated a charged complaint label as the artifact's observed role

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Quote or paraphrase the complaint only as user input, not as artifact fact.
Inspect the artifact before naming its role.
Trace callers, commands, tests, docs, generated output, filesystem writes, install reach, and ownership.
```

### Acceptance check

- - Artifact-role answers cite observed inputs, outputs, callers, writes, ownership, and install reach. - User complaint labels are not reused as factual classifications unless inspection confirms them. - Removal commits do not leave stale references. - The same rejected behavior is not recreated under a new name. - Final reports separate what was observed from what changed.
- - User wording is not copied into product claims without evidence. - Universal need claims do not appear before caller and reach accounting. - Removal proposals include behavior accounting and reference cleanup. - Final reports separate user criticism, observed artifact behavior, changed files, command evidence, and remaining unverified claims.

<a id="complaint-to-utility-verdict"></a>

## complaint-to-utility-verdict

**ID**: `complaint-to-utility-verdict`

**Merged from**: `utility-verdict-from-user-complaint`, `rhetorical-challenge-to-class-policy`, `operational-prompt-complaint-leakage`
**Category**: `complaint-mirroring`

### Trigger

- Use when: the agent repeats a user's complaint as its own conclusion that an artifact, command, field, setting, dependency, or workflow is not needed.
- Use when: the agent turns a user's artifact challenge into a generalized policy about a class of files, scripts, commands, checks, docs, tests, generators, or configs.
- Use when: the assistant drafts instructions for another agent but includes the user’s criticism, frustration, prior failure report, or adversarial commentary that is not needed to execute the task.

### Observed failure

- ❌ `"Nobody needs this" repeated as the agent's conclusion.`
- ❌ `"This is not needed here" before a trace.`
- ❌ `"It just does X" before reading the artifact.`
- ❌ `"Agreed, I'll remove it" as the first response.`
- ❌ `Treating user frustration as authorization, evidence, and design direction at once.`
- ❌ `"I'll remove it and its references."`
- ❌ `"Scripts like this are not needed."`
- ❌ `"This proves the verifier layer should go."`
- ❌ `"No prose scripts."`
- ❌ `"That whole category should not exist."`

### Required behavior

```text
When a user challenges one artifact in language that sounds general:
treat the named artifact as the initial target, not as proof of a class rule
locate exact paths, aliases, commands, and generated outputs
trace callers, writes, exits, install reach, and user-file reach
separate artifact facts from user judgment
state whether the issue is file-specific, pattern-specific, or policy-level
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When a user challenges one artifact in language that sounds general:
treat the named artifact as the initial target, not as proof of a class rule
locate exact paths, aliases, commands, and generated outputs
```

### Acceptance check

- Every utility verdict names the observed behavior and reference trace that support it. Without that trace, the response says what will be inspected instead of declaring whether the artifact belongs.
- Before changing a class of artifacts, the agent can state the exact member list, shared behavior, callers, outputs, product claims, lost coverage, replacement route, and explicit user approval for the class-level change.
- The drafted prompt can stand alone as an operational instruction. Removing the prior conversation does not remove any necessary task information, and the prompt contains no complaint, blame, self-analysis, or negative evaluation unless explicitly requested.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
