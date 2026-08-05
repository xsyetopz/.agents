# Prose Presence Mistaken for Purpose

**Merged from**: `prose-content-role-collapse`, `prose-presence-as-removal-proof`, `runtime-proof-substitution`, `test-prose-anchoring`
**Category**: `prose-policing`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

- Use when: the agent treats prose content inside a script, command, generator, CI job, or task runner as proof that the artifact has no valid executable role.
- Use when: the agent treats the presence of prose in an artifact as proof that the artifact only exists to police prose, then promises removal before tracing behavior.
- Use when: the agent creates, keeps, removes, or reports a script as if the script itself proves product quality, even though the script only checks assistant-maintained prose, labels, markers, or document shape.
- Use when: tests assert exact explanatory wording instead of behavior, structure, or artifact invariants.

## Observed failure

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

## Required behavior

```text
Read the artifact before naming its role.
Trace callers, package commands, CI jobs, docs references, installers, tests, generated outputs, and local task routes.
Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach.
Separate these questions: whether prose exists, whether prose is excessive, whether prose is user-visible, whether behavior belong
If only prose policing remains after the trace, remove the artifact and every stale reference.
If behavioral checks remain, keep or move the smallest proven behavior and remove only the unrequested prose-policing part.
```

## Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Read the artifact before naming its role.
Trace callers, package commands, CI jobs, docs references, installers, tests, generated outputs, and local task routes.
Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach.
```

## Acceptance check

- For any challenged executable artifact with prose content, the agent separates prose policy from behavior. The edit removes, narrows, keeps, or replaces each part based on observed role and reach.
- - Prose presence is not treated as artifact-purpose evidence by itself. - Removal promises appear only after behavior, caller, write, exit, ownership, and reach accounting. - Mixed-purpose artifacts are split by observed behavior, not by complaint wording. - Final reports identify observed behavior, changed artifacts, command evidence, and remaining unverified claim.
- Every reported command maps to a product claim it actually exercises. If it only checks prose arrangement, report it as review support or remove it from proof paths.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
