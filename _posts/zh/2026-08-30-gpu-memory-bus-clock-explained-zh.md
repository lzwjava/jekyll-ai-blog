---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU显存总线与时钟解析
translated: true
type: note
---

问题：GPU中的“显存”、“显存位宽”和“显存频率”分别是什么意思？

答案：

**显存（VRAM）**
GPU专用视频内存——一个高速内存池，用于存储GPU正在处理的所有内容：纹理、帧缓冲区、渲染目标、着色器和几何数据。更大的显存容量允许你运行更高的分辨率、更大的纹理和更复杂的场景，而不会出现卡顿。常见类型有GDDR6、GDDR6X和HBM3。

**显存位宽（Memory Bus Width）**
连接GPU芯片与其显存的物理“高速公路”。以位为单位（例如128位、256位、384位）。位宽越宽，意味着每个时钟周期可以并行传输的数据越多——因此，在其他条件相同的情况下，256位总线一次移动的数据量是128位总线的两倍。它直接决定了可能达到的原始带宽。

**显存频率（Memory Frequency）**
显存的工作速度，以MHz或Gbps（有效值）衡量。频率越高，总线每秒传输数据的次数就越多。制造商通常宣传*有效*速度（例如“18 Gbps”），这已经考虑了GDDR内存的双倍/四倍泵送特性。

---

**三者如何结合——显存带宽：**
这三个因素共同作用，得出最重要的衍生指标：

> **带宽（GB/s）=（位宽 ÷ 8）× 有效频率**

示例——RTX 4090：
- 位宽：384位 → 48字节宽度
- 频率：约21 Gbps有效
- 带宽：48 × 21 = **约1,008 GB/s**

如果GPU带宽不足（无法满足其着色器吞吐量），无论其计算核心有多强大，性能都会受限。

---

参考：
- [GPU显存带宽详解 — TechPowerUp](https://www.techpowerup.com/gpu-specs/)
- [VRAM：你需要多少？ — Digital Foundry / Eurogamer](https://www.eurogamer.net/digitalfoundry-2023-how-much-vram-do-you-need)
- [GDDR6 vs GDDR6X vs HBM — AnandTech](https://www.anandtech.com)