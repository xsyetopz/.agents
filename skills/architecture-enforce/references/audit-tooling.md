# Executable architecture tooling

Use the bundled adapter for tool discovery and syntax evidence. It never
installs software, executes repository-provided shell commands, rewrites files,
or treats a missing provider as a clean result.

## Capability preflight

```bash
python3 scripts/providers.py capabilities --root <repo> --format json
```

The report distinguishes `ready` from `unavailable` and records the resolved
binary and version. Providers include ast-grep, Semgrep, Tree-sitter, clangd,
Cargo, Go, CMake, Ninja, Xmake, and Conan. Availability is not proof that a
provider has the project grammar, compilation database, build directory, or
manifest it needs.

## Read-only AST query

```bash
python3 scripts/providers.py ast-query \
  --root <repo> --tool ast-grep --language rust \
  --pattern 'unsafe { $$$BODY }' --rule-id unsafe-block \
  --severity warning --message 'review unsafe boundary' src
```

The adapter invokes `ast-grep run --json=stream --color never` with direct
arguments and validates every returned range and path against `<repo>`. It
returns a versioned envelope with provider version, argv, exit status, timing,
SHA-256 digests, normalized findings, and diagnostics. Exit codes are `0` for
clean, `1` for matches, `3` for unavailable, `4` for provider failure, `5` for
timeout/resource failure, and `6` for malformed output.

## Repository rules

The bundled audit always runs its inline-test/benchmark detector independently
of repository configuration. Add repeatable supplemental syntax gates to
`.architecture-enforcement.json` without putting commands in repository
configuration:

```json
{
  "syntax_rules": [
    {
      "id": "forbidden-python-import",
      "tool": "ast-grep",
      "language": "python",
      "pattern": "import $MODULE",
      "severity": "error",
      "message": "this module crosses the protected boundary",
      "mode": "required",
      "paths": ["src"]
    }
  ]
}
```

If a runner owns a custom test source set that cannot use the exact bundled
path conventions, document its exact root for provenance. This metadata is not
an acceptance exemption and never turns off the detector:

```json
{
  "test_source_roots": [
    {
      "path": "qa",
      "reason": "JUnit source set declared by the build runner",
      "owner": "quality platform",
      "control": "JUnit source-set discovery check",
      "review": "remove on build runner upgrade"
    }
  ]
}
```

Configured test-source roots are rejected by the acceptance audit; repository
metadata cannot reclassify production source or waive the inline-test gate.
Use only the scanner's built-in test-source conventions.

Syntax rules must use `mode: "required"` and severity `error` or `warning`.
`advisory` mode and `notice` severity are invalid policy. Required rules fail
closed on `blocked`, `timeout`, `tool-failed`, or `invalid-output`. Filename
and structural inventory findings are also enforced; an inventory evidence
label is not a severity downgrade. A supplemental rule cannot replace or waive
a bundled finding. Do not lower severity, disable a
rule/provider/job, override thresholds or baselines, exclude paths, add an
ignore or exception, set `allow-failure` or `continue-on-error`, or
weaken/delete tests to obtain a passing acceptance result. Fix the owning
cause; a suspected tool defect needs a minimal reproducer and explicit
policy-change authorization while the gate remains blocked.

## Package graph

Use the native resolver without configuring or generating a build:

```bash
python3 scripts/providers.py graph --root <repo> --tool auto --format json
```

`cargo-metadata` consumes `cargo metadata --format-version=1 --no-deps`; `go-list`
consumes `go list -json ./...`. The adapter accepts only structured JSON, keeps
provider diagnostics and digests, and reports resolver failures as
`tool-failed` rather than inventing a dependency graph.
