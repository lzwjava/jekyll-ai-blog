---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM 工具使用决策详解
translated: true
type: note
---

**问题：** LLM 决定是否调用工具的那个 LLM API 功能叫什么？这个决定是通过 pre-training 还是通过 RLHF 内置到模型中的，LLM 在做出这个决定方面是否真的擅长？

---

**回答：**

## 这个功能叫什么？

您描述的功能称为 **Tool Calling**（也称为 **Function Calling**）。它是现代 LLM API（OpenAI、Anthropic、Google 等）的核心能力，允许模型自主决定是否需要调用外部函数/工具，如果需要，则生成带有正确参数的结构化调用。

Tool calling 是 LLM 调用外部函数或服务来完成任务的机制。模型不会幻觉响应，而是将特定请求传递给外部工具——例如，将数学问题发送到计算器、检查 weather API 获取预报，或查询数据库获取客户详情。

---

## 这个“决定”在运行时是如何工作的？

当您向 LLM API 发送请求时，您会包含可用工具定义列表（名称、描述、参数的 JSON schema）。模型会与用户消息一起阅读这些定义，然后决定：

- **是的，我需要工具** → 输出结构化的 JSON tool call（不是纯文本）
- **不，我可以直接回答** → 输出正常的文本响应

这个决定仍然是概率性的——您可以通过 prompts、schema 和 `tool_choice` 来塑造它，但不能像确定性规则引擎那样编程它。

您还可以通过 API 的 `tool_choice` 参数强制指定行为：
- **`auto`** — 模型自行决定（最常见）
- **`required`** — 强制模型总是调用工具
- **`none`** — 完全禁止工具调用
- **特定工具名称** — 强制调用特定工具

---

## 这个能力来自 Pre-Training 还是 RLHF？

答案是 **两者都有**，分层应用。这是一个多阶段训练过程：

### 1. Pre-training（基础知识）
在海量文本语料库上进行 pre-training 时，模型学习通用推理、语言模式和意图识别。LLM 发展出对语言模式、语义关系和意图的深刻理解。当它遇到工具定义时，它学会将用户查询中的特定模式与工具描述的功能关联起来。这不是显式编程，而是从训练数据中学到的关联。

### 2. Supervised Fine-Tuning (SFT) — 主要机制
教授 tool-calling 的主要方式是通过 **SFT on tool-use trajectories**（正确 tool-calling 行为的示例）。大多数现代 tool-use 语料库是合成的或 bootstrapped 的——如 Toolformer 风格的自标注或 ToolBench 中的大规模生成。对于训练目标，针对工具轨迹的 supervised fine-tuning (SFT) 教授基本的格式化和工具选择。这会 bootstrapping 该行为，通常足以建立技能的基础。

### 3. Preference Optimization (DPO / RLHF) — 精炼
在 SFT 之后，使用 RLHF 或 DPO 来精炼 *何时* 调用工具 vs. 直接回答。针对轨迹的 preference optimization（例如 DPO）可以改善何时调用工具 vs. 直接回答的决策。对于具有多步工具使用的 agentic 任务，使用环境反馈（任务成功、约束满足）的 RL 成为自然目标——模型从其工具增强动作是否实际解决问题中学到经验。

因此完整流程如下：

```
Pre-training → SFT on tool trajectories → DPO/RLHF for when-to-call decisions → RL from environment outcomes (for agents)
```

---

## LLM 在这个决定方面真的擅长吗？

**总体上是的，但不完美。** 以下是细致的分析：

**模型擅长：**
- 识别明显的需要工具的查询（例如，“现在天气怎么样？”、“搜索 X”）
- 当工具描述清晰且命名良好时，选择正确的工具
- 根据 JSON schema 正确格式化参数

**模型可能挣扎：**
- 工具使用可选的模糊情况
- 在多个相似工具之间选择
- 知道 *何时不* 调用工具（过度调用）
- 糟糕的工具描述会导致坏决策

在 system prompt 中添加关于何时及如何使用工具的明确指导，可以提供额外上下文。这可能显得重复，但有助于 LLM 做出更好决策，尤其是多个工具时。

一些模型，尤其是 reasoning models，在决定何时及如何调用工具方面表现更好。

**关键洞见：** 您的工具 *描述* 和 *system prompt 指导* 的质量会极大地影响决策质量——这是训练和运行时 prompting 的协作。

---

## 总结表格

| 阶段 | 在 Tool Calling 中的作用 |
|---|---|
| Pre-training | 学习语言、推理、语义意图 |
| SFT | 学习工具调用格式和基本选择 |
| DPO/RLHF | 学习 *何时* 调用 vs. 直接回答 |
| RL (agentic) | 从结果中学习多步决策 |
| Runtime prompting | 通过描述和 system prompt 进一步塑造决策 |

---

**参考文献：**

- [What is LLM Tool Calling? — Portkey](https://portkey.ai/blog/what-is-llm-tool-calling/)
- [The Anatomy of Tool Calling in LLMs — martinuke0](https://martinuke0.github.io/posts/2026-01-07-the-anatomy-of-tool-calling-in-llms-a-deep-dive/)
- [How Tool Calling Works in LLMs — Scalable Thread](https://newsletter.scalablethread.com/p/how-tool-calling-works-in-llms)
- [Tool Use — RLHF Book by Nathan Lambert](https://rlhfbook.com/c/13-tools)
- [Function Calling — Prompt Engineering Guide](https://www.promptingguide.ai/agents/function-calling)
