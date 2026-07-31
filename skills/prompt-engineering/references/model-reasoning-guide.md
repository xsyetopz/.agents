# Model Reasoning Guide

How to adapt prompts for different model types and reasoning modes. Data sourced
from the agent model workflow comparison (2026-07-28 snapshot), OpenAI docs,
Anthropic docs, and [models.dev](https://models.dev) — the canonical open-source
database of AI models with provider IDs, context windows, reasoning support, and
pricing.

## Model type overview

### Reasoning models (always-on thinking)

**Families**: Kimi K3

**Characteristics**:

- Internal chain-of-thought is always active; cannot be disabled
- 1M+ context windows
- Effort controls: low, high, max (verified distinct tiers)
- Best for complex multi-step tasks, architecture, and planning

**Prompting strategy**:

- Give high-level goals and success criteria, not step-by-step instructions
- Avoid "think step by step" or "explain your reasoning" prompts — they already
  reason internally
- Be very specific about the end goal and what success looks like
- Use fewer examples; try zero-shot first
- Focus output constraints on format and completeness, not reasoning process
- Higher effort = deeper internal reasoning, not different output structure

**Example**:

```markdown
# Identity
You are a senior software architect. Your goal is to design a data pipeline.

# Instructions
- Propose a complete architecture with data flow, error handling, and scaling strategy.
- Output as a structured design document with sections for overview, components,
  data flow, failure modes, and deployment.
- Do NOT describe your reasoning process. Output only the design.
```

### Reasoning models (toggleable)

**Families**: DeepSeek V4 Pro/Flash, GLM-5.2, GPT-5.6 Sol/Luna/Terra,
Qwen3.6 27B, Qwen3.7 Max/Plus, gpt-oss-120b, Nemotron 3 Super 120B, Muse
Spark 1.1, Hy3

**Characteristics**:

- Can switch between reasoning and non-reasoning modes
- Reasoning mode: internal chain-of-thought, handles ambiguity well
- Non-reasoning mode: faster, cheaper, needs more explicit instructions
- Effort controls vary by model (see table below)

**Prompting strategy (reasoning mode)**:

- Same as always-on reasoning: high-level goals, zero-shot first
- Reasoning effort controls depth of internal thinking
- More effort = better on complex tasks, but slower and more expensive

**Prompting strategy (non-reasoning mode)**:

- Provide explicit, detailed instructions
- Include logical steps, decision trees, and constraints
- Few-shot examples are high-impact
- Break complex tasks into explicit sub-tasks

### Adaptive thinking models

**Families**: MiniMax-M3

**Characteristics**:

- Adaptive Thinking mode: model decides when to think
- Effort labels (low/medium/high) enable/disable Adaptive Thinking but do NOT
  tune reasoning depth
- 1M context window, 428B total / 23B active params
- Multimodal: text, image, video input

**Prompting strategy**:

- Provide structure but don't over-specify — model handles its own thinking
  allocation
- Don't rely on effort labels to control reasoning depth; they only toggle the
  mode
- Treat as a middle ground between reasoning and non-reasoning
- Good for cost-sensitive tasks that still benefit from some reasoning

### Non-reasoning models

**Families**: GLM-4.7-Flash (non-reasoning mode), Qwen3.6 27B (non-reasoning
mode), DeepSeek V4 (non-reasoning mode)

**Characteristics**:

- No internal chain-of-thought
- Faster and cheaper than reasoning mode
- Need explicit, detailed prompting

**Prompting strategy**:

- Provide explicit, step-by-step instructions
- Include decision rules and edge case handling
- Few-shot examples are critical for complex patterns
- Use structured output constraints (JSON schema, format templates)

### Small models (<30B active parameters)

**Families**: Qwen3.6 27B (27.8B), GLM-4.7-Flash (3B), gpt-oss-120b (5.1B
active), Nemotron 3 Super 120B (12.7B active), DeepSeek V4 Flash (13B)

**Characteristics**:

- Limited reasoning capacity
- Faster and cheaper
- Context windows: 131K–262K for smaller models, up to 1M for DeepSeek Flash

**Prompting strategy**:

- Single objective per prompt — don't give multiple unrelated tasks
- Short, concrete instructions with explicit acceptance criteria
- Avoid open-ended tasks without clear structure
- Provide output format templates
- Use few-shot examples for any non-trivial pattern

---

## Effort control reference

Models that support verified reasoning effort tiers:

| Model | Effort levels | Default | Distinct tiers | Notes |
| --- | --- | --- | --- | --- |
| Kimi K3 | low, high, max | max | Yes (verified) | Always-thinking; can't disable |
| DeepSeek V4 Pro | high, max | — | Yes (verified) | Also has non-reasoning mode |
| DeepSeek V4 Flash | high, max | — | Yes (verified) | Also has non-reasoning mode |
| GLM-5.2 | low, high, max | high | Yes (verified) | Also has non-reasoning mode |
| GPT-5.6 Sol | low, medium, high, xhigh, max | — | Yes | Reasoning mode only |
| GPT-5.6 Luna | low, medium, high, max | — | Yes | Reasoning mode only |
| GPT-5.6 Terra | low, medium, high, max | — | Yes | Reasoning mode only |
| Qwen3.6 27B | low, high, max | low (default) | Yes (verified) | Also has non-reasoning mode |
| gpt-oss-120b | low, medium, high | medium | Yes | Reasoning mode only |

Models where effort labels do NOT tune depth:

| Model | What effort does | Notes |
| --- | --- | --- |
| MiniMax-M3 | Toggles Adaptive Thinking on/off | Low/medium/high all map to same adaptive behavior |
| Kimi K2.7 Code | Fixed reasoning configuration | No reasoning_effort parameter |
| GLM-4.7-Flash | Toggles reasoning mode on/off | Two modes only, no depth tuning |
| Qwen3.7 Max/Plus | Provider-defined canonical config | No independent effort tiers |
| MiMo-V2.5/V2.5-Pro | Canonical reasoning config | Single default configuration |

---

## Context window sizes

| Size | Models |
| --- | --- |
| 1M+ tokens | Kimi K3 (1,049,000), DeepSeek V4 Pro (1,000,000), DeepSeek V4 Flash (1,000,000), GLM-5.2 (1,000,000), MiniMax-M3 (1,000,000), MiMo-V2.5 (1,000,000), GPT-5.6 series (1,000,000), Qwen3.7 series (1,000,000), Nemotron 3 Super (1,000,000) |
| 256K–262K | Kimi K2.7 Code (256,000), Qwen3.6 27B (262,144), Hy3 (260,000) |
| 131K–200K | GLM-4.7-Flash (200,000), gpt-oss-120b (131,072) |

---

## Per-family prompting notes

### Kimi K3 (Moonshot AI)

- 2.8T total / 104B active, always-thinking
- Strong at agentic coding, frontend, complex architecture
- Give high-level goals; avoid over-specifying steps
- 1M context — can handle very large prompts
- Effort max recommended for architecture and complex tasks

### DeepSeek V4 Pro/Flash (DeepSeek)

- Pro: 1.6T/49B, Flash: 685B/13B
- MIT license, open weights
- Reasoning mode for complex tasks; non-reasoning for speed
- Pro for deep reasoning; Flash for bulk/parallel work
- Good for adversarial review (cross-family against Kimi)

### GPT-5.6 series (OpenAI)

- Sol: flagship reasoning, Luna: balanced, Terra: fast/cheap
- All support reasoning with multiple effort levels
- Follow OpenAI prompt engineering guide: developer > user > assistant
- Use `instructions` parameter for high-level guidance
- GPT models (non-reasoning) need explicit step-by-step

### GLM-5.2 (Z.ai / Tsinghua)

- 40B active, 1M context
- Strong at long-task execution and engineering standards
- Good as cross-family reviewer for Kimi implementations
- Effort controls verified distinct

### MiniMax-M3 (MiniMax)

- 428B/23B active, 1M context, multimodal
- Cost-effective (~1/20 of Opus-class)
- Adaptive Thinking — don't try to tune depth with effort labels
- Good for exploration, bulk sharding, and cost-sensitive implementation

### Small/cheap models

- Qwen3.6 27B: good for narrow mechanical tasks with explicit constraints
- GLM-4.7-Flash: fastest/cheapest, only for single-objective short tasks
- gpt-oss-120b: general-purpose backup, limited context (131K)

---

## Cross-model review strategy

For adversarial review and quality assurance:

- Use different model families for implementer vs reviewer (avoids family blind
  spots)
- Kimi implementation → GLM or DeepSeek review
- DeepSeek implementation → Kimi or GLM review
- GPT implementation → Kimi or DeepSeek review

---

# Complete Model Family Reference

Self-contained model data from the agent model workflow comparison
(2026-07-28 snapshot, 60 configurations across 21 families). Combined
with [models.dev](https://models.dev) canonical IDs where available.

## DeepSeek V4 Flash

**Developer**: DeepSeek
**Open weights**: True
**License**: MIT
**Input modalities**: text
**Parameters**: 284B total / 13B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek V4 Flash (max) | reasoning | max | ✓ | | 40 | 124.0 | |
| DeepSeek V4 Flash (high) | reasoning | high | ✓ | | 37 | 124.0 | |
| DeepSeek V4 Flash (non-thinking) | non-reasoning | non-thinking | ✓ | | 29 | 124.0 | |

---

## DeepSeek V4 Pro

**Developer**: DeepSeek
**Open weights**: True
**License**: MIT
**Input modalities**: text
**Parameters**: 1600B total / 49B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| DeepSeek V4 Pro (max) | reasoning | max | ✓ |  | 44 | 72.0 |  |
| DeepSeek V4 Pro (high) | reasoning | high | ✓ |  | 43 | 72.0 |  |
| DeepSeek V4 Pro (non-thinking) | non-reasoning | non-thinking | ✓ |  | 31 | 72.0 |  |

---

## GLM-4.7-Flash

**Developer**: Zhipu AI / Z.AI
**Open weights**: True
**License**: MIT
**Input modalities**: text
**Parameters**: 30B total / 3B active
**Max context**: 200,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| GLM-4.7-Flash (non-reasoning) | non-reasoning | non-reasoning | ✓ |  | 16 |  |  |
| GLM-4.7-Flash (reasoning) | reasoning | reasoning | ✓ |  | 23 | 91.7 |  |

---

## GLM-5.2

**Developer**: Zhipu AI / Z.AI
**Open weights**: True
**License**: MIT
**Input modalities**: text
**Parameters**: 753B total / 40B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5.2 (high) | reasoning | high | ✓ | | | | 36.3% |
| GLM-5.2 (low) | reasoning | high | — | | | | 36.3% |
| GLM-5.2 (medium) | reasoning | high | — | | | | 36.3% |
| GLM-5.2 (max) | reasoning | max | ✓ | | 51 | 211.8 | 43.8% |
| GLM-5.2 (xhigh) | reasoning | max | — | | 51 | 211.8 | 43.8% |
| GLM-5.2 (minimal) | non-reasoning | none | — | | 34 | | |
| GLM-5.2 (none) | non-reasoning | none | ✓ | | 34 | | |

---

## GPT-5.6 Luna

**Developer**: OpenAI
**Open weights**: False
**License**: None
**Input modalities**: text
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.6 Luna (max) | reasoning | max | ✓ | | 51 | | 67.2% |
| GPT-5.6 Luna (xhigh) | reasoning | xhigh | ✓ | | 49 | | 56.9% |
| GPT-5.6 Luna (high) | reasoning | high | ✓ | | 46 | | 44.2% |
| GPT-5.6 Luna (low) | reasoning | low | ✓ | | 33 | | 1.5% |
| GPT-5.6 Luna (medium) | reasoning | medium | ✓ | | 38 | | 11.3% |
| GPT-5.6 Luna (none) | non-reasoning | none | ✓ | | 27 | | |

---

## GPT-5.6 Sol

**Developer**: OpenAI
**Open weights**: False
**License**: None
**Input modalities**: text
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.6 Sol (high) | reasoning | high | ✓ | | 56 | 72.0 | 69.4% |
| GPT-5.6 Sol (xhigh) | reasoning | xhigh | ✓ | | 58 | 73.0 | 70.7% |
| GPT-5.6 Sol (max) | reasoning | max | ✓ | | 59 | 73.1 | 72.7% |
| GPT-5.6 Sol (medium) | reasoning | medium | ✓ | | 54 | 73.0 | 61.1% |
| GPT-5.6 Sol (low) | reasoning | low | ✓ | | 49 | 71.2 | 45.4% |
| GPT-5.6 Sol (none) | non-reasoning | none | ✓ | | 41 | | |

---

## GPT-5.6 Terra

**Developer**: OpenAI
**Open weights**: False
**License**: None
**Input modalities**: text
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.6 Terra (max) | reasoning | max | ✓ | | 55 | 145.3 | 69.6% |
| GPT-5.6 Terra (high) | reasoning | high | ✓ | | 49 | 115.9 | 53.8% |
| GPT-5.6 Terra (xhigh) | reasoning | xhigh | ✓ | | 52 | | 60.2% |
| GPT-5.6 Terra (medium) | reasoning | medium | ✓ | | 46 | | 35.1% |
| GPT-5.6 Terra (low) | reasoning | low | ✓ | | 40 | 127.5 | 24.1% |
| GPT-5.6 Terra (none) | non-reasoning | none | ✓ | | 34 | | |

---

## Grok 4.5

**Developer**: xAI
**Open weights**: False
**License**: None
**Input modalities**: text

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Grok 4.5 (high) | reasoning | high | ✓ |  | 54 | 53.3 | 53.8% |

---

## Hy3

**Developer**: Hunyuan / Tencent
**Open weights**: True
**License**: model license not verified in this dataset
**Input modalities**: text
**Parameters**: 295B total / 21B active
**Max context**: 260,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Hy3 (reasoning) | reasoning | reasoning | ✓ |  | 41 | 59.0 |  |
| Hy3 (non-reasoning) | non-reasoning | non-reasoning | ✓ |  | 26 | 158.6 |  |

---

## Kimi K2.7 Code

**Developer**: Moonshot AI
**Open weights**: True
**License**: Kimi model license
**Input modalities**: text|image
**Parameters**: 1000B total / 32B active
**Max context**: 256,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Kimi K2.7 Code | reasoning | default | — | default | 42 | 44.4 | 30.5% |

---

## Kimi K3

**Developer**: Moonshot AI
**Open weights**: True
**License**: Kimi model license (conditional/restricted)
**Input modalities**: text|image
**Parameters**: 2800B total / 104B active
**Max context**: 1,049,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Kimi K3 (max) | always-thinking | max | ✓ | max | 57 | 32.0 | 68.5% |
| Kimi K3 (high) | always-thinking | high | ✓ | max |  |  |  |
| Kimi K3 (low) | always-thinking | low | ✓ | max |  |  |  |

---

## MiMo-V2.5

**Developer**: Xiaomi
**Open weights**: True
**License**: MIT
**Input modalities**: text|image
**Parameters**: 310B total / 15B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| MiMo-V2.5 | reasoning | default | — | default | 37 | 73.5 |  |

---

## MiMo-V2.5-Pro

**Developer**: Xiaomi
**Open weights**: True
**License**: permissive model license (exact identifier not extracted)
**Input modalities**: text
**Parameters**: 1020B total / 42B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| MiMo-V2.5-Pro | reasoning | default | — | default | 42 | 66.8 |  |

---

## MiniMax-M3

**Developer**: MiniMax
**Open weights**: True
**License**: MiniMax model license
**Input modalities**: text|image|video
**Parameters**: 428B total / 23B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MiniMax-M3 (high) | adaptive-thinking | adaptive | — | interface-dependent | 44 | 83.0 | |
| MiniMax-M3 (low) | adaptive-thinking | adaptive | — | interface-dependent | 44 | 83.0 | |
| MiniMax-M3 (medium) | adaptive-thinking | adaptive | — | interface-dependent | 44 | 83.0 | |
| MiniMax-M3 (minimal) | adaptive-thinking | adaptive | ✓ | interface-dependent | 44 | 83.0 | |
| MiniMax-M3 (none) | non-reasoning | none | ✓ | interface-dependent | | | |

---

## Muse Spark 1.1

**Developer**: Muse / provider unspecified
**Open weights**: False
**License**: None
**Input modalities**: text

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Muse Spark 1.1 (xhigh) | reasoning | xhigh | ✓ |  | 51 | 127.8 | 53.3% |

---

## Nemotron 3 Super 120B A12B

**Developer**: NVIDIA
**Open weights**: True
**License**: NVIDIA Nemotron Open Model License
**Input modalities**: text
**Parameters**: 120.6B total / 12.7B active
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| NVIDIA Nemotron 3 Super 120B A12B (reasoning) | reasoning | reasoning | ✓ |  | 25 | 155.0 |  |

---

## Qwen3.6 27B

**Developer**: Alibaba / Qwen
**Open weights**: True
**License**: Apache-2.0
**Input modalities**: text|image|video
**Parameters**: 27.8B total / 27.8B active
**Max context**: 262,144 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.6 27B (default) | reasoning | reasoning | ✓ | default reasoning | 37 | 56.0 | |
| Qwen3.6 27B (high) | reasoning | reasoning-high | — | default reasoning | | | |
| Qwen3.6 27B (low) | reasoning | reasoning-low | — | default reasoning | | | |
| Qwen3.6 27B (max) | reasoning | reasoning-max | — | default reasoning | | | |
| Qwen3.6 27B (none) | non-reasoning | non-reasoning | ✓ | default reasoning | 30 | | |

---

## Qwen3.6 Plus

**Developer**: Alibaba / Qwen
**Open weights**: False
**License**: None
**Input modalities**: text|image|video
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Qwen3.6 Plus | reasoning | default | — | default | 40 | 52.7 |  |

---

## Qwen3.7 Max

**Developer**: Alibaba / Qwen
**Open weights**: False
**License**: None
**Input modalities**: text
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Qwen3.7 Max | reasoning | default | — | default | 46 | 203.4 |  |

---

## Qwen3.7 Plus

**Developer**: Alibaba / Qwen
**Open weights**: False
**License**: None
**Input modalities**: text|image
**Max context**: 1,000,000 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
|---|---|---|---|---|---|---|---|
| Qwen3.7 Plus | reasoning | default | — | default | 39 | 52.7 |  |

---

## gpt-oss-120b

**Developer**: OpenAI
**Open weights**: True
**License**: Apache-2.0
**Input modalities**: text
**Parameters**: 117B total / 5.1B active
**Max context**: 131,072 tokens

| Configuration | Reasoning mode | Effort | Distinct | Default | AA Index | Speed (t/s) | SWE-bench |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b (high) | reasoning | high | ✓ | medium | 24 | 265.5 | |
| gpt-oss-120b (low) | reasoning | low | ✓ | medium | 15 | 296.5 | |
| gpt-oss-120b (medium) | reasoning | medium | ✓ | medium | | | |

---
