---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微星B760M迫击炮WiFi接口
translated: true
type: note
---

我有来自官方微星数据表的足够验证数据（涵盖基础版 MAG B760M MORTAR WIFI，而非“II”或“MAX”版本——这些是不同的 SKU，带有额外的 M.2 插槽和接口）。

问题：微星 MAG B760M Mortar WiFi 主板（LGA 1700，DDR5）有哪些接口？

回答：

这是原版 **MAG B760M MORTAR WIFI**（而非“II”或“MAX”更新版——后者有第三个 M.2 插槽和不同的接口布局，所以不要与这些评测的规格混淆）。根据微星的官方数据表：

**后置 I/O 面板**
| 接口 | 规格 |
|---|---|
| USB 3.2 Gen 2x2 Type-C | 1 个，20 Gbps |
| USB 3.2 Gen 2 Type-A | 3 个，10 Gbps |
| USB 3.2 Gen 1 Type-A | 2 个，5 Gbps |
| USB 2.0 | 1 个（后置，其余为内部接口） |
| DisplayPort | 1.4 |
| HDMI | 2.1（4K@60Hz，需要核显） |
| LAN | Realtek RTL8125BG，2.5Gbps RJ45 |
| Wi-Fi/BT 天线 | 2 个（Intel Wi-Fi 6E + BT 5.3） |
| 音频插孔 | 5 个 3.5mm + 光纤 S/PDIF 输出 |

**存储**
- 2 个 M.2 Gen4 x4（64 Gbps）插槽——一个来自 CPU，一个来自芯片组（带 M.2 Shield Frozr 散热片）
- 4 个 SATA 6Gb/s 端口

**扩展插槽**
- 1 个 PCIe 5.0 x16（CPU，Lightning Gen 5，最高 128GB/s）
- 1 个 PCIe 4.0 x16（物理 x16，电气 x4，芯片组）
- 1 个 PCIe 3.0 x1（芯片组）

**内存**
- 4 个 DDR5 DIMM 插槽，双通道，最高 7000+ MT/s（超频）

**内部接口（来自共享的微星 MAG 系列接口布局——建议对照您具体主板的丝印确认，因为微星未在数据表中发布此非 II 版本的确切内部接口表）**
- 1 个 24 针 ATX_PWR1，2 个 8 针 CPU_PWR
- CPU_FAN1、PUMP_FAN1、SYS_FAN1~4（共 6 个风扇接口）
- JFP1/JFP2 前置面板（电源/重置/硬盘 LED、蜂鸣器）
- JAUD1 前置音频
- JUSB4（USB 3.2 Gen2 Type-C 前置面板）、JUSB3（USB 3.2 Gen1 接口，2 个端口）、JUSB1~2（USB 2.0 接口，4 个端口）
- JTPM1（TPM 2.0 接口）
- JRGB1（12V RGB）、JARGB_V2_1~2（5V 可寻址 ARGB Gen2）
- JCI1（机箱入侵检测）
- JBAT1（清除 CMOS 跳线）

对于您的工作站构建场景——此主板限制为 2 个 M.2 Gen4 插槽，第二个 GPU/NIC 通道为 PCIe 4.0 x4，如果您计划添加第二个 NVMe 用于模型检查点/数据集，或为您的 AMD 开发云设置透传网卡，这一点很重要。如果您经常处理大型本地数据集，2 个 M.2 插槽的限制（相比“II”版本的 3 个）是在购买前需要根据实际使用情况仔细核对的规格。

参考：

- [微星 MAG B760M MORTAR WIFI 官方数据表](https://storage-asset.msi.com/datasheet/mb/us/MAG-B760M-MORTAR-WIFI.pdf)
- [Tom's Hardware 评测——微星 MAG B760M Mortar](https://www.tomshardware.com/reviews/msi-mag-b760m-mortar-wifi-review)