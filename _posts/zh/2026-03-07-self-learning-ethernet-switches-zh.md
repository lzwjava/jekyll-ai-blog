---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网交换机中的自学习
translated: true
type: note
---

**问题：** 以太网交换机是一种即插即用设备，它使用“________”算法逐步构建其转发表。（参考答案：Self-learning）

**答案：**

正确答案是 **Self-learning (自学习)** 算法。

---

## 以太网交换机中的 Self-Learning 算法是什么？

以太网交换机是一种即插即用设备，这意味着它无需 **手动配置** 即可开始工作。它使用 **self-learning algorithm** 自动构建其 MAC 地址转发表（也称为 CAM table）。以下是全面解释：

---

### 核心概念

交换机通过检查从端口接收到的帧的 **source MAC addresses** 来动态构建其 MAC 地址表。交换机通过在帧中的 destination MAC address 与 MAC 地址表中的条目进行匹配来转发帧。

---

### Self-Learning 算法的工作原理 — 逐步解析

**步骤 1 — 学习：** 当帧到达时，交换机检查 source MAC address 并更新其 MAC 地址表，记录 MAC address 及其来源端口。

**步骤 2 — 转发/过滤决策：** 交换机基于 destination MAC address 决定将帧转发到何处。

**步骤 3 — 转发：**
- 如果 destination MAC 在表中（已知单播），交换机仅将帧转发到正确的端口。
- 如果 destination MAC 不在表中（未知单播），交换机会 **flood** 帧的副本到除传入端口外的所有端口。

**步骤 4 — 时效：** 如果某个 MAC address 在一定时间内（默认 300 秒）未再次出现，则从 MAC 地址表中移除。

这一整体过程也称为 **“Flood and Learn”**。

---

### 详细示例

考虑一个连接到三台计算机 H1、H2 和 H3 的交换机。当 H1 向 H2 发送帧时：
- 交换机读取 H1 的 **source MAC address** 并将其与传入接口一起记录在其 MAC 地址表中。
- 由于交换机尚未有 H2 的 MAC address 条目，它会将帧 flood 到除来源接口外的所有接口。
- 当 H2 回复时，交换机从 H2 回复帧的 source 字段学习 H2 的 MAC address 并记录它。
- 从此以后，H1 和 H2 之间的帧将直接交换 — H3 不再看到它们。

---

### Self-Learning 算法的关键特性

 

| Property | Description |
|---|---|
| **Plug-and-play** | 无需手动配置 |
| **Source-based learning** | 仅从传入帧的 **source** MAC address 学习 |
| **Dynamic entries** | 条目会自动添加和移除 |
| **Flooding for unknowns** | 未知 destination MAC address 会触发 flooding |
| **Aging mechanism** | 超时后移除过时条目 |

---

### 为什么称为“Self-Learning”？

交换机使用 self-learning 算法来 **自动** 填充其 MAC 地址表，无需任何管理员干预。动态条目作为默认行为自动学习。

相比之下，路由器使用路由算法和 IP addresses 计算其转发表，而交换机使用 **flooding、learning 和 MAC addresses** 学习其转发表。

---

### 总结

Self-learning 算法使以太网交换机能够：
1. 以 **empty** 转发表开始
2. 随着帧流动 **gradually** 学习 MAC address 到端口的映射
3. 最终 **efficiently** 转发帧，而无需不必要的 flooding
4. 当设备移动或断开连接时 **automatically** 适应（通过 aging）

这就是为什么以太网交换机被描述为 **plug-and-play** 设备 — self-learning 算法自动完成所有工作。

**参考文献：**

- [How Switches Work – Study CCNA](https://study-ccna.com/how-switches-work/)
- [Overview of Switching Logic – NetworkAcademy.IO](https://www.networkacademy.io/ccna/ethernet/switching-logic)
- [Ethernet Switching – MAC Address Table – Cisco Press](https://www.ciscopress.com/articles/article.asp?p=3089352&seqNum=6)
- [How Does a Switch Learn MAC Addresses – NetworkLessons](https://networklessons.com/switching/how-does-a-switch-learn-mac-addresses)
- [Troubleshoot LAN Switching Environments – Cisco](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/12006-chapter22.html)