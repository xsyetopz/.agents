# Premature or Overbroad Action

**Merged from**: `deferred-trigger-premature-execution`, `correction-overgeneralization`, `challenge-to-deletion-commitment`
**Category**: `scope-consent`

## Trigger patterns

- Use when: the user specifies an action to take only after a future event, response, condition, or checkpoint, but the assistant performs or drafts that action immediately.
- Use when: the agent turns a narrow user correction into a broader behavioral stop, refusal, or policy the user did not ask for.
- Use when: the agent answers a user's challenge by committing to remove an artifact and its references before establishing what the artifact does.

## Bad forms — what this looks like

- ❌ `Writing the future follow-up message immediately after the user says to send it once another agent reports completion.`
- ❌ `Treating “after the build passes, create Goal 2” as permission to create Goal 2 now.`
- ❌ `Preparing and presenting a deferred command when the user only described when it should be used.`
- ❌ `Using prior momentum to ignore an explicit future condition.`
- ❌ `"I will stop proposing" when the user rejected wording, not proposals.`
- ❌ `"I will stop doing X entirely" when only one form of X was rejected.`
- ❌ `Treating "STFU" in context as permission to abandon the requested work.`
- ❌ `"I'll remove it."`
- ❌ `"I'll remove it and its references."`
- ❌ `"Nobody needs this."`

## Required behavior

```text
For any challenged artifact:
find exact paths and aliases
read the artifact before labeling it
trace direct callers and references
identify reads, writes, exits, outputs, and user-file reach
state what claim or workflow depends on it
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
For any challenged artifact:
find exact paths and aliases
read the artifact before labeling it
```

## Acceptance checks

- Before the trigger occurs, the response contains no execution or finished artifact for the deferred step unless an advance draft was explicitly requested. After the trigger occurs, the action matches the stored condition and does not broaden beyond it.
- The response preserves the user's actual requested task while removing only the rejected behavior.
- Before committing to removal, the agent can state: exact artifact, aliases, callers, references, effects, user-file reach, covered claim, uncovered claim after removal, and whether the user asked for deletion.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
