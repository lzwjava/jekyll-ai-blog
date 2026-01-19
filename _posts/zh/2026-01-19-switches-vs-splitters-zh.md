---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网交换机与被动式 RJ45 分线器的比较
translated: true
type: note
---

Question: 如果我将 Router 的一个 WAN 端口（通常应为 LAN 端口）连接到我的 5-port Gigabit Ethernet switch（例如 Mercusys SG105 系列），然后将我的 Laptop 和其他设备连接到 Switch 上剩余的端口，这些设备可以访问 Internet 吗？这与只允许一个下游设备的简单 RJ45 splitter 有什么不同吗？

Answer: 

**是的，连接到 Switch 的 Laptop 和其他设备将能够访问 Internet。**

一个 5-port 类型的 unmanaged Gigabit Ethernet switch（如 Mercusys MS105G, SG105, SG105C 等）的工作原理与被动式 RJ45 splitter / Y-splitter 完全不同。

以下是核心区别：

- **被动式 RJ45 splitter / 1-to-2 适配器**  
  这些不是真正的网络 Switch。它们试图将单个 100 Mbps 的 Ethernet 连接（通常仅使用 2 对线缆）拆分为两个连接。  
  → 它们一次仅支持**一个活动的下游设备**。  
  → 它们无法与 Gigabit Ethernet 正常工作（或完全无法工作）。  
  → 当多个设备尝试通信时，它们会导致严重的性能问题或直接无法工作。

- **真正的 Ethernet switch（您的 5-port 设备）**  
  这是一个真正的、主动的、多端口网络 Switch（即使它是 unmanaged 类型）。  
  它拥有自己的内部 switching chip，可以：  
  - 学习 MAC addresses  
  - 仅将 frames 转发到正确的端口  
  - 支持 full-duplex 通信  
  - 每个端口同时处理 Gigabit 速度 (1000 Mbps)  
  - 允许**多个设备同时进行通信**

典型的正确设置：

```
Internet
   ↓
Router (LAN port 1) ────→ Switch port 1 (任何端口)
                            ├── Switch port 2 → Laptop
                            ├── Switch port 3 → Desktop / NAS
                            └── Switch port 4 → Smart TV / 其他设备
```

只要满足以下条件：

1. 从 Router 的 LAN port 到 Switch 的线缆正常  
2. Switch 已接通电源（大多数 Mercusys unmanaged switches 需要供电）  
3. 您使用的是标准 Ethernet 线缆（Gigabit 需使用 Cat5e 或更高版本）

那么**插入 Switch 的所有设备都将获得 Internet 访问权限**，并能在本地网络上相互通信 —— 这与它们直接插入 Router 的不同 LAN 端口的效果完全相同。

您可以使用 Switch 上的 5 个端口中的任何一个作为连接到 Router 的上行链路 —— 这些简单的 unmanaged switches 没有专门的 "WAN" 或 "Uplink" 端口。所有端口都是对等的。

**总结**  
您的 Switch 是一个**真正的网络 Switch**，而不是 splitter。  
您可以连接多个设备（Laptop + 手机 + 电视 + 打印机等），它们都将拥有 Internet 访问权限和完整的 Gigabit 本地网络性能 —— 而不像廉价的 splitters 那样只能伪造支持一个额外设备，且通常在现代设备上运行失败。

References:  

- [Mercusys MS105G product page](https://www.mercusys.com/en/product/details/ms105g)  
- [Mercusys SG105 product description](https://www.mercusys.com/en/product/details/sg105)