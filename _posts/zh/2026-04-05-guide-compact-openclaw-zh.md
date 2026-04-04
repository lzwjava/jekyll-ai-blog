---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw中/compact使用指南
translated: true
type: note
---

问题：如何在 OpenClaw（AI 代理）中使用带有指令的 `/compact` 命令？

答案：

## OpenClaw 中的 `/compact` 是什么？

`/compact [指令]` 命令会压缩会话上下文并报告剩余的上下文容量。这是消息界面（WhatsApp、Telegram、Discord 等）中可用的内置斜杠命令，能帮助你在 AI 的上下文窗口完全填满前进行管理。

---

## 基本语法

```
/compact
/compact [此处可添加可选指令]
```

---

## 工作原理

### 不使用指令
单独发送 `/compact` 会触发上下文压缩，代理将回复确认操作，并告知剩余的上下文容量。

### 使用指令
你可以附加自定义指令来引导**在压缩过程中保留或优先处理哪些内容**。例如：

```
/compact 专注于我们讨论的编程任务。忘记较早的购物计划。
```

```
/compact 保留 API 集成上下文。简要总结其他所有内容。
```

```
/compact 优先处理我的项目截止日期，忽略闲聊历史。
```

`/compact` 后的指令文本会指导模型在压缩时如何总结或筛选会话历史。

---

## 为何使用 `/compact`？

OpenClaw 代理在长会话中会快速积累上下文。你的代理会迅速积累上下文。定期检查它记住了什么，并清理过时内容。**在**它触发自动压缩之前执行此操作——一旦自动压缩，你将失去对保留内容的控制权。

手动使用 `/compact`（并附加指令）可以让你控制代理保留与丢弃的内容，而不是任由其随意自动压缩。

---

## 相关会话命令

你也可以使用 `/new` 或 `/reset` 来为该聊天开启一个新会话（可通过 `resetTriggers` 配置）。若单独发送，代理将回复简短问候以确认重置。

| 命令 | 效果 |
|---|---|
| `/compact` | 压缩上下文，报告剩余容量 |
| `/compact [指令]` | 按照指示压缩，引导保留内容 |
| `/new` 或 `/reset` | 清除会话并重新开始 |
| `/status` | 显示压缩会话状态（模型 + token 数，成本） |

---

## 建议

- 在上下文窗口耗尽**之前**使用 `/compact`——一旦代理自动压缩，你将失去手动控制权。
- 当你希望保留特定任务线程（例如编程项目或进行中的研究）时，务必包含具体指令。
- 压缩后，代理会报告剩余的上下文容量，帮助你规划何时需要再次压缩。

参考资料：

- [OpenClaw 个人助理设置（官方文档）](https://docs.openclaw.ai/start/openclaw)
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)
- [如何部署你自己的 AI 代理——完整的 OpenClaw 设置指南](https://jsmastery.com/blogs/how-to-deploy-your-own-ai-agent-the-complete-openclaw-setup-guide)