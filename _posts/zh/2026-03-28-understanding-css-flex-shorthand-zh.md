---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深入理解 CSS Flex 简写属性
translated: true
type: note
---

Question: 在 CSS 中 `flex: 0 1 20%` 是什么意思？

Answer: `flex` 属性是三个特定 flexbox 属性的缩写。当你写下 `flex: 0 1 20%` 时，你正在定义一个 flex item 如何 grow、shrink 以及它的初始 size。

### 属性值详解

1.  **`0` (flex-grow):**
    这定义了在 container 存在剩余空间时，flex item 增长的能力。值为 `0` 意味着该 item **不会增长** 来填充剩余空间。它将仅保持其内容宽度或其 `flex-basis` 定义的宽度。

2.  **`1` (flex-shrink):**
    这定义了在 container 空间不足时，flex item 缩小的能力。值为 `1`（默认值）意味着该 item **会缩小**，与其他 items 成比例缩放，以防止溢出 container。

3.  **`20%` (flex-basis):**
    这定义了在分配剩余空间之前元素的默认 size。将其设置为 `20%` 意味着该 item 的初始宽度（或高度，取决于 `flex-direction`）为 **parent container 的 20%**。

---

### 总结表

| Property | Value | Description |
| :--- | :--- | :--- |
| **flex-grow** | `0` | 不会扩展以填充额外空间。 |
| **flex-shrink** | `1` | 如果 container 变得太小，则会缩小。 |
| **flex-basis** | `20%` | 初始大小为 container 宽度/高度的 20%。 |

### 实际表现
如果你有一行包含五个都设置为 `flex: 0 1 20%` 的 items，它们将完美地填满这一行。但是，如果你只有两个设置为此属性的 items，它们将各占宽度的 20%，并留下 container 60% 的空白，因为 `flex-grow` 设置为了 `0`。

需要我为你展示这与 `flex: 1 1 20%` 表现差异的代码示例吗？