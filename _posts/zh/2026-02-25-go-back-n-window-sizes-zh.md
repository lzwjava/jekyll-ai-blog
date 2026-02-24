---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Go-Back-N 窗口大小详解
translated: true
type: note
---

问题：在 Go-Back-N sliding window protocol 中，sending window 和 receiving window 的大小分别是多少？

答案：

## Go-Back-N (GBN) Protocol — 窗口大小

正确答案是 **B: Sending Window > 1, Receiving Window = 1**

---

## 三种滑动窗口协议的解释

| Protocol | Sending Window | Receiving Window |
|---|---|---|
| Stop-and-Wait | = 1 | = 1 |
| **Go-Back-N (GBN)** | **> 1** | **= 1** |
| Selective Repeat (SR) | > 1 | > 1 |

---

## 为什么 Go-Back-N 的 Receiving Window = 1？

**Go-Back-N** 允许发送方在不等待确认的情况下传输多个帧（sending window > 1），但 **receiver 只按严格的顺序接受帧**。

- 如果收到 **乱序帧**，receiver **丢弃它** 并且不缓冲它。
- 因为 receiver 只需跟踪 **下一个期望帧**（无需缓冲乱序帧），因此 receiving window 大小为 **1**。
- 当 frame *n* 发生错误时，发送方必须 **回退并重传 frame n 及所有后续帧** — 故名为“Go-Back-N”。

## 为什么不是选项 C（两者均 > 1）？

选项 C 描述的是 **Selective Repeat (SR)** 协议，而不是 Go-Back-N。在 SR 中：
- receiver **缓冲乱序帧**，因此 receiving window > 1。
- 仅需重传特定的错误帧（无需重传所有后续帧）。

## 总结

Go-Back-N 以 **receiver 缓冲简单性**（window = 1，无需缓冲）换取 **重传效率**（错误时必须重发多个帧）。这是与 Selective Repeat 的关键区别。