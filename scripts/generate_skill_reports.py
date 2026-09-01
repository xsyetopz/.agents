#!/usr/bin/env python3
"""Generate the canonical performance report templates."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path

MARKER = "<!-- GENERATED FILE. Regenerate with scripts/generate_skill_reports.py. -->"
REPORT_TARGETS = {
    "bun-typescript-performance-optimization": Path(
        "skills/bun-typescript-performance-optimization/assets/PR_PERF_REPORT.md"
    ),
    "rust-performance-optimization": Path(
        "skills/rust-performance-optimization/assets/PR_PERF_REPORT.md"
    ),
}
METRIC_HINTS = {
    "bun-typescript-performance-optimization": "Bun-specific metrics: JS heap, native heap, RSS, GC, queue/backpressure, load-generator capacity.",
    "rust-performance-optimization": "Rust-specific metrics: allocations/copies, lock/cache/syscall signals, RSS, binary size/i-cache, target CPU/NUMA.",
}


def discover_report_paths(root: Path) -> dict[str, Path]:
    """Return the explicit performance report targets owned by this generator."""

    return {
        skill: root / relative_path for skill, relative_path in REPORT_TARGETS.items()
    }


def render_report(skill: str) -> str:
    metric_hint = METRIC_HINTS.get(
        skill,
        "Skill-specific metrics: name the metric that controls this decision and its collection method.",
    )
    return f"""# Controlled empirical evidence report

{MARKER}

> Generated for `{skill}`. Use this shared report shape for the skill.

## Decision summary

- Decision:
- Evidence status:
- Acceptance result:

## Fixed scope and hypothesis

- Scope and acceptance boundary:
- Hypothesis and mechanism:
- Preserved semantic, safety, compatibility, and resource contracts:

## Baseline/control

- Baseline revision/artifact:
- Control configuration and comparison:
- Baseline selection rationale:

## Environment

- Runtime/compiler/tool versions:
- OS, CPU, container/cgroup, memory, affinity/NUMA, and deployment topology:
- Repository revision, flags, dependency/lockfile state, and relevant configuration:

## Workload/cases

- Representative workload matrix (input/payload distribution, access pattern, concurrency, cache state, errors/retries, downstream behavior):
- Warm-up/cold-start treatment and duration:
- Holdout workload/cases not used for tuning:

## Intervention

- Changed paths and owning decision:
- Exact commands/configuration used:
- Safety/ownership/lifetime/backpressure/durability invariants:

## Metrics/results

{metric_hint}

| Scope | Case | Trial | Before/control | After/candidate | Delta | Raw result/variation | Command or artifact |
|---|---|---:|---:|---:|---:|---|---|
| Micro |  | 1 |  |  |  |  |  |
| Macro |  | 1 |  |  |  |  |  |
| Holdout |  | 1 |  |  |  |  |  |

- Report repeated independent raw trials, distributions/spread, throughput, p50/p95/p99, errors/timeouts, CPU, memory, and bottleneck-specific signals as applicable.

## Semantic/correctness gates

- Tests, type/build checks, replay/output comparison, and invariant checks:
- Error, ordering, cancellation, ownership/lifetime, portability, and security results:

## Threats to validity

- Runner noise, workload representativeness, holdout limits, profiler/measurement bias:
- Unseen behavior, environment drift, model/runtime specificity, and remaining confounders:

## Reproduction commands

```text
# Pin environment and run the baseline/control:
# Pin environment and run the candidate/intervention:
# Run semantic/correctness gates and holdout:
```

## Decision/rollback

- Decision and acceptance rule:
- Rollback condition and preserved baseline/artifact:
- Baseline refresh or follow-up review path:

## Unresolved risks

-
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write canonical templates")
    mode.add_argument(
        "--check", action="store_true", help="fail when a template drifts"
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    drifted = False
    for skill, path in discover_report_paths(root).items():
        expected = render_report(skill)
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            print(f"generated {path.relative_to(root)}")
            continue
        if not path.exists():
            drifted = True
            print(f"drift: missing {path.relative_to(root)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual == expected:
            continue
        drifted = True
        print(f"drift: {path.relative_to(root)}")
        diff = difflib.unified_diff(
            actual.splitlines(),
            expected.splitlines(),
            fromfile=str(path),
            tofile=f"{path} (canonical)",
            lineterm="",
        )
        print("\n".join(diff))

    if args.check:
        if drifted:
            return 1
        print(f"report templates in sync ({len(REPORT_TARGETS)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
