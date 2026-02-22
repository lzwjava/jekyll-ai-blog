---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MAC 协议与 CSMA/CD 基础
translated: true
type: note
---

问题：共享介质局域网 (LAN) 中的介质访问控制 (MAC) 协议必须解决哪三个具体问题，以及 CSMA/CD 介质访问控制的基本概念如何简单概括？

回答： 

### 共享介质 LAN 中 MAC 协议解决的三个问题

在多个节点共享同一传输介质的局域网 (LAN) 中，介质访问控制 (MAC) 协议对于协调数据传输并防止混乱至关重要。它具体解决了以下三个核心问题：

1.  **Channel Allocation (谁发送？)**：确定在任何给定时刻哪个节点允许发送数据。由于介质是共享的，理想情况下一次只有一个节点发送，以确保数据完整性。
2.  **Collision Detection (会发生冲突吗？)**：识别当两个或多个节点同时尝试发送时是否会发生碰撞（数据干扰），或者已经发生碰撞。
3.  **Collision Resolution (如何处理冲突？)**：定义检测到碰撞时要遵循的具体程序，确保相关节点能够在不立即重复碰撞的情况下重试发送。

### CSMA/CD 的基本概念

**CSMA/CD** 表示 **Carrier Sense Multiple Access with Collision Detection**。其基本操作理念可以概括为两个主要阶段：

*   **“先听后说”（Carrier Sense）**：在节点尝试发送数据之前，首先监听信道检查是否空闲。如果信道忙，则节点等待；如果空闲，则节点开始发送。
*   **“边说边听”（Collision Detection）**：在发送数据的同时，节点继续监控信道。如果检测到信号失真表明发生了碰撞（另一个节点同时开始发送），则立即停止发送、发送干扰信号，并等待随机退避时间后再尝试重传。

简而言之，核心逻辑是：**先听，然后发；边发边听。**

参考文献：  

- [IEEE 802.3 Ethernet Standard Overview](https://www.ieee802.org/3/)