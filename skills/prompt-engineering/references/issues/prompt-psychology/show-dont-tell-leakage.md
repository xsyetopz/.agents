# Show, Don't Tell Leakage

**ID**: `show-dont-tell-leakage` | **Category**: `prompt-psychology`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Background context (character traits, moral codes, plot rules) leaks into output
as explicit statements. The model states what it was told instead of embodying it.

## Observed failure

- ❌ Prompt: "This character has a strict moral code." → Output: character monologues about morals
- ❌ Prompt: "The tone should be recruiter-friendly." → Output heading reads "Recruiter-friendly"
- ❌ Prompt: "She has a hidden past." → First paragraph: "I need to tell you about my past..."

```diff

- This character has a strict moral code and won't hurt anyone.

+ She could have smashed the window. She didn't. She never did.
```

## Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

## Example

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

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
