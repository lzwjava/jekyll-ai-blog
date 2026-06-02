---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网标准、速度和布线
translated: true
type: note
---

**问题：** Ethernet 标准 10BASE-T、100BASE-T 和 1000BASE-T 是什么意思？

**答案：**

## 命名规则解析

名称的每个部分都有特定含义。以 **1000BASE-T** 为例：

| 部分 | 含义 |
|------|---------|
| **数字** (10 / 100 / 1000) | 传输速度（Mbps） |
| **BASE** | 基带信号——电缆上仅传输 Ethernet 信号 |
| **T** | 双绞线——使用的物理电缆介质 |

“BASE” 指基带信号，表示介质上仅传输 Ethernet 信号。“T” 指传输信号的双绞线物理介质。

---

## 10BASE-T — 标准 Ethernet

10BASE-T 是 IEEE 标准，定义了在非屏蔽双绞线 (UTP) 电缆上以 **10 Mbps** 发送信息的要求。它是 10 Mbps Ethernet 的最流行形式，使用 UTP 电缆连接站点，并使用集线器形成网络。虽然它支持最大 10 Mbps 带宽，但实际网络中的碰撞会将有效吞吐量降低到大约 4–6 Mbps。

- 10BASE-T 以 **Half Duplex** 模式运行，即一次只能单向通信——类似于对讲机，必须停止发送才能接收。
- 10BASE-T 可与 **Cat3** 或更高等级电缆配合使用。

---

## 100BASE-T — 快速 Ethernet

100BASE-T 是 10BASE-T 的增强形式，用于快速数据传输速率高达 **100 Mbps** 的网络标准——比标准 Ethernet 快 10 倍。像标准 Ethernet 一样，它遵循 CSMA/CD 技术来避免碰撞。

- 100BASE-T 支持 **Full Duplex**，即双向运行，大大提高可用速度。
- 最常见的变体是 **100BASE-TX**，使用两对双绞线电缆。适用于典型的家庭网络、小型办公室以及文件共享、网页浏览和电子邮件等常规任务。
- 对于 100 Mbps 传输，需要使用 **Cat5** 或更好电缆。

---

## 1000BASE-T — 吉比特 Ethernet

1000BASE-T 是当今最常见的网络标准。它迅速取代了较旧的 Ethernet 标准，成为网络设备的实际标准，实现 **1 Gbps (1,000 Mbps)** 速度。

- 1000BASE-T 使用所有 **四对线** 双向传输，利用混合电路和消除器。数据使用 4D-PAM5（四维脉冲幅度调制，五种电压电平）编码。
- 1000BASE-T 可与 **Cat5e、Cat6** 或更高品质电缆配合使用。
- 1000BASE-T 向后兼容较旧标准（10BASE-T 和 100BASE-TX），因此可轻松集成到现有网络基础设施中。它支持最大电缆长度 **100 米**。

---

## 快速比较表

| 标准 | 速度 | 常见名称 | 双工模式 | 最小电缆 | 使用的线对 |
|---|---|---|---|---|---|
| 10BASE-T | 10 Mbps | Ethernet | Half | Cat3 | 2 pairs |
| 100BASE-T | 100 Mbps | Fast Ethernet | Full | Cat5 | 2 pairs |
| 1000BASE-T | 1000 Mbps (1 Gbps) | Gigabit Ethernet | Full | Cat5e | 4 pairs |

---

## 向后兼容性和自动协商

当设备连接到 10/100/1000 BASE-T 网络时，它会自动与另一端设备协商支持的最高速度。例如，如果两端设备均支持 1000BASE-T，它们将以 1 Gbps 运行。这种自动速度调整使 10/100/1000 BASE-T 高度通用，适用于住宅和商业环境。

---

**参考文献：**

- [Differences of 10BASE-T, 100BASE-T and 1000BASE-T – Sopto](http://www.sopto.com/learningcenter_learningcenter_34/differences_of_10base-t,_100base-t_and_1000base-t.shtml)
- [What Does 10/100/1000 Base-T Mean? – trueCABLE](https://www.truecable.com/blogs/cable-academy/10-100-1000-base-t)
- [Differences of 10BASE-T, 100BASE-T, and 1000BASE-T – VCELINK](https://www.vcelink.com/blogs/focus/differences-of-10base-t-100base-t-and-1000base-t-in-networking)
- [What is 1000BASE-T – TechTarget](https://www.techtarget.com/searchnetworking/definition/1000BASE-T)
- [Ethernet over Twisted Pair – Wikipedia](https://en.wikipedia.org/wiki/Ethernet_over_twisted_pair)
