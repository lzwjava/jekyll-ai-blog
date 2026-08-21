---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停等自动重传请求的两个关键优势
translated: true
type: note
---

问题：停等ARQ（Stop-and-Wait ARQ）有哪些优点，为什么“简单”被认为是其中之一？

答案：停等ARQ之所以被认为**简单**，原因如下：

1. **最小化的逻辑**：发送方每次只发送一帧，然后等待ACK（确认）后再发送下一帧。这种逐一进行的机制所需的控制逻辑非常少。
2. **无序列复杂性**：由于任何时候只有一帧在传输中，只需1位序列号（0或1）就能区分当前帧和重传帧。
3. **简单的错误处理**：若超时未收到ACK，发送方只需重传同一帧——无需跟踪窗口或缓冲多帧。
4. **小缓冲区需求**：发送方和接收方每次只需缓冲一帧，内存管理简单直接。

总之，两个主要优点是：

- ✅ **简单**（实现和逻辑极简）
- ✅ **所需缓冲区小**（一次只缓冲1帧）

主要缺点是**信道效率低**，因为发送方在等待每个ACK时处于空闲状态，浪费带宽——尤其在高速迟链路上。

参考来源：

- [停等ARQ – 维基百科](https://en.wikipedia.org/wiki/Stop-and-wait_ARQ)
- [ARQ协议 – GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
