# Artifact Substitution Without Consent

**Merged from**: `requested-artifact-substitution`, `requested-area-artifact-shape-override`, `artifact-category-substitution`
**Category**: `scope-consent`

## Trigger patterns

- Use when: the agent substitutes a nearby artifact for the user-named artifact and treats that substitution as edit authority.
- Use when: the user authorizes a destination, pool, or documentation area, and the agent chooses the artifact shape, split, granularity, or file boundary without being asked.
- Use when: the agent preserves superficial request details while substituting a different artifact category.

## Bad forms — what this looks like

- ❌ `"There is no X, so I updated Y."`
- ❌ `"The active file is Y, so I changed it."`
- ❌ `"I assumed you meant Y."`
- ❌ `"I will not invent a duplicate, so I edited Y."`
- ❌ `"You asked for it in this area, so I created a new issue."`
- ❌ `"I chose the artifact shape myself."`
- ❌ `"I made it separate because it seemed distinct."`
- ❌ `"I’m folding it back after realizing..."`
- ❌ `Treating a destination path as approval for a new file.`
- ❌ `Treating a pool name as approval for a new category.`

## Required behavior

```text
When the user names an area, pool, directory, or documentation family, the agent must: 1. Treat the named location as a destinatio
```

## Concrete example

- User asked for a schema/directory edge case to be covered in `docs/_internal/llm-issues`. The agent created a standalone issue even though the user had not asked for a separate issue, and the edge case belonged under the broader consent issue.

**✅ CORRECT** (shortest path, minimal tool calls):

```text
When the user names an area, pool, directory, or documentation family, the agent must: 1. Treat the named location as a destinatio
```

## Acceptance checks

- When the requested artifact is absent, the next action is a report or clarification request, not an edit to a substitute file.
- Before creating a new documentation artifact inside a user-named area, the agent can identify: 1. the exact user-authorized destination, 2. the nearest existing artifact that could own the content, 3. why that existing artifact is insufficient, or why it should be extended, 4. whether the user explicitly authorized a separate artifact. If those checks do not justify a new file, the change goes into the existing owning artifact.
- The resulting artifact can be described using the same noun the user used for the requested deliverable. If the user asked for a file tree, the artifact contains a file tree. If the user asked for code, the artifact contains code. If the user asked for tests, the artifact contains tests.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
