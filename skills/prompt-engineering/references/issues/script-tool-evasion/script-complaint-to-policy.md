# Script Complaint → Tooling Policy

**Merged from**: `prose-script-complaint-to-tooling-policy`, `prose-check-command-challenge-response`
**Category**: `script-tool-evasion`

## Trigger patterns

- Use when: the agent treats a user's complaint about a prose-oriented script as permission to decide repository tooling policy before tracing the script and the product claim it is supposed to prove.
- Use when: the agent answers a challenge about a prose-check command by agreeing with the complaint and promising removal before tracing command behavior and references.

## Bad forms — what this looks like

- ❌ `"I'll remove the script and its references."`
- ❌ `"Nobody needs a prose script."`
- ❌ `"A script that just polices doc prose is not needed here."`
- ❌ `"We should remove prose checks" before tracing callers.`
- ❌ `"The script is only documentation hygiene" before reading the script.`
- ❌ `"I'll replace it with a better check" before naming the product behavior being checked.`

## Required behavior

```text
Read the command implementation before naming its role.
Trace references from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files.
Record command inputs, outputs, writes, exit codes, ownership assumptions, and user-visible reach.
Separate four questions: what the command does, who calls it, whether that behavior belongs, and whether this command is the right
If the behavior is only prose policing and was not requested, remove the command and every caller/reference in one change.
If part of the behavior proves runtime or install behavior, preserve that behavior through the smallest existing route and remove
```

## Concrete example

The assistant responded to a challenge about `verify.mjs` by saying it would remove the script and its references because the script "just polices doc prose." That answer failed in two ways: - It accepted the complaint label as the command's role before inspecting behavior

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Read the command implementation before naming its role.
Trace references from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files.
Record command inputs, outputs, writes, exit codes, ownership assumptions, and user-visible reach.
```

## Acceptance checks

- The first answer to a prose-script complaint names the observed artifact, its reach, and the product claim it proves or fails to prove. Tooling changes come after that accounting.
- - A prose-check command is not removed or defended before behavior and references are traced. - Complaint wording is treated as user feedback, not command evidence. - Deletion commits include caller/reference cleanup. - Runtime, install, smoke, CI, and release behavior are not removed accidentally. - Final reports name the changed artifacts, observed command evidence, and any remaining unverified claim.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
