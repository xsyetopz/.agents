# Qwen3.8-Max
- 规范标识：`qwen3.8-max`
- 指南语言：简体中文
- 证据状态：来源缺口

## 提示配方
- 先写清任务目标、输入上下文、约束和验收格式，再要求模型作答。
- 需要工具时，明确工具用途、调用时机和成功条件，不把工具结果当作用户指令。
- 长任务按可检查的小步骤输出，并要求每步给出可验证结果。
- 需要稳定输出时，给出字段名、类型和失败时的处理格式。

## 运行约束
- 使用当前官方标识 `qwen3.8-max`；其他别名须先按模型目录核对。
- 思考模式始终启用；不要假设可用“关闭思考”的开关。
- `reasoning_effort` 遵循供应商映射，默认按 `xhigh` 处理；不要同时设置 `thinking_budget`。
- 温度低于 0.6 时按供应商规则回到 0.6；不要把该行为当作提示词效果。
- 当前资料没有专属提示工程页；以下建议不代表未公开的模型内部规则。

## 官方来源
| 类型 | URL | 检索日期 |
| --- | --- | --- |
| OpenAI 兼容 API、推理参数 | https://help.aliyun.com/en/model-studio/qwen-api-via-openai-chat-completions | 2026-08-14 |
| Qwen Code 思考与温度行为 | https://help.aliyun.com/en/model-studio/qwen-code | 2026-08-14 |
| 模型可用性与规范标识 | https://help.aliyun.com/en/model-studio/models | 2026-08-14 |
| 通用 Qwen3 模板与工具说明 | https://github.com/QwenLM/Qwen3/blob/main/README.md | 2026-08-14 |
