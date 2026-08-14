# Qwen3.6 35B-A3B

- Provider: Alibaba Cloud (Qwen)
- Provider identifier: `Qwen3.6-35B-A3B`
- Normalized slug: `qwen3.6-35b-a3b`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: source-gap
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 将任务目标、输入上下文、限制条件和验收输出明确分段书写。
- 使用模型卡给出的 chat template；不要手写或混用其他模型的特殊标记。
- 对支持的多模态输入，按模型卡示例编排消息，并明确希望模型执行的操作。
- 工具或推理配置仅引用官方资料中的参数和格式，不根据 “A3B” 名称推断能力。

## 运行约束

- 使用精确标识 `Qwen3.6-35B-A3B`；不要与 Qwen3.6-27B 合并配置。
- 官方 Qwen3.6 资料没有专属提示工程页；本页不能据此推断未记录的默认值或能力。
- 不声明未经官方资料确认的思考开关、工具协议、采样默认值或上下文限制。
- 若后端改写模板或参数，优先遵循该后端的官方部署文档。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Qwen3.6 engineering repository | https://github.com/QwenLM/Qwen3.6 | 2026-08-14 |
| 35B-A3B model card and template | https://huggingface.co/Qwen/Qwen3.6-35B-A3B | 2026-08-14 |
| Qwen3 template and tool notes | https://github.com/QwenLM/Qwen3/blob/main/README.md | 2026-08-14 |
