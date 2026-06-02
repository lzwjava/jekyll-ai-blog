---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停止等待 ARQ 过程步骤
translated: true
type: note
---

问题：在数据通信的错误控制技术中，Stop-and-Wait ARQ 是错误检测和重传的常用方法之一。下图描述了发送方和接收方传输数据时使用 Stop-and-Wait ARQ 的过程。请写出图中①至⑥的内容。

答案：

由于您的问题中未提供具体的图像，我将基于计算机网络考试和教材中典型的 **Stop-and-Wait ARQ (Automatic Repeat reQuest)** 协议工作流程，推断①至⑥的标准内容。

在涉及发送方和接收方的标准 Stop-and-Wait ARQ 图中，序列通常描绘帧的传输、错误处理（丢失或损坏）以及确认机制。此类图的典型流程如下：

1. **正常传输**：发送方发送带有序列号的帧（例如，Frame 0）。
2. **确认**：接收方成功接收后发送该帧的 ACK（Acknowledgment）。
3. **下一帧**：发送方发送下一帧（例如，Frame 1）。
4. **错误场景（丢失/损坏）**：帧发送但在传输中丢失或损坏。
5. **超时**：发送方的定时器因未收到 ACK 而到期。
6. **重传**：发送方重传相同的帧。

基于此标准逻辑，以下是①至⑥的可能内容：

* **① Data Frame（例如，Frame 0）**：发送方发送的初始数据包。通常包含序列号（0 或 1）。
* **② ACK（Acknowledgment）**：接收方发送的确认，表示成功接收前一帧（例如，ACK 0 或 ACK 1）。
* **③ Data Frame（例如，Frame 1）**：接收第一个 ACK 后发送的后续数据包。
* **④ Lost or Corrupted Frame**：传输但未能正确到达接收方的帧（通常描绘为消失或标记为“X”）。
* **⑤ Timeout**：发送方等待定时器因未在规定时间内收到预期 ACK 而到期的事件。
* **⑥ Retransmitted Frame**：发送方因超时而重新发送特定帧（与④相同）。

**过程的详细解释：**

1. **发送方发送 Frame 0**：发送方传输带有序列号 0 的数据帧并启动定时器。
2. **接收方接收 Frame 0**：接收方检查错误。如果正确，则将数据交付给上层并回送 **ACK 0**。
3. **发送方接收 ACK 0**：发送方停止定时器并继续发送 **Frame 1**。
4. **Frame 1 丢失/损坏**：在④场景中，Frame 1 在信道中丢失或带有错误到达。接收方丢弃它且不发送任何内容（或根据具体变体发送前一帧的重复 ACK，但在基本的 Stop-and-Wait 中，通常不发送）。
5. **发送方超时**：由于发送方未在超时时间内收到 Frame 1 的 ACK，因此发生 **timeout** 事件（⑤）。
6. **重传**：发送方假设帧丢失并 **重传 Frame 1**（⑥）。接收方然后接受此重传帧并发送 ACK 1。

此机制通过结合错误检测、超时和重传，确保在不可靠信道上可靠地传输数据。

参考资料：

* [Stop-and-Wait ARQ - GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
* [Automatic Repeat Request (ARQ) - Wikipedia](https://en.wikipedia.org/wiki/Automatic_repeat_request)
