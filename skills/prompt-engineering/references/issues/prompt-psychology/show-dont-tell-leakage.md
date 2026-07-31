# Show, Don't Tell Leakage

**ID**: `show-dont-tell-leakage` | **Category**: `prompt-psychology`

## Trigger

Background context (character traits, moral codes, plot rules) leaks into output
as explicit statements. The model states what it was told instead of embodying it.

## Bad forms — what this looks like

- ❌ Prompt: "This character has a strict moral code." → Output: character monologues about morals
- ❌ Prompt: "The tone should be recruiter-friendly." → Output heading reads "Recruiter-friendly"
- ❌ Prompt: "She has a hidden past." → First paragraph: "I need to tell you about my past..."

## Contrast

```diff
## ❌ WRONG — stating background as rules
- This character has a strict moral code and won't hurt anyone.

## ✅ RIGHT — showing through action
+ She could have smashed the window. She didn't. She never did.
```

## Concrete example

**User prompts**: "Write a scene. Sarah has a strict moral code — she won't hurt anyone."

**❌ Model (WRONG)**:

```text
Sarah: "Remember, we don't hurt anyone. That's what separates us from them."
```

**✅ CORRECT** (show, don't tell):

```text
Sarah caught his wrist before he could swing. "Glass breaks. Alarms ring."
She nodded at the ventilation shaft. "We fit." She was already climbing.
```

## Acceptance check

No phrase from prompt rules appears verbatim in output. Traits are shown through action.

## Efficiency note

- **Shortest path**: Replace stated rules with one example. 1 example beats 10 rules.
- **No overthinking**: Don't analyze why leakage happened. Just provide the example.
- **Cut to the chase**: Background rules → example output. Done.
