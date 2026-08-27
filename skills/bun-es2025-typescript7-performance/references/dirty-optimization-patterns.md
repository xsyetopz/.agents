# Deliberately non-idiomatic Bun optimizations

Use a non-idiomatic rewrite only when a representative measurement identifies the cost and the code can state the preserved invariant. [EXAMPLE: BUN-TECH-SHAPES-ALLOCS] [EXAMPLE: BUN-TECH-BYTE-VIEWS]

Examples include mutable scratch buffers, hand-written loops instead of allocation-heavy combinators, shape-stable records, specialization for a dominant input class, explicit queue bounds, and byte views that avoid copies. Place a `PERF:` comment beside each choice with the workload/metric and invariant. Keep a simpler reference path when it is required for rare semantics; test both paths. [EXAMPLE: BUN-TECH-SHAPES-ALLOCS] [EXAMPLE: BUN-TECH-BACKPRESSURE] [EXAMPLE: BUN-TECH-BYTE-VIEWS]

Do not use mutable reuse across requests, workers, async callbacks, or cancellation boundaries unless ownership is provable. Do not turn off validation, logging, error handling, durability, or security checks without an explicit contract change. [EXAMPLE: BUN-TECH-BYTE-VIEWS] [EXAMPLE: BUN-TECH-ERROR-MIX]
