---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超级能力插件：先确认后执行
translated: true
type: note
---

**Question:** Claude Code 的 Superpowers plugin 有哪些好处，特别是关于它在执行任务前如何提出澄清建议的？

**Answer:**

是的，你的理解完全正确。Claude Code 的 **Superpowers** plugin 的设计初衷正是如此：在前期提出大量澄清问题，以便在最终执行时，输出结果能更精准地匹配你的实际需求。

### 什么是 Superpowers？

Superpowers 是一个开源的 agentic framework，它能将 Claude Code 从一个简单的 code generator 转化为一个真正的资深 AI developer。该插件可通过官方 Claude plugin marketplace 获取。

### 核心优势：先提问，后行动

当你告诉 Claude 你想构建什么时，它不会立即编写代码，而是会激活 brainstorming 技能。它会提出澄清性问题，探索替代方案，并将你的初步想法完善为一份稳健的 design document。它甚至会分块展示设计方案，以便你逐节阅读和验证。

这正是你所描述的权衡过程：

- **它会提出大量问题** —— 以确认你真正的意图。
- **随后更准确地执行** —— 因为它在开始前已经深入理解了你的 requirements。

### 为什么这很重要

即使模型向你提出澄清问题，你也不一定总是确定自己想要什么 —— 尤其是如果你不是 programmer，或者你熟悉的主技术栈有所不同。此外，AI assistants 通常倾向于尝试一次性完成所有构建，而不是将工作拆分为更小、可管理的 pieces。

Superpowers 通过强制执行 structured dialogue 来解决这一问题。brainstorming 技能不再盲目接受模糊的请求，而是强制进行结构化对话。Claude 会提出智能问题来细化 requirements —— 例如询问 brand identity、layout priorities，或者哪种 UI pattern 最符合你的目标。

### 三阶段工作流 (3-Phase Workflow)

其工作流为：首先 Brainstorm → 隔离你的 branch → 编写详细 plan → 最后执行。每一个步骤都是下一阶段的闸门。

具体而言：
- **brainstorming** 技能通过“一次一个问题”的对话模式探索用户意图，提出 2–3 种权衡后的方案，并在编写任何代码之前生成一份经过批准的 design document。
- **writing-plans** 技能随后将批准的设计转化为分步实施计划，其详细程度足以让一名 junior engineer 遵循。
- **verification-before-completion** 技能要求运行实际的 verification commands 并确认真实输出，然后 Claude 才能声明任务已“完成”或“修复”。

### 总结

所以，是的 —— Superpowers 有意放慢了开始阶段（通过提问），以加速并改善最终结果（执行）。提问过程可能感觉比较慢，但它们能确保数天的工作量不偏离航线。

**References:**

- [Superpowers for Claude Code: Complete Guide 2026](https://www.pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)
- [Superpowers Plugin – Claude.ai](https://claude.com/plugins/superpowers)
- [GitHub - obra/superpowers](https://github.com/obra/superpowers)
- [Claude Code Got 100x Better With Superpowers Skill](https://medium.com/@codeandbird/claude-code-got-100x-better-with-superpowers-skill-a36450f708b1)
- [The Superpowers Plugin for Claude Code – Builder.io](https://www.builder.io/blog/claude-code-superpowers-plugin)