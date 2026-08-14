# DeepSeek V4 Pro (0813)
- 规范标识：`deepseek-v4-pro`（版本 `DeepSeek-V4-Pro-0813`）
- 指南语言：简体中文
- 证据状态：API/工程指南

## 提示配方
- 在 Responses API 中把 instructions 放在首条 system 消息，明确目标、上下文、工具和输出契约。
- 按工作量选择 `reasoning_effort`：简单任务 `low`，日常代理 `high`，复杂长程任务 `max`。
- 工具调用后回传完整 `reasoning_content` 与工具调用历史，保持多轮推理状态。
- 要求代理先规划，再执行工具，并在最终输出中给出结果、证据和未解决项。
- 用固定评估任务比较 effort 档位，先看成功率和完整性，再权衡成本与延迟。

## 运行约束
- API 标识是 `deepseek-v4-pro`；`0813` 是 GA 版本号，不要发明独立 API slug。
- thinking 模式忽略 `temperature` 和 `top_p`；不要靠采样参数替代思考强度选择。
- 工具后续请求必须保留完整 `reasoning_content`，否则多轮工具链可能失去必要状态。
- 使用官方 Responses API 和当前版本文档；版本、配额或行为变化须重新核对。
- 分开审查工具效果、最终回答和版本状态，不用最终文本掩盖调用失败。

## 官方来源
| 类型 | URL | 检索日期 |
| --- | --- | --- |
| 版本与发布变更 | https://api-docs.deepseek.com/updates/ | 2026-08-14 |
| 模型标识与版本 | https://api-docs.deepseek.com/quick_start/pricing/ | 2026-08-14 |
| 思考模式与工具调用 | https://api-docs.deepseek.com/guides/thinking_mode/ | 2026-08-14 |
| Responses API | https://api-docs.deepseek.com/guides/responses_api/ | 2026-08-14 |
