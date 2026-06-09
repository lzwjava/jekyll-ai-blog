---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 910万美元的AI机架
translated: true
type: note
---

问题：为什么英伟达的 Rubin AI 机柜（NVL72）会如此昂贵，估计每个机柜的价格高达 910 万美元？

回答：近期，伯恩斯坦研究公司和摩根士丹利等投资机构发布的 2026 年财务与供应链报告，详细剖析了英伟达下一代 **Vera Rubin NVL72** 服务器机柜（即“柜”或机柜）的惊人成本。虽然摩根士丹利最初估计成本约为 780 万美元，但伯恩斯坦的最新数据预测，每台机柜的成本可能达到 **910 万美元**。

与上一代 Blackwell（成本低于 400 万美元）相比，这一价格大幅飙升，原因在于多个严峻的硬件与供应链限制因素：

### 1. 内存与存储成本大幅飙升（约 320 万美元）

内存是推高价格的最大单一因素，与旧架构相比，成本惊人地增长了 **435% 至 485%**。

* **HBM4 价格暴涨：** Rubin 架构采用了下一代**高带宽内存（HBM4）**。由于 AI 需求旺盛且制造工艺复杂，HBM4 的价格预计将飙升至每 GB **53 美元**。仅 HBM4 组件就占每台机柜成本的约 **109 万美元**。
* **系统内存与存储：** 该系统严重依赖昂贵的 LPDDR5X 内存（占 **80 万美元**）以及直接连接的 3D NAND 存储（占 **128 万美元**）。2026 年波动的闪存与 DRAM 市场价格已将这些数字显著推高，超出最初预期。

### 2. 高端处理器的高密度配置（约 414 万美元）

* **72 个 Rubin GPU：** 单个 NVL72 机柜搭载了 72 个下一代 Rubin GPU。按每个 GPU **5.5 万美元**的批量价格估算，仅图形处理器就占据了机柜近一半的成本，达到 **396 万美元**。
* **36 个 Vera CPU：** 机柜还包含 36 个高性能 Vera CPU，这增加了另外 **18 万美元**（每颗芯片 5000 美元）。

### 3. 复杂的网络与基础设施（约 127 万美元）

为了连接 72 个 GPU 并确保数据流无瓶颈，架构基础设施已变得指数级复杂：

* **高级交换设备：** 包括约 **25 万美元**的高速 NVLink 交换机和 **20 万美元**的 Spectrum-X 网络交换机。
* **布线及背板：** 复杂的物理布线、铜缆/光缆布线以及背板成本增加约 **62 万美元**。

### 4. 先进材料与工程限制（约 50 万美元）

* **超高端 PCB：** 印刷电路板进行了大幅升级。例如，交换托盘 PCB 从 24 层扩展到 32 层，并采用了更高等级的材料（从 M7 标准升级到 M8 标准）。这导致 PCB 总成本上涨 **233%**（达到约 11.7 万美元）。
* **散热与电源：** 每个机柜功耗高达 **220 kW**，专用的液冷系统（约 **16 万美元**）和重型电源系统（约 **15 万美元**）进一步增加了高昂的溢价。

虽然单个机柜成本接近 910 万美元，但云巨头们仍在持续购买，因为其每美元对应的计算效率和带宽，在训练和部署前沿 AI 模型方面，仍然远超上一代架构。

参考文献：

* [伯恩斯坦警告，英伟达 Vera Rubin 机柜成本将达 910 万美元，HBM4 价格翻三倍至每 GB 53 美元](https://wccftech.com/bernstein-warns-nvidias-vera-rubin-racks-will-hit-9-1-million-as-hbm4-prices-triple-to-53-per-gigabyte/)
* [英伟达内存成本飙升 485%，最新 AI 系统造价达 780 万美元——内存现占总成本的 25%](https://www.google.com/search?q=https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidias-memory-costs-soar-485-percent-latest-ai-systems-now-cost-usd7-8-million-to-build-memory-now-comprises-25-percent-of-the-total-cost)
* [英伟达 Vera Rubin 机柜价格飙升到 780 万美元；PCB、MLCC、内存成本合计翻倍](https://finance.biggo.com/news/MrEuTZ4BX0tZvRTv67Pr)
