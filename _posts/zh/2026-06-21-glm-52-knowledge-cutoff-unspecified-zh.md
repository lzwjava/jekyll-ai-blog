---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GLM-5.2 知识截止日期未指定
translated: true
type: note
---

**问题：** GLM-5.2 的知识截止日期是什么？**答案：**

GLM-5.2 的知识截止日期**未公开说明**。以下是已知信息：

- GLM-5.2 于 2026 年 6 月 13 日由 Z.ai 发布。在模型规格数据库中，知识截止日期字段显示为 `-`（未指定）。
- 对于之前的 GLM-5，训练日期标注为 2026 年 2 月，但已发布的元数据中并未明确给出知识截止日期。
- GLM-5.2 是一个 753B 参数的 MoE 模型，上下文窗口为 1M token。技术报告见 arxiv.org/abs/2602.15763，但公开的模型卡片中未提及截止日期。

因此简而言之：**Z.ai 尚未为 GLM-5.2 发布正式的知识截止日期。** 考虑到 GLM-5 引用的训练日期为 2026 年 2 月，而 GLM-5.2 于 2026 年 6 月发布，训练数据很可能覆盖至 2026 年早中期左右，但需要直接测试模型或等待完整技术报告才能获得确认日期。

**参考资料：**

- [GLM-5.2 规格 — apxml.com](https://apxml.com/models/glm-52)
- [GLM-5 — MindStudio](https://www.mindstudio.ai/models/glm-5)
- [GLM-5.2 — LLM Stats](https://llm-stats.com/models/glm-5.2)
