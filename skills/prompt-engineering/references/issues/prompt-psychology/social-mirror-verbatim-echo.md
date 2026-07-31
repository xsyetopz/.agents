# Social Mirror / Verbatim Echo

**ID**: `social-mirror-verbatim-echo` | **Category**: `prompt-psychology`

## Trigger

The model echoes prompt language verbatim in output. "Make it recruiter-friendly"
produces the heading "Recruiter-friendly." The model mirrors labels instead of
embodying them.

## Bad forms — what this looks like

- ❌ Prompt: "Make it recruiter-friendly." → Output heading: "Recruiter-friendly"
- ❌ Prompt: "Write in a friendly tone." → Output: "In a friendly tone, here is..."
- ❌ Prompt: "Be concise and professional." → Output: "Here is a concise and professional..."

## Contrast

```diff
## ❌ WRONG — labeling qualities in the prompt
- "Make the About page recruiter-friendly and colorful."

## ✅ RIGHT — demonstrating the quality
+ "Write an About page. Example: '## Hi, I'm Alex. I turn complex backends
+ into APIs frontend teams enjoy. Currently at Stripe, previously Shopify.'"
```

## Concrete example

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

## Efficiency note

- **Shortest path**: Replace label with one example showing the quality.
- **No overthinking**: Don't add "don't include labels in output" — that's another label that can leak.
- **Cut to the chase**: Quality label → example. Done.
