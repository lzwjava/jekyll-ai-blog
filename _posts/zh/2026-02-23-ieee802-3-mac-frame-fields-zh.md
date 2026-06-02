---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE 802.3 MAC 帧字段详解
translated: true
type: note
---

问题：IEEE 802.3 MAC 帧格式中每个字段的名称和长度（以字节为单位）是什么？

答案：

IEEE 802.3 MAC（Media Access Control）帧格式由以下字段组成，按从帧首到帧尾的顺序列出：

1.  **Preamble**
    *   **长度：** 7 bytes
    *   **描述：** 交替的 1 和 0 的模式（`10101010...`），用于将接收器的时钟与发送器的时钟同步。

2.  **Start Frame Delimiter (SFD)**
    *   **长度：** 1 byte
    *   **描述：** 序列 `10101011`，表示帧的开始。最后两个比特（`11`）信号目标地址的开始。
    *   *注意：* 在许多现代上下文中，Preamble 和 SFD 通常被组合为 8 字节的“Preamble”字段，但严格来说，它们是独立的。它们通常在物理层处理帧的其余部分之前被剥离。

3.  **Destination Address (DA)**
    *   **长度：** 6 bytes
    *   **描述：** 包含目标接收者的 MAC 地址。可以是单播、多播或广播地址。

4.  **Source Address (SA)**
    *   **长度：** 6 bytes
    *   **描述：** 包含发送站的 MAC 地址。这始终是单播地址。

5.  **Length / Type**
    *   **长度：** 2 bytes
    *   **描述：**
        *   如果值为小于或等于 1500（0x05DC），则表示数据字段的 **Length**（IEEE 802.3 标准）。
        *   如果值为大于或等于 1536（0x0600），则表示负载中封装的协议 **Type**（Ethernet II 帧格式，常用于 IEEE 802.3 物理层之上）。

6.  **Data (and Padding)**
    *   **长度：** 46 到 1500 bytes
    *   **描述：** 包含上层的数据负载（例如 IP 数据包）。
        *   **最大值：** 1500 bytes（Maximum Transmission Unit - MTU）。
        *   **最小值：** 46 bytes。如果实际数据小于 46 bytes，则添加填充字节以达到此最小值。这确保从 Destination Address 到 FCS 的总帧大小至少为 64 bytes，这在 CSMA/CD 网络中是碰撞检测所必需的。

7.  **Frame Check Sequence (FCS)**
    *   **长度：** 4 bytes
    *   **描述：** 包含对 Destination Address、Source Address、Length/Type 和 Data 字段计算的 32 位循环冗余校验（CRC）值。用于错误检测。

**摘要表格：**

| Field Name | Length (Bytes) |
| :--- | :--- |
| Preamble | 7 |
| Start Frame Delimiter (SFD) | 1 |
| Destination Address | 6 |
| Source Address | 6 |
| Length / Type | 2 |
| Data (Payload + Padding) | 46 – 1500 |
| Frame Check Sequence (FCS) | 4 |
| **Total Frame Size** | **64 – 1518** |

*(注意：如果使用 VLAN tagging (802.1Q)，则在 Source Address 后插入额外的 4 字节标签，将最大帧大小增加到 1522 bytes。)*
