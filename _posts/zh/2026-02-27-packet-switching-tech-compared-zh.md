---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分组交换技术比较
translated: true
type: note
---

Frame Relay 是一种在 X.25 之后开发的数据通信技术。从原理角度来看，Frame Relay、X.25 和 ATM 都属于同一类交换技术。以下哪一项正确？
A. Circuit switching
B. Packet switching
C. Message switching
D. Cell switching

你的答案：D
正确答案：B

答案：

正确答案是 **B. Packet switching**（分组交换）。

**详细解释：**

- **X.25**：这是一个经典的 **packet-switched** 网络协议（packet switching），1970年代至1990年代广泛使用。它在每个节点进行逐跳错误检查和重传（link-layer retransmission），这带来了高可靠性，但也导致高延迟和低吞吐量。

- **Frame Relay**：作为 X.25 的更快、更高效的继任者开发，Frame Relay 仍然本质上是 **packet switching**。它使用可变长度帧，并消除了逐跳错误检查和流量控制（端到端错误控制留给上层）。这使其更快，更适合现代数字线路。

- **ATM (Asynchronous Transfer Mode)**：ATM 使用固定长度的 **cells**（53 字节），也是一种 **packet switching** 的形式，但它是通常称为 **cell switching** 或 **cell-relay** 的特殊类型。尽管一些教科书中称为 "cell switching"，但从更广泛的技术分类角度来看，ATM 仍然属于 **packet switching**（分组交换），因为它将用户数据分解成小包（cells）并进行统计复用。

**本题关键点**：

大多数中国认证考试（如 soft exam / Huawei / H3C / network engineer exams）和许多教科书将 **X.25、Frame Relay 和 ATM** 归类在 **分组交换 (packet switching)** 下。

术语“信元交换 (cell switching)”有时专门用于 ATM，但在本题语境中，预期且官方正确答案是 **B. 分组交换**。

**为什么 D 在此语境中不正确**：

虽然 ATM 确实是基于 cell 的交换，但题目使用了“帧中继、X.25及ATM都同属于”的表述。中国教学材料和考试标准中的常见分类将它们全部归入 **分组交换**，而非更狭窄的术语“信元交换”（仅适用于 ATM）。

因此，标准答案是 **B**。

参考资料：

- 无（基于中国标准网络工程教学材料和认证考试模式）
