---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 精准上下文优于仅自然语言
translated: true
type: note
---

Question:
称其为“LLM's language”是不正确的吗？更准确的看法是否应该是 Prompt 应该包含具体的 Context（如 CSS selectors、HTML 或 code），而不仅仅是自然英语？

Answer:

是的——说 **“LLM’s language”** 并不准确。你修正后的理解更为到位。

LLM **并没有一种特殊的语言**。它们接受 **任何文本**：

* English
* Chinese
* code
* HTML
* CSS selectors
* logs
* stack traces
* JSON
* 混合内容

真正重要的是 **context precision**（上下文精确度），而不是所谓“LLM language”。

你的想法可以更精确地表达如下：

### Core Idea

当 **prompt 包含具体的、机器层面的 context**，而不是模糊的自然语言时，LLM 的表现最好。

Bad prompt（模糊）：

```
Click that button and extract the text
```

Good prompt（精确上下文）：

```
Click this element:
<button class="btn-primary submit-order" data-testid="checkout-submit">

CSS selector:
button[data-testid="checkout-submit"]

Then extract text from:
<div id="order-confirmation">
```

第二个效果更好，因为：

* 消除了歧义
* 减少了 hallucination
* 提供了准确的 DOM 结构
* 与模型在代码中见到的内容相匹配

---

### Why English-only prompts are weaker

自然语言：

```
click the blue button on the right
```

问题：

* 可能存在多个蓝色按钮
* 布局可能会改变
* 模型必须进行猜测

但这是确定性的：

```
document.querySelector('#checkout > button.primary')
```

LLM 不需要猜测——它直接执行 reasoning。

---

### So the real principle

不是“LLM language”，而是：

**LLM 更倾向于 structured context，而非 descriptive language**

最佳的 prompt = 以下内容的混合：

* 自然语言（意图）
* code（精确度）
* selectors（位置）
* logs（状态）
* errors（反馈）

理想 prompt 示例：

```
Goal: click checkout button

HTML:
<button id="checkout-btn" class="primary">

Selector:
#checkout-btn

Error:
Element not clickable at point (532, 410)

What's wrong?
```

这种方式非常强力。

---

### Why Copilot / Claude Code work better with copied code

因为它们是 **context-driven**（上下文驱动），而不是语言驱动。

当你粘贴：

* VSCode code
* DOM HTML
* CSS selectors
* stack trace

你为模型缩小了 **search space**。

更少的猜测 → 更好的输出。

---

### Your corrected statement (most accurate)

你改进后的理解是正确的：

* LLM 不需要特殊语言
* 任何文本都有效
* 但是 **prompt + context 必须自洽 (self-consistent)**
* 复制真实 code/HTML/selectors 会提升结果

这完全正确。

---

### One-sentence summary

LLM 不需要特殊语言——当 prompt 包含 **精确的真实 context (code, selectors, logs)** 而非模糊的自然语言时，其表现最佳。