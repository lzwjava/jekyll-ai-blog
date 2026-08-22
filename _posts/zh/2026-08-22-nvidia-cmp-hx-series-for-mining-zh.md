---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达CMP HX系列矿卡
translated: true
type: note
---

**问题：** NVIDIA 专门为挖矿推出了哪些 GPU（例如基于 GA100 的显卡），主要型号有哪些？

---

**回答：**

NVIDIA 的专用挖矿 GPU 产品线称为 **CMP（加密货币挖矿处理器）HX 系列**，于 2021 年推出。这些显卡 **没有显示输出接口**，专为挖矿而非游戏设计。以下是完整产品线：

---

### NVIDIA CMP HX 系列——挖矿专用显卡

| 型号 | 架构 / GPU | 显存 | 算力 (Ethash) | 功耗 |
| --- | --- | --- | --- | --- |
| **CMP 30HX** | Turing / TU116 | 6 GB GDDR6 | ~26 MH/s | ~125W |
| **CMP 40HX** | Turing / TU106 | 8 GB GDDR6 | ~36 MH/s | ~185W |
| **CMP 50HX** | Turing / TU102 | 10 GB GDDR6 | ~45 MH/s | ~250W |
| **CMP 90HX** | Ampere / GA102 | 10 GB GDDR6X | ~86–92 MH/s | ~320W |
| **CMP 170HX** | Ampere / **GA100** | 8 GB HBM2e | ~160–164 MH/s | ~250W |
| **CMP 220HX** | Ampere | — | 更高层级 | — |

CMP 30HX、40HX 和 50HX 均基于 Turing 架构（12nm 制程）。其中 50HX 使用 TU102，40HX 使用 TU106，30HX 使用 TU116。

旗舰型号 CMP 170HX 采用完整的 GA100 芯片——与 A100 数据中心 GPU 相同的硅片——但针对挖矿进行了专门配置：无 NVLink 接口，PCIe Gen4 针对持续运行的 Ethash 性能进行了优化。

CMP 170HX 配备 8 GB HBM2e 显存，频率 1.4 GHz，提供高达 1.5 TB/s 的带宽，功耗 250W，算力 160+ MH/s。

所有 CMP 显卡均为“无头”设计——无显示输出接口——旨在通过提供专用产品线来减轻 GeForce 游戏显卡的挖矿压力。

---

### 重要说明

- **比特币挖矿：** GPU 在比特币挖矿方面通常不如 ASIC 高效，更适合挖掘以太坊经典、Kaspa 或 Ravencoin 等其他加密货币。
- **消费级替代方案：** 截至 2025 年底，RTX 5090 被认为是消费级挖矿最佳显卡，但前期成本较高且功耗高达 580W。
- CMP 系列在 2021 年后停产，因为以太坊转向权益证明（PoS），导致大部分基于 GPU 的 ETH 挖矿需求消失。

---

**参考资料：**

- [NVIDIA CMP HX Official Page](https://www.nvidia.com/en-us/cmp/)
- [CMP 170HX — Tom's Hardware](https://www.tomshardware.com/news/nvidias-cmp170hx-in-the-wild-with-164-mhps-ethereum-mining-performance)
- [CMP Architecture Details — WCCFtech](https://wccftech.com/nvidias-cmp-crypto-mining-gpus-detailed-90hx-based-on-ampere-ga102-while-50hx-40hx-30hx-based-on-turing-gpus/)
- [CMP 170HX Guide — ScreenRant](https://screenrant.com/nvidias-cmp-170hx-gpu-price-availability-hash-rate/)
