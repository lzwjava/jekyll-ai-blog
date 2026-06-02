---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 源编码中的模数转换
translated: true
type: note
---

问题：A/D conversion 涉及 sampling、quantization 和 encoding；这是在哪个阶段进行的？

答案：

Analog-to-Digital (A/D) conversion 过程，包括 **sampling**、**quantization** 和 **encoding**，是在数字通信系统中的 **Source Encoding**（或 **信源编码**）阶段进行的。

### 详细解释

1. **Sampling**：这是将连续时间 analog signal 通过定期取样转换为离散时间信号的过程。根据 Nyquist-Shannon sampling theorem，采样率必须至少是信号最高频率分量的两倍，以避免 aliasing。
2. **Quantization**：这一步将采样信号的连续幅度值映射到有限的离散电平集合。这会引入 quantization error（噪声），但对于数字表示是必需的。
3. **Encoding**：在 A/D conversion 的最后一步，每个 quantized level 被分配一个唯一的 binary code（比特序列）。

在通信系统模型的上下文中：

- **Source Encoding** 的目的是将源信息（可能是 analog 的，如 voice 或 video）高效转换为数字 bit stream。如果源是 analog 的，它通常包括 compression 和 A/D conversion 过程本身。
- **Channel Encoding** 在 source encoding 之后，对 bit stream 添加冗余以保护传输过程中免受错误影响（例如，添加 parity bits）。
- **Modulation** 将数字基带信号转换为适合在物理信道上传输的形式。

因此，由于 A/D conversion 将原始 analog 源信息转换为数字格式，它完全属于 **Source Encoding** 的范畴。

参考文献：

- [Analog-to-Digital Conversion - Wikipedia](https://en.wikipedia.org/wiki/Analog-to-digital_converter)
- [Source Coding - Britannica](https://www.britannica.com/technology/source-coding)
