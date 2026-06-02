---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HDLC 帧标志详解
translated: true
type: note
---

Question: 在 HDLC 帧格式中，flag 字段 F 是什么？

Answer:

## HDLC Flag Field

正确答案是 **D: 01111110**

### Explanation

HDLC (High-Level Data Link Control) 使用一个特殊的位模式作为 **flag** 来标记帧的边界。

flag 字段的值是：

```
01111110
```

这个模式有两个用途：

- 它标记前一个帧的 **end**
- 它标记下一个帧的 **beginning**

### Why 01111110?

flag `01111110` 包含 **六个连续的 1s**，周围被 0s 包围。为了防止这个模式意外出现在数据负载中，HDLC 使用一种称为 **bit stuffing** 的技术：

- **Sender side**：在数据中每五个连续 1s 后，自动插入一个 `0`
- **Receiver side**：接收到五个连续 1s 后，如果下一个位是 `0`，则自动移除（destuffed）

这确保 `01111110` 模式 **only** 作为实际的帧分隔符出现，而不会作为数据内容的一部分。

### Why the other options are wrong?

| 选项 | 值      | 原因                          |
|------|---------|-------------------------------|
| A    | 11111111 | 全 1 — 不是 HDLC 标准 flag   |
| B    | 10000001 | 不是定义的 flag 模式          |
| C    | 01111101 | 相似但不正确 — 只有五个 1，缺少一个 |
| D    | 01111110 | ✅ 正确 — 标准 HDLC flag     |

选项 C (`01111101`) 是一个常见的陷阱，因为它看起来相似，但位排列错误，不符合 HDLC 规范。
