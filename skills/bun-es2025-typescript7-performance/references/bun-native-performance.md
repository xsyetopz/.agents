# Bun-native performance choices

Evaluate an API replacement at the boundary it removes. Prefer a Bun-native primitive only when it preserves the application’s observable behavior and measurably eliminates compatibility work, copies, parsing, syscall round trips, or dependency overhead. [EXAMPLE: BUN-TECH-ROUTES-FILES] [EXAMPLE: BUN-TECH-BYTE-VIEWS]

- For byte/file paths, track every conversion among string, `Buffer`, `Uint8Array`, `ArrayBuffer`, stream chunk, and JSON text. Use views or transfer ownership only while lifetime and mutation/aliasing rules remain valid. [EXAMPLE: BUN-TECH-BYTE-VIEWS]
- For HTTP, distinguish handler CPU from TLS, socket backpressure, compression, serialization, upstream waits, and load-generator capacity. Benchmark the deployed server configuration rather than a handler function in isolation. [EXAMPLE: BUN-TECH-ROUTES-FILES] [EXAMPLE: BUN-TECH-MACRO-GATE]
- Use `Bun.serve({ routes })` for known paths instead of a hot catch-all chain when route semantics permit; exact/parameter/wildcard precedence and static `Response` caching are part of the behavior to preserve. Static `Response` values suit fixed health/config/redirect payloads because Bun documents zero-allocation dispatch after initialization. Validate headers, reload behavior, and response mutability before sharing one. [EXAMPLE: BUN-TECH-ROUTES-FILES]
- Choose static versus file responses by access pattern: startup-buffered bytes remove per-request filesystem work but consume RAM; `new Response(Bun.file(path))`/directory routes preserve streaming, range handling, and backpressure for large or changing files. In production, prebuild imported HTML assets so bundling/transpilation is not on the request path. [EXAMPLE: BUN-TECH-ROUTES-FILES] [EXAMPLE: BUN-TECH-BUNDLING]
- For subprocesses and workers, include startup, message serialization/transfer, synchronization, exit/error handling, and cancellation costs. Reuse workers only when measured work amortizes those costs. [EXAMPLE: BUN-TECH-WORKERS]
- For bundling/compilation, measure artifact size, startup, deploy time, and production request behavior separately. A faster build can increase cold-start or runtime cost. [EXAMPLE: BUN-TECH-BUNDLING]

Do not substitute a runtime API merely to remove a package if it changes timeout, retry, streaming, backpressure, error, security, or portability semantics. [EXAMPLE: BUN-TECH-ROUTES-FILES] [EXAMPLE: BUN-TECH-ERROR-MIX]

## Source locations

- Bun runtime and API documentation: `https://bun.com/docs`
- Compiled executable runtime options: `https://bun.com/docs/bundler/executables`
