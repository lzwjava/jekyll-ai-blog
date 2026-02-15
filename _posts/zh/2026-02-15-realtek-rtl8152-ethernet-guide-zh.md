---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 瑞昱 RTL8152 百兆以太网指南
translated: true
type: note
---

Question: Provide an introduction to the Realtek RTL8152 Fast Ethernet adapter.

Answer: 

**Realtek RTL8152**（常见型号如 RTL8152B-VB 或类似变体）是一款流行的、低成本 **USB-to-Ethernet controller chipset**，专为 **10/100 Mbps Fast Ethernet** 连接而设计。

### Main Characteristics

- **Speed**: 支持 **10/100 Mbps** Ethernet (Fast Ethernet) —— 实际双向最大吞吐量约为 94–100 Mbps。
- **Interface**: 通过 **USB 2.0** 连接（理论总线速度为 480 Mbps，足以满足 100 Mbps Ethernet 的需求）。
- **Physical port**: 标准 **RJ45** Ethernet 接口。
- **Chipset role**: 集成了 MAC (Media Access Controller)、USB controller、10/100 transceiver，以及通常包含一个小型的片上内存缓冲区。
- **Common form factor**: 广泛用于无数廉价的 USB Ethernet adapters、USB-C to RJ45 dongles（使用 USB 2.0 信号）、docking station 的网口以及嵌入式设备中。

### Key Technical Features

- 符合 **IEEE 802.3** 和 **802.3u** 标准
- 支持 Auto-negotiation、crossover detection & auto-correction、polarity correction
- 支持 **Wake-on-LAN** (WoL)，包括在某些配置下的 **RealWoW!** (Wake-on-WAN)
- 在较新的驱动程序/固件组合中支持 **Energy Efficient Ethernet** (EEE – IEEE 802.3az)
- 支持 **Checksum offload** 和部分协议卸载功能 (TCP/UDP/IPv4/IPv6)，以降低 CPU 负载
- 功耗极低 —— 是笔记本电脑、平板电脑和常开设备的理想选择
- 驱动支持非常出色，几乎内置于所有现代操作系统中：
  - Windows (Vista 及更新版本，通常为 plug-and-play)
  - macOS (自 10.9 版本起，原生支持)
  - Linux (kernel module 为 `r8152`，自 2012–2014 年左右的内核已包含)
  - 多种 BSD 变体、Android (需相应的 kernel 支持) 等

### Typical Use Cases (2026 perspective)

- 为没有内置 RJ45 接口的 ultrabooks、平板电脑或 mini-PCs 增加有线 Ethernet 连接
- 提供比 Wi-Fi 更稳定、延迟更低的连接
- 当主 NIC 故障时作为备用网络接口
- 在仅有 USB-C 或 USB-A 接口的设备上获取有线网络的一种廉价方案
- 目前在价格约 5–15 美元的 USB-A / USB-C Ethernet adapters 中仍被广泛销售

### Comparison with Related Chips

| Chip | Max Speed | USB Version | Typical Year of Peak Usage | Notes |
| :--- | :--- | :--- | :--- | :--- |
| RTL8152 | 100 Mbps | USB 2.0 | 2012–2018 | Fast Ethernet, very cheap |
| RTL8153 | 1 Gbps | USB 3.0 | 2015–2022 | Gigabit upgrade, still very common |
| RTL8156 | 2.5 Gbps | USB 3.0/3.2 | 2020–present | Multi-gig entry level |

即便是在 2026 年，RTL8152 依然广泛可用，原因在于：
- 极低的制造成本
- 跨平台的极其稳定的驱动支持
- 对于许多非游戏、非 4K 推流的使用场景（如网页浏览、办公、SSH、轻量文件传输）性能绰绰有余

如果你只需要基础的有线连接而不需要千兆速度，基于 RTL8152 的适配器仍然是一个完全合理、可靠且廉价的选择。

References:  

- [Realtek official product page for RTL8152B-VB-CG](https://www.realtek.com/Product/Index?cate_id=786&id=4079)
- [Realtek USB Ethernet software downloads (including RTL8152B)](https://www.realtek.com/Download/List?cate_id=585)