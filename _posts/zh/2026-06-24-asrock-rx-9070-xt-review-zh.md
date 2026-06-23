---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 撼讯RX 9070 XT评测
translated: true
type: note
---

**问题：** ASRock Challenger Radeon RX 9070 XT 是什么？它值得考虑吗？

**答案：**

这是 **ASRock Challenger RX 9070 XT 16GB**——AMD 当前一代 RDNA 4 旗舰（位于 9070 XT 更大尺寸型号之下），在 Walmart（通过 Newegg）售价为 **699.99 美元**。

**核心规格：**

| 规格 | 值 |
|------|------|
| GPU | Radeon RX 9070 XT (RDNA 4) |
| 显存 | 16GB GDDR6，256-bit 位宽 |
| 流处理器 | 4096 |
| 加速频率 | 2970 MHz |
| 接口 | PCIe 5.0 x16 |
| 显示输出 | 1× HDMI 2.1b，3× DisplayPort 2.1a |
| 功耗 | ~304W TDP（参考） |
| 尺寸 | 3.9 英寸高，3.3 磅 |

**这张卡是什么？**

RX 9070 XT 采用 AMD 的 RDNA 4 架构，于 2025 年初推出。RDNA 4 相比 RDNA 3 带来了显著的 IPC 提升、改进的光线追踪（RT 吞吐量是 RDNA 3 的 2 倍）、用于 FSR 4（AMD 对 DLSS 4 的回应）的硬件加速 AI 推理单元，以及搭载 GDDR6 的 256 位总线，带宽具有竞争力。“Challenger”是 ASRock 的入门级散热系列——双风扇/三风扇，功能实用但不如其 Taichi 或 Phantom 系列那样高端。

**与竞品相比的定位：**

- **RTX 5070（$599–629）**——DLSS 4 Multi Frame Generation 如果倾向 NVIDIA 则是大事；12GB GDDR7 但总线更窄。在 1440p/4K 光栅化方面，9070 XT 互有胜负。
- **RX 9070（非 XT，~$550–600）**——相同架构，速度慢约 10–15%。如果预算紧张，9070 是极佳选择。
- **RTX 5070 Ti（~$850–950）**——明显更快，但价格高得多。

在 699 美元价位上，Challenger 是最便宜的 9070 XT 型号（ASRock 自家的 Taichi 为 789 美元，Steel Legend 为 749 美元）。它基本是参考散热级别的显卡，带有一条基础 RGB 灯带。评测指出它降压表现良好，可获得额外的散热/效率空间。

**与你的配置的相关性：**

你的 Ubuntu 工作站上已经有一块 RTX 4070（12GB）。9070 XT 在光栅化方面快约 35–45%，并且拥有 16GB 对比 12GB——如果你进行本地推理或训练，这很有意义（16GB 可容纳更大模型/批次）。然而：截至 2026 年中，RDNA 4（gfx1200/gfx1201）上的 ROCm 支持仍在完善中。如果你在这张卡上运行 ML 工作负载，请在购买前验证 ROCm 6.x 与你目标框架的兼容性——AMD 的消费级显卡在计算 vs 游戏方面历来较为挑剔。

对于纯游戏或作为副显示卡来说，这是一个很划算的选择。对于 ML 计算，你已可访问的 AMD MI300X 要好几个数量级，因此这张卡主要可以作为你工作站的游戏/显示升级。
