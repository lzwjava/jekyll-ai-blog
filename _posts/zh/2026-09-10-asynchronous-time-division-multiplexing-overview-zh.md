---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 异步时分复用概述
translated: true
type: note
---

**问题：** 什么是异步时分多路复用（Asynchronous Time Division Multiplexing）？

**答案：**

**背景——什么是 TDM？**

时分多路复用（TDM）是一种让多个数据流通过按时间轮流使用同一通信信道的技术。信道被划分为多个时隙，每个发送方轮流使用。

**同步 TDM（基本形式）**

在同步 TDM 中，每个时隙被预先分配给固定的源。无论这些源是否有数据要发送，时隙都会被广播，当源空闲时会浪费带宽。

**异步 TDM（ATDM）——改进方案**

异步 TDM，也称为统计 TDM，会根据需求*动态*地将时隙分配给数据流。仅当数据流有数据要发送时才会分配时隙，因此更加灵活。

关键机制：

- 在 ATDM 中，如果有 *n* 条输入线路，多路复用器会扫描所有输入线路并接收数据，直到帧被填满。帧填满后，便通过链路发送。如果发送方没有足够的数据填满该帧，则按部分填充状态发送。
- 由于所有发送设备都可以使用任何可用时隙，接收方无法仅通过计算时隙位置来识别数据——因此需要一种寻址机制，为每个时隙提供唯一地址。

**与同步 TDM 相比的主要优势**

仅当需要发送数据时才使用时隙，避免了带宽浪费。动态分配使得可用带宽的使用更加灵活，可以为需求更高的数据流分配更多时隙。

**实际应用**

异步传输模式（ATM）——一种主要的电信交换技术——使用异步时分多路复用将数据编码为小型、固定长度的信元。ATM 在 1990 年代至 2000 年代广泛部署于骨干网络中。

**同步 TDM 与异步 TDM 对比一览：**

| | 同步 TDM | 异步 TDM |
| --- | --- | --- |
| 时隙分配 | 固定、预先分配 | 动态、按需分配 |
| 带宽浪费 | 有（空闲时隙被浪费） | 无（时隙始终承载数据） |
| 是否需要寻址 | 否 | 是（每个时隙有地址） |
| 别称 | — | 统计 TDM |
| 可扩展性 | 限于 N 个设备 = N 个时隙 | 可支持超过时隙数量的设备 |

---

**参考文献：**

- [Difference between Synchronous TDM and Asynchronous TDM – GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/difference-between-synchronous-tdm-and-asynchronous-tdm/)
- [Asynchronous Time Division Multiplexing – TutorialsPoint](https://www.tutorialspoint.com/data_communication_computer_network/asynchronous_tdm.htm)
- [What is ATM? – Dialogic](https://www.dialogic.com/glossary/asynchronous-transfer-mode-atm)
