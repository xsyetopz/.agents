# Rust concurrency, locality, and NUMA

Scale from one worker to saturation and identify the first saturated resource. Report throughput and tail latency together with CPU, runnable/blocked work, queue depth, lock contention, allocator activity, remote-memory indicators, and memory use. Compare async task count with actual worker parallelism; tasks overlap waits while CPU cores determine parallel execution. [EXAMPLE: RUST-TECH-ATOMIC-LOCK] [EXAMPLE: RUST-TECH-NUMA]

- Use ownership partitioning, sharding, batching, and bounded queues before weakening atomic ordering or adding threads. [EXAMPLE: RUST-TECH-ATOMIC-LOCK] [EXAMPLE: RUST-TECH-PIPELINE-IO]
- Preserve backpressure, cancellation, fairness, shutdown, and panic propagation. A higher steady-state throughput that creates unbounded queues or unacceptable tails is not a valid optimization. [EXAMPLE: RUST-TECH-ATOMIC-LOCK] [EXAMPLE: RUST-TECH-ERROR-EDGES]
- Reduce shared mutable state and cross-core handoffs; place data with the worker that most often reads/writes it when the measured workload allows. [EXAMPLE: RUST-TECH-NUMA]
- Batch messages and pipeline stages at explicit boundaries. For filesystem or durable storage, sweep batch sizes and both sequential/random access, reporting throughput and completion tails; never trade away flush, ordering, or failure semantics for a benchmark result. This follows the durable-I/O measurement caution in arXiv:2002.07515. [EXAMPLE: RUST-TECH-PIPELINE-IO]
- Treat atomics and lock choice as correctness-sensitive. Select an ordering from the required happens-before relation, then prove it—not from a throughput result alone. [EXAMPLE: RUST-TECH-ATOMIC-LOCK]
- Test NUMA affinity, allocator locality, and first-touch behavior only on the deployment topology. Compare pinned and unpinned runs under the same cgroup/container policy, and retain portable defaults unless operations owns the placement configuration. Include uncontended/single-thread runs, migration rates, fairness/starvation, and tail latency; a contended lock win is insufficient. arXiv:1810.05600 motivates local lock handoff under contention but does not justify a universal lock or placement policy. [EXAMPLE: RUST-TECH-NUMA]

Do not claim CPU parallel speedup from async task count, nor generalize a machine-specific NUMA result to different hosts. [EXAMPLE: RUST-TECH-NUMA] [EXAMPLE: RUST-TECH-ATOMIC-LOCK]
