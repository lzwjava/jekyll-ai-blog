---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLC与MAC子层分离
translated: true
type: note
---

**问题：** 数据链路层是如何划分为LLC和MAC子层的？

**答案：**

IEEE决定将第2层（数据链路层）拆分为两个子层，以便将硬件相关的关注点与协议多路复用关注点分离开来。

**LLC — 逻辑链路控制（上层子层，IEEE 802.2）**

LLC位于第3层正下方，为网络层提供统一接口，无论底层使用何种物理介质。其主要职责包括：

- **协议多路复用** — 使用服务访问点（SAP）允许多个第3层协议（IPv4、IPv6、IPX等）共享同一条链路。
- **成帧** — 添加头部/尾部来将数据包分隔成帧。
- **错误检测与可选流量控制** — 根据模式（无连接 vs 面向连接），可检测丢失或损坏的帧。

**MAC — 媒体访问控制（下层子层，IEEE 802.x）**

MAC是面向物理硬件的子层。其职责包括：

- **寻址** — 48位MAC（硬件）地址位于此处；它标识本地网段上的特定网卡。
- **介质访问** — 当多个设备共享同一信道时，确定谁可以发送（例如，以太网802.3使用CSMA/CD，Wi-Fi 802.11使用CSMA/CA）。
- **硬件级帧定界** — 添加前导码、帧起始定界符和FCS（CRC校验和）。

**为何拆分很重要**

LLC/MAC边界使得相同的LLC逻辑（IEEE 802.2）可以不加修改地运行在完全不同的物理介质之上——以太网、Wi-Fi、令牌环等。每种介质都有自己的MAC标准（802.3、802.11、802.5……），而它们之上的LLC保持不变。您可以点击图中的任意框以获取更多详情。

**参考文献：**

- [IEEE 802.2 LLC标准概述 – Wikipedia](https://en.wikipedia.org/wiki/Logical_link_control)
- [IEEE 802 LAN/MAN标准概述 – Wikipedia](https://en.wikipedia.org/wiki/IEEE_802)
- [MAC子层 – Wikipedia](https://en.wikipedia.org/wiki/Medium_access_control)
