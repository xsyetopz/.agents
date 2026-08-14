# Source Traceability Manifest

Retrieved and assembled: 2026-07-27.

The skill distinguishes three source classes:

1. **Format and host behavior** - current official product documentation and the Agent Skills specification.
2. **Architecture foundations** - original papers, standards, method owners, and authoritative pattern descriptions.
3. **Domain mechanics** - language/runtime/protocol specifications and official implementation documentation.

Prompt-facing instructions additionally use current official OpenAI model
guidance. Model-specific claims must be refreshed before a new prompt migration;
the repository snapshot is traceability evidence, not permanent authority.

## Source-to-artifact map

| Skill area | Principal source families | Files informed |
| --- | --- | --- |
| Skill package format and progressive disclosure | OpenAI Build Skills, Agent Skills specification/best practices, OpenAI eval guidance, Claude Code skills | `SKILL.md`, `README.md`, validators, eval cases |
| MVC semantic meaning | Original Smalltalk-80 MVC description | core model, pattern catalog, domain mappings, worked examples |
| DDD and bounded contexts | Evans DDD Reference | core model, decision procedure, context template, enterprise example |
| Information hiding and change boundaries | Parnas module-decomposition paper | core model, component contracts, decision procedure |
| Ports and adapters | Cockburn Hexagonal Architecture | pattern catalog, domain mappings, component contracts |
| State machines and actors | Harel statecharts; Hewitt actor formalism | pattern catalog, flowgraphs, runtime and agent mappings |
| Quality-attribute tradeoffs | SEI ATAM; ISO/IEC/IEEE 42010 concepts | decision procedure, rigor modes, report/eval templates |
| Architecture views and decisions | C4 model; Nygard ADR | artifact contracts and templates |
| Compiler and runtime decomposition | MLIR IR/pass management; JVM specification; WebAssembly specification | domain mappings, flowgraphs, compiler example |
| CLI/TUI interaction | POSIX utility syntax; Elm Architecture | domain mappings, flowgraphs, TUI example |
| Binary/protocol correctness | Protocol Buffers encoding; Kaitai Struct; relevant protocol specs | domain mappings, binary example, verification rules |
| Agent orchestration and persistence | OpenAI Agents SDK; Anthropic agent/harness guidance; MCP architecture | agent mappings, flowgraphs, agent-harness example, eval cases |
| GPT-5.6 prompt behavior | Current OpenAI model guidance and prompt-engineering guide | SKILL.md activation/workflow, prompt-facing templates, routing and behavioral eval rules |

## Evidence policy

The bibliography stores links, not copied publications. Open and inspect the
applicable current source before making a source-dependent claim. Record the
claim, version or retrieval date, and evidence location in the evidence ledger.
Evaluate tool/filesystem effects separately from the final answer when the claim
concerns agent behavior.

See `references/09-bibliography.md` for the full curated list.
