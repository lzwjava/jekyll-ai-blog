---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 审查 AI 智能体流程策略
translated: true
type: note
---

Question: When working with OpenClaw (AI agent), is using a prompt like "give review about how you do it" a good strategy to get the agent to explain its process in detail, so we can copy and save that review?

Answer:

## 在 AI Agents 中使用 "Give Review About How You Do It"

是的 —— 这实际上是一个 **非常稳健的 prompting strategy**，以下是它之所以奏效的原因以及一些需要注意的细节。

---

### ✅ 为什么有效

当你要求像 OpenClaw 这样的 AI agent **"give a review about how you did it"** 时，你实际上是在触发一个 **self-reflection / retrospective step（自我反思/回顾步骤）**。这会促使 agent 执行以下操作：

- **总结完成任务所采取的步骤**
- **解释其决策背后的推理过程**
- **呈现其执行的 tool calls、API 请求或 sub-tasks**
- **突出显示其遇到的任何假设或 tradeoffs（权衡）**

这在 agent prompting 中有时被称为 **"post-task debrief"** 模式 —— 它是非常实用的。

---

### 📋 这种方法能带给你什么

| 优势 | 描述 |
| --- | --- |
| **Transparency（透明度）** | 你不仅能看到结果，还能看到 agent 做了 *什么* |
| **Auditability（可审计性）** | 你可以验证执行步骤是否正确 |
| **Documentation（文档化）** | review 本身成为了一个可重复使用的记录 |
| **Debugging（调试）** | 如果出现错误，review 会揭示问题出在哪里 |
| **Learning（学习）** | 帮助你理解 agent 的 workflow，以便后续复制 |

---

### 🔧 如何使其更出色

你可以稍微强化 prompt 以获得结构更清晰的输出：

```
"Give a review of how you completed this task — include:
1. The steps you took
2. Any tools or sources you used
3. Key decisions you made and why
4. Any limitations or assumptions"
```

或者，使用简短版本：

```
"Summarize what you did step by step, so I can save it as a log."
```

---

### ⚠️ 需要注意的事项

- **AI agents 可能会对自己的处理过程产生 hallucinate（幻觉）** —— 它们描绘的步骤可能听起来很合理，但未必是内部真正发生的情况。请务必结合实际输出来进行交叉检查。
- 某些 agent 对其内部 tool calls 的 **自我感知有限** —— review 可能是一种事后重构，而非真实的 log。
- 如果你需要 **真实的 audit trail（审计追踪）**，应寻找 agent platform 内置的 logging 功能，而不是仅仅依赖其自我汇报的 review。

---

### ✅ 总结

总结来说，**"give review about how you do it"** 是一个完全有效且实用的 prompt。这是一种无需访问 backend logs 就能从 agent 提取流程总结的轻量化方法。只需将其视为一份 **human-readable（人类可读）的任务总结**，而不是保证 100% 准确记录了每一个内部步骤。
