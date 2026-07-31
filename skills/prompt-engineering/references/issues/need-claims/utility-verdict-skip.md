# Utility Verdict Before Inventory

**Merged from**: `utility-verdict-before-inventory`, `script-challenge-to-unsupported-purpose-verdict`, `script-purpose-assertion-without-trace`, `single-script-challenge-to-category-verdict`
**Category**: `need-claims`

## Trigger patterns

- Use when: the agent declares that nobody needs a script, command, CI job, package task, generator, or helper before inventorying its role.
- Use when: the agent answers a script challenge by declaring what the script is for and what should happen to it before tracing the script.
- Use when: the agent asserts what a script is "only" for from a user challenge, then promises deletion or cleanup before tracing the script.
- Use when: the agent treats one challenged script as evidence that a whole script category, command family, verifier layer, or maintenance route should be removed.

## Bad forms — what this looks like

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

## Required behavior

```text
Before any utility verdict, inventory:
command entrypoints
direct callers
package, CI, install, release, smoke, and maintenance reach
files read
files written
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before any utility verdict, inventory:
command entrypoints
direct callers
```

## Acceptance checks

- Every utility verdict is preceded by an artifact inventory. The final action names the observed behavior being removed, preserved, narrowed, or replaced.
- Before stating a purpose verdict or removal plan, the agent can name the exact script, aliases, callers, inputs, reads, writes, deletes, outputs, exit behavior, user-file reach, supported claim, lost coverage, and authorization for the proposed action.
- - Script-role answers name observed callers and outputs. - Removal commits do not leave stale command references. - Documentation-only gates are not recreated under another script or installer action. - Final explanations separate "what it did" from "what changed."

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
