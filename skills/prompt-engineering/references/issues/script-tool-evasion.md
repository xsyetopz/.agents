# Script Tool Evasion Cases

**Category:** `script-tool-evasion`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="script-challenge-to-removal"></a>

## script-challenge-to-removal

**ID**: `script-challenge-to-removal`

**Merged from**: `script-role-question-removal-reflex`, `label-and-delete-script-response`, `prose-script-label-to-deletion`, `prose-script-response-pattern`
**Category**: `script-tool-evasion`

### Trigger

- Use when: the agent receives a question about why a script exists and answers with removal, relabeling, or agreement before tracing what the script does.
- Use when: the agent answers a script role question by labeling the script from the user's complaint and promising removal before tracing behavior.
- Use when: the agent turns a challenged script, command, or automation step into a prose-only artifact and promises deletion before tracing behavior.
- Use when: the agent responds to a challenged script by describing it as prose machinery and promising removal before proving what the script does.

### Observed failure

- ❌ `"I'll remove the script and its references."`
- ❌ `"Nobody needs this script."`
- ❌ `"It just polices prose."`
- ❌ `"That command is unnecessary."`
- ❌ `"I'll delete it" before finding callers.`
- ❌ `"I'll replace it with a cleaner check" before proving the current behavior and the replacement behavior.`
- ❌ `"I'll remove it."`
- ❌ `"It is just a prose script."`
- ❌ `"Nobody needs this."`
- ❌ `"A script like this is not needed here."`

### Required behavior

```text
For a challenged script, trace these facts before any commitment:
direct command references
package, CI, install, release, and smoke paths
files read
files written
command output
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
For a challenged script, trace these facts before any commitment:
direct command references
package, CI, install, release, and smoke paths
```

### Acceptance check

- The first response to a script-role question contains observed role and reach. Any edit promise comes after the trace, not before it.
- - Script-role answers do not adopt complaint labels as fact. - Deletion is never promised before behavior accounting. - If a script is removed, no package command, doc, CI job, installer, or smoke path still points to it. - Final reports separate observed role, defect, changed files, and remaining unverified claims.
- - No script, command, or automation step is called prose-only before role tracing. - User complaint wording is not reused as factual classification unless inspection confirms it. - Removal includes caller and reference cleanup. - Any preserved behavior has an observed owner and path. - Final reports distinguish changed artifacts, command evidence, source evidence, and remaining unverified claims.

<a id="script-complaint-to-policy"></a>

## script-complaint-to-policy

**ID**: `script-complaint-to-policy`

**Merged from**: `prose-script-complaint-to-tooling-policy`, `prose-check-command-challenge-response`
**Category**: `script-tool-evasion`

### Trigger

- Use when: the agent treats a user's complaint about a prose-oriented script as permission to decide repository tooling policy before tracing the script and the product claim it is supposed to prove.
- Use when: the agent answers a challenge about a prose-check command by agreeing with the complaint and promising removal before tracing command behavior and references.

### Observed failure

- ❌ `"I'll remove the script and its references."`
- ❌ `"Nobody needs a prose script."`
- ❌ `"A script that just polices doc prose is not needed here."`
- ❌ `"We should remove prose checks" before tracing callers.`
- ❌ `"The script is only documentation hygiene" before reading the script.`
- ❌ `"I'll replace it with a better check" before naming the product behavior being checked.`

### Required behavior

```text
Read the command implementation before naming its role.
Trace references from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files.
Record command inputs, outputs, writes, exit codes, ownership assumptions, and user-visible reach.
Separate four questions: what the command does, who calls it, whether that behavior belongs, and whether this command is the right
If the behavior is only prose policing and was not requested, remove the command and every caller/reference in one change.
If part of the behavior proves runtime or install behavior, preserve that behavior through the smallest existing route and remove
```

### Example

The assistant responded to a challenge about `verify.mjs` by saying it would remove the script and its references because the script "just polices doc prose." That answer failed in two ways: - It accepted the complaint label as the command's role before inspecting behavior

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Read the command implementation before naming its role.
Trace references from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files.
Record command inputs, outputs, writes, exit codes, ownership assumptions, and user-visible reach.
```

### Acceptance check

- The first answer to a prose-script complaint names the observed artifact, its reach, and the product claim it proves or fails to prove. Tooling changes come after that accounting.
- - A prose-check command is not removed or defended before behavior and references are traced. - Complaint wording is treated as user feedback, not command evidence. - Deletion commits include caller/reference cleanup. - Runtime, install, smoke, CI, and release behavior are not removed accidentally. - Final reports name the changed artifacts, observed command evidence, and any remaining unverified claim.

<a id="script-purpose-without-trace"></a>

## script-purpose-without-trace

**ID**: `script-purpose-without-trace`

**Merged from**: `prose-script-certainty-before-trace`, `script-role-collapse`, `script-removal-without-runtime-accounting`, `script-burden-of-proof`, `prose-script-contract-before-action`
**Category**: `script-tool-evasion`

### Trigger

- Use when: the agent answers a script role question by declaring the script to be prose tooling before tracing observed behavior.
- Use when: the agent treats a challenged script as removable prose tooling before tracing its actual role.
- Use when: the agent promises to remove a challenged script before tracing its runtime behavior, callers, outputs, ownership, and replacement needs.
- Use when: the agent adds, keeps, removes, or promises to remove a script before proving why that script belongs in the repository at all.

### Observed failure

- ❌ `"I'll remove it" as the first response to "why is this here?"`
- ❌ `"Nobody needs a prose script" before tracing callers and outputs.`
- ❌ `"It just polices docs" before reading the script.`
- ❌ `Adding a command so the final report can list a check.`
- ❌ `Wiring a prose-heavy command into release or install paths.`
- ❌ `Deleting a challenged script without naming the product claim it was supposed to prove.`
- ❌ `"I'll remove the script."`
- ❌ `"Nobody needs a prose script."`
- ❌ `"It just polices doc prose."`
- ❌ `"I'll remove its references" before tracing references.`

### Required behavior

```text
Before adding a script:
name the product behavior it will exercise
name the real input and output
name the caller or command that will own it
explain why direct inspection or an existing test is insufficient
keep it out of install, update, remove, release, and smoke paths unless it exercises those paths Before removing a challenged scri
```

### Example

The assistant responded to "why is this script here?" by immediately saying it would remove the script and by repeating the user's label as the script's purpose: - It called the script a prose script before reading it

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before adding a script:
name the product behavior it will exercise
name the real input and output
```

### Acceptance check

- - A script is not called a prose script until its behavior is traced. - A deletion promise never appears before caller/output/write/install accounting. - Role answers distinguish observed behavior from proposed edits. - Prose-policing automation is not recreated under a different filename, package command, CI job, or install action. - Final reports include changed artifact, source evidence, observed command evidence, and remaining unverified claim.
- - Script cleanup starts with a role trace. - Removal patches include reference cleanup for command surfaces that called the script. - Documentation-only gates are not moved to another command under a new name. - The final report states whether the script had user-facing install reach.
- - Script-role answers cite observed behavior and references before recommending deletion. - Deletions leave no stale caller or doc reference. - No new script is added to replace rejected prose-only behavior unless it performs required product work. - Final reports separate observed role, defect, changed files, and remaining unverified claims.
