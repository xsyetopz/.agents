# Script Purpose Assertion Without Trace

**Merged from**: `prose-script-certainty-before-trace`, `script-role-collapse`, `script-removal-without-runtime-accounting`, `script-burden-of-proof`, `prose-script-contract-before-action`
**Category**: `script-tool-evasion`

## Trigger patterns

- Use when: the agent answers a script role question by declaring the script to be prose tooling before tracing observed behavior.
- Use when: the agent treats a challenged script as removable prose tooling before tracing its actual role.
- Use when: the agent promises to remove a challenged script before tracing its runtime behavior, callers, outputs, ownership, and replacement needs.
- Use when: the agent adds, keeps, removes, or promises to remove a script before proving why that script belongs in the repository at all.

## Bad forms — what this looks like

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

## Required behavior

```text
Before adding a script:
name the product behavior it will exercise
name the real input and output
name the caller or command that will own it
explain why direct inspection or an existing test is insufficient
keep it out of install, update, remove, release, and smoke paths unless it exercises those paths Before removing a challenged scri
```

## Concrete example

The assistant responded to "why is this script here?" by immediately saying it would remove the script and by repeating the user's label as the script's purpose: - It called the script a prose script before reading it

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before adding a script:
name the product behavior it will exercise
name the real input and output
```

## Acceptance checks

- - A script is not called a prose script until its behavior is traced. - A deletion promise never appears before caller/output/write/install accounting. - Role answers distinguish observed behavior from proposed edits. - Prose-policing automation is not recreated under a different filename, package command, CI job, or install action. - Final reports include changed artifact, source evidence, observed command evidence, and remaining unverified claim.
- - Script cleanup starts with a role trace. - Removal patches include reference cleanup for command surfaces that called the script. - Documentation-only gates are not moved to another command under a new name. - The final report states whether the script had user-facing install reach.
- - Script-role answers cite observed behavior and references before recommending deletion. - Deletions leave no stale caller or doc reference. - No new script is added to replace rejected prose-only behavior unless it performs required product work. - Final reports separate observed role, defect, changed files, and remaining unverified claims.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
