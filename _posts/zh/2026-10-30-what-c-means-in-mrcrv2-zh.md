---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MRCRv2中C的含义
translated: true
type: note
---

**问题：** “Multi-Round Coreference Resolution version 2”中的“C”代表什么？

**回答：**

**C = Coreference** —— 即 **Coreference Resolution**，一个经典的NLP概念。

---

### 什么是Coreference Resolution？

在语言学和NLP中，**coreference** 指两个或多个表达指向同一个**实体**。

> 示例：
> - *“写一首关于企鹅的诗……现在把**那首诗**再给我一次。”*
> - “那首诗” **co-refers** 到之前关于企鹅的诗的请求。

**Coreference resolution** 是找出文本中哪些表达指向同一事物的任务。

---

### 它在MRCRv2中的应用

在MRCR中，模型必须在长对话中导航，用户请求撰写各种主题的文本（诗、谜语、散文），并且必须重现与其中一个请求匹配的特定输出（“needle”），将其与类似的混淆输出区分开，例如“关于企鹅的诗”与“关于火烈鸟的诗”。

因此，**“C”（Coreference）** 的挑战在于：
- 模型看到多轮对话
- 一个查询指向**一个特定的早期交流**（例如，“第一首关于企鹅的诗”）
- 模型必须正确**解析查询所co-refer的是哪个先前的回答**
- 然后准确重现它

“Multi-Round”部分意味着这种coreference跨越**许多轮次**，出现在很长的上下文（最高1M tokens）中。

---

### 全称分解

| 部分 | 含义 |
|---|---|
| **Multi-Round** | 跨越多个对话轮次 |
| **Coreference** | 指向同一早期项目 |
| **Resolution** | 正确识别所指的项目 |
| **v2** | 增强版本，包含更多needle和更长上下文 |

**参考文献：**
- [Michelangelo Paper (arXiv:2409.12640)](https://arxiv.org/abs/2409.12640)
- [MRCR Leaderboard - LLM Stats](https://llm-stats.com/benchmarks/mrcr)