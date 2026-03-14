---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 内存两层详解
translated: true
type: note
---

问题：OpenClaw 的内存是基于会话的吗？当创建新会话时，聊天历史记录会消失吗？

回答：

是的，也不是——OpenClaw 有**两个不同的内存层**，理解它们的区别是关键：

---

## 1. 会话历史记录 (基于会话 — 临时)

会话历史记录仅限于当前会话，并在重启时清除。代理记住当前对话中说过的一切，但当 OpenClaw 实例重启或开始新会话时，此历史记录会重置。

会话历史记录为您提供对话内存，但当您重置会话或开始新会话时，该会话中的一切都会消失。需要一个独立的内存系统——持久知识，能够在会话重置后存活。

---

## 2. 长期内存 (持久 — 跨会话存活)

长期内存让您的 OpenClaw 代理记住跨不同对话的信息。这对于个人偏好、项目上下文和关于您的事实特别有用。只需告诉您的代理“Remember that [fact]”，它就会将其存储在长期内存中，并在未来的对话中自动使用。

OpenClaw 的 AI 会自动将每日日志写入 Markdown 文件。这些文件是真相来源，模型仅“记住”写入磁盘的内容。人类开发者可以打开这些 Markdown 文件，直接编辑它们，并随时查看 AI 记住的内容。

---

## 会话管理方式

会话会被重用直到过期，过期评估在下一个传入消息时进行。默认情况下，网关主机本地时间上午 4:00 进行每日重置。一旦会话的最后更新早于最近的每日重置时间，该会话就被视为过时。可选的空闲重置 (`idleMinutes`) 添加了一个滑动空闲窗口。

---

## 会话日志仍保存到磁盘

尽管聊天历史从活动上下文中清除，但会话日志仍保存在 `~/.openclaw/agents/<agentId>/sessions/` 下，作为索引文件和每个会话的 `.jsonl` 记录。每一行是一个包含元数据和消息条目的 JSON 对象。

开始新会话时，OpenClaw 可以自动将之前的对话保存到带有描述性 slug 的时间戳文件。这些会话记录被索引和可搜索，允许代理回忆过去的对话。

---

## 总结表格

| 内存类型 | 跨会话持久？ | 存储位置 |
|---|---|---|
| 会话历史记录 | ❌ 否 | 仅内存中 |
| 长期内存 (MEMORY.md) | ✅ 是 | 磁盘 (Markdown 文件) |
| 会话日志 (.jsonl) | ✅ 是 (可读/可搜索) | `~/.openclaw/.../sessions/` |

**底线：** 活动聊天历史在新会话时会被清除，但您可以通过明确告诉代理记住它，或使用会话日志搜索工具检索过去对话来保留重要信息。

参考资料：

- [https://openclawlaunch.com/guides/openclaw-memory](https://openclawlaunch.com/guides/openclaw-memory)
- [https://docs.openclaw.ai/concepts/session](https://docs.openclaw.ai/concepts/session)
- [https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive](https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive)
- [https://playbooks.com/skills/openclaw/openclaw/session-logs](https://playbooks.com/skills/openclaw/openclaw/session-logs)
- [https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md](https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md)