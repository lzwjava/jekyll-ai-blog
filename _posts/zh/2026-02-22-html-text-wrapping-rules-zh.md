---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HTML 文本换行规则详解
translated: true
type: note
---

问题：在 HTML 中，如果不使用换行标签，文本何时换行到新行？

答案：

在标准的 HTML 渲染中，如果在一段文本中不使用明确的换行标记（如 `<br>` 标签）或块级元素，浏览器会根据**containing element 的宽度**（viewport 或父容器）自动处理换行。

文本将在一行上继续，直到达到**窗口边界**（或特定容器的宽度）。一旦文本到达此边界，浏览器会自动将剩余内容换行到下一行，以确保其适合可见区域。此行为称为 "word wrapping"。

因此，在没有手动标记的情况下，断行仅在遇到窗口边界时发生这一说法是**正确的**。

参考资料：

- [https://developer.mozilla.org/en-US/docs/Web/CSS/white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)
- [https://www.w3.org/TR/CSS2/text.html#white-space-prop](https://www.w3.org/TR/CSS2/text.html#white-space-prop)