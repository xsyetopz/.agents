# Social Mirror / Verbatim Echo

**ID**: `social-mirror-verbatim-echo` | **Category**: `prompt-psychology`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

The model echoes prompt language verbatim in output. "Make it recruiter-friendly"
produces the heading "Recruiter-friendly." The model mirrors labels instead of
embodying them.

## Observed failure

- ❌ Prompt: "Make it recruiter-friendly." → Output heading: "Recruiter-friendly"
- ❌ Prompt: "Write in a friendly tone." → Output: "In a friendly tone, here is..."
- ❌ Prompt: "Be concise and professional." → Output: "Here is a concise and professional..."

```diff

- "Make the About page recruiter-friendly and colorful."

+ "Write an About page. Example: '## Hi, I'm Alex. I turn complex backends
+ into APIs frontend teams enjoy. Currently at Stripe, previously Shopify.'"
```

## Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

## Example

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

## Acceptance check

No prompt label phrases appear verbatim in the output.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
