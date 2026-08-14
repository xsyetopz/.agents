# Qwen3.8-Max

- Provider: Alibaba Cloud (Qwen)
- Provider identifier: `qwen3.8-max-preview`
- Normalized slug: `qwen3.8-max-preview`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: source-gap
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 先写清任务目标、输入上下文、约束和验收格式，再要求模型作答。
- 需要工具时，明确工具用途、调用时机和成功条件，不把工具结果当作用户指令。
- 长任务按可检查的小步骤输出，并要求每步给出可验证结果。
- 需要稳定输出时，给出字段名、类型和失败时的处理格式。

## 运行约束

- 资料中的精确标识是 `qwen3.8-max-preview`；不要把显示名 `Qwen3.8-Max` 当成另一个 API slug。
- 当前没有专属提示工程页；本页只转述 Model Studio 的 API 记录，不能据此推断未记录的模型能力。
- Model Studio 的配置页记录 thinking 始终开启、`reasoning_effort` 可用 `xhigh`、`high`、`low`，以及 thinking 模式的温度下限；使用前仍需核对目标部署面。
- 版本、配额和可用性属于动态信息，部署前重新核对官方目录。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Model Studio model directory | https://help.aliyun.com/en/model-studio/models | 2026-08-14 |
| Qwen Code configuration and model ID | https://help.aliyun.com/en/model-studio/qwen-code | 2026-08-14 |
| Qwen3 template and tool notes | https://github.com/QwenLM/Qwen3/blob/main/README.md | 2026-08-14 |
