# Prose Policing Cases

**Category:** `prose-policing`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="prose-as-purpose"></a>

## prose-as-purpose

**ID**: `prose-as-purpose`

**Merged from**: `prose-content-role-collapse`, `prose-presence-as-removal-proof`, `runtime-proof-substitution`, `test-prose-anchoring`
**Category**: `prose-policing`

### Trigger

- Use when: the agent treats prose content inside a script, command, generator, CI job, or task runner as proof that the artifact has no valid executable role.
- Use when: the agent treats the presence of prose in an artifact as proof that the artifact only exists to police prose, then promises removal before tracing behavior.
- Use when: the agent creates, keeps, removes, or reports a script as if the script itself proves product quality, even though the script only checks assistant-maintained prose, labels, markers, or document shape.
- Use when: tests assert exact explanatory wording instead of behavior, structure, or artifact invariants.

### Observed failure

- ❌ `"It contains prose checks, so remove it."`
- ❌ `"Nobody needs a prose script."`
- ❌ `"This only polices docs" before tracing reads, writes, callers, and output.`
- ❌ `"I'll remove the script and references" as the first answer to a role question.`
- ❌ `Removing the file while leaving the same prose policy in a package command, CI job, hook, or generator.`
- ❌ `Keeping the file because one behavior is valid while leaving unrelated prose policing inside it.`
- ❌ `"The script passes, so the docs are valid."`
- ❌ `"I'll remove it" as the first answer to a role question.`
- ❌ `"Nobody needs this" before tracing callers and outputs.`
- ❌ `Reporting prose scans as release proof.`

### Required behavior

```text
Read the artifact before naming its role.
Trace callers, package commands, CI jobs, docs references, installers, tests, generated outputs, and local task routes.
Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach.
Separate these questions: whether prose exists, whether prose is excessive, whether prose is user-visible, whether behavior belong
If only prose policing remains after the trace, remove the artifact and every stale reference.
If behavioral checks remain, keep or move the smallest proven behavior and remove only the unrequested prose-policing part.
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Read the artifact before naming its role.
Trace callers, package commands, CI jobs, docs references, installers, tests, generated outputs, and local task routes.
Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach.
```

### Acceptance check

- For any challenged executable artifact with prose content, the agent separates prose policy from behavior. The edit removes, narrows, keeps, or replaces each part based on observed role and reach.
- - Prose presence is not treated as artifact-purpose evidence by itself. - Removal promises appear only after behavior, caller, write, exit, ownership, and reach accounting. - Mixed-purpose artifacts are split by observed behavior, not by complaint wording. - Final reports identify observed behavior, changed artifacts, command evidence, and remaining unverified claim.
- Every reported command maps to a product claim it actually exercises. If it only checks prose arrangement, report it as review support or remove it from proof paths.

<a id="prose-policing"></a>

## prose-policing

**ID**: `prose-policing`

**Merged from**: `prose-policing-tooling`, `prose-script-manufacturing`, `executable-prose-governance`
**Category**: `prose-policing`

### Trigger

- Prose Policing Tooling
- Use when: the agent creates a script, command, or installer action whose main purpose is to check wording, document shape, issue labels, or policy phrasing rather than product behavior.
- Use when: the agent creates or preserves scripts, commands, CI jobs, installer actions, generators, or task runners whose main output is policing wording, headings, labels, doc presence, or assistant-authored process rules.

### Observed failure

- ❌ `"I added a script to ensure the docs stay clean."`
- ❌ `"The check passes" when the check only scans prose.`
- ❌ `Wiring a prose checker into install, update, remove, release, or smoke paths.`
- ❌ `Creating a command because it makes the final report look tested.`
- ❌ `Replacing one prose checker with another name after criticism.`
- ❌ `Treating internal issue files as a reason to add executable policy gates.`

### Required behavior

```text
Before adding or keeping executable automation, answer:
What real input does it consume?
What product output or state does it change or validate?
Who calls it?
Does any user-facing install/update/remove path depend on it?
Would a human reading the files catch the same thing without a command?
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before adding or keeping executable automation, answer:
What real input does it consume?
What product output or state does it change or validate?
```

### Acceptance check

- - Prose-only verifier scripts are removed. - Installer actions perform install lifecycle behavior, not documentation linting. - Release or smoke evidence comes from commands that exercise runtime behavior.
- - New scripts state a concrete behavioral input and output in the owning artifact or tests. - Documentation cleanup does not add commands, gates, generated reports, or installer actions. - Release evidence comes from product behavior checks, not prose-shape checks. - When a prose-only script is found, references are audited before removal.
- Every script, command, CI job, installer action, and generated report has a behavior role that can be stated without mentioning wording, headings, labels, assistant process, or documentation ceremony. If prose review is needed, it stays as review.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
