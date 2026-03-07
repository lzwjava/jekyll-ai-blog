---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X 翻译跳过引用帖子
translated: true
type: note
---

**问题：** 在 Twitter/X 上，我设置了从中文到英文的自动翻译。当有人转发中文帖子时，转发中添加的文字显示为英文——这没问题——但原始被引用/嵌入的帖子仍然显示为中文。这是为什么，以及如何修复？

---

**回答：**

这是 X (Twitter) 在处理转发和引用帖子上下文中的翻译功能的**已知限制**。以下是清晰的解释，以及你可以采取的措施。

---

## 为什么会这样

当有人转发（或引用推文）一个中文帖子时，屏幕上实际上渲染了**两个独立的文本块**：

1. **转发者的评论** —— 这是转发者撰写的“新”帖子，因此 X 的自动翻译引擎会正常处理并将其翻译成英文。
2. **嵌入的原始帖子** —— 这是一个独立的嵌套帖子对象。X 的翻译系统**并不总是自动翻译嵌入/引用的帖子**，即使启用了自动翻译。原始帖子被视为引用的卡片，而不是你时间线中的新鲜内容。

这本质上是 X 翻译功能的**设计缺陷** —— 自动翻译适用于顶级时间线帖子，但嵌入的引用内容可能会漏译。

---

## 你可以做什么

### 选项 1：手动翻译原始帖子
点击原始帖子的日期/时间链接，直接跳转到该帖子。因为现在你将其视为独立帖子，X 会直接在其上显示**“翻译帖子”**链接 —— 点击即可获取翻译。

### 选项 2：使用 Grok 自动翻译（如果你的账户可用）
X 已推出使用 Grok AI 自动翻译时间线帖子的功能。帖子翻译后，你会在推文顶部看到“Translated by Grok – Show original”文字。如果你的账户已激活此功能，它可能比旧系统更可靠地翻译嵌入帖子。

### 选项 3：使用浏览器内置翻译
如果你使用 Microsoft Edge 或 Chrome，可以拖动选中中文文本，右键选择“Translate Selection to English” —— 浏览器的内置翻译（由 Google Gemini 或类似技术提供）可以处理 X 系统遗漏的文本。

### 选项 4：使用浏览器扩展
像“Post Translator for Twitter X”这样的扩展可以自动检测原始语言，并在不干扰页面布局的情况下直接在其下方翻译文本，覆盖 X 原生翻译可能遗漏的内容 —— 包括嵌入的引用帖子。

---

## 总结

  
| Content Type | Auto-Translated? |
|---|---|
| Reposter's own comment | ✅ 是（通常） |
| Embedded original Chinese post | ❌ 经常被跳过 |

这是平台级限制。在 X 改进嵌套/引用帖子的翻译覆盖之前，**点击进入原始帖子**或**使用浏览器扩展**是你最可靠的解决方案。

---

**参考资料：**

- [Ask Dave Taylor – How to Translate Posts on X](https://www.askdavetaylor.com/how-to-translate-foreign-language-posts-on-twitter-x/)
- [Croma – How to Turn Off X's Grok Auto-Translations](https://www.croma.com/unboxed/how-to-turn-off-x-grok-translations)
- [Chrome Web Store – Post Translator for Twitter X](https://chromewebstore.google.com/detail/post-translator-for-twitt/pbmchlbpmommkfpafninfdcjheapdkfi)