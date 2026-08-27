# Bibliography and Primary References

> Package-local primary/standards source map, not a verified citation set or generated snapshot; source gap: check the exact source, version, and retrieval date. Live verification is required for current behavior.

This bibliography is a source map, not a reading list to copy mechanically. Prefer the primary source that defines a concept, standard, protocol, or tool. Verify publication versions and current product behavior before relying on them.

## GitHub Mermaid compatibility

GitHub requires Mermaid syntax inside a fenced code block with the `mermaid`
language identifier and warns that third-party Mermaid plugins can produce
different results. To inspect the renderer version currently used by GitHub,
render an `info` diagram before relying on version-sensitive syntax. The
architecture diagrams in this package therefore use stable node IDs, quoted
labels where punctuation could be ambiguous, and `A -->|label| B` edge labels.

- [GitHub Docs: Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) - primary renderer and syntax guidance (checked 2026-08-14; re-check live behavior when publishing).

## Agent Skills and coding agents

1. OpenAI, **Build skills** - required `SKILL.md`, optional `scripts/`, `references/`, and `assets/`, progressive disclosure, and Codex/ChatGPT invocation.
   - <https://developers.openai.com/codex/build-skills>
2. Agent Skills, **Specification** - portable directory and frontmatter rules.
   - <https://agentskills.io/specification>
3. Agent Skills, **Skill creation best practices** - concise core instructions, progressive disclosure, and calibrated strictness.
   - <https://agentskills.io/skill-creation/best-practices>
4. OpenAI, **Evaluate skills** - trigger, process, outcome, style, and efficiency evaluation.
   - <https://developers.openai.com/blog/eval-skills>
5. OpenAI, **Codex customization** - repository and user-level instruction/skill discovery.
   - <https://developers.openai.com/codex/customization>
6. OpenAI API, **Skills** - zip/upload packaging and skill containers.
   - <https://platform.openai.com/docs/guides/tools-skills>
7. Anthropic, **Agent Skills in Claude Code** - compatible `SKILL.md` organization and invocation.
   - <https://docs.anthropic.com/en/docs/claude-code/skills>
8. OpenAI, **Agents SDK** - agents, handoffs, guardrails, sessions, tracing, and orchestration.
   - <https://openai.github.io/openai-agents-python/>
9. Anthropic, **Building effective agents** - workflows versus autonomous agents and composable patterns.
   - <https://www.anthropic.com/research/building-effective-agents>
10. Anthropic, **Effective harnesses for long-running agents** - continuity, progress files, clean initialization, and incremental work.
    - <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
11. Model Context Protocol, **Architecture** - host/client/server boundaries and capability negotiation.
    - <https://modelcontextprotocol.io/docs/learn/architecture>

## Foundations of architecture and modularity

 1. Trygve Reenskaug; Glenn Krasner; Stephen Pope, **A Description of the Model-View-Controller User Interface Paradigm in the Smalltalk-80 System**.
    - <https://folk.universitetetioslo.no/trygver/2007/MVC_Originals.pdf>
 2. Eric Evans, **Domain-Driven Design Reference** - bounded contexts, ubiquitous language, model-driven design, aggregates, repositories, and context mapping.
    - <https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf>
 3. Alistair Cockburn, **Hexagonal Architecture** - ports and adapters around application semantics.
    - <https://alistair.cockburn.us/hexagonal-architecture>
 4. David Parnas, **On the Criteria To Be Used in Decomposing Systems into Modules** - information hiding and design decisions likely to change.
    - <https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf>
 5. David Harel, **Statecharts: A Visual Formalism for Complex Systems** - hierarchy, concurrency, and history for stateful reactive systems.
    - <https://www.inf.ed.ac.uk/teaching/courses/seoc/2005_2006/resources/statecharts.pdf>
 6. Carl Hewitt; Peter Bishop; Richard Steiger, **A Universal Modular ACTOR Formalism for Artificial Intelligence**.
    - <https://www.ijcai.org/Proceedings/73/Papers/027B.pdf>
 7. Martin Fowler, **CQRS** - separating mutation models from query models when divergent models are justified.
    - <https://martinfowler.com/bliki/CQRS.html>
 8. Roy Fielding, **Architectural Styles and the Design of Network-based Software Architectures**.
    - <https://ics.uci.edu/~fielding/pubs/dissertation/top.htm>

## Architecture evaluation and representation

 1. Software Engineering Institute, **Architecture Tradeoff Analysis Method (ATAM)**.
    - <https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/>
 2. Simon Brown, **The C4 model for visualising software architecture**.
    - <https://c4model.com/>
 3. Michael Nygard, **Documenting Architecture Decisions** - lightweight ADR structure.
    - <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
 4. ISO/IEC/IEEE 42010, **Systems and software engineering - Architecture description**.
    - <https://www.iso.org/standard/74393.html>

## Compilers, interpreters, and runtimes

 1. LLVM Project, **MLIR Language Reference** - operations, regions, blocks, values, types, and attributes.
    - <https://mlir.llvm.org/docs/LangRef/>
 2. LLVM Project, **MLIR Pass Management** - pass nesting, analysis preservation, scheduling, and instrumentation.
    - <https://mlir.llvm.org/docs/PassManagement/>
 3. Oracle, **The Java Virtual Machine Specification** - class format, runtime data areas, execution, linking, and loading.
    - <https://docs.oracle.com/javase/specs/jvms/se25/html/>
 4. WebAssembly Community Group, **WebAssembly Core Specification** - validation, execution, store, modules, and embedding.
    - <https://webassembly.github.io/spec/core/>
 5. Language Server Protocol, **Specification** - client/server language tooling contracts.
    - <https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/>
 6. DWARF Debugging Information Format Committee, **DWARF Standard**.
    - <https://dwarfstd.org/>

## CLI, TUI, protocols, and binary data

 1. The Open Group, **Utility Syntax Guidelines** - portable command-line option conventions.
    - <https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html>
 2. Elm, **The Elm Architecture** - model, update, view, and commands/subscriptions.
    - <https://guide.elm-lang.org/architecture/>
 3. Protocol Buffers, **Encoding** - wire types, tags, scalar encoding, and parser implications.
    - <https://protobuf.dev/programming-guides/encoding/>
 4. Kaitai Struct, **User Guide** - declarative binary format descriptions and generated parsers.
    - <https://doc.kaitai.io/user_guide.html>
 5. IETF, **RFC 2119 / RFC 8174** - normative requirement language.
    - <https://www.rfc-editor.org/rfc/rfc2119>
    - <https://www.rfc-editor.org/rfc/rfc8174>

## Web and enterprise application structure

 1. Microsoft, **Overview of ASP.NET Core MVC** - web MVC concerns and request handling.
    - <https://learn.microsoft.com/aspnet/core/mvc/overview>
 2. Microsoft, **.NET Microservices: Architecture for containerized .NET applications** - domain/application/infrastructure boundaries and distributed-system tradeoffs.
    - <https://learn.microsoft.com/dotnet/architecture/microservices/>
 3. Chris Richardson, **Microservices patterns** - sagas, transactional outbox, API composition, and related distributed data patterns.
    - <https://microservices.io/patterns/>

## Source-selection boundary

Use a primary specification or paper when one exists, open the source, locate the
relevant passage, and record its version, retrieval date, exact claim,
preconditions, and consequences in the evidence ledger. Treat implementation
guides as context-specific evidence rather than universal architecture rules.
