# Kimi K3

- Provider: Moonshot AI
- Provider identifier: `kimi-k3`
- Normalized slug: `kimi-k3`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: first-party-guidance
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 按“角色—上下文—任务—输出格式”写提示，先给必要背景再给动作要求。
- 复杂任务拆成可验证的小任务；明确每一步的完成条件和最终交付格式。
- 给一个代表性示例时，同时说明输入、期望输出和不可接受的偏差。
- 需要引用资料时，标出资料边界，要求结论只依据提供的内容。

## 运行约束

- 使用 API 标识 `kimi-k3`；官方模型仓库记录该模型始终启用 thinking，并支持 `low`、`high`、`max` effort。
- 多轮或工具调用必须原样保留完整 assistant 消息，包括 `reasoning_content` 与 `tool_calls`。
- 不要只回传文字答案替换历史 assistant 消息，否则后续工具链上下文会丢失。
- 工具调用前说明目标和参数；工具结果回传后再要求模型继续完成任务。
- 需要结构化结果时，在提示中固定字段和失败表达，不臆造额外协议。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| API prompt best practices | https://platform.kimi.ai/docs/guide/prompt-best-practice | 2026-08-14 |
| K3 model, thinking, and tool history | https://github.com/MoonshotAI/Kimi-K3 | 2026-08-14 |
| Kimi prompt basics | https://www.kimi.com/help/getting-started/what-is-prompt | 2026-08-14 |
