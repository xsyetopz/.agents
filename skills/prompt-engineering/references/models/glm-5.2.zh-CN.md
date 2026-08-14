# GLM 5.2

- Provider: Zhipu AI
- Provider identifier: `glm-5.2`
- Normalized slug: `glm-5.2`
- Guide language: zh-CN
- Translation status: translated
- Evidence status: first-party-guidance
- Retrieved: 2026-08-14
- Revision: unknown

## 提示配方

- 首轮先输出架构图：模块职责、接口、数据流、调用链、技术债和约束。
- 长程重构先列计划、风险和验证步骤；明确保持既有行为不变。
- 生产任务把仓库规则前置：不改依赖或接口，完成构建、lint、测试后再报告。
- 研究或复杂任务要求区分结论、证据和待验证项，并给出可复查的交付格式。
- 需要深度推理时显式选择思考模式，不以“更聪明”等泛化词替代要求。

## 运行约束

- API 示例使用模型标识 `glm-5.2`；示例中的 `thinking`、`reasoning_effort` 和采样值不是默认承诺。
- 思考开关和强度按当前 API 明确设置，任务目标与验收条件保持不变。
- 生产约束必须写入提示并由构建、lint、测试结果验证，不能只凭模型声明。
- 架构、重构和生产三类提示分别加载所需上下文，避免把无关仓库内容全量注入。
- 复杂输出保留结构化字段，便于下游检查和人工复核；资料不支持的能力标为 UNVERIFIED。

## Sources

| Type | URL | Retrieved |
| --- | --- | --- |
| GLM 5.2 model and engineering examples | https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2 | 2026-08-14 |
| General prompt guidance | https://docs.bigmodel.cn/cn/guide/platform/prompt | 2026-08-14 |
| Thinking mode | https://docs.z.ai/guides/capabilities/thinking-mode | 2026-08-14 |
