---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MEM 1215兆赫含义
translated: true
type: note
---

**问题：** NVIDIA GPU 中的“MEM 1215 MHz”是什么意思？

**答案：**

**MEM MHz** 指的是 GPU 的**显存时钟频率**——具体来说，就是显存（VRAM）每秒处理数据的周期数。

**1215 MHz** 意味着 GPU 上的显存芯片以每秒 12.15 亿个周期运行。然而，**有效**（实际数据传输）速度要高得多，具体取决于显存类型：

| 显存类型 | 基础时钟频率 | 有效速度（乘以） |
| --- | --- | --- |
| GDDR5 | 1215 MHz | × 4 → ~4860 MHz |
| GDDR5X | 1215 MHz | × 8 → ~9720 MHz |
| GDDR6 | 1215 MHz | × 16 → ~19440 MHz |

因此，您在 GPU-Z 或 nvidia-smi 等工具中看到的数字是**基础时钟频率**，而非最终带宽速率。

**为什么重要：**

- MEM MHz 越高 = 显存与 GPU 核心之间的数据传输越快
- 影响内存密集型任务的性能：4K 游戏、AI/ML 工作负载、视频编辑
- 您可以超频 MEM MHz 以获取额外性能，但过高会导致画面异常或崩溃

**1215 MHz 具体来说**，是中端 NVIDIA GPU（例如 GTX 1060、GTX 1070 时代）常见的默认时钟频率。

参考来源：

- [GPU 显存时钟频率详解 – GPU-Z](https://www.techpowerup.com/gpuz/)
- [NVIDIA GDDR 显存类型](https://www.nvidia.com/en-us/geforce/graphics-cards/)
