# MiMo V2.5 Pro

- Provider: Xiaomi
- Provider identifier: `mimo-v2.5-pro`
- Normalized slug: `mimo-v2.5-pro`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: source-gap
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 先写目标、输入边界、不可改变的约束和可验收结果。
- 将长任务拆成可检查阶段；每阶段产出结构化状态。
- 在关键节点保存检查点，并在后续阶段显式注入必要记忆。
- 把动态工具编排放入宿主工作流；提示只声明目标、工具契约和停止条件。

## 运行约束

- 面向长时程智能体任务，持续维护目标、约束和当前状态。
- 用结构化状态记录已完成项、待办项、风险和验证结果。
- 恢复任务时只注入当前阶段所需记忆，避免重复无关上下文。
- 每次工具调用都定义输入、预期输出和失败处理。
- 完成前独立验证结果；不要把“生成完成”当作“任务正确”。
- 所列来源未确认具体 API 参数、工具语法、思考开关或默认值；使用前查 API 文档，不要据此推断。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Model/product page | https://mimo.xiaomi.com/mimo-v2-5-pro | 2026-08-14 |
| API/engineering notes | https://mimo.xiaomi.com/blog/mimo-code-long-horizon | 2026-08-14 |
