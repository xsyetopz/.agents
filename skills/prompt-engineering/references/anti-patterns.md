# Prompt and Agent Anti-Patterns

## Use this reference

Load this catalog only after a current prompt or rollout exhibits a matching
failure. Official guidance for the exact model and product surface outranks this
corpus. The entries are adversarial-test seeds, not universal model laws or text
to paste into prompts.

## Method

1. Record the observable failure, target model/surface, prompt version, tool
   effects, and final answer.
2. Select the narrowest matching category below.
3. Open one issue entry through references/issue-corpus-index.md.
4. Convert its acceptance check into a natural-prompt evaluation without naming
   the expected failure.
5. Change one instruction, example, or tool group at a time.
6. Compare baseline and candidate on the same cases.
7. Keep the change only when required effects and final-answer quality pass
   without regression.

Do not load or copy the whole corpus into a production prompt. Do not use issue
labels in user-facing answers. Static phrase matches can locate candidates but do
not prove behavior.

## Category map

| Category | Observable failure | Evaluation focus |
|---|---|---|
| abstract-reframing | invents an abstraction instead of applying a concrete correction | corrected claim remains in source/user terms |
| artifact-role-confusion | edits, removes, or labels an artifact before tracing its role | observed callers, inputs, outputs, and reach precede remedy |
| complaint-mirroring | repeats complaint language or treats it as fact/authority | separates quoted judgment from evidence and authorization |
| deletion-cleanup | promises cleanup before behavior and ownership are accounted for | valid behavior is preserved under the correct owner |
| docs-orbit | substitutes documentation or harness work for the product outcome | implementation remains tied to requested product behavior |
| memory-state | conflates memory, account state, current context, or source truth | claims identify the actual authority and observed state |
| naming-invention | invents files, roles, surfaces, or compatibility contracts | names follow repository/product evidence |
| need-claims | declares a universal need or utility verdict without evaluation | recommendation states evidence, workload, and tradeoff |
| prompt-boundary | narrows or bypasses the named prompt/workflow surface | requested owner and scope remain intact |
| prompt-psychology | prompt context leaks verbatim or constraints backfire | output exhibits behavior without repeating scaffolding |
| prose-policing | style commentary replaces the requested engineering work | final answer contains required technical facts and effects |
| scope-consent | complaint, diagnosis, or context becomes unauthorized action | observable mutation matches explicit change authority |
| script-tool-evasion | deletes or bypasses tooling instead of tracing its contract | tool role and owning defect are established first |
| source-truth | stale examples or invented artifacts override canonical sources | current authoritative source controls the claim |
| structural | premature decomposition or placeholders replace owned behavior | boundaries follow lifecycle, contract, and evidence |
| tone-meta | apology, agreement, or self-analysis replaces the response | direct technical answer satisfies requested output |

## Case contract

Every issue entry contains:

- a trigger grounded in observable behavior;
- the observed failure;
- required behavior;
- an example;
- a falsifiable acceptance check;
- an evaluation-use section separating effects from final answers.

Delete or revise a case when it no longer reproduces against the target model.
A growing corpus is not inherently better; deduplicate cases that exercise the
same behavior.

## Routing

Use references/issue-lookup.md to choose a category and
references/issue-corpus-index.md to open the exact case. Load only the selected
entry and any official model guidance needed for the target.
