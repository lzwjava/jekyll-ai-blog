---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 了解 Claude Code 技能系统
translated: true
type: note
---

Question: Claude Code 中的 skills 是如何工作的？它们是 markdown 文件、使用 Claude API 的脚本，还是通过 tool calls 创建的？

Answer:

Claude Code 的 skills 系统本质上是一种以结构化方式扩展 AI 自定义行为的机制。以下是其在实践中的运作方式：

1. **Skill 定义格式**

   * Skills 通常存储为 **YAML 或类似 JSON 的配置文件**，而不是纯 markdown。
   * 每个 skill 定义了 **triggers**、**inputs**、**actions** 和 **responses**。
   * 虽然部分文档或说明可能以 markdown 形式提供，但 skill 逻辑本身是机器可读的数据。

2. **Custom Script 集成**

   * Skills 可以包含 Claude model 执行的 **custom scripts 或 prompts**。
   * 这些脚本通常是指令的小型模板，允许进行动态计算或条件响应。
   * 从本质上讲，skill 是一种用特定行为和 context 封装 Claude API 调用（call）的方式。

3. **Tool Calls / Function Hooks**

   * Skills 可以调用 **tool calls**，即与外部服务、APIs 或本地 functions 的集成。
   * 例如，一个 skill 可以从数据库抓取数据、执行计算或调用第三方 API，然后将结果反馈给 Claude 进行进一步处理。

4. **执行流程 (Execution Flow)**

   * 当用户激活一个 skill 时，Claude 会读取 skill 定义，确定适用的部分，（可选地）调用任何 tools/scripts，然后生成 response。
   * 这使得 skills 能够将 **static instructions**、**dynamic scripts** 和 **external actions** 结合成无缝的体验。

**Summary:**
Skills 不仅仅是 markdown 或简单的脚本——它们是结构化的配置，可以包含 prompt templates、可调用的脚本和 tool integrations。它们充当 Claude 的模块化“plugins”，让你能够以特定的方式扩展其行为。

References:

* [Claude by Anthropic Documentation](https://www.anthropic.com/)
* [Claude Code GitHub](https://github.com/obra/superpowers) (用于查看社区示例和 skill 结构)
