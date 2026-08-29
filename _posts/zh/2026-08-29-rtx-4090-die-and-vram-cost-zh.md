---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4090核心与显存成本
translated: true
type: note
---

**问题：** NVIDIA RTX 4090 中 GPU 核心和显存的生产成本是多少？

**回答：**

NVIDIA 并未公开其物料清单（BOM），但行业分析师已拼凑出可信的估算。以下是成本明细：

---

### 🔲 GPU 核心 (AD102)

AD102 核心采用台积电 4nm EUV（4N）工艺制造，拥有 763 亿个晶体管，核心面积为 608 mm²。

基于此核心面积，NVIDIA 每片晶圆大约只能切割出 **约 90 颗完整核心**。据报道，台积电 4N 节点的成本**至少是**台积电 N7/N6 等旧节点的两倍——这意味着 AD102 每颗芯片的成本是上一代 RTX 3090 所用 GA102 的两倍以上。

独立分析师估计，AD102 GPU 核心的制造成本约为 **175 至 200 美元**，不过这个数字自计算以来可能已经发生变化。

---

### 🧠 显存 (24 GB GDDR6X)

RTX 4090 配备 **24 GB GDDR6X 显存**，采用 384-bit 位宽，运行速度为 21 Gbps，可提供约 1 TB/s 的显存带宽。

NVIDIA 没有披露显存的合约价，但 GDDR6X 是最昂贵的消费级显存之一。行业估计，GDDR6X 的批量价格约为**每 GB 8 至 10 美元**，这意味着 24 GB 显存的原生成本约为 **190 至 240 美元**——显存子系统的成本与核心本身相当。

---

### 💰 完整画面（估算 BOM）

| 组件            | 估算成本       |
|---------------|------------|
| AD102 GPU 核心  | ~175–200 美元 |
| 24 GB GDDR6X 显存 | ~190–240 美元 |
| PCB、供电、散热、接口  | ~80–150 美元  |
| **BOM 总成本（约）** | **约 450–600 美元** |

除原材料成本外，NVIDIA 还需考虑研发、工程、台积电晶圆预留及封装费用。随后，NVIDIA、AIB 合作伙伴和零售商在显卡到达消费者手中之前都会层层加价。

该显卡于 2022 年 10 月以 **1,599 美元的建议零售价（MSRP）** 发布。截至 2026 年中，市场价通常在 **2,400 至 2,800 美元**之间，远高于首发价，原因是 NVIDIA 于 2024 年底停止生产，且市场对 24 GB 显存的 AI 需求依然旺盛。

因此，约 450 至 600 美元的制造成本对比 1,600 至 2,800 美元的零售价，反映了 NVIDIA 众所周知的超高利润率——旗舰消费级 GPU 的毛利率估计在 **60% 以上**。

---

**参考资料：**

- [Why Nvidia's RTX 4080, 4090 Cost so Damn Much — Tom's Hardware](https://www.tomshardware.com/news/why-nvidias-4080-4090-cost-so-damn-much)
- [Spitballing Nvidia's RTX 5090 GPU Die Manufacturing Costs — Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/spitballing-nvidias-gb202-gpu-die-manufacturing-costs-die-could-cost-as-little-as-usd290-to-make)
- [RTX 4090 Doesn't Max-Out AD102 — TechPowerUp](https://www.techpowerup.com/299091/nvidia-rtx-4090-doesnt-max-out-ad102-ample-room-left-for-future-rtx-4090-ti)
- [NVIDIA RTX 4090: Specs, 24GB VRAM, Price & AI Performance — RunPod](https://www.runpod.io/articles/guides/nvidia-rtx-4090)
- [How Much Is the RTX 4090's Production Cost? — Quora](https://www.quora.com/How-much-is-the-RTX-4090-s-production-cost-Is-it-overpriced-If-it-is-how-much-do-you-think-it-should-cost)
