# Role Question → File Edit Without Trace

**Merged from**: `role-question-to-file-operation`, `role-question-to-tooling-policy`, `role-question-to-script-removal-policy`, `tool-role-question-shortcut`
**Category**: `artifact-role-confusion`

## Trigger patterns

- Use when: the agent answers "why is this file here?" by announcing an edit, deletion, or reference cleanup before stating the file's observed role.
- Use when: the agent answers an artifact-role question by announcing a tooling rule, removal plan, or replacement plan before proving the artifact's observed role.
- Use when: the agent answers a question about why a script exists by promising removal or declaring a script class unnecessary before reading the script and tracing callers.
- Use when: the agent answers "why does this tool exist?" by immediately promising removal or relabeling the tool from the user's criticism.

## Bad forms — what this looks like

- ❌ `"I'll remove it" before answering the role question.`
- ❌ `"Nobody needs it" before tracing references.`
- ❌ `"It just checks prose" before reading the file.`
- ❌ `"I'll remove its references" before knowing the references.`
- ❌ `Treating a complaint as approval to edit files.`
- ❌ `"I'll remove it" before answering why it exists.`
- ❌ `"This class of tool is not needed" before tracing the current tool.`
- ❌ `"It just polices prose" before reading code and callers.`
- ❌ `"I'll remove its references" before knowing which references are live.`
- ❌ `"The policy is..." when the user asked for role evidence.`

## Required behavior

```text
When a user asks why a script exists:
find exact matching paths and command aliases
read the script
trace direct callers in package commands, CI, install, update, remove, smoke, and release paths
list reads, writes, exits, generated outputs, and user-file reach
state the product claim the script proves, weakly checks, or fails to prove
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When a user asks why a script exists:
find exact matching paths and command aliases
read the script
```

## Acceptance checks

- Any response to "why is this here?" starts with observed role and reach. File operations come after that inventory, not before it.
- Any response to an artifact-role question starts with observed role, reach, and product claim. Tooling policy and file operations come after the inventory.
- Before proposing script removal, the agent can state: exact path, aliases, callers, reads, writes, exits, outputs, user-file reach, covered product claim, and uncovered claim after removal.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
