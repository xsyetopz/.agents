# Qwen3.6-27B

- Provider: Alibaba Cloud (Qwen)
- Provider identifier: `Qwen3.6-27B`
- Normalized slug: `qwen3.6-27b`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: source-gap
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 把目标、上下文、约束和输出验收条件分开写，避免依赖隐含意图。
- 使用模型卡展示的 chat template；不要自行改写消息边界或特殊标记。
- 对支持的多模态输入，按模型卡示例组织内容，并明确每种输入的任务。
- 工具、推理或部署参数只采用官方资料已展示的形式，不从模型名称推断行为。

## 运行约束

- 使用精确标识 `Qwen3.6-27B`；不要把 27B 与 35B-A3B 当成同一模型。
- 当前没有专属 Qwen3.6 提示工程页；本页只转述模型卡和工程仓库，不能据此推断未记录的默认值或能力。
- 不声明未经官方资料确认的思考开关、工具协议、采样默认值或上下文限制。
- 若运行时提供不同模板，先以对应部署后端的官方文档为准。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Qwen3.6 engineering repository | https://github.com/QwenLM/Qwen3.6 | 2026-08-14 |
| 27B model card and template | https://huggingface.co/Qwen/Qwen3.6-27B | 2026-08-14 |
| Qwen3 template and tool notes | https://github.com/QwenLM/Qwen3/blob/main/README.md | 2026-08-14 |
