---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: Wi-Fi MAC 层浅析
translated: true
type: note
---

问题：IEEE 802.11 在 MAC layer 使用哪种协议？

答案：IEEE 802.11 (Wi-Fi) 在 MAC layer 使用 **CSMA/CA** (Carrier Sense Multiple Access with Collision Avoidance) 协议。

### 为什么使用 CSMA/CA 而不是 CSMA/CD？

在有线 Ethernet (IEEE 802.3) 中，使用的是 **CSMA/CD** (Collision Detection)。然而，无线网络面临着独特的挑战，使得 Collision Detection 几乎不可能实现：

* **“Hidden Node” 问题：** 一个节点可能能够看到 Access Point (AP)，但看不到其他也正在与该 AP 通信的节点。因此，它无法检测到在 AP 端发生的 collision。
* **Half-Duplex 特性：** 无线电台通常无法在同一时间在同一频率上进行发送和接收，这意味着工作站在忙于发送数据时无法“听”到 collision。

### CSMA/CA 的工作原理

CSMA/CA 并不试图在冲突发生时捕捉它，而是专注于**预防**。它遵循“先听后说”的方法，并增加了安全缓冲：

1. **Carrier Sense：** 工作站监听信道。如果介质忙碌，它就会等待。
2. **IFS (Inter-Frame Spacing)：** 即使在介质空闲后，工作站也会等待一小段时间 (DIFS)。
3. **Random Backoff：** 为了防止多个工作站在同一毫秒内同时介入，每个工作站都会选择一个随机等待计时器。
4. **ACK (Acknowledgement)：** 与有线 Ethernet 不同，Wi-Fi 中的每个成功数据包都必须由接收方通过 ACK 进行确认。如果发送方没有收到 ACK，它会认为发生了 collision 并重试。

---

### 对比一览

| 特性 | CSMA/CD (有线) | CSMA/CA (无线) |
| --- | --- | --- |
| **全称** | Collision Detection | Collision Avoidance |
| **策略** | 冲突后停止并重传 | 发送前避免冲突 |
| **应用场景** | Ethernet (802.3) | Wi-Fi (802.11) |
| **效率** | 在有线环境中效率很高 | 由于 overhead/等待，效率较低 |

您是否需要我更详细地解释 “Hidden Node” 问题以及 **RTS/CTS** 机制如何帮助解决它？