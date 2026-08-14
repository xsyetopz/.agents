# DeepSeek V4 Flash (0731)

- Provider: DeepSeek
- Provider identifier: `deepseek-v4-flash`
- Normalized slug: `deepseek-v4-flash`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: engineering-guidance
- Retrieved: 2026-08-14
- Revision: DeepSeek-V4-Flash-0731

## 提示配方

- 在 Responses API 中把任务说明放在首条 system/instructions，随后给上下文、工具和输出契约。
- 按任务复杂度选择 `reasoning_effort`；可用值和映射以当前 API 文档为准。
- 工具调用后回传完整 `reasoning_content` 与工具调用历史，保持多轮状态连续。
- 明确每个工具的输入、成功条件、失败处理和最终交付格式，避免只写“自行完成”。
- 将 public beta 版本和验收标准写入评估记录，不把单次成功当作稳定性证明。

## 运行约束

- API 标识是 `deepseek-v4-flash`；`0731` 是版本号，不要拼出另一个 API slug。
- thinking 模式不支持 `temperature`、`top_p`、`presence_penalty` 或 `frequency_penalty`；设置这些字段不会改变 thinking 行为。
- 工具请求的后续消息必须保留完整 `reasoning_content`；缺失时 API 可能返回 400。
- Responses API、工具结果和最终回答分别记录，便于定位提示或调用链问题。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Release and version changes | https://api-docs.deepseek.com/updates/ | 2026-08-14 |
| Thinking mode and tool calls | https://api-docs.deepseek.com/guides/thinking_mode/ | 2026-08-14 |
| Responses API | https://api-docs.deepseek.com/guides/responses_api/ | 2026-08-14 |
| Flash 0731 model card | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 | 2026-08-14 |
