---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CSMA/CD 网络中的共享介质
translated: true
type: note
---

问题：在 CSMA/CD 上下文中，术语 **"Multiple Access"** 的含义是什么？

答案：

### CSMA/CD 中 **"Multiple Access"** 的含义

在缩写 **CSMA/CD**（Carrier Sense **Multiple Access** with Collision Detection）中，术语 **Multiple Access** 指的是网络拓扑和使用模型，其中 **多个节点（计算机、打印机等）共享同一个通信信道或传输介质**。

以下是其含义的详细分解：

1.  **共享介质**：与点对点连接不同（两台设备之间有专用的线缆），**Multiple Access** 网络（如使用同轴电缆或 hub 的传统 Ethernet）将许多设备连接到一个公共总线上。所有设备物理连接到同一条线缆上。
2.  **平等权利**：术语 **"Access"** 意味着网络上的每个节点都有平等的权利尝试向共享介质发送数据。没有中央控制器（如主站）明确授予特定节点以固定顺序发言的权限（那将是“受控访问”）。
3.  **协调需求**：由于多个设备同时可以访问同一条线，如果两个或更多设备恰好在同一时间发送，它们的信号将重叠并相互破坏。这种现象称为 **collision**。
4.  **与协议的关系**：正是 **"Multiple Access"** 的特性，使得 CSMA/CD 的其他部分变得必要：
    *   **Carrier Sense (CS)** 是必需的，因为大家共享线路；你必须检查是否有人在使用它。
    *   **Collision Detection (CD)** 是必需的，因为多人 *可以* 同时访问线路，从而导致潜在冲突。

**总结**：**"Multiple Access"** 简单描述了 **多个用户竞争使用单一共享通信路径** 的场景，这需要一个协议来管理他们轮流发言以避免数据碰撞。

参考资料：  

- [Britannica: Multiple Access](https://www.britannica.com/technology/multiple-access)
- [GeeksforGeeks: Channel Allocation Problems in Computer Networks](https://www.geeksforgeeks.org/channel-allocation-problems-in-computer-networks/)