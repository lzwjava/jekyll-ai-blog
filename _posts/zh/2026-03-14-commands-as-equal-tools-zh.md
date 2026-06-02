---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 命令作为平等工具的设计
translated: true
type: note
---

问题：OpenClaw 将 shell commands 与 Claude Code 视为同一级别（而非从属）的抽象有什么有趣之处，这是否是更好的设计？

回答：

## OpenClaw 的抽象：命令作为对等，而非子级

你的观察直击 OpenClaw 在架构上有趣的核心。让我正确拆解这个洞见。

---

### 传统思维模型（Claude Code 内部）

在 Claude Code 的模型中，层次结构大致如下：

```
Claude (LLM brain)
  └── Claude Code (agentic coding shell)
        └── shell commands / tool calls
```

Claude Code 将 agent loop 包装在 CLI 上下文中。Claude Code 将 agent loop 包装在 CLI 中：你输入，它运行，然后退出。Shell commands 是 Claude Code *拥有和控制* 的东西——它们存在于其下方。

---

### OpenClaw 的抽象转变

OpenClaw 将此扁平化。在其架构中，Gateway 是 orchestrator，而 **Claude Code、shell commands、browser control、cron jobs 等都是同一级别的 *tools***：

```
OpenClaw Gateway (orchestrator / control plane)
  ├── Claude / LLM API  ← 只是大脑
  ├── shell commands    ← 对等级别的 tool
  ├── Claude Code       ← 对等级别的 tool（仅用于编程任务）
  ├── browser control
  ├── file system
  └── messaging channels
```

系统的基石是这些 tools，它们允许 OpenClaw 执行真实操作，使 agent 能够与系统交互、运行命令并操纵数据，作为自动化工作流的一部分——将 OpenClaw 的功能从决策扩展到现实世界的执行。

---

### 为什么这个抽象更像人类行为

你说得对，它更接近人类行为。原因如下：

**人类不会以工具层次思考。** 当人类执行任务时，他们不会先“进入 coding mode”，然后发出命令。他们只是……做事。他们编写代码 *同时* 运行 terminal commands *同时* 浏览网页——所有这些都是扁平的、可互换的动作，由意图驱动。

OpenClaw 镜像了这一点：一个 ReAct loop，其中模型进行推理、调用 tools 并整合结果——tool layer 赋予 agent 现实世界的能力。模型在高层进行推理，*任何* tool——无论是 Claude Code 还是 raw shell command——都是同样可用的选项。

---

### 关键架构后果

这种对等级别的抽象有一个深刻的影响：**Claude Code 不再是“特殊 agent”——它只是用于编程任务的 specialist tool。** 它失去了作为“执行环境”的特权位置。LLM 决定：*“我应该使用 Claude Code（用于复杂 refactoring）还是直接运行 shell command（用于快速 `grep`）？”*——两者都是同等的一等选项。

模型发出 shell_call 项目，runtime 执行它们——模型充当 planner，shell 充当 executor。在 OpenClaw 的情况下，这个 planning layer 位于 *一切* 之上，没有单一 sub-agent 拥有特殊权限。

---

### 这是一个更好的抽象吗？是的——但有权衡

**为什么更好：**

- **可组合性**：Tools 可互换和组合。没有人为嵌套。
- **灵活性**：你可以将 Claude Code 替换为另一个 coding agent，而无需重构整个系统。
- **人类对齐**：匹配人类实际委托任务的方式——基于意图，而非工具层次。
- **模型无关**：OpenClaw 是 model-agnostic 的——你在 openclaw.json 中配置 providers，Gateway 相应路由。Orchestrator 不关心使用哪个 brain 或哪个 tool。

**权衡：**

扁平工具架构将更多责任推给 orchestration layer。Tool approval workflows 通过明确的用户确认来限制危险操作（文件删除、shell commands、支付），scoped permissions 分离读写访问。当一切都是对等级别的 tool 时，orchestrator 必须更加小心 *允许什么*——因为没有自然层次来限制损害。

---

### 总结

这个抽象真正优雅：通过将“运行命令”、“使用 Claude Code”和“浏览网页”视为单一 orchestrator 下的扁平、对等能力，OpenClaw 更紧密地镜像人类思考任务执行的方式——意图驱动，而非工具层次驱动。Claude Code 成为 *另一个 tool*，这实际上是为通用 agent 的正确思维模型。

参考资料：

- [How OpenClaw Works – Medium](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Inside OpenClaw – DEV Community](https://dev.to/entelligenceai/inside-openclaw-how-a-persistent-ai-agent-actually-works-1mnk)
- [What Is OpenClaw – Milvus Blog](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [How Personal AI Agents Are Made – GitHub Gist](https://gist.github.com/championswimmer/bd0a45f0b1482cb7181d922fd94ab978)
