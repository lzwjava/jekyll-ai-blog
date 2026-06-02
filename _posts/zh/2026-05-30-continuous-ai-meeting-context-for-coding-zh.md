---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 持续AI会议编程上下文
translated: true
type: note
---

问题：

要获得一个精确且全面的 Zoom AI 助手，一种方法是否就是让它每 3–5 分钟总结一次，将所有响应存储在一个 Markdown 文件中，然后将其与背景信息（如共享的 Excel 表格或文档）一起提供给 Copilot 或 Claude 用于代码优化？

答案：

是的，这种方法对于在会议或编码过程中创建一个精确且具备上下文感知能力的 AI 助手来说，既实用又有效。以下是对其工作原理及有效性的详细分析：

1. **高频总结**

   * 每 3–5 分钟捕捉一次总结，可确保 AI 跟上对话节奏，不会遗漏关键信息。
   * 与原始转录日志相比，总结更易于存储、处理并馈送到其他 AI 系统。

2. **集中式 Markdown 文件**

   * 将所有总结存储在一个 Markdown 文件中，可创建一个单一且结构化的权威来源。
   * Markdown 支持标题、代码块、表格和链接，既便于人工审阅，也适合 AI 读取。

3. **注入背景信息**

   * 包含外部数据（Excel 表格、文档、幻灯片）可为 AI 提供对话之外的相关上下文。
   * 你可以将链接或内容复制到 Markdown 文件中，供 Copilot/Claude 在生成或优化代码时参考。

4. **通过 AI 进行代码优化**

   * 通过提供最新的总结以及上下文文档，Copilot 或 Claude 能够生成反映最新讨论、决策和数据的代码。
   * 这有助于减少错误、避免重复工作，并确保输出与会议意图保持一致。

5. **实施建议**

   * 利用 Zoom 转录功能配合 AI 总结脚本，实现总结捕捉的自动化。
   * 在 Markdown 中使用统一的标题/标签，以便轻松解析各章节。
   * 定期（而非持续流式传输原始对话）将 Markdown 文件输入 Copilot/Claude。
   * 可选择将行动项或代码片段单独突出显示，以便 AI 进行针对性优化。

这种方法本质上创建了一份会议的“动态文档”，既可作为会议记录，也可作为 AI 代码助手的可操作输入。

这是一种可扩展的方式，让 AI 助手不仅能跟踪讨论，还能实时主动提升工作产出。

参考资料：

* [Zoom AI 助手概述](https://zoom.us/features/ai)
* [用于知识管理的 Markdown](https://www.markdownguide.org/extended-syntax/)
* [GitHub Copilot 文档](https://docs.github.com/en/copilot)
* [Claude AI 总结功能](https://www.anthropic.com/claude)
