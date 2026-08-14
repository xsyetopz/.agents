# MiMo V2.5

- Provider: Xiaomi
- Provider identifier: `mimo-v2.5`
- Normalized slug: `mimo-v2.5`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: source-gap
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 先写最终目标，再说明文本、图像或音频输入各自承担的作用。
- 将长任务拆成可检查阶段；每阶段产出结构化状态。
- 用检查点保存进度，并在后续阶段只注入当前需要的记忆。
- 把动态工具编排放入宿主工作流；提示声明目标、工具契约和停止条件。

## 运行约束

- 面向多模态和智能体任务，保持目标、输入作用和当前状态一致。
- 用结构化状态记录已完成项、待办项、风险和验证结果。
- 恢复任务时避免重复注入无关上下文，保留与当前阶段相关的记忆。
- 每次工具调用都定义输入、预期输出和失败处理。
- 完成前独立验证结果；不要把“生成完成”当作“任务正确”。
- 所列来源未确认具体 API 参数、工具语法、思考开关或默认值；使用前查 API 文档，不要据此推断。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| Model/product page | https://mimo.xiaomi.com/mimo-v2-5 | 2026-08-14 |
| API/engineering notes | https://mimo.xiaomi.com/blog/mimo-code-long-horizon | 2026-08-14 |
