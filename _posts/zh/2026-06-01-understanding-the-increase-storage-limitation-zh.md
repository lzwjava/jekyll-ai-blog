---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解存储增加的限制
translated: true
type: note
---

答案就在HTML中：

```html
<input type="number" min="101" max="16384" step="1" value="101">
```

**`min="101"`** — 允许的最小大小是 **101 GB**。

但 `200 > 101`，所以它应该能通过HTML5约束。该"invalid size"错误很可能是因为 **你的卷大小已经 >= 200 GB**。这是一个 **"Increase storage size"** 模态框——它只允许 **大于当前卷大小** 的值。如果卷已经是200或更大，你就不能将其设置为200。

你当前的卷大小是多少？如果已经是200 GB，你需要输入至少201。
