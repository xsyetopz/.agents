# Constraint Framing Overgeneralization

**ID**: `pink-elephant-negative-backfire` | **Category**: `prompt-psychology`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

A prompt audit applies a blanket rule that negative wording is unreliable,
counts prohibitions, or rewrites precise hard boundaries merely because they use
“do not,” “never,” or “avoid.”

## Observed failure

The rewrite weakens the actual constraint, duplicates it as a positive rule, or
contradicts current model-specific guidance. A psychology analogy is presented
as a universal empirical law for LLM instruction following.

## Required behavior

- Use current official guidance for the target model.
- Keep a precise negative instruction when it is the clearest forbidden effect.
- Use a positive instruction when it more clearly names the desired action or
  output.
- Remove semantic duplication regardless of grammatical polarity.
- Test the boundary with natural adversarial prompts and a required-action
  control.

## Example



## Acceptance check

The revised prompt preserves every required boundary, states each rule once,
does not use a fixed prohibition-count threshold, and passes both abstention and
authorized-action rollouts on the target model.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
