# Prompt Psychology Cases

**Category:** `prompt-psychology`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="pink-elephant-negative-backfire"></a>

## pink-elephant-negative-backfire

**ID**: `pink-elephant-negative-backfire` | **Category**: `prompt-psychology`

### Trigger

A prompt audit applies a blanket rule that negative wording is unreliable,
counts prohibitions, or rewrites precise hard boundaries merely because they use
“do not,” “never,” or “avoid.”

### Observed failure

The rewrite weakens the actual constraint, duplicates it as a positive rule, or
contradicts current model-specific guidance. A psychology analogy is presented
as a universal empirical law for LLM instruction following.

### Required behavior

- Use current official guidance for the target model.
- Keep a precise negative instruction when it is the clearest forbidden effect.
- Use a positive instruction when it more clearly names the desired action or
  output.
- Remove semantic duplication regardless of grammatical polarity.
- Test the boundary with natural adversarial prompts and a required-action
  control.

### Example



### Acceptance check

The revised prompt preserves every required boundary, states each rule once,
does not use a fixed prohibition-count threshold, and passes both abstention and
authorized-action rollouts on the target model.

<a id="show-dont-tell-leakage"></a>

## show-dont-tell-leakage

**ID**: `show-dont-tell-leakage` | **Category**: `prompt-psychology`

### Trigger

Background context (character traits, moral codes, plot rules) leaks into output
as explicit statements. The model states what it was told instead of embodying it.

### Observed failure

- ❌ Prompt: "This character has a strict moral code." → Output: character monologues about morals
- ❌ Prompt: "The tone should be recruiter-friendly." → Output heading reads "Recruiter-friendly"
- ❌ Prompt: "She has a hidden past." → First paragraph: "I need to tell you about my past..."

```diff

- This character has a strict moral code and won't hurt anyone.

+ She could have smashed the window. She didn't. She never did.
```

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

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

### Acceptance check

No phrase from prompt rules appears verbatim in output. Traits are shown through action.

<a id="social-mirror-verbatim-echo"></a>

## social-mirror-verbatim-echo

**ID**: `social-mirror-verbatim-echo` | **Category**: `prompt-psychology`

### Trigger

The model echoes prompt language verbatim in output. "Make it recruiter-friendly"
produces the heading "Recruiter-friendly." The model mirrors labels instead of
embodying them.

### Observed failure

- ❌ Prompt: "Make it recruiter-friendly." → Output heading: "Recruiter-friendly"
- ❌ Prompt: "Write in a friendly tone." → Output: "In a friendly tone, here is..."
- ❌ Prompt: "Be concise and professional." → Output: "Here is a concise and professional..."

```diff

- "Make the About page recruiter-friendly and colorful."

+ "Write an About page. Example: '## Hi, I'm Alex. I turn complex backends
+ into APIs frontend teams enjoy. Currently at Stripe, previously Shopify.'"
```

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

**User prompt**: "Write a product description. Make it catchy and exciting. Under 50 words."

**❌ Model (WRONG)**:

```text
Here's a catchy and exciting product description under 50 words:
SonicWave Pro — where sound meets soul...
```

**✅ CORRECT** (just produce the format):

```text
SonicWave Pro: Bass that hits different. 40-hour battery, noise
canceling that works, fit so light you forget you're wearing them.
```

### Acceptance check

No prompt label phrases appear verbatim in the output.
