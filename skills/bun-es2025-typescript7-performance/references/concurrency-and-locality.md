# Bun concurrency, parallelism, locality, and NUMA

JavaScript async concurrency overlaps waits; it does not make CPU-bound work parallel. Measure CPU saturation, queueing, downstream capacity, heap/RSS, and tail latency before changing fan-out. [EXAMPLE: BUN-TECH-BACKPRESSURE]

- Bound in-flight work at the resource that saturates: upstream connection pool, database, disk, CPU, memory, or external rate limit. Add backpressure and cancellation rather than an unbounded promise queue. [EXAMPLE: BUN-TECH-BACKPRESSURE]
- Batch only while the resulting queue delay, memory retention, deadline, and durability semantics remain within contract. [EXAMPLE: BUN-TECH-DURABLE-IO] [EXAMPLE: BUN-TECH-BACKPRESSURE]
- Move CPU-heavy, independent work to workers/processes only if the measured work amortizes startup and message transfer. Keep messages compact; transfer/reuse bytes when ownership permits. [EXAMPLE: BUN-TECH-WORKERS] [EXAMPLE: BUN-TECH-BYTE-VIEWS]
- Prefer data-local partitions and ownership to cross-worker sharing. Measure worker count from one to saturation and stop before oversubscription raises tail latency. [EXAMPLE: BUN-TECH-WORKERS]
- Treat CPU affinity/NUMA policy as a deployment experiment. Validate on the actual hardware with the same container/cgroup policy; encode topology assumptions in portable application logic only with an operational owner. [EXAMPLE: BUN-TECH-NUMA]
