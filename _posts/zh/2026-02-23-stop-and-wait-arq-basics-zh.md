---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停等ARQ基础详解
translated: true
type: note
---

问题：What are the characteristics of the Stop-and-Wait ARQ error control mechanism?

答案：

正确答案是 **A: Small buffer space required, low channel efficiency**。

### 详细解释

**Stop-and-Wait ARQ (Automatic Repeat reQuest)** 是数据链路层中使用的最简单的错误控制协议。其操作特性由以下逻辑定义：

1. **Window Size**：发送方窗口和接收方窗口的大小均为 **1**。这意味着发送方一次只能传输一个帧。
2. **Operation Flow**：
    * 发送方传输单个帧。
    * 发送方必须随后 **停止** 并等待接收方的确认 (ACK)。
    * 如果正确接收到 ACK，发送方继续传输下一个帧。
    * 如果发生超时或接收到否定确认 (NAK)，发送方重新传输相同的帧。
3. **Buffer Space (Small)**：由于系统一次只处理一个帧（发送下一个帧前等待确认），发送方和接收端所需的缓冲存储空间最小。
4. **Channel Efficiency (Low)**：这种方法的主要缺点是效率低下，尤其是在高带宽或长传播延迟的链路上。在发送方等待 ACK 的时间内，通信信道处于空闲未使用状态。这导致低吞吐量和可用信道容量的利用率差。

因此，其定义特性是需要 **small buffer space** 但遭受 **low channel efficiency**。

参考资料：

* [Stop-and-Wait ARQ - GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
* [Automatic Repeat Request - Wikipedia](https://en.wikipedia.org/wiki/Automatic_repeat_request)
