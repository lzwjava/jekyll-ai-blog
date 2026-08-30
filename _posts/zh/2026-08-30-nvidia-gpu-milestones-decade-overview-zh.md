---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达GPU十年里程碑概览
translated: true
type: note
---

**问题：** 过去十年（及更早）中，英伟达最大、最强大的 GPU 里程碑有哪些？

**答案：**

以下是英伟达标志性 GPU 的编年史巡礼——从游戏霸主到 AI 超级计算：

---

**🎮 GTX 980（2014年）——麦克斯韦架构**  
旗舰级 GTX 980 横扫了 AMD 的 R9 290X 以及英伟达自家的上一代 GTX 780 Ti。麦克斯韦架构带来了巨大的能效提升。

---

**🎮 GTX 1080 / 1080 Ti（2016–2017年）——帕斯卡架构**  
16nm 帕斯卡架构遥遥领先于竞争对手，以至于 GeForce GTX 10 系列显卡在多年后仍具竞争力——这在显卡市场上几乎是个异类。GTX 1080 Ti 相比 1080 又带来了 30% 的性能提升，进一步巩固了英伟达在高端市场的统治地位。

---

**✨ RTX 2080（2018年）——图灵架构**  
基于图灵架构的 RTX 20 系列首次在面向消费者的显卡中实现了实时光线追踪硬件支持。这是历史性的第一次，尽管初期普及速度较慢。

---

**🚀 RTX 3080 / A100（2020年）——安培架构**  
RTX 3080 在 4K 分辨率下相比 RTX 2080 Ti 带来了显著的 30% 性能提升。在数据中心侧，安培架构为 AI 工作负载带来了巨大的扩展性和稀疏性改进。

---

**🤖 H100（2022年）——霍珀架构**  
伏特架构于 2017 年引入了 Tensor Core；霍珀和布莱克韦尔架构则扩展了 Transformer 加速和机架级计算。H100 成为现代 AI 基础设施的骨干，为 ChatGPT 级别的训练提供算力。H100 配备 80 GB HBM3 显存和 3.35 TB/s 显存带宽。

---

**🧠 H200（2024年）——霍珀刷新版**  
H200 在 H100 基础上采用更新的 HBM3e 显存，并将总显存提升至 141 GB，从而在推理过程中支持更大的批处理量和更高的吞吐量。它提供约 241.3 TFLOPS FP16 算力和约 4.89 TB/s 显存带宽。

---

**⚡ B200 / GB200 NVL72（2024–2025年）——布莱克韦尔架构**  
当前的 reigning champion。B200 采用双芯片小芯片设计，包含 2080 亿个晶体管，基于台积电 4NP 工艺，每颗 GPU 提供 20 petaFLOPS FP4 AI 算力和 192 GB HBM3e 显存。GB200 NVL72 将 72 颗 B200 集成到一个 13.4 TB 液冷机架中，专为万亿参数模型打造。B200 的算力是 H200 的 2.3 倍，显存带宽是 H200 的 1.7 倍。

---

**快速总结表：**

| 年份 | GPU | 架构 | 关键里程碑 |
|------|-----|-------------|---------------|
| 2014 | GTX 980 | Maxwell | 能效飞跃 |
| 2016 | GTX 1080 Ti | Pascal | 游戏统治 |
| 2018 | RTX 2080 | Turing | 首次 RT 硬件 |
| 2020 | A100 / RTX 3080 | Ampere | AI + 游戏爆发 |
| 2022 | H100 | Hopper | AI 训练时代 |
| 2024 | H200 | Hopper+ | 141 GB HBM3e |
| 2024–25 | B200 / GB200 | Blackwell | 20 PFLOPS, 192 GB |

---

**参考资料：**
- [Top 10 Most Significant Nvidia GPUs — TechSpot](https://www.techspot.com/article/2177-top-10-nvidia-graphics/)
- [Evolution of NVIDIA Data Center GPUs — ServerSimply](https://www.serversimply.com/blog/evolution-of-nvidia-data-center-gpus)
- [NVIDIA GPU History: GeForce 256 to Vera Rubin — IoHTechCo](https://iohtechco.com/resources/nvidia-gpu-history-evolution)
- [B200 vs H200 Comparison — vast.ai](https://vast.ai/article/nvidia-h200-vs-b200-comparing-datacenter-grade-accelerators)
- [NVIDIA Blackwell Architecture — AI Tool Discovery](https://www.aitooldiscovery.com/ai-infra/nvidia-blackwell-architecture)