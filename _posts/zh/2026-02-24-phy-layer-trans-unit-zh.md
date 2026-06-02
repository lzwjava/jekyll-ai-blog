---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 物理层传输单元详解
translated: true
type: note
---

我会搜索有关 OSI 模型的 physical layer 及其传输单元的信息。问题：OSI 参考模型最底层的 physical layer 的传输单元是什么？

答案：

physical layer 是 OSI 参考模型中最低（Layer 1）层。physical layer 的传输单元是 **bit**（二进制位）。

physical layer 以 bit 的形式包含信息，并负责将单个 bit 从一个节点传输到下一个节点。physical layer 定义了通过连接网络节点的 physical data link 传输原始 bit 流的方法。这也是数据被转换为 bit stream 的层，bit stream 是 1 和 0 的字符串。

physical layer 处理将数字数据转换为电、光或无线电信号的过程，这些信号可以传输通过诸如电缆、光纤线路或无线信道等 physical media。它为跨网络传输这些单个 bit 提供了机械、电气和程序规范。

因此，正确答案是 **A: 比特 (Bit)**。

参考资料：

- [GeeksforGeeks - What is OSI Model? - Physical-Layer](https://www.geeksforgeeks.org/computer-networks/open-systems-interconnection-model-osi/)
- [Wikipedia - Physical Layer](https://en.wikipedia.org/wiki/Physical_layer)
- [Cloudflare - What is the OSI Model?](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
