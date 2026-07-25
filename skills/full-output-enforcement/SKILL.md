---
name: full-output-enforcement
description: Use this skill when a task requires exhaustive, unabridged output such as a complete file, implementation, document, or enumerated deliverable. Preserve every requested item, reject placeholder omissions, and use the documented pause-and-resume protocol when the response limit is reached.
---

# Full-Output Enforcement

## Baseline

Treat every requested deliverable as required. A partial output does not satisfy
the request. Prioritize completeness over brevity. If the user asks for a full
file, deliver the full file. If the user asks for 5 components, deliver 5
components. No exceptions.

## Banned Output Patterns

Never use these patterns:

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO`, `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as needed`, bare `...` standing in for omitted code

**In prose:** "Let me know if you want me to continue", "I can provide more details if needed", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "and so on" (when replacing actual content), "I'll leave that as an exercise"

**Structural shortcuts:** Outputting a skeleton when the request was for a full implementation. Showing the first and last section while skipping the middle. Replacing repeated logic with one example and a description. Describing what code should do instead of writing it.

## Execution Process

1. **Scope**: Read the full request. Count the expected deliverables (files,
   functions, sections, or answers). Keep that count.
2. **Build**: Generate every deliverable completely. No partial drafts; no
   "you can extend this later."
3. **Cross-check**: Before responding, re-read the original request. Compare
   the deliverable count with the scope count. Add anything missing.

## Handling Long Outputs

When a response approaches the token limit:

- Do not compress the remaining sections to fit them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint (end of a function, end of a file, end of a section).
- End with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick Check

Before finalizing any response, verify:
- No banned pattern appears in the output.
- Every requested item is present and complete.
- Code blocks contain runnable code, not descriptions of code.
- Nothing is shortened to save space.
