---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BSC适配器的半双工设计
translated: true
type: note
---

问题：我们应该如何理解IBM PC BSC通信适配器主要是为半双工传输线路设计的？

回答：

IBM PC **BSC（二进制同步通信）** 适配器基于半双工通信的操作模式构建，这意味着数据可以**双向流动，但一次只能朝一个方向**——而非同时进行。

以下是理解这一设计选择的方式：

**什么是BSC？**  
BSC（也称Bisync）是IBM在20世纪60年代开发的一种面向字符的同步数据链路协议。在异步串行通信普及之前，它广泛用于大型机和终端之间的通信。

**为什么半双工天然适合BSC**  
BSC本质上是一种**停等协议**：

- 发送方传输一个数据块
- 然后*停止*并等待来自接收方的ACK（确认）或NAK（否定确认）
- 只有在收到回复后才发送下一个数据块

这种固有的交替发送/接收模式完美匹配半双工线路——全双工能力会被浪费，因为双方从不需要在同一时刻传输。

**对适配器的实际影响**

- 适配器控制**RTS/CTS（请求发送/允许发送）**握手信号来翻转线路方向
- 它处理**调制解调器转向时间**——即线路从发送模式切换到接收模式所需的延迟
- 它针对**租用电话线路**和**两线电路**进行了优化，这些线路本身即为半双工

**总结**

| 概念 | 详情 |
| --- | --- |
| 协议 | IBM二进制同步（Bisync） |
| 方向 | 一次单向 |
| 流程 | 发送块 → 等待ACK → 发送下一个块 |
| 线路类型 | 通常为两线租用或交换电话线路 |
| 为何不是全双工？ | BSC的ACK/NAK周期不需要同时双向传输 |

这一设计并非局限，而是有意为之的匹配——该协议的逻辑以及当时物理线路基础设施都指向半双工作为实用且充分的选择。

参考文献：

- [IBM Binary Synchronous Communications - Wikipedia](https://en.wikipedia.org/wiki/Binary_Synchronous_Communications)
- [IBM PC Hardware Reference Library - BSC Adapter](https://www.pcjs.org/documents/manuals/ibm/)
- [Half-duplex vs Full-duplex Explained](https://en.wikipedia.org/wiki/Duplex_(telecommunications))
