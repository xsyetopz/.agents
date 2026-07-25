# Source index

Retrieved 2026-07-25. These sources inform the workflow and pattern families.
The skill does not claim that a phrase proves machine authorship. It does not
copy prose or examples from sources without permission.

| Source | Used for | Limits |
| --- | --- | --- |
| <https://agentskills.io/specification> | Skill layout, frontmatter, and progressive disclosure | Follow the live specification when it changes |
| <https://github.com/woerndl/unsloppify> | Six failure modes, context rules, necessity tests, scanner shape, and manual false-positive fixtures | MIT repository; preserve attribution when adapting ideas; do not imply this skill is the upstream project |
| <https://raw.githubusercontent.com/woerndl/unsloppify/main/SKILL.md> | Upstream main file and trigger boundary | Read as a reference; this skill is independently written |
| <https://raw.githubusercontent.com/woerndl/unsloppify/main/references/patterns.md> | Pattern families and escape-clause design | MIT repository; phrases are candidates, not bans |
| <https://gist.github.com/ossa-ma/f3baa9d25154c33095e22272c631f5a1> | Tropes grouped by word choice, structure, tone, formatting, and composition | No license field; cite and summarize, do not republish its prose or examples |
| <https://tropes.fyi/aidr> | Distillation concept and public trope taxonomy | A prompt-distillation tool, not a quality or authorship detector |
| <https://tropes.fyi/> | Public trope directory and categories | No general license stated; use as inspiration and link |
| <https://learn.microsoft.com/en-us/style-guide/word-choice/avoid-jargon> | Audience-aware jargon decisions | Technical shorthand remains valid for an audience that knows it |
| <https://learn.microsoft.com/en-us/style-guide/word-choice/use-technical-terms-carefully> | Common words first; keep technical terms only when they are the clearest precise term | Define unfamiliar terms and keep one term for one concept |
| <https://plainlanguage.gov/guidelines/> | Federal plain-language entry point | Redirects to Digital.gov; use the current guide below |
| <https://digital.gov/guides/plain-language> | Audience-first structure, direct verbs, and active voice when responsibility matters | Passive voice can be correct when the actor is unknown or irrelevant |
| <https://digital.gov/guides/plain-language/principles/short-simple> | Short words, base verbs, active voice, and removal of unnecessary modifiers | Examples target public-facing government writing; adapt to the audience |
| <https://digital.gov/guides/plain-language/writing> | Present tense, active voice, hidden-verb removal, and direct action wording | Use other tenses or passive voice when accuracy requires them |
| <https://pubs.opengroup.org/onlinepubs/9799919799.2024edition/utilities/command.html> | POSIX-adjacent command vocabulary and direct utility descriptions | POSIX utility names are interface terms, not a universal prose thesaurus |
| <https://pubs.opengroup.org/onlinepubs/9699919799.2016edition/utilities/test.html> | `test` as a short operation that evaluates and reports a result | Preserve the exact utility name and exit-status semantics |
| <https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html> | `exec` as an exact process-replacement operation | Do not replace the system-call or command name when it is the contract |
| <https://help.apple.com/applestyleguide/> | Apple Style Guide entry point | JavaScript redirect; current guide links are below |
| <https://support.apple.com/guide/applestyleguide/welcome/web> | Apple terminology and international style | Authority for Apple documentation, not a command-translation rule |
| <https://support.apple.com/guide/applestyleguide/intro-to-international-style-apsg1ff68ab5/1.0/web/1.0> | Simple structures, idiom avoidance, and international conventions | Apply to the requested locale and audience |
| <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing> | Structural signals such as inflated significance, promotional tone, bold-first lists, and generic conclusions | Advice page; signals are neither proof nor a license to conceal authorship |
| <https://arxiv.org/abs/2603.18161> | Semantic and voice drift during LLM revision | Preprint; use to justify semantic checks, not a lexical ban |
| <https://github.com/nanxstats/llm-cliches> | MIT adjective, noun, and verb seed lists | Candidate signals only; lists are not exhaustive |
| <https://pubmed.ncbi.nlm.nih.gov/38963503/> | User-supplied record checked for accuracy | This record is unrelated to excess LLM vocabulary; do not cite it for that claim |
| <https://pubmed.ncbi.nlm.nih.gov/40601754/> | Corrected excess-vocabulary study record | Aggregate vocabulary-density evidence only; it cannot identify an author |
| <https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/> | Open full text of the corrected study | Summarize findings; do not reproduce tables |
| <https://arxiv.org/abs/2406.07016> | Corrected study preprint | Use as aggregate context |
| <https://github.com/berenslab/llm-excess-vocab> | Corrected study code and data | Inspect its current license before vendoring |
| <https://github.com/blader/humanizer> | Detect, rewrite, and second-pass workflow | MIT; rules here are independently summarized |
| <https://github.com/conorbronsdon/avoid-ai-writing> | Detect/rewrite/edit modes and signals-not-proof posture | MIT; do not treat its detector as authorship evidence |
| <https://github.com/jalaalrd/anti-ai-slop-writing> | Additional anti-slop pattern ideas | No visible license found; do not copy text or lists |

The supplied gist comments add useful concerns: false exclusivity needs
evidence, programming prose often overuses numbered phase labels, criticism is
frequently wrapped in a compliment sandwich, and fake-casual quoted reactions
are a recurring model habit. One commenter also warned that trope lists can
become evasion aids. This skill therefore aims for reader value and
semantic preservation, not for undetectable machine output.
