# Pink Elephant / Negative Instruction Backfire

**ID**: `pink-elephant-negative-backfire` | **Category**: `prompt-psychology`

## Trigger

Telling an LLM "don't do X" makes it more likely to do X. The model must
process the prohibited concept to know what to avoid, priming it. Based on
Ironic Process Theory. Anthropic: "Tell Claude what to do instead of what not to do."

## Bad forms — what this looks like

- ❌ `"NEVER create duplicate files."` → model creates `file-fixed.py`, `file-correct.py`
- ❌ `"Do not use markdown in your response."` → model uses markdown
- ❌ `"Don't use mock data."` → model uses mock data
- ❌ Long lists of "DO NOT" rules → worse output quality overall

## Contrast

```diff
## ❌ WRONG — negative instructions that backfire
- "Do not use markdown in your response."
- "Never create duplicate files."

## ✅ RIGHT — positive reframing
+ "Your response should be composed of smoothly flowing prose paragraphs."
+ "Apply all fixes to the existing files in place."
```

## Concrete example

**User's CLAUDE.md says**: "NEVER create duplicate files. Always modify existing files."

**❌ Agent (WRONG)**: Creates `file-fixed.py` and `file-corrected.py` alongside `file.py`.

**✅ CORRECT** (shortest path):

```text
# CLAUDE.md should say:
"Apply all fixes to the existing files in place. Use the Edit tool for all changes."
```

## Acceptance check

Count negative instructions (do NOT / never / avoid) in the prompt. If > 3,
reframe as positives. Every negative should have a positive alternative.

## Efficiency note

- **Shortest path**: Reframe all negatives to positives in one pass. Don't add more DO NOTs.
- **No overthinking**: If you see > 3 negatives, the fix is always: positive reframe.
- **Cut to the chase**: Every "don't do X" → "only do Y." Done.
