# Source index

Use primary documentation for version-sensitive claims; verify the installed
runtime/compiler rather than assuming a URL or feature applies to every patch.

## Official sources

- Bun 1.4 release: <https://bun.com/blog/bun-v1.4>
- Bun benchmarking, memory, CPU/heap profiling: <https://bun.com/docs/project/benchmarking>
- Bun HTTP server and routes/static/file responses: <https://bun.com/docs/runtime/http/server> and <https://bun.com/docs/runtime/http/routing>
- Bun TypeScript runtime: <https://bun.com/docs/runtime/typescript>
- Bun TypeScript 6/7 compatibility: <https://bun.com/docs/typescript-6>
- TypeScript 7 stable announcement: <https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/>
- ECMAScript 2025 standard: <https://tc39.es/ecma262/2025/>

## Relevant prior art

- arXiv:2605.23570, *Misleading Microbenchmarks on the Java Virtual Machines* — managed-runtime profile-realism warning; JVM evidence only, used here to motivate JSC application-context validation: <https://arxiv.org/abs/2605.23570>
- arXiv:2212.09515, *Using Microbenchmark Suites to Detect Application Performance Changes* — micro suites can detect changes but can produce false positives: <https://arxiv.org/abs/2212.09515>
- arXiv:2501.12878, *μOpTime* — stability-based repetition budgets are useful, but metric choice is project/language-specific: <https://arxiv.org/abs/2501.12878>
- arXiv:2211.13525, *Evaluating Search-Based Software Microbenchmark Prioritization* — simple historical prioritization can be effective, but cannot cover novel paths: <https://arxiv.org/abs/2211.13525>
