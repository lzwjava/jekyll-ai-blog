---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniCPM：小型高效开源模型
translated: true
type: note
---

问：什么是MiniCPM？

OpenBMB MiniCPM 是一系列**小型、高效的开源基础模型**，由OpenBMB开发（贡献者包括ModelBest、THUNLP和中国人民大学高瓴人工智能学院）。核心思想是：

> **让大语言模型足够小，可以在本地/边缘设备上运行，同时保持接近更大模型的能力。**

可以将其视为中国AI生态系统对微软Phi、Meta Platforms Llama小模型、阿里巴巴集团Qwen小模型等模型的回应。

---

## 模型演进

### MiniCPM（文本大语言模型）

最初的MiniCPM专注于**小语言模型（SLMs）**：

* MiniCPM-1B / 2B 级别
* 与7B-13B模型相比，性能出人意料地强大
* 专为低成本推理和研究实验设计

2024年的论文引入了1.2B和2.4B参数模型，并表明精心设计的训练策略可以使小模型与更大模型竞争。

```
Llama2-13B
      |
      v
MiniCPM-2B
```

不是因为架构神奇，而是因为：

```
更好的数据
+
更好的训练方法
+
小巧高效的架构
=
更高的能力/每FLOP
```

---

## MiniCPM-V（视觉-语言）

这可能是最著名的分支。

架构：

```
Image
 |
Vision Encoder
 |
Projector
 |
LLM backbone
 |
Text answer
```

类似的想法有：

* GPT-4V
* Gemini Vision
* Qwen-VL

应用场景：

* OCR
* 文档理解
* 图像问答
* 图表/表格
* 截图

MiniCPM-V系列因其在相对较小的参数规模下提供了强大的视觉能力而变得流行。

---

## MiniCPM-o（全模态）

"o"代表"全"。

它结合了：

```
text
+
image
+
audio
+
speech output
```

示例：

```
camera stream
      |
      v
MiniCPM-o
      |
      +--> understands scene
      |
      +--> talks back
```

最近的MiniCPM-o版本面向实时全双工交互：

* 边说边听
* 观看实时视频
* 语音对话

4.5版本是一个9B级别的多模态模型，专为高效的实时交互设计。

---

## MiniCPM4 / MiniCPM5

这些更侧重于**大语言模型效率工程**。

MiniCPM4引入了以下技术：

* sparse attention
* 高效推理
* quantization
* 长上下文优化

目标：

```
cloud-scale capability
        ↓
edge device deployment
```

例如：

```
Server:
H100
1000W

vs

Phone:
5-10W
```

MiniCPM试图将能力推向第二类。

---

## 为什么MiniCPM在技术上有趣

从工程角度来看，它代表了一种趋势：

### 1. 参数效率

旧思维：

```
bigger model = smarter
```

新思维：

```
better training + better architecture
=
smaller model with similar capability
```

示例：

```
70B model
    |
    |
    v

7B distilled model
    |
    |
    v

1B model optimized for edge
```

---

### 2. 本地AI

MiniCPM的目标：

* 手机
* 笔记本电脑
* 机器人
* 嵌入式设备

因为推理成本很重要：

内存：

```
FP16:

7B params × 2 bytes
≈ 14GB VRAM

1B params × 2 bytes
≈ 2GB VRAM
```

量化后：

```
1B INT4

≈ 0.5GB
```

所以手机可以运行它。

---

### 3. 智能体方向

小模型正在变得有用，作为：

* 工具路由器
* 本地助手
* 机器人大脑
* OCR engines
* 个人智能体

未来的架构可能看起来像：

```
              Cloud LLM
                  |
        -------------------
        |                 |
    Local MiniCPM     Local tools
        |
     phone/robot
```

---

对于你的背景（训练GPT-2 760M、运行本地模型、ROCm/GPU实验），MiniCPM尤其有趣，因为它基本上就是**“我们能把1B模型推到多远？”**的研究方向。

一个好的实验：

```bash
# compare capability per VRAM

Qwen3-8B
vs
MiniCPM5-1B
vs
Llama-3.2-1B

same hardware:
RTX 4070 12GB
```

测量：

```
tokens/sec
VRAM
MMLU
HumanEval
Chinese benchmark
agent tool use
```

这正是行业的发展方向：**不仅扩大规模，而且提升智能效率。**

参考文献：

* [MiniCPM GitHub repository](https://github.com/openbmb/minicpm?utm_source=chatgpt.com)
* [MiniCPM paper: Unveiling the Potential of Small Language Models with Scalable Training Strategies](https://arxiv.org/abs/2404.06395?utm_source=chatgpt.com)
* [MiniCPM4: Ultra-Efficient LLMs on End Devices](https://arxiv.org/abs/2506.07900?utm_source=chatgpt.com)

[1]: https://github.com/openbmb/minicpm?utm_source=chatgpt.com "GitHub - OpenBMB/MiniCPM: MiniCPM5-1B: A SOTA 1B on-device LLM, small yet powerful. · GitHub"
[2]: https://arxiv.org/abs/2404.06395?utm_source=chatgpt.com "MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies"
[3]: https://huggingface.co/openbmb/models?utm_source=chatgpt.com "openbmb (OpenBMB)"
[4]: https://arxiv.org/abs/2604.27393?utm_source=chatgpt.com "MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction"
[5]: https://arxiv.org/abs/2506.07900?utm_source=chatgpt.com "MiniCPM4: Ultra-Efficient LLMs on End Devices"