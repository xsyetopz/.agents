# Prior-art protocol for empirical skill guidance

This is a concise source/protocol index, not a literature review. The IDs below are supporting prior art to retrieve and verify before making a claim:

`2603.03298` · `2312.08642` · `2404.02800` · `2504.07408` · `2512.04106` · `2506.21182` · `2603.26137` · `2605.29059` · `2603.14019` · `2508.02868`

## Transfer rule

Treat a paper's result as **source evidence**, not as a universal rule. Transfer to a skill only as an explicitly labeled inference, after checking the paper's task, model/runtime, workload, controls, and metric. Prompting studies are domain/model-specific; retrieved or synthetic examples can be wrong or overfit; replay traces miss unseen behavior. Keep representative holdouts, semantic/correctness gates, repeated raw trials, and threats to validity in the report.

## Minimal protocol

1. Retrieve the primary record and record title, version/date, task, model/runtime, workload, controls, and metric.
2. State the local hypothesis and the exact mechanism believed to transfer; label that mechanism **INFERENCE**.
3. Reproduce or replay the smallest relevant case, then test representative and holdout cases against a baseline/control.
4. Reject universal wording when the local environment, task, or acceptance metric differs; record the limitation and rollback condition.

The IDs are deliberately kept without synthesized titles here: source identity and claims must be verified at use time rather than guessed from an identifier.
