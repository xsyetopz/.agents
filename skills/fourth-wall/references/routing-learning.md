# Evidence-driven routing

Use this reference when a host records routing experiments or curates a dispatch policy from measured task results. It is not required for routine assignment selection.

Fourth Wall's dispatch matrix is a capability baseline, not a model ranking. AAII scores and prices supplied by a host may be stored as candidate metadata or an initial prior, but they must never become a fixed route table. Selection starts with an experiment assignment and ends with empirical learning from independently verified outcomes.

## Assignment contract

Before a comparable task runs, the host records a bounded assignment containing:

- a task-family, complexity, risk, and horizon stratum using the shared
  `single-agent`/`multi-agent` and `sequential`/`parallel`/`hybrid` vocabulary;
- the candidate set and selected model, reasoning effort, workflow topology,
  decomposition, role plan, context strategy, agent count, and parallelism;
- an experiment and policy revision, assignment method, and randomized
  propensity or reproducible seed; and
- the safety floor and eligibility constraints used for that assignment.

The host owns model selection, transport, credentials, and endpoint policy. The
repository runtime only binds the assignment to dispatch and pre-approval
evidence.
An assignment without its candidate set and propensity is observational data,
not evidence for changing policy.

## Measurement contract

Record one privacy-safe observation for every task attempt and join it to the
root task/run identity, runtime receipt, and dispatch digests. Never retain
prompts, paths, titles, secrets, or raw model output in the routing dataset.
Require a disjoint token ledger and include:

- model and reasoning effort for every stage, role, and agent;
- input, cached-input, uncached-input, output, and reasoning tokens, context
  estimates, and necessary versus accidental duplicated context;
- repeated repository reads, reprocessed tool results, coordinator, review,
  correction, retry, failed-loop, escalation, replacement, follow-up, and
  end-to-end latency tokens/counts;
- first-pass completion, terminal completion, deterministic checks, runtime
  smoke, independent review, root rescue, and the final verified-success bit;
- dispatch/receipt digests, policy/model revisions, and missing-join coverage.

`verified-success` is true only when the task reaches its causal acceptance
boundary, required objective checks and runtime proof pass, independent review
finds no material issue, and all verification fields are present. A missing
verification join, guardian allow, model-produced completion claim, or
source-only test is not sufficient.

Count workflow tokens as model usage plus separately measured, explicitly
disjoint coordinator and coordination overhead. Count duplicated context only
once as overhead; cached input is a usage attribute, not an additional copy.
Do not infer retries, escalation, or replacement from task names.

## Learning loop

1. Keep high-risk, security, migration, crash, and final-acceptance floors
   explicit. Never explore an ineligible candidate merely because its prior is
   cheap or highly rated.
2. For each comparable stratum, exercise every eligible candidate enough to
   clear the configured minimum-sample gate. Randomized assignment or a
   recorded propensity is required before comparing candidates.
3. Estimate expected workflow tokens per independently verified success. Keep
   unsuccessful work in the denominator and include retries, failed loops,
   context duplication, escalation, replacement, and coordinator overhead.
4. Reject candidates that fail the reliability/verification gate. Among the
   remaining candidates, prefer the lowest empirically supported expected
   tokens per successful task. Use money and latency only as secondary
   tie-breakers or explicit constraints.
5. Promote a route only after independent review and causal runtime proof. Keep
   the policy revision and evidence digest with the promotion; retain the
   candidate set, uncertainty, sample count, and missingness.
6. Escalate the task-family floor after failed acceptance or causal regression.
   Cool down only after the documented clean-success window, and reset the
   window after repair, rescue, or regression.

The `@skizzles/usage-analysis` routing API provides strict in-memory parsing, workflow-token accounting, stratified empirical summaries, and an acceptance-gated recommendation. It does not own a live model endpoint or silently change host policy.
