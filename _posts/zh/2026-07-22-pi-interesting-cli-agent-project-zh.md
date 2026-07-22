---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Pi: 有趣的CLI代理项目'
translated: true
type: note
---

问题：你是在问，根据你使用 Pi 并对比 Copilot、Claude Code、OpenClaw、Hermes、Codex、Amp 等工具的经验，Pi 是否真的很好。

回答：

是的。根据我所看到的，**Pi 是近期比较有趣的 CLI agent 项目之一**。它并非试图在原始模型质量上超越 Claude Code——而是优化了 *agent runtime*。

其突出之处包括：

* **激进的内容缩减（Aggressive context minimization）。** 不是反复将整个对话塞进提示词，而是尝试只保留当前步骤所需的信息。这降低了延迟、token 用量和上下文漂移。
* **快速迭代。** 更轻量的上下文意味着前向传播成本更低，因此 agent 的响应速度明显更快。
* **插件架构。** 你的 `/note` 插件就是一个很好的例子。当 CLI agent 可以通过扩展小命令而非修改核心来增强功能时，它就会变得更有用。
* **Unix 哲学。** Pi 更接近“小型可组合工具”，而非“一个巨大的 IDE”。

你的工作流就是一个很好的例子：

```
Agent
  ↓
/note
  ↓
ww note queue
  ↓
ww note watch
  ↓
blog
```

这比手动将 agent 的回复复制到笔记中要好得多。

---

你关于切换工具的看法也符合当今许多高级用户的实践。

人们不再只选择**一个** AI IDE，而是越来越多地组合一个工具箱：

* Copilot → 自动补全
* Claude Code → 大型重构和仓库推理
* Pi → 快速终端 agent
* OpenClaw / Hermes → 开源实验
* Codex → OpenAI 生态
* Amp → 另一种编码工作流

每个工具在以下方面各有不同的权衡：

* 延迟 (latency)
* 上下文管理 (context management)
* 工具执行 (tool execution)
* 定价 (pricing)
* 可扩展性 (extensibility)

这个生态系统仍在快速演变，因此切换工具并不一定是优柔寡断——它往往反映了前沿正在快速移动。

从你描述的内容中，我特别喜欢你的 `/note` 插件。这种集成会随时间产生复利效应。通过一条命令将上一次 agent 的响应直接保存到你的知识管道中，这种自动化每天会被使用数十次。

至于 YOLO 模式——如果你在自己控制的机器上使用并了解风险，许多经验丰富的 CLI agent 用户也会为了速度而做出同样的权衡。`/usr/bin` 的故事也是一个很好的提醒：即使是经验丰富的用户，偶尔也会键入破坏性命令；拥有可复现的系统设置或良好的备份，能让 YOLO 模式不那么痛苦。

总的来说，我认为 Pi 是一个真正有趣的项目——不是因为它的模型最强，而是因为它探索了设计空间中的一个不同点：**优化 agent runtime 和上下文管理，而不是仅仅换用更大的 LLM。**

参考：

* Pi: [https://github.com/earendil-works/pi](https://github.com/earendil-works/pi)
* ww: [https://github.com/lzwjava/ww](https://github.com/lzwjava/ww)
