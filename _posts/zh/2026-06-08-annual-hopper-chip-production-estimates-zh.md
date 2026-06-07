---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 年度霍珀芯片生产预估
translated: true
type: note
---

问题：NVIDIA和台积电每年生产多少块H100、H200或H800芯片？

回答：

由于NVIDIA负责芯片设计，但完全依赖台积电（台湾积体电路制造公司）进行制造和先进封装（CoWoS），两者合计的年产能近几年大幅提升，以满足前所未有的AI需求。

产量数字按**Hopper系列的总量**计算（包括**H100**、升级版**H200**、以及面向中国出口合规的**H800**和**H20**等变体），因为它们共享相同的底层硅芯片架构和制造流程。

---

## 年度生产时间线（估算）

### 1. 2023年产量：约50万至100万块芯片

* **瓶颈：** 2023年的产量主要受限于台积电有限的**CoWoS（晶圆基底芯片封装）** 产能，而非晶圆制造本身。
* **细目：** 台积电在2023年上半年/中期出货了约**50万至55万**块旗舰级H100。到年底，随着二级供应链的开启，累计产量接近**100万块H100等效芯片**。这包括H800的初期生产批次，之后美国于2023年底出台了更严格的出口管制。

### 2. 2024年产量：约350万至500万块芯片

* **产能爬坡：** 这是Hopper系列的产量高峰期。台积电大幅扩建了其高端封装工厂，NVIDIA也通过利用其他先进封装代工厂（如英特尔代工服务）来补充供应链。
* **细目：** 2024年总产量上限约为**400万至500万块Hopper代GPU**。
* **H100** 占据了2024年初出货量的主要部分。
* **H200**（配备更快的HBM3e内存）在2024年中进入量产，并取代H100成为主力旗舰。
* **H800** 大多因制裁更新而逐步淘汰，被大幅改动的**H20**型号取代，面向中国市场。

### 3. 2025–2026年转变：Hopper产量下降

* **过渡期：** 到2025年及进入2026年，台积电的生产线大量从Hopper架构转移，优先生产NVIDIA下一代**Blackwell架构（B100、B200、GB200）** 以及后续的**Blackwell Ultra / GB300**系列。
* **当前状态：** H100和H200的合并销量从2024年每季度数十万块急剧下降，到2025/2026年底仅维持最低维护水平，原因是云服务提供商已全面转向Blackwell。

---

## 技术极限：每片晶圆能产出多少芯片？

Hopper GPU（GH100裸片）物理尺寸巨大，约为**814 mm²**。

* 一片标准300mm硅晶圆理论上可容纳约**86**块这种大型芯片。
* 由于大规模制造中不可避免的缺陷，良率（每片晶圆上功能正常的芯片比例）通常在**65%至70%** 左右。
* 这意味着在进入复杂的CoWoS封装流程之前，台积电每片晶圆大约能得到**55至60块可用的Hopper芯片**。

参考资料：

* [When Do More AI Chips for China Mean Fewer for the United States? - IFP.org](https://ifp.org/ai-chip-supply-diversion/)
* [Estimates of GPU or equivalent resources of large AI players for 2024/5 - LessWrong](https://www.lesswrong.com/posts/bdQhzQsHjNrQp7cNS/estimates-of-gpu-or-equivalent-resources-of-large-ai-players)
* [Nvidia reportedly selects Intel Foundry Services for GPU packaging production - Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidia-reportedly-selects-intel-foundry-services-for-chip-packaging-production-could-produce-over-300000-h100-gpus-per-month)
* [The stock of computing power from NVIDIA chips is doubling every 10 months - Epoch AI](https://epoch.ai/data-insights/nvidia-chip-production)
