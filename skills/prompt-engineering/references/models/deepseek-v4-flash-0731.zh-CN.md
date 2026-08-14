# DeepSeek V4 Flash (0731)
- 规范标识：`deepseek-v4-flash`（版本 `DeepSeek-V4-Flash-0731`）
- 指南语言：简体中文
- 证据状态：模型卡 + API/工程指南

## 提示配方
- 在 Responses API 中把任务说明放在首条 system/instructions，随后给上下文、工具和输出契约。
- 按任务复杂度选择 `reasoning_effort`：简单任务用 `low`，复杂代理任务再提高。
- 工具调用后回传完整 `reasoning_content` 与工具调用历史，保持多轮状态连续。
- 明确每个工具的输入、成功条件、失败处理和最终交付格式，避免只写“自行完成”。
- 将公共 beta 版本和验收标准写入评估记录，不把单次成功当作稳定性证明。

## 运行约束
- API 标识是 `deepseek-v4-flash`；`0731` 是版本号，不要拼出另一个 API slug。
- thinking 模式忽略 `temperature` 和 `top_p`；调它们不会改变思考模式行为。
- 工具后续请求必须保留完整 `reasoning_content`，不得只传最终文本。
- Flash 0731 标为 public beta；上线前重新核对版本状态、接口和配额。
- Responses API、工具结果和最终回答分别记录，便于定位提示或调用链问题。

## 官方来源
| 类型 | URL | 检索日期 |
| --- | --- | --- |
| 版本与发布变更 | https://api-docs.deepseek.com/updates/ | 2026-08-14 |
| 思考模式与工具调用 | https://api-docs.deepseek.com/guides/thinking_mode/ | 2026-08-14 |
| Responses API | https://api-docs.deepseek.com/guides/responses_api/ | 2026-08-14 |
| Flash 0731 模型卡 | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 | 2026-08-14 |
