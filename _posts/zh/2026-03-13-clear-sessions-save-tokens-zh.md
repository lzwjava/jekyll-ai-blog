---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清除会话节省令牌始终
translated: true
type: note
---

**问题：** 对于 OpenCode / Claude Code / Codex CLI，在完成一项不相关任务后，我们应该创建新会话还是运行 `/clear` 来减少 token 使用量，还是 prompt caching（如同 Gemini/Claude 使用的）会自动处理，因此我们无需担心？

---

**回答：**

## 简短回答

**是的，在不相关任务之间应该使用 `/clear` 或启动新会话。** Prompt caching 确实有帮助，但它并不能消除携带前一任务的陈旧 context 的成本——它只是让重新阅读陈旧 context 更便宜，而不是免费。

---

## Context Window 的实际工作原理

在会话中发送的每条消息都会**重新发送整个对话历史**给模型。这对 Claude Code、OpenCode（使用 Claude/Gemini backend）和 Codex CLI 都是如此。

随着对话通过轮次推进，每个用户消息和助手响应都会在 context window 中累积。先前轮次完全保留，遵循线性增长模式。

因此，50 轮会话每条消息发送的 token 显著多于 5 轮会话——即使模型似乎“瞬间记住”一切。

---

## Prompt Caching 实际的作用

Prompt caching（Anthropic 的 Claude 和 Google 的 Gemini 使用的）减少了重新阅读已见内容的**成本**，但并不消除它：

- Prompt caching 的工作原理是因为 Claude Code 经常重新阅读相同的 context。文件在请求之间不变。System prompt 是静态的。对话历史逐步增长。Cache 捕获所有这些。

- 在跟踪 100M tokens 的真实世界数据中：84% 的输入 token 来自 Anthropic 的 prompt cache。

- 然而，cache read token 完全计入你的使用配额。每条消息都会重新发送完整的 instruction set，无论它是否改变。一个 100 条消息的会话仅从 instructions 就产生 1.5M cache reads 的成本。

因此，cache **降低每个 token 的成本**（约为标准价格的 10%），但 token 仍然**累积并计入**。带有无关先前 context 的长会话会在每条后续消息上浪费配额。

---

## 为什么对于不相关任务，`/clear` 或新会话很重要

当你在同一会话中切换到完全不同的任务时：

1. 所有先前的 tool calls、file reads 和对话轮次仍在 context 中。
2. 你发送的每条新消息都会重新发送所有那些无关历史。
3. 模型可能因陈旧 context（context rot）而困惑或“分心”。
4. 你反复为所有那些无关内容支付 cache-read token。

Token 成本随 context 大小扩展：Claude 处理的 context 越多，你使用的 token 越多。在任务之间 clear：切换到不相关工作时使用 `/clear` 重新开始。陈旧 context 在每条后续消息上浪费 token。

---

## 每个工具的实用指导

### Claude Code

- 在不相关任务之间使用 **`/clear`**。当你注意到 Claude 丢失跟踪时使用 `/compact`，切换到完全不同工作时使用 `/clear`。
- 当仍在同一任务但会话变长时，使用 **`/compact`**（不是 `/clear`）——它总结历史同时保留意图。
- Claude Code 通过 prompt caching（减少重复内容如 system prompts 的成本）和 auto-compaction（接近 context 限制时总结对话历史）自动优化成本。

### Codex CLI (OpenAI)

- 当对话变长时使用 `/compact` 命令来总结历史并释放 token。
- 使用 `/fork` 分支出会话用于不同方法，保留原版。
- 对于真正不相关的工作，推荐使用新会话从头开始。

### OpenCode

- OpenCode 较新，provider-agnostic 的 `/compact` 命令和 auto-compaction 支持是拟议功能——尚未在所有 backend 普遍可用。
- 在不相关任务之间启动新会话仍是目前最安全的方法。

---

## “每个逻辑任务一个会话”规则

每个逻辑任务一个会话效果最佳。一个 bug 修复，一个功能，一个重构。不要试图在一个对话中修复三个 bug 并添加两个功能。

会话之间，使用 `CLAUDE.md` 文件来持久化重要项目 context：包含关键架构决策、文件位置和惯例的 CLAUDE.md 文件意味着 Claude 每次重新发现你的项目结构花费更少的 token。

---

## 总结表格

| 场景 | 推荐 |
|---|---|
| 同一任务，长会话 | `/compact` — 总结，继续 |
| 切换到不相关任务 | `/clear` 或新会话 |
| 相关后续任务 | 保持会话 或 先使用 `/compact` |
| 稍后恢复旧工作 | 使用 `CLAUDE.md` 提供 context 的 `/resume` |
| 非常长的代码库分析 | 每个逻辑单元新会话 |

**底线：** Prompt caching 是成本乘数（更便宜的读取），不是“免费 context”通行证。无关先前 context 总是让你付出代价——在不相关任务之间清除它是最高杠杆优化之一。

---

**参考：**

- [Claude Code Cost Management Docs](https://code.claude.com/docs/en/costs)
- [Anthropic Context Windows Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [7 Ways to Cut Claude Code Token Usage – DEV Community](https://dev.to/boucle2026/7-ways-to-cut-your-claude-code-token-usage-elb)
- [Claude Code Token Usage: Real Data From 100M Tokens](https://docs.bswen.com/blog/2026-03-10-claude-code-token-usage-per-request/)
- [Claude Code Context Window Optimization](https://claudefa.st/blog/guide/mechanics/context-management)
- [OpenCode /compact Feature Discussion](https://github.com/anomalyco/opencode/issues/4317)
- [Codex CLI Session Resume Guide](https://inventivehq.com/knowledge-base/openai/how-to-resume-sessions)
