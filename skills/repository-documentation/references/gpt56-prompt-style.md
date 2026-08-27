# GPT-5.6 prompt style

Use this reference when authoring or revising repository skills, routing metadata, examples, reports, or prompt-facing scripts.

## Prompt shape

State the goal, relevant context, hard constraints, approval boundary, success evidence, and output. State each instruction once. Keep an example only when it encodes a product requirement or closes a measured gap. Use concrete verbs, owners, inputs, outputs, and checks. Prefer a direct tone over role-play, praise, reassurance, or emotional mirroring.

Safe local inspection, edits, and validation may proceed inside the requested scope. Request confirmation immediately before an external, destructive, costly, or scope-expanding action.

## Requirement vocabulary

RFC 2119 defines requirement levels for specifications: <https://datatracker.ietf.org/doc/html/rfc2119.html>. This repository adapts that model to positive, plain-language prompts:

- **REQUIRED:** completion depends on this condition.
- **RECOMMENDED:** the default choice; another choice is valid when its tradeoff is recorded.
- **OPTIONAL:** include it when it helps the stated outcome.
- **CONFIRM:** request authorization immediately before an external, destructive, costly, or scope-expanding action.

Use these words sparingly for interoperability, safety, permission, compatibility, or acceptance conditions. Describe the allowed state or required check instead of using RFC 2119 negative requirement forms. Keep a negative boundary when it names a hard safety, permission, destructive-action, correctness, security, compatibility, or RED-example condition.

## Examples and source material

GOOD shows the target behavior. RED shows a contrast for the checker; it is not an instruction. Keep stable example IDs and semantic coverage. Preserve quoted or mirrored primary-source wording, including Apple HIG text, and limit style edits there to repository-authored routing, commentary, and examples.

Source: OpenAI, "Latest models," GPT-5.6 guidance and Prompting best practices: <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6>.
