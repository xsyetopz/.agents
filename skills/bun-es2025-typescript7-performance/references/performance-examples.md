# Bun performance example map

This reference is the auditable example contract for the ten optimization-order items. Each stable ID has both exact-label **GOOD** and **RED** blocks. RED is an anti-pattern, not executable advice. Benchmark the representative macro workload, preserve semantics, and report repeated raw trials before accepting any change.

## Optimization-order map

| Item | Stable example ID | Primary decision |
| ---: | --- | --- |
| 1 | `BUN-OPT-01` | Remove repeated work, requests, parsing, serialization, copies, and initialization |
| 2 | `BUN-OPT-02` | Remove temporary allocations, closures, and Promise choreography |
| 3 | `BUN-OPT-03` | Preserve stable object shapes and simple representations |
| 4 | `BUN-OPT-04` | Use typed arrays/views/streaming only with ownership and lifetime proof |
| 5 | `BUN-OPT-05` | Improve contiguous locality and fuse only material-removing passes |
| 6 | `BUN-OPT-06` | Batch and bound I/O, queues, and downstream concurrency |
| 7 | `BUN-OPT-07` | Choose static routes, buffered files, or streaming by response semantics |
| 8 | `BUN-OPT-08` | Replace compatibility layers with measured Bun-native APIs |
| 9 | `BUN-OPT-09` | Specialize common cases and isolate cold/error paths |
| 10 | `BUN-OPT-10` | Tune build/topology/PGO only after application waste is addressed |

## Reference-technique coverage

Every technique in the six listed references is either shown by the mapped pair or grouped under that named pair. The ID is the auditable join key.

| Source reference | Technique or caveat | Example ID |
| --- | --- | --- |
| `benchmarking-and-profiling.md` | Micro versus macro benchmark boundary; realistic type/branch mix; warm-up; repeated independent trials; holdout; p50/p95/p99/errors/CPU/RSS/heap/queue metrics | `BUN-OPT-01` |
| `benchmarking-and-profiling.md` | CPU/heap profiles; JS heap versus native heap versus RSS; allocation/retention distinction | `BUN-OPT-02` |
| `benchmarking-and-profiling.md` | `heapStats`, heap snapshots, deliberate `Bun.gc`, `Bun.unsafe.mimallocDump`, and process faults | `BUN-OPT-02` |
| `benchmarking-and-profiling.md` | `mitata` micro harness and external `bombardier`/`oha`-style load generation | `BUN-OPT-01`, `BUN-OPT-06` |
| `benchmarking-and-profiling.md` | External load-generator capacity; durable-write batch/flush and filesystem access pattern | `BUN-OPT-06` |
| `benchmarking-and-profiling.md` | Noise-aware reviewed regression gates and baseline refresh | `BUN-OPT-10` |
| `bun-native-performance.md` | Byte/string/Buffer/Uint8Array/ArrayBuffer conversions, views, ownership, mutation, lifetime | `BUN-OPT-04` |
| `bun-native-performance.md` | `Bun.serve({ routes })`, exact precedence, static `Response`, response mutability | `BUN-OPT-07` |
| `bun-native-performance.md` | `Bun.file`, startup buffering versus streaming/range/backpressure | `BUN-OPT-07` |
| `bun-native-performance.md` | Worker/process startup, transfer, serialization, cancellation, reuse | `BUN-OPT-06` |
| `bun-native-performance.md` | Bundling/compilation artifact size, startup, deploy time, request behavior | `BUN-OPT-10` |
| `concurrency-and-locality.md` | Bounded in-flight work, backpressure, cancellation, downstream capacity | `BUN-OPT-06` |
| `concurrency-and-locality.md` | Batching and bounded memory/deadline semantics | `BUN-OPT-06` |
| `concurrency-and-locality.md` | Workers/processes, compact messages, transfer ownership, amortization | `BUN-OPT-06` |
| `concurrency-and-locality.md` | Data-local partitions and measured worker count | `BUN-OPT-05` |
| `concurrency-and-locality.md` | CPU affinity/NUMA as deployment-specific experiment | `BUN-OPT-10` |
| `dirty-optimization-patterns.md` | Mutable scratch buffers and hand-written loops | `BUN-OPT-02` |
| `dirty-optimization-patterns.md` | Shape-stable records and common-case specialization | `BUN-OPT-03`, `BUN-OPT-09` |
| `dirty-optimization-patterns.md` | Explicit queue bounds and byte views | `BUN-OPT-04`, `BUN-OPT-06` |
| `dirty-optimization-patterns.md` | Preserve rare semantics, validation, logging, durability, error handling, and security | `BUN-OPT-09` |
| `js-ts-hotpaths.md` | Hoist lookup tables/encoders/regex/configuration | `BUN-OPT-01` |
| `js-ts-hotpaths.md` | Fuse traversals without changing errors | `BUN-OPT-05` |
| `js-ts-hotpaths.md` | Spread/rest/slice/concat/map/filter/flatMap/JSON/string-copy removal | `BUN-OPT-02` |
| `js-ts-hotpaths.md` | Stable fields/value kinds; typed arrays and deliberate trust/mutation copies | `BUN-OPT-03`, `BUN-OPT-04` |
| `js-ts-hotpaths.md` | Avoid closure retention; verify Unicode, encoding, aliasing, cancellation, observability | `BUN-OPT-09` |
| `system-performance.md` | Macro topology, warm-up, holdout, repeated trials, load-generator ceiling | `BUN-OPT-01` |
| `system-performance.md` | Bottleneck identification, bounded queues, locality, process/worker count | `BUN-OPT-05`, `BUN-OPT-06` |
| `system-performance.md` | NUMA/CPU pinning and allocator policy only on matching hosts | `BUN-OPT-10` |
| `system-performance.md` | Runtime warm-up is not build PGO; supported native/compiler PGO training and holdout | `BUN-OPT-10` |
| `system-performance.md` | Correctness-first, noise-aware regression gate and reviewed baseline | `BUN-OPT-10` |

## Named technique coverage

| Stable technique ID | Source references | Required GOOD tokens |
| --- | --- | --- |
| `BUN-TECH-PROFILER` | `benchmarking-and-profiling.md`, `system-performance.md` | `--cpu-prof`, `heapStats`, `mimallocDump` |
| `BUN-TECH-MACRO-GATE` | `benchmarking-and-profiling.md`, `system-performance.md` | `oha`, `holdout`, `p99` |
| `BUN-TECH-DURABLE-IO` | `benchmarking-and-profiling.md` | `fsync`, `batch`, `p99` |
| `BUN-TECH-ROUTES-FILES` | `bun-native-performance.md` | `Bun.serve`, `Bun.file`, `routes` |
| `BUN-TECH-BYTE-VIEWS` | `bun-native-performance.md`, `js-ts-hotpaths.md` | `Uint8Array`, `lifetime` |
| `BUN-TECH-SHAPES-ALLOCS` | `dirty-optimization-patterns.md`, `js-ts-hotpaths.md` | `scratch`, `stableShape`, `copyCount` |
| `BUN-TECH-BACKPRESSURE` | `concurrency-and-locality.md` | `boundedDownstream`, `AbortSignal`, `downstream` |
| `BUN-TECH-WORKERS` | `bun-native-performance.md`, `concurrency-and-locality.md` | `Worker`, `pending`, `postMessage`, `AbortSignal`, `batch` |
| `BUN-TECH-BUNDLING` | `bun-native-performance.md`, `system-performance.md` | `bun build`, `artifact`, `startup` |
| `BUN-TECH-NUMA` | `concurrency-and-locality.md`, `system-performance.md` | `affinity`, `NUMA`, `holdout` |
| `BUN-TECH-PGO` | `system-performance.md` | `warm-up`, `PGO`, `native` |
| `BUN-TECH-WORKLOAD-MIX` | `benchmarking-and-profiling.md`, `system-performance.md` | `typeof`, `branch`, `warmupInput` |
| `BUN-TECH-TRIALS` | `benchmarking-and-profiling.md`, `system-performance.md` | `Bun`, `trials`, `process` |
| `BUN-TECH-COLD-STEADY` | `benchmarking-and-profiling.md`, `system-performance.md` | `cold`, `warmup`, `steady` |
| `BUN-TECH-MICRO` | `benchmarking-and-profiling.md` | `mitata`, `micro`, `consume` |
| `BUN-TECH-HOIST` | `js-ts-hotpaths.md` | `encoder`, `regex`, `lookup`, `config` |
| `BUN-TECH-CLOSURE` | `js-ts-hotpaths.md` | `closure`, `request`, `id` |
| `BUN-TECH-UNICODE` | `js-ts-hotpaths.md` | `TextEncoder`, `TextDecoder`, `unicode` |
| `BUN-TECH-ERROR-MIX` | `benchmarking-and-profiling.md`, `js-ts-hotpaths.md`, `system-performance.md` | `try`, `catch`, `error` |

## Paired examples

<a id="bun-opt-01"></a>
<!-- [EXAMPLE: BUN-OPT-01] -->
### `BUN-OPT-01` — remove repeated work

#### GOOD

```diff
--- a/src/handler.ts
+++ b/src/handler.ts
@@
-const payload = JSON.stringify(await buildPayload(id));
+const payload = cachedPayloadFor(id); // measured: removes repeated build/serialization
```

#### RED

```diff
--- a/src/handler.ts
+++ b/src/handler.ts
@@
+// Claims a faster microbenchmark while rebuilding and serializing on every request.
+const payload = JSON.stringify(await buildPayload(id));
```

<a id="bun-opt-02"></a>
<!-- [EXAMPLE: BUN-OPT-02] -->
### `BUN-OPT-02` — remove hot-path allocation

#### GOOD

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
-const out = parts.map(parsePart).filter(Boolean);
+const out: Part[] = [];
+for (const part of parts) if (parsePartInto(part, out)) continue;
```

#### RED

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
+const out = parts.map(parsePart).filter(Boolean); // unmeasured temporary arrays/callbacks
```

<a id="bun-opt-03"></a>
<!-- [EXAMPLE: BUN-OPT-03] -->
### `BUN-OPT-03` — stable object shapes

#### GOOD

```diff
--- a/src/record.ts
+++ b/src/record.ts
@@
+const record = { id: 0, value: 0, error: null as Error | null };
+record.error = failed ? err : null;
```

#### RED

```diff
--- a/src/record.ts
+++ b/src/record.ts
@@
+const record = failed ? { id, value, error: err } : { id, value }; // polymorphic shape
```

<a id="bun-opt-04"></a>
<!-- [EXAMPLE: BUN-OPT-04] -->
### `BUN-OPT-04` — bytes and lifetime

#### GOOD

```diff
--- a/src/bytes.ts
+++ b/src/bytes.ts
@@
-const bytes = input;
+const view = new Uint8Array(input.buffer, input.byteOffset, input.byteLength);
+consumeBytes(view);
```

#### RED

```diff
--- a/src/bytes.ts
+++ b/src/bytes.ts
@@
-const bytes = input;
+const copy = Uint8Array.from(input);
+consumeBytes(copy);
```

<a id="bun-opt-05"></a>
<!-- [EXAMPLE: BUN-OPT-05] -->
### `BUN-OPT-05` — locality and material intermediates

#### GOOD

```diff
--- a/src/index.ts
+++ b/src/index.ts
@@
-const ids = rows.map(row => row.id);
-const active = ids.filter(isActive);
+const active: number[] = [];
+for (const row of rows) if (isActive(row.id)) active.push(row.id);
```

#### RED

```diff
--- a/src/index.ts
+++ b/src/index.ts
@@
+const active = rows.map(row => row.id).filter(isActive); // no evidence fusion helps macro behavior
```

<a id="bun-opt-06"></a>
<!-- [EXAMPLE: BUN-OPT-06] -->
### `BUN-OPT-06` — bounded concurrency and backpressure

#### GOOD

```diff
--- a/src/fetch.ts
+++ b/src/fetch.ts
@@
-await Promise.all(urls.map(fetchOne));
+await mapWithLimit(urls, 32, fetchOne, { signal, onBackpressure: pauseProducer });
```

#### RED

```diff
--- a/src/fetch.ts
+++ b/src/fetch.ts
@@
+await Promise.all(urls.map(fetchOne)); // unbounded fan-out can overload downstream/RSS
```

<a id="bun-opt-07"></a>
<!-- [EXAMPLE: BUN-OPT-07] -->
### `BUN-OPT-07` — route and file response semantics

#### GOOD

```diff
--- a/src/server.ts
+++ b/src/server.ts
@@
-server = Bun.serve({ fetch: request => new Response(Bun.file("public/app.js")) });
+server = Bun.serve({ routes: { "/health": new Response("ok"), "/app.js": new Response(Bun.file("public/app.js")) } });
```

#### RED

```diff
--- a/src/server.ts
+++ b/src/server.ts
@@
+// Buffers a changing/large file without measuring RSS, range, or backpressure behavior.
+const body = await Bun.file(path).bytes();
+return new Response(body);
```

<a id="bun-opt-08"></a>
<!-- [EXAMPLE: BUN-OPT-08] -->
### `BUN-OPT-08` — measured native replacement

#### GOOD

```diff
--- a/src/read.ts
+++ b/src/read.ts
@@
-const text = await fs.promises.readFile(path, "utf8");
+const text = await Bun.file(path).text(); // benchmarked: semantics and errors match
```

#### RED

```diff
--- a/src/read.ts
+++ b/src/read.ts
@@
+import fs from "node:fs/promises";
+const text = await fs.readFile(path, "utf8"); // compatibility cost not measured against Bun.file
```

<a id="bun-opt-09"></a>
<!-- [EXAMPLE: BUN-OPT-09] -->
### `BUN-OPT-09` — common and cold paths

#### GOOD

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
+if (isCommonShape(input)) return parseCommon(input);
+return parseAndReportRareCase(input); // retains validation and observability
```

#### RED

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
+if (isCommonShape(input)) return fastParse(input);
+return undefined; // silently drops rare/error semantics
```

<a id="bun-opt-10"></a>
<!-- [EXAMPLE: BUN-OPT-10] -->
### `BUN-OPT-10` — topology/build/PGO evidence

#### GOOD

```diff
--- a/perf/decision.md
+++ b/perf/decision.md
@@
+gate --macro --trials=5 --holdout=fixtures/holdout --errors-first --metric=p99 --metric=RSS
+compare-artifacts release candidate --workers=4 --cpu=measured --rollback-on=holdout,p99,RSS
```

#### RED

```diff
--- a/perf/decision.md
+++ b/perf/decision.md
@@
+microbench --run=fastest --pgo --numa --native --no-holdout
```

## Caveats

A view can prolong a large backing buffer; static responses can change mutability/reload behavior; worker concurrency can overload downstream services; NUMA and PGO are deployment/toolchain-specific; and warm-up is not build PGO. Preserve backpressure, cancellation, correctness, portability, and the macro acceptance boundary.

## Named technique pairs

The following named pairs are the concrete coverage targets in the table above. Each pair keeps the mechanism small while making the required evidence and semantic caveat visible.

<!-- [EXAMPLE: BUN-TECH-PROFILER] -->
### `BUN-TECH-PROFILER` — profiler and memory-signal selection

#### GOOD

```diff
--- a/perf/capture.sh
+++ b/perf/capture.sh
@@
+bun --cpu-prof --heap-prof-md --cpu-prof-dir profiles ./perf/capture-metrics.ts
--- a/perf/capture-metrics.ts
+++ b/perf/capture-metrics.ts
@@
+import { heapStats } from "bun:jsc";
+await runRepresentativeWorkload();
+console.log(JSON.stringify({ heapStats: heapStats(), nativeHeap: Bun.unsafe.mimallocDump(), rss: process.memoryUsage().rss }));
```

#### RED

```diff
--- a/perf/capture.sh
+++ b/perf/capture.sh
@@
+bun --cpu-prof ./src/server.ts # CPU samples alone do not explain JS/native heap or RSS
```

<!-- [EXAMPLE: BUN-TECH-MACRO-GATE] -->
### `BUN-TECH-MACRO-GATE` — external representative gate

#### GOOD

```diff
--- a/perf/gate.sh
+++ b/perf/gate.sh
@@
+oha -z 60s -c 64 https://localhost:3000/api --output raw.json
+p99=$(extract_p99 raw.json); baseline_p99=$(extract_p99 baseline.json)
+gate --fail-on-p99-regression --max-p99="$baseline_p99" --holdout=fixtures/holdout.json --errors=raw.json
```

#### RED

```diff
--- a/perf/gate.sh
+++ b/perf/gate.sh
@@
+mitata bench-local-handler.ts # no external load, representative mix, p99, or holdout
```

<!-- [EXAMPLE: BUN-TECH-DURABLE-IO] -->
### `BUN-TECH-DURABLE-IO` — batching and durable tails

#### GOOD

```diff
--- a/src/writer.ts
+++ b/src/writer.ts
@@
+const batch = 64; await writeBatch(records, { batchSize: batch });
+await fsync(fd); const p99 = measureP99(completions); recordMetric("p99", p99);
```

#### RED

```diff
--- a/src/writer.ts
+++ b/src/writer.ts
@@
+buffer.push(...records); // throughput-only batch; no fsync, bound, or p99 evidence
```

<!-- [EXAMPLE: BUN-TECH-ROUTES-FILES] -->
### `BUN-TECH-ROUTES-FILES` — route/file response contract

#### GOOD

```diff
--- a/src/server.ts
+++ b/src/server.ts
@@
+const healthResponse = new Response("ok", { headers: { "cache-control": "no-store", "content-type": "text/plain" } });
+const reloadsPerRequest = true;
+const routes = {
+  "/health": healthResponse,
+  "/users/:id": (request: Request & { params: { id: string } }) => Response.json({ id: request.params.id }),
+  "/assets/*": (request: Request) => {
+    const filePath = new URL(`.${new URL(request.url).pathname}`, import.meta.url).pathname;
+    return new Response(Bun.file(filePath)); // lazy file read: reloads per request, streaming/range semantics stay intact
+  },
+};
+Bun.serve({ routes, fetch: () => new Response("not found", { status: 404 }) });
```

#### RED

```diff
--- a/src/server.ts
+++ b/src/server.ts
@@
+return new Response(await Bun.file(path).bytes()); // buffers without range/RSS/backpressure proof
```

<!-- [EXAMPLE: BUN-TECH-BYTE-VIEWS] -->
### `BUN-TECH-BYTE-VIEWS` — byte views and lifetime

#### GOOD

```diff
--- a/src/bytes.ts
+++ b/src/bytes.ts
@@
+const view = new Uint8Array(input.buffer, input.byteOffset + offset, length);
+const lifetimeBound = consumeBytes(view);
```

#### RED

```diff
--- a/src/bytes.ts
+++ b/src/bytes.ts
@@
+const copy = Uint8Array.from(input.subarray(offset, offset + length));
+const lifetimeBound = consumeBytes(copy);
```

<!-- [EXAMPLE: BUN-TECH-SHAPES-ALLOCS] -->
### `BUN-TECH-SHAPES-ALLOCS` — stable shapes and scratch storage

#### GOOD

```diff
--- a/src/scan.ts
+++ b/src/scan.ts
@@
+const scratch = new Array<number>(); // PERF: measured reuse within one synchronous call
+const stableShape = { id: 0, value: 0, error: null as Error | null };
+const copyCount = 0;
```

#### RED

```diff
--- a/src/scan.ts
+++ b/src/scan.ts
@@
+return { id, ...(failed ? { error } : {}), values: [...values] }; // shape/copy churn
```

<!-- [EXAMPLE: BUN-TECH-BACKPRESSURE] -->
### `BUN-TECH-BACKPRESSURE` — bounded async work

#### GOOD

```diff
--- a/src/fetch.ts
+++ b/src/fetch.ts
@@
+const boundedDownstream = new Semaphore(32);
+const downstreamCapacity = boundedDownstream.capacity;
+const downstream = boundedDownstream;
+await mapWithLimit(urls, boundedDownstream, fetchOne, { signal: AbortSignal.timeout(5000) });
```

#### RED

```diff
--- a/src/fetch.ts
+++ b/src/fetch.ts
@@
+await Promise.all(urls.map(fetchOne)); // unbounded downstream fan-out
```

<!-- [EXAMPLE: BUN-TECH-WORKERS] -->
### `BUN-TECH-WORKERS` — persistent worker protocol and lifecycle

#### GOOD

```diff
--- a/src/worker-pool.ts
+++ b/src/worker-pool.ts
@@
+type Pending = { resolve(value: unknown): void; reject(error: Error): void };
+const worker = new Worker(new URL("./worker.ts", import.meta.url).href);
+const pending = new Map<number, Pending>();
+let nextRequestId = 0;
+worker.onmessage = ({ data }) => { const request = pending.get(data.id); if (!request) return; pending.delete(data.id); data.error ? request.reject(new Error(data.error)) : request.resolve(data.value); };
+worker.addEventListener("error", (event) => { for (const request of pending.values()) request.reject(event.error ?? new Error("worker error")); pending.clear(); });
+worker.addEventListener("close", (event) => { for (const request of pending.values()) request.reject(new Error(`worker exited: ${event.code}`)); pending.clear(); });
+async function submit(batch: Uint8Array, signal: AbortSignal) {
+  const id = ++nextRequestId;
+  return new Promise((resolve, reject) => {
+    pending.set(id, { resolve, reject });
+    signal.addEventListener("abort", () => {
+      pending.delete(id);
+      reject(new DOMException("aborted", "AbortError"));
+    }, { once: true });
+    const message = { id, batch };
+    worker.postMessage(message, [batch.buffer]);
+  });
+}
+const signal = AbortSignal.timeout(5000);
+for (const batch of batches(records, 64)) await submit(batch, signal); // one persistent boundary; transfer, batching, cancellation, and correlation are explicit
```

#### RED

```diff
--- a/src/request.ts
+++ b/src/request.ts
@@
+const worker = new Worker("./job.ts"); // startup and serialization paid per request
+worker.postMessage(JSON.stringify(request));
```

<!-- [EXAMPLE: BUN-TECH-BUNDLING] -->
### `BUN-TECH-BUNDLING` — reproducible build and production comparison

#### GOOD

```diff
--- a/package.json
+++ b/package.json
@@
-{"scripts": {}}
+{"scripts": {"build": "bun build ./src/index.ts --outdir dist --minify"}}
--- a/perf/build-gate.sh
+++ b/perf/build-gate.sh
@@
+set -euo pipefail
+SOURCE_DATE_EPOCH=1700000000; export SOURCE_DATE_EPOCH; mkdir -p results
+for variant in baseline candidate; do
+  rm -rf "dist/$variant"; build_start=$(date +%s%3N)
+  bun build ./src/index.ts --outdir "dist/$variant" --minify
+  build_ms=$(( $(date +%s%3N) - build_start )); artifact_bytes=$(wc -c < "dist/$variant/index.js")
+  startup_ms=$(./perf/measure-startup.sh "dist/$variant/index.js")
+  deploy_start=$(date +%s%3N); ./perf/deploy-local.sh "dist/$variant"; deploy_ms=$(( $(date +%s%3N) - deploy_start ))
+  oha -z 60s -c 32 "http://127.0.0.1:3000/api?variant=$variant" --output "results/$variant.json"
+  record_production_behavior "$variant" "$build_ms" "$artifact_bytes" "$startup_ms" "$deploy_ms" "results/$variant.json"
+done
```

#### RED

```diff
--- a/src/server.ts
+++ b/src/server.ts
@@
+return await Bun.build({ entrypoints: [htmlPath] }); // bundling/transpilation on request path
```

<!-- [EXAMPLE: BUN-TECH-NUMA] -->
### `BUN-TECH-NUMA` — measured affinity experiment

#### GOOD

```diff
--- a/perf/topology.md
+++ b/perf/topology.md
@@
+const affinity = await runPinnedAndUnpinned(NUMANode.Production);
+const NUMA = NUMANode.Production;
+const holdout = recordMetrics(affinity); const p99 = holdout.p99; const rss = holdout.RSS;
```

#### RED

```diff
--- a/src/runtime.ts
+++ b/src/runtime.ts
@@
+process.setAffinity(0); // hard-coded topology assumption without NUMA evidence or holdout
```

<!-- [EXAMPLE: BUN-TECH-PGO] -->
### `BUN-TECH-PGO` — warm-up versus supported build PGO

#### GOOD

```diff
--- a/perf/pgo.md
+++ b/perf/pgo.md
@@
+warmup_label=warm-up; PGO_MODE=native; PGO=verified compare --release --pgo --holdout=fixtures/holdout
+test -n "$PGO_MODE" && record_artifact_metrics release pgo
```

#### RED

```diff
--- a/perf/pgo.md
+++ b/perf/pgo.md
@@
+PGO_MODE=runtime compare --label=warm-up --single-microbenchmark
```

<!-- [EXAMPLE: BUN-TECH-WORKLOAD-MIX] -->
### `BUN-TECH-WORKLOAD-MIX` — realistic type and branch mix

#### GOOD

```diff
--- a/perf/workload.ts
+++ b/perf/workload.ts
@@
+const warmupInput = inputs.small.concat(inputs.medium, inputs.large);
+for (const value of warmupInput) { const branch = typeof value === "string"; consume(branch ? parseText(value) : parseBytes(value)); }
```

#### RED

```diff
--- a/perf/workload.ts
+++ b/perf/workload.ts
@@
+for (const value of ["same-shape", "same-shape"]) consume(parseText(value));
```

<!-- [EXAMPLE: BUN-TECH-TRIALS] -->
### `BUN-TECH-TRIALS` — independent process trials

#### GOOD

```diff
--- a/perf/trials.ts
+++ b/perf/trials.ts
@@
+const trials = [1, 2, 3, 4, 5]; const results: Array<{ trial: number; status: number }> = [];
+for (const trial of trials) {
+  const child = Bun.spawn([process.execPath, "run", "bench.ts", `--trial=${trial}`]);
+  const exitCode = await child.exited; if (exitCode !== 0) throw new Error(`trial ${trial} failed`);
+  results.push({ trial, status: exitCode });
+}
+const processCount = results.length;
```

#### RED

```diff
--- a/perf/trials.ts
+++ b/perf/trials.ts
@@
+for (const trial of trials) runInSameProcess(trial); // same warmed process, not independent Bun processes
```

<!-- [EXAMPLE: BUN-TECH-COLD-STEADY] -->
### `BUN-TECH-COLD-STEADY` — cold start versus steady state

#### GOOD

```diff
--- a/perf/run.sh
+++ b/perf/run.sh
@@
+measure --label=cold ./start.sh
+./warmup.sh 30s; measure --label=steady ./load.sh 60s
```

#### RED

```diff
--- a/perf/run.sh
+++ b/perf/run.sh
@@
+./load.sh 1s # mixes cold startup with an unstabilized steady result
```

<!-- [EXAMPLE: BUN-TECH-MICRO] -->
### `BUN-TECH-MICRO` — consumed local mechanism

#### GOOD

```diff
--- a/bench/encode.ts
+++ b/bench/encode.ts
@@
+const micro = mitata("encode", () => { const value = encode(input); consume(value); });
```

#### RED

```diff
--- a/bench/encode.ts
+++ b/bench/encode.ts
@@
+mitata("micro encode", () => encode(input)); // result not consumed; optimizer/harness may mislead
```

<!-- [EXAMPLE: BUN-TECH-HOIST] -->
### `BUN-TECH-HOIST` — hoisted immutable helpers

#### GOOD

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
+const encoder = new TextEncoder(); const regex = /item/g; const lookup = new Map(table);
+const config = Object.freeze(runtimeConfig);
+function parse(value: string) { return lookup.get(value) ?? encoder.encode(value.replace(regex, config.replacement)); }
```

#### RED

```diff
--- a/src/parse.ts
+++ b/src/parse.ts
@@
+function parse(value: string) { return new TextEncoder().encode(value.replace(/item/g, "")); }
```

<!-- [EXAMPLE: BUN-TECH-CLOSURE] -->
### `BUN-TECH-CLOSURE` — closure retention

#### GOOD

```diff
--- a/src/cache.ts
+++ b/src/cache.ts
@@
+const id = request.id;
+const closure = () => cache.get(id);
+return closure(); // closure retains only the small id, not the request/body
```

#### RED

```diff
--- a/src/cache.ts
+++ b/src/cache.ts
@@
+return () => cache.get(request.id); // closure retains the complete request and body
```

<!-- [EXAMPLE: BUN-TECH-UNICODE] -->
### `BUN-TECH-UNICODE` — encoding correctness

#### GOOD

```diff
--- a/src/text.ts
+++ b/src/text.ts
@@
+const bytes = new TextEncoder().encode(unicode);
+const roundTrip = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
+assert(roundTrip === unicode);
```

#### RED

```diff
--- a/src/text.ts
+++ b/src/text.ts
@@
+const bytes = Buffer.from(unicode); // implicit encoding can alter malformed/unicode behavior
+assert(bytes.toString() === unicode);
```

<!-- [EXAMPLE: BUN-TECH-ERROR-MIX] -->
### `BUN-TECH-ERROR-MIX` — exception timing and error mix

#### GOOD

```diff
--- a/src/decode.ts
+++ b/src/decode.ts
@@
+try { return decode(input); } catch (error) { record(error); throw error; }
+for (const input of [valid, malformed, timeout]) measureErrorTiming(() => decode(input));
```

#### RED

```diff
--- a/src/decode.ts
+++ b/src/decode.ts
@@
+return decode(input) ?? fallback; // changes error timing and hides the error mix
```
