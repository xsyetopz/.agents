# JS/TS hot paths: work, allocation, and copies

Use profiles and allocation evidence to identify an operation that occurs often enough to matter. Then inspect its data movement and object lifetime. [EXAMPLE: BUN-TECH-PROFILER] [EXAMPLE: BUN-TECH-SHAPES-ALLOCS]

## Common high-value changes

- Hoist immutable lookup tables, encoders/decoders, regexes, and configuration out of repeated paths. [EXAMPLE: BUN-TECH-HOIST]
- Fuse traversals only when it removes measured intermediate collections or callback/closure churn without obscuring error semantics. [EXAMPLE: BUN-OPT-05]
- Replace spread/rest, `slice`, `concat`, chained `map`/`filter`/`flatMap`, JSON round trips, and string re-encoding only when they create demonstrated copies or temporary retention. [EXAMPLE: BUN-TECH-SHAPES-ALLOCS]
- Keep frequently accessed objects initialized consistently; avoid adding/removing properties or changing value kinds inside a loop. [EXAMPLE: BUN-TECH-SHAPES-ALLOCS]
- Use typed arrays and byte views for binary data when consumers can operate on the same backing storage. Copy at trust, mutation, ownership, or lifetime boundaries deliberately. [EXAMPLE: BUN-TECH-BYTE-VIEWS]
- Avoid retaining an entire request, response, cache, or large buffer through a closure when only a small value is required. [EXAMPLE: BUN-TECH-CLOSURE]

## Checks before merging

Verify numerical behavior, Unicode/encoding, aliasing/mutation ownership, buffer lifetime, exception/error timing, cancellation, and observability. A hot path with less allocation but higher retained memory is not automatically better. [EXAMPLE: BUN-TECH-UNICODE] [EXAMPLE: BUN-TECH-ERROR-MIX] [EXAMPLE: BUN-TECH-BYTE-VIEWS]
