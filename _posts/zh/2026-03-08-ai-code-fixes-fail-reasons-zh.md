---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么 AI 代码修复经常失败
translated: true
type: note
---

**问题：** AI 编码助手如 Copilot（或 GPT-5.1-codex-max、GPT-5.2、GPT-5.3-codex 等变体模型）无法修复代码的主要原因是什么——是提示/上下文不良，还是模型能力限制？

**回答：**

## 重要澄清先行

模型名称 **gpt-5.1-codex-max**、**gpt-5.2** 和 **gpt-5.3-codex** 并不对应截至 2026 年 3 月任何公开发布或文档化的 OpenAI/GitHub Copilot 模型。这些似乎是推测性的、内部引用的或记错的名称。下面分析适用于一般的 Copilot 驱动的 AI 代码助手（使用 OpenAI 模型），因为失败模式与具体模型版本无关，是一致的。

---

## Copilot / 基于 LLM 的代码修复器失败的顶级原因

### 1. 上下文不足或不良（罪魁祸首 #1）

这是最常被引用的根本原因。尽管授予 Copilot 访问所有项目文件，但它仅分析代码的一小部分，并用假设填充其余部分——而不警告用户其限制。在实践中，这意味着 Copilot 甚至在实际代码可用时，也可能捏造 API 结构、认证流程、数据库关系和文件结构。

上下文问题以多种方式表现：

- **未包含足够的相關文件** — 除非明确在范围内，否则 Copilot 无法理解跨文件依赖。
- **提示过于模糊** — 说“修复 bug”而不指定哪个文件、哪个函数或预期行为，会让模型猜测。
- **上下文窗口过载** — 系统提示、对话历史、检索文档和输出 token 都会争夺同一空间。即使未达到硬 token 限制，“上下文腐烂”也可能发生——即随着输入长度增加，模型性能下降。

### 2. “迷失在中间”问题（模型注意力偏差）

即使提供了正确的上下文，模型也可能无法有效利用它。LLM 倾向于更重视提示的开头和结尾——称为 primacy 和 recency bias。因此，放置在中间的重要上下文可能被模型低估。对于长代码库，埋藏在大文件中间的关键 buggy 函数可能根本得不到足够的模型注意力。

### 3. 幻觉和过度假设

跨文件的变量名称不匹配（例如，一个文件中的 `phone` 与另一个中的 `phone_number`）、数据类型不匹配，以及重复逻辑而不是重用 utility 函数，都是常见错误。模型自信地生成看起来合理但不正确的代码，因为它是从训练数据中进行模式匹配，而不是从您的实际代码库中推理。

### 4. 模型做了超出要求的事（范围蔓延 / 指令遵循失败）

当被要求制定计划或讨论某事时，Copilot 有时会开始实现整个功能。例如，当要求实现 database models 时，它会超出范围，生成 migration 文件，尝试运行它们，失败，读取代码库，修改 migration 文件，再次尝试运行，又失败，并陷入循环。这反映了 **提示指令遵循的弱点**，而非模型智能问题——模型未能严格遵守请求的范围。

### 5. 整文件重写而不是针对性修复

Copilot 有时会用更新代码重新生成整个文件，而不是仅编写针对性片段，这意味着开发者无法轻松看到变化，必须从头审查整个文件。这是 UX 失败，也是模型未正确限定输出范围的症状。

### 6. 缺乏系统级 / 架构理解

Copilot 编写的代码单个工作正常，但整个系统变成架构混乱。它在函数或文件级别优化，而不是系统架构级别。除非您每次在提示中明确编码，否则它没有对您的设计模式、命名约定或长期可维护性目标的持久理解。

### 7. 长对话下的上下文窗口退化

在多轮对话中，每一轮交换都会增加 token。LLM 在多轮对话中的表现明显不如单轮交互，高性能模型在扩展对话中会变得像较小模型一样不可靠。运行多轮“修复这个，现在修复那个”的调试会话会逐渐降低模型正确推理的能力。

### 8. 提示质量往往是用户的错

自动程序修复的研究证实了这一点：LLM 修复代码的有效性仍受随意确定的上下文限制——无法根据每个缺陷情况自适应选择特定上下文。包含失败测试、错误消息和相关代码部分的结构化、针对性提示，远胜于通用的“修复我的 bug”指令。

---

## 总结：是提示/上下文还是模型能力？

**两者皆有——但上下文/提示质量是更具可操作性和主导因素。** 对于大多数日常 bug，模型的原始能力并非主要瓶颈。失败最常追溯到：

| Factor | Weight |
|--------|--------|
| 提供的上下文不足 | 非常高 |
| 模糊或范围不明的提示 | 高 |
| 迷失在中间 / 上下文放置 | 中高 |
| 长会话中的上下文窗口溢出 | 中等 |
| 真正的模型推理限制 | 中等（针对复杂 bug） |
| 幻觉 / 过度假设 | 中等 |

**实用改进：** 始终指定确切的文件、函数、错误消息和预期行为。保持会话简短且专注。对于多文件 bug，手动粘贴仅直接相关的部分，而不是依赖 Copilot 查找它们。

**参考文献：**

- [GitHub Copilot Serious Issue Discussion (GitHub Community)](https://github.com/orgs/community/discussions/162634)
- [Stop Blindly Trusting GitHub Copilot: 4 Reasons It's Failing (HowToGeek)](https://www.howtogeek.com/github-copilot-is-powerful-but-these-issues-kept-slowing-me-down/)
- [GitHub Copilot Wrote 80% of Our Code. We're Rewriting All of It (Medium)](https://medium.com/codetodeploy/github-copilot-wrote-80-of-our-code-were-rewriting-all-of-it-6c76a1ca6ef0)
- [Context Window Overflow in 2026 (Redis)](https://redis.io/blog/context-window-overflow/)
- [Context-Aware Prompting for LLM-Based Program Repair (Springer)](https://link.springer.com/article/10.1007/s10515-025-00512-w)
- [LLM Context Window Limitations: Impacts, Risks, and Fixes (Atlan)](https://atlan.com/know/llm-context-window-limitations/)
- [Top Techniques to Manage Context Lengths in LLMs (Agenta)](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms)