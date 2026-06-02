---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 应避免的 AI 提示错误
translated: true
type: note
---

Question: 人们常见地错误或低效使用 AI/LLM 工具（如 Claude、Copilot 等）的方式有哪些，特别是在编写简单提示时没有提供适当的上下文或明确的问题？

Answer:

是的，你完全正确。这是当今 AI 使用中最普遍且有充分记录的问题之一。以下是全面的分解：

---

## The Core Problem: "Prompt and Pray" Mentality

人们最常见的错误之一是提交模糊、一般的提示，并期望 AI “读心”。弱提示会造成“priming problem”，AI 缺少足够的上下文来提供相关响应。

糟糕的提示编写不仅仅限于终端用户——构建调用 LLM API 应用程序的人也经常编写缺乏细节的简短提示，导致不满意且不一致的结果。

---

## The Main Ways People Use AI Inefficiently

### 1. Vague, Imprecise Language
使用主观或不精确的语言，如“make it more professional”或“summarize this”，这让 LLM 不知道“professional”对你意味着什么。这会导致非确定性、不一致的输出，无法可靠使用。

**Example of weak vs. strong prompt:**
- ❌ Weak: `"How do I add numbers in Excel?"`
- ✅ Strong: `"How do I add up a row of dollar amounts in Excel? I want to do this automatically for a whole sheet of rows with all the totals ending up on the right in a column called 'Total'."`

---

### 2. Missing Context (No Background, Audience, or Purpose)
一个常见的错误是遗漏重要的背景细节，如目标受众、语气或目的。像“Create an article on market segmentation”这样的模糊提示无法提供足够的指导来获得专注的结果。

对于 Claude Code 和 Copilot 来说，这意味着没有告诉 AI：
- 你使用的是什么语言/框架
- 现有代码库的样子
- 该功能对终端用户应该做什么

---

### 3. No Clear Goal / Wrong Problem Framing
“Type III Error”发生在提示编写得很好且模型精确遵循，但输出无关或无帮助，因为底层任务被误解了。模型精确做了被要求的事，但提示针对的是错误的目标。失败不在执行，而在框架。

---

### 4. Not Specifying Output Format or Length
没有指定期望的输出长度或细节级别，会让模型猜测——它可能给你一个句子而你需要一段话，或者给你一篇完整的文章而你只需简短摘要。

---

### 5. Overloading a Single Prompt
将太多内容塞进单个提示会导致混淆和稀释的输出。相反，将请求分解成更小、更专注的部分，能让 AI 更容易处理并交付连贯的结果。

---

### 6. Not Telling the AI What to *Exclude*
告诉 LLM 包括什么但不告诉排除什么，可能会导致模型包含样板文本、免责声明或你不想要的特定主题——迫使你手动编辑输出，这违背了自动化的目的。

---

### 7. Hidden Assumptions — Assuming the AI Knows What You Know
你不能假设 AI 知道你知道的，因为你的专业知识可能不在其训练数据中。因此，你应该总是审视提示并问“仅凭提供的信息我能解决吗？”很多时候，你基于自身经验认为明显的东西其实一点也不明显。

---

### 8. Not Iterating — Expecting Perfect Results on the First Try
常见的错误包括期望提示第一次就完美工作、不基于结果迭代、不在测试时隔离变量，或事情不顺时过早放弃。将提示编写视为迭代和实验过程——假设、隔离并系统地精炼。

---

### 9. Trusting AI Output Without Verification
常见的错误包括信任模型的自信、不事实核查重要信息、假设连贯性意味着正确，或不验证逻辑一致性。

---

## Quick Reference: What a Good Prompt Should Include

| 元素 | 示例 |
|---|---|
| **Role/Context** | "You are a senior Python developer..." |
| **Task** | "...refactor this function to be async..." |
| **Constraints** | "...without changing the existing API signature..." |
| **Output format** | "...and explain the changes in bullet points." |
| **Audience** | "Assume the reader is a junior dev." |
| **Exclusions** | "Do not use third-party libraries." |

---

## The Golden Rule

即使是最聪明的 LLM 如 GPT-4 或 Claude，也无法读心——模糊提示会消耗你的计算预算、增加错误并侵蚀信任。要明确——绝不假设 AI “知道”你的业务。

把 AI 想象成一个非常能干但全新的承包商：他们需要完整的简报，而不仅仅是粗略的想法。

参考文献：

- [10 Common LLM Prompt Mistakes Killing Your AI's Performance](https://www.goinsight.ai/blog/llm-prompt-mistake/)
- [Thinking Clearly with LLMs: Mental Models and Cognitive Pitfalls](https://dev.to/puritanic/thinking-clearly-with-llms-mental-models-and-cognitive-pitfalls-in-prompt-engineering-3dmm)
- [Common AI Prompt Mistakes and How to Fix Them](https://www.godofprompt.ai/blog/common-ai-prompt-mistakes-and-how-to-fix-them)
- [Common Prompt Engineering Mistakes to Avoid in 2026](https://treyworks.com/common-prompt-engineering-mistakes-to-avoid/)
- [Beyond "Prompt and Pray": 14 Prompt Engineering Mistakes](https://odsc.medium.com/beyond-prompt-and-pray-14-prompt-engineering-mistakes-youre-probably-still-making-c2c3a32711bc)
- [Overcoming Bad Prompts with Help from LLMs](https://www.dbreunig.com/2025/03/16/overcoming-bad-prompts-with-help-from-llms.html)
- [Tricks to Fix Stubborn Prompts](https://incident.io/building-with-ai/tricks-to-fix-stubborn-prompts)
