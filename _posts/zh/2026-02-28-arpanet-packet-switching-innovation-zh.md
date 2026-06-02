---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ARPANET的分组交换创新
translated: true
type: note
---

**问题：** ARPANET 使用了哪种交换技术来连接不同类型的计算机并传输数据信号？

**答案：**

正确答案是 **C. 分组交换技术** (Packet Switching technology)。

**解释：**

ARPANET 由美国国防部高级研究计划局 (ARPA) 于 1960 年代后期开发，是世界上第一个运行的 **packet-switched** 网络，也是现代 Internet 的直接前身。

ARPANET 使用 **packet switching** 的关键特征和原因：

- 它将消息分解成小的、独立的 **packets**，每个包含目标地址信息。
- **Packets** 可以独立穿越网络，如果必要，可以采取不同的路由。
- 这种方法高度弹性——如果一条路径失败（例如战时），**packets** 可以自动重新路由。
- 它允许**不同类型的计算机**（具有不同的架构、操作系统和字长）有效通信，因为通信协议以标准化的 **packet** 格式处理数据，而不是要求相同的硬件。
- 与 **circuit switching** 相比，它更有效地利用网络带宽（资源动态共享）。

与其他选项的比较：

- **A. 电路交换技术 (Circuit Switching)**
  用于传统电话网络。在通信开始前建立专用的端到端路径，并整个持续时间内保持占用。不适合连接异构计算机或突发性数据流量。ARPANET **没有**使用此技术。

- **B. 报文交换技术 (Message Switching)**
  整个消息作为一个单元发送，并在每个节点存储-转发。它具有高延迟（尤其是长消息），并且需要在中间节点提供大量存储。ARPANET **没有**使用纯 **message switching**。

- **C. 分组交换技术 (Packet Switching)**
  正确选择。这是 ARPANET 的基本创新。

- **D. ATM交换技术 (ATM Switching)**
  Asynchronous Transfer Mode——1980 年代至 1990 年代为宽带网络开发的基于信元的交换技术。ARPANET 创建时（1969–1980 年代）它**不存在**。

**结论：**
ARPANET 对现代网络的最重要技术贡献是成功实施了 **packet switching**，这就是为什么选项 **C** 是正确的。

您的原始选择 (A) 是常见的误解——许多人将 **circuit switching** 与传统通信系统联系起来，但它**不是** ARPANET 使用的技术。

**参考文献：**

- 此为公认的历史网络事实，无需参考文献。
