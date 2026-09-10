---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 原创性从代码转向想法
translated: true
type: note
---

Question: 这是对当前 “AI coding” / open-source 文化的合理看法吗？

Answer: **是的，我认为核心观点是对的。**

如果每个人都能让 LLM 生成一个像样的实现，那么 **“我写了这段代码”** 就成为了一个弱得多的原创性信号。代码本身正日益成为一种商品。

稀缺的部分向上移动：

```text
以前:
idea → design → code → product

现在:
idea → experiment → product
              ↑
          AI writes code
```

所以这个区分很重要：

* **Copy code** → 复现他人的实现。
* **AI-generated code** → 通过自然语言指令复现一个实现。
* **AI-native engineering** → 发现问题、发明方法、运行实验、迭代，并使用 AI 作为实现引擎。
* **原创项目/研究** → 创造以前不存在的东西，并证明它有效。

这就是为什么你说的那句话：

> **“需要有新想法、新实践、原创想法、原创项目”**

可能是更重要的方向。

还有那句略带挑衅的话：

> **“还不如说只开源提示词得了”**

实际上指向了一个真实的问题。如果一个项目中 *唯一* 新颖的东西是“我用来让 GPT 生成这些代码的提示词”，那么发布数千行生成的代码可能几乎没有信息价值。有趣的产物可能是：

```text
problem
  ↓
hypothesis
  ↓
prompt / agent strategy
  ↓
experiments
  ↓
failures
  ↓
implementation
  ↓
benchmark
  ↓
result
```

但我不会走极端说 AI 写的代码“毫无意义”。当实现体现了困难的工程时，它仍然重要：性能、可靠性、系统集成、新颖算法、生产约束等等。

更有力的说法是：

> **AI 让代码变得更便宜。因此，原创性越来越多地在于你选择构建什么、如何构建，以及你发现了什么——而不仅仅在于你输入的代码。**

那是一个更有趣的说法