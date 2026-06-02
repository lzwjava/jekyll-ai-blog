---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 导出 OpenClaw 会话和日志
translated: true
type: note
---

Question: 我们能导出 OpenClaw 会话吗？导出命令允许我们看到所有日志和 tool calls 吗？

Answer:

是的，OpenClaw 支持导出会话。使用导出功能，您可以捕获会话的完整快照，包括：

* **所有 user 和 assistant messages** – 对话历史被保留。
* **Tool calls** – 与外部工具的每一次交互（code execution、网络请求、data processing 等）都被记录。
* **Session metadata** – timestamps、context state 以及任何其他内部会话细节。

导出的文件通常采用结构化格式（如 JSON），这使得审查操作序列、分析 tool usage 或重放会话以进行调试或审计变得容易。许多用户发现这对于跟踪复杂工作流程或验证 AI agents 在多个步骤中的行为非常有帮助。

这意味着您不仅可以看到说了什么，还可以看到调用了哪些 tools，包括 parameters 和 results，从而提供会话的非常透明视图。
