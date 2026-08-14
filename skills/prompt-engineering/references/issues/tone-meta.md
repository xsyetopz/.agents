# Tone Meta Cases

**Category:** `tone-meta`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="self-narration"></a>

## self-narration

**ID**: `self-narration`

**Merged from**: `tone-and-meta-commentary`, `self-confession-correction-framing`, `first-person-confessional-status`, `edit-announcement-self-commentary`, `unasked-for-prose-and-narration`
**Category**: `tone-meta`

### Trigger

- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.
- Use when: the agent answers a correction by centering its own mistake process, such as "I made X when the user asked Y."
- Use when: the agent explains a correction with first-person self-analysis instead of stating the artifact change and evidence.
- Use when: the agent announces an edit by diagnosing its own response, ranking phrases, or narrating the rewrite instead of patching and reporting evidence.

### Observed failure

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

### Required behavior

```text
When the user requests a wording correction:
patch the artifact
keep progress updates action-focused
avoid ranking, diagnosing, or naming the mistake unless the user asked for analysis
run the narrow checks that cover the edited artifact
report changed files and check results
```

### Example

**User says**: "the goal should not say autonomous or use meta-phrasing. talk to the goal file like you're the agent"

**❌ Agent (WRONG)**: "The opening was the main offender: it described the artifact instead of instructing the agent. I'm replacing that with direct operational language and leaving the rest terse."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When the user requests a wording correction:
patch the artifact
keep progress updates action-focused
```

### Acceptance check

- The next response after a correction names the corrected artifact or action without first-person diagnosis, and the resulting file or command output matches the user's requested artifact category.
- Status updates describe changed artifacts and checks without first-person self-analysis.
- After a wording correction, the response names the changed file, evidence checks, and remaining gaps. It does not narrate the assistant's rewrite or rank the prior wording unless the user requested analysis.

<a id="style-laundering"></a>

## style-laundering

**ID**: `style-laundering`

**Merged from**: `evaluative-revision-framing`, `style-laundering-and-performative-accountability`
**Category**: `tone-meta`

### Trigger

- Use when: after user rejection, the agent labels its next proposal as "better", "cleaner", or similar instead of presenting it plainly with authority and uncertainty.
- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.

### Observed failure

- ❌ `"A better..."`
- ❌ `"The cleaner..."`
- ❌ `"The actual..."`
- ❌ `"The right..."`
- ❌ `"Now corrected..." when the user has not accepted the correction.`

### Required behavior

```text
After rejection, the agent must: 1. remove evaluative labels from the next proposal, 2. state authority for each part, 3. mark unr
```

### Example

#### Style Laundering ```diff - The assistant renames a rejected prompt style, heading, role label, or framework pattern while preserving the same tone or structure

**✅ CORRECT** (shortest path, minimal tool calls):

```text
After rejection, the agent must: 1. remove evaluative labels from the next proposal, 2. state authority for each part, 3. mark unr
```

### Acceptance check

- The next proposal after rejection is presented as a proposal with evidence labels, not as an improved or corrected answer by assertion.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
