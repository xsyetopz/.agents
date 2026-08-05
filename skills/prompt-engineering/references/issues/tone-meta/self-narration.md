# Self-Narration, Confession, and Meta-Commentary

**Merged from**: `tone-and-meta-commentary`, `self-confession-correction-framing`, `first-person-confessional-status`, `edit-announcement-self-commentary`, `unasked-for-prose-and-narration`
**Category**: `tone-meta`

## Trigger patterns

- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.
- Use when: the agent answers a correction by centering its own mistake process, such as "I made X when the user asked Y."
- Use when: the agent explains a correction with first-person self-analysis instead of stating the artifact change and evidence.
- Use when: the agent announces an edit by diagnosing its own response, ranking phrases, or narrating the rewrite instead of patching and reporting evidence.

## Bad forms — what this looks like

- ❌ `"You’re right."`
- ❌ `"I made X when..."`
- ❌ `"I misunderstood..."`
- ❌ `"I overstepped..."`
- ❌ `"I was drifting..."`
- ❌ `"I’ll fix my mistake by..."`
- ❌ `"I kept treating..."`
- ❌ `"I was still..."`
- ❌ `"I can't help myself..."`
- ❌ `"That was me..."`

## Required behavior

```text
When the user requests a wording correction:
patch the artifact
keep progress updates action-focused
avoid ranking, diagnosing, or naming the mistake unless the user asked for analysis
run the narrow checks that cover the edited artifact
report changed files and check results
```

## Concrete example

**User says**: "the goal should not say autonomous or use meta-phrasing. talk to the goal file like you're the agent"

**❌ Agent (WRONG)**: "The opening was the main offender: it described the artifact instead of instructing the agent. I'm replacing that with direct operational language and leaving the rest terse."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When the user requests a wording correction:
patch the artifact
keep progress updates action-focused
```

## Acceptance checks

- The next response after a correction names the corrected artifact or action without first-person diagnosis, and the resulting file or command output matches the user's requested artifact category.
- Status updates describe changed artifacts and checks without first-person self-analysis.
- After a wording correction, the response names the changed file, evidence checks, and remaining gaps. It does not narrate the assistant's rewrite or rank the prior wording unless the user requested analysis.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
