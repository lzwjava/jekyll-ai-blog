---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 提示的勉强好原则
translated: true
type: note
---

问题： “doing things barely” 原则如何应用于为 LLM 编写提示词以及使用 Claude Code 等工具——在上下文过少和过多之间找到甜蜜点？

回答：

## LLM 提示词的 “Barely Good” 原则

这是该哲学的一个尖锐延伸。对于 LLM，同样存在校准挑战——但动态是独特的，因为 **LLM 已经携带着庞大的世界知识**。你不是从零教它们；你是在 *引导* 一个已经高度能力的事物。

---

## 两种失败模式

| Too Little | Barely Good | Too Much |
|---|---|---|
| LLM 不知道目标 | 清晰意图 + 关键约束 | 过度指定、僵硬、浪费 tokens |
| 做出错误假设 | 正确假设引导 | 没有空间给 LLM 自己的判断 |
| 输出偏离要点 | 输出很好命中目标 | LLM 变成哑巴执行者 |
| Agent 徘徊或循环 | Agent 有目的地前进 | Agent 被微观管理到失败 |

---

## 为什么 LLM 需要比你想象的少

像 Claude 这样的 LLM 已经内化了：
- Coding best practices、design patterns、languages
- Writing styles、formats、genres
- 医学、法律、科学、工程等领域的领域知识
- Reasoning frameworks 和 step-by-step problem solving

所以当你编写提示词时，你 **不是填充一个空容器**——你是在 **给专家一个方向**。一个好的经理不会向资深工程师解释什么是 for-loop。他们会说：*“为 API 构建一个 rate limiter，使用 Redis 支持，每用户 100 req/min。”* 就是这样。

---

## 将此应用于 Claude Code

Claude Code 是一个 agentic coding tool。此处的 “barely enough” 提示词原则意味着：

**告诉它：**
- 目标是什么
- 关键约束或非显而易见上下文
- “done” 是什么样子（如果不明显）

**不要告诉它：**
- 如何编写每个函数
- 哪些 libraries 存在（它知道）
- 标准任务的 step-by-step 指示
- 你已经知道的关于 codebase 的所有内容，它可以自己读取

**示例 — Too Much：**
> "Please open the file users.py, look at the User class, add a method called get_full_name that concatenates first_name and last_name with a space between them, make sure to add a docstring, use f-strings, and return a string."

**示例 — Too Little：**
> "Fix users."

**示例 — Barely Good：**
> "Add a `get_full_name` method to the User model in users.py."

Claude Code 会读取文件，理解现有风格，编写 idiomatic code，如果那是模式，还会添加 docstring——无需被告知。

---

## Barely Good 提示词的艺术

技巧是知道 **省略什么**——这需要理解：

1. **LLM 已经知道什么** — standard patterns、common libraries、language idioms。不要解释这些。
2. **什么对你情况独特** — 你的 business logic、你的 architecture decisions、非显而易见约束。始终包含这些。
3. **目标是什么样子** — 成功标准的简短陈述。一句话往往就够。
4. **什么要避免** — 如果有真正偏离方向的风险，一两个负面约束（“don't modify the schema”）。

---

## 更深层的洞见

就像眼镜和空调一样——该原则要求 **你非常了解领域** 才能应用它。新手无法编写 barely-good 提示词，因为他们不知道 LLM 已经处理什么。他们出于焦虑过度指定，或出于懒惰欠指定。

掌握表现为 **简洁而精确**——少量词语、正确词语、对模型会正确推断的正确假设。

> 编写 barely good 提示词本身就是一个证明理解的技能——对任务、对 LLM 能力，以及它们之间实际差距的理解。

这正是为什么经验丰富的工程师比新手写更短的提示词，并获得更好结果。

参考：

- [https://lzwjava.github.io/vision-tips-en](https://lzwjava.github.io/vision-tips-en)
- [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)