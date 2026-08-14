# MiniMax M3

- Provider: MiniMax
- Provider identifier: `MiniMax-M3`
- Normalized slug: `minimax-m3`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: engineering-guidance
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 先写目标、边界、上下文和交付格式；使用直接、可执行的句子。
- 长上下文用清晰标签分段，只要求模型使用与任务相关的部分。
- 格式或风格不可偏离时，给出最小的正例，并固定可复用模板。
- 为每个工具写明用途、输入、成功条件和失败处理；独立调用才并行。
- 代理任务写清停止条件、交付物和评估标准，再据结果迭代提示。

## 运行约束

- 官方提示页是 M-series 通用指南，并非 M3 专属；不要据此推断 M3 独有默认值。
- 工具调用必须遵循已配置的 API 工具契约，不因模型名称扩大权限。
- 长文任务保留必要上下文，避免重复注入相同材料。
- 并行工具调用仅适用于互不依赖的请求；有依赖时按顺序执行。
- 使用评估结果修订提示，分别检查工具结果和最终回答。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| M-series prompt guide | https://platform.minimax.io/docs/token-plan/prompting-best-practices | 2026-08-14 |
| M3 model page | https://www.minimax.io/models/text/m3 | 2026-08-14 |
