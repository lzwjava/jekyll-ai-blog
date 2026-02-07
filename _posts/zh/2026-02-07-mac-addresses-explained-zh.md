---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 多 MAC 地址详解
translated: true
type: note
---

Question: 如果一台计算机安装了多个局域网 (LAN) 适配器，它会拥有多个哪种类型的地址？

Answer: 一台拥有多个 network adapters 的计算机将拥有多个 **MAC (Media Access Control)** 地址。

### 为什么有多个 MAC 地址？

每一个 network interface card (NIC) 或适配器——无论是物理 Ethernet 端口、Wi-Fi 芯片，还是虚拟适配器——在制造时都会在硬件中烧录一个唯一的识别码。

* **1:1 关系：** 每个独立的适配器都被分配了唯一的 MAC 地址。因此，如果你有两个适配器（例如，一个用于 Wi-Fi，一个用于 Ethernet），你的计算机本质上就拥有两个 MAC 地址。
* **硬件层：** MAC 地址运行在 OSI model 的 **Data Link Layer (Layer 2)**。它作为该特定硬件设备的永久物理“指纹”。

### 那 IP 地址呢？

虽然针对你具体问题的答案是 **MAC**，但值得注意的是，这类计算机通常也会有多个 **IP 地址**。

* **逻辑 vs. 物理：** MAC 地址是物理且永久的，而 IP 地址是逻辑的，由网络分配 (Layer 3)。
* **连接性：** 为了通过不同的适配器同时在不同的网络上通信，每个适配器必须被分配一个唯一的 IP 地址。

---

### Comparison Table

| Feature | MAC Address | IP Address |
| --- | --- | --- |
| **Full Name** | Media Access Control | Internet Protocol |
| **OSI Layer** | Layer 2 (Data Link) | Layer 3 (Network) |
| **Permanence** | Hardcoded/Permanent | Dynamic/Assigned |
| **Function** | Identifies the specific hardware | Identifies the location on the network |

你想让我解释如何在你的特定操作系统上查找当前所有激活的 MAC 地址吗？