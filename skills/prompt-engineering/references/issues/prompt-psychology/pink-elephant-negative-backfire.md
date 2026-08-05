# Constraint Framing Overgeneralization

**ID**: `pink-elephant-negative-backfire` | **Category**: `prompt-psychology`

## Trigger

A prompt audit applies a blanket rule that negative wording is unreliable,
counts prohibitions, or rewrites precise hard boundaries merely because they use
“do not,” “never,” or “avoid.”

## Failure

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

## Acceptance check

The revised prompt preserves every required boundary, states each rule once,
does not use a fixed prohibition-count threshold, and passes both abstention and
authorized-action rollouts on the target model.
