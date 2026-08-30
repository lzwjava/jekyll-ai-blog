---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU缩放：前景与限制
translated: true
type: note
---

**问题：** GPU 性能能否持续增长，其极限在哪里？

**回答：**

能——但扩展正变得愈发困难、昂贵且多维化。以下是完整图景：

---

**🟢 仍在扩展的部分：英伟达截至 2028 年的路线图**

英伟达已从两年一代转向**一年一代的发布节奏**，每一代目标性能提升约 2 倍：

| 年份 | 平台 | 关键 GPU | FP4 算力 |
|---|---|---|---|
| 2025 | Blackwell Ultra | B300 | ~20 PFLOPS |
| 2026 | Vera Rubin | R100 | ~50 PFLOPS |
| 2027 | Rubin Ultra | R300 | ~100 PFLOPS（预估） |
| 2028 | Feynman | — | 待定 |

Vera Rubin 平台提供 50 petaFLOPS 的 NVFP4 算力，相比 Blackwell 推理成本降低 10 倍。

---

**🔴 硬性极限——扩展正遭遇的瓶颈**

**1. 晶体管密度（摩尔定律放缓）**
晶体管密度扩展在 5nm 以下已明显减速，并接近栅极长度、漏电流和互连电阻的物理极限。每操作能耗的改进正在放缓——5nm 以下每个节点通常仅提升 1.3–1.5 倍，而较老节点可达 1.7–2 倍。传统摩尔定律的翻倍节奏已不复存在。

随着制程节点推进至 1nm 及以下，晶体管尺寸正接近硅原子的物理尺度——传统摩尔定律的扩展正在减速，并变得物理上不可行。

**2. 功耗/热墙**
功耗限制将成为 AI 扩展的主要制约因素。尽管效率有所提升，模型规模和推理需求的指数级增长意味着总功耗将持续上升。数据中心运营商将越来越多地受限于电网容量而非硬件可用性。Vera Rubin 机架功耗已达 190–230 kW，高于 Blackwell 的约 130 kW——并且需要全液冷。

**3. 内存（HBM）供应瓶颈**
HBM 已售罄至 2026 年，新增产能到 2027 年才会实质影响供应，紧缺状况预计持续至 2028 年。三星、SK 海力士和美光三家供应商控制了全球约 95% 的 DRAM 产能，它们正理性地将晶圆产能重新分配给利润极高的 HBM。

**4. 封装（CoWoS）瓶颈**
到 2026 年中，CoWoS 封装产能——而非原始晶圆启动——已成为 AI 硬件供应的刚性约束，CoWoS-S 和 CoWoS-L 均已满负荷预订，交货周期长达 52–78 周。这直接扼杀了 Rubin Ultra 最雄心勃勃的版本：在 GTC 2026 上发布的原始四芯片 Rubin Ultra GPU 因台积电尚无法解决的制造限制而被取消。实际将于 2027 年出货的 GPU 将只提供宣布规格约一半的计算能力和一半的内存带宽。

**5. 互连/带宽瓶颈**
对于单机架部署，英伟达正将铜互连推向绝对物理极限。Rubin Ultra NVL144 使用全铜扩展网络连接 144 颗 GPU——超越这一极限后，业界将转向共封装光学（CPO）以维持带宽增长。

---

**🔵 英伟达如何绕过这些瓶颈**

策略已从单纯缩小晶体管转向：

- **Chiplets（小芯片）** ——将多个芯片粘合在一起（B200 已使用 2 颗芯片；4 芯片设计已规划）
- **更低精度** ——FP8 → FP4 → 未来 FP2？每减半精度，有效吞吐量翻倍
- **机架级思维** ——GB200 NVL72 和 VR200 NVL72 将整个机架视为“一颗 GPU”
- **稀疏性** ——利用含大量零的矩阵实现 2 倍免费加速
- **共封装光学** ——用光取代铜进行 GPU 间通信

---

**核心结论：** 每项技术都会遇到极限。问题不在于极限是否存在——数学已证明其存在。约束不会终结进步，而是引导其方向。GPU 性能将持续增长，但将更多地依赖于精巧的封装、机架级集成和新的精度格式——而非单纯依靠晶体管缩小。

---

**参考资料：**
- [Nvidia GPU Roadmap 2026–2030 — VRLA Tech](https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/)
- [Rubin Ultra Four-Die GPU Cancelled — TechTimes](https://www.techtimes.com/articles/319410/20260701/nvidia-rubin-ultra-four-die-gpu-cancelled-packaging-limits-cut-2027-performance-half.htm)
- [HBM4 and Fab Limits — NextBigFuture](https://www.nextbigfuture.com/2026/07/hbm4-and-fab-limits-prevent-1000-vera-rubin-racks-per-day-in-2026-or-2027.html)
- [Hitting the Wall: Physical Limits of AI Chips — TetraMem](https://tetramem.com/hitting-the-wall-the-1d-2d-and-3d-physical-limits-threatening-the-future-of-ai-chips/)
- [The Memory Wall — SemiAnalysis](https://newsletter.semianalysis.com/p/the-memory-wall)