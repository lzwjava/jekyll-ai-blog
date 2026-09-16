---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATDM动态时隙分配
translated: true
type: note
---

**什么是异步时分复用（ATDM）？**

**答案：**

**异步时分复用（ATDM）** 是一种数据传输技术，它根据实际需求动态分配时隙给各信道，而不是无论是否有数据发送都分配固定时隙。

**工作原理：**

在传统（同步）时分复用中，每个信道在重复的帧中都有一个固定时隙——即使该信道没有数据要发送，该时隙也会被浪费。ATDM 通过以下方式解决这一问题：

1. **按需分配时隙** —— 仅当某个信道实际有数据要传输时，才为其分配时隙。
2. **为每个数据包打上地址或标识符**，因为时隙不再与固定位置相关联。
3. **在发送端缓冲数据**，直到有时隙可用为止。

**主要特征：**

| 特征 | 同步时分复用 | 异步时分复用 |
| --- | --- | --- |
| 时隙分配 | 固定 | 动态 / 按需 |
| 效率 | 低（空闲时隙被浪费） | 高（无空闲时隙） |
| 开销 | 无（位置即身份） | 需要地址头 |
| 复杂度 | 简单 | 较复杂 |

**为何重要：**

- 显著提高了突发性流量（如计算机网络数据）的带宽利用率。
- 构成了**ATM（异步传输模式）**的概念基础，ATM 是广泛应用于宽带和电信基础设施的主要网络技术。
- 非常适合不同信源以可变且不可预测的速率进行传输的场景。

**常见应用场景：** ATM 网络、统计复用器以及早期宽带通信系统。

参考资料：

- [异步时分复用 – Techopedia](https://www.techopedia.com/definition/1704/asynchronous-time-division-multiplexing-atdm)
- [多路复用 – GeeksforGeeks](https://www.geeksforgeeks.org/multiplexing-channel-sharing-in-computer-network/)
- [ATM（异步传输模式）– Britannica](https://www.britannica.com/technology/asynchronous-transfer-mode)
