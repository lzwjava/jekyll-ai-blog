---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.1-schnell 概述
translated: true
type: note
---

## 问题：`black-forest-labs/FLUX.1-schnell` 简介

## 回答

Black Forest Labs 的 **FLUX.1-schnell** 是继 Stable Diffusion 之后最重要的开源权重图像生成模型之一。它是一个 **12B 参数 text-to-image 模型**，基于 **rectified flow transformer** 架构，专为 **极速生成** 而优化。([Hugging Face][1])

仓库：
[FLUX.1-schnell on Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-schnell?utm_source=chatgpt.com)

---

## 1. 整体概览

传统扩散：

```
noise
  |
  |  many denoising steps (20-1000)
  v
clean image
```

FLUX.1-schnell：

```
text prompt
    |
    v
CLIP/T5 text encoder
    |
    v
Flux Transformer (12B)
    |
    v
few flow steps (1-4)
    |
    v
VAE decode
    |
    v
image
```

关键思想：

**构建一个庞大而强大的模型，然后进行蒸馏，使推理只需少量步骤。** ([Hugging Face][1])

---

## 2. 为什么叫 "schnell"？

`schnell` 在德语中意为快速。

FLUX 系列：

| Model          | 用途                 | 许可证                | 速度   |
| -------------- | --------------------- | --------------------- | ------- |
| FLUX.1-pro     | 最佳质量的 API 模型   | 商业 API              | 最慢    |
| FLUX.1-dev     | 研究/开发质量         | 非商业许可证          | 中等    |
| FLUX.1-schnell | 本地快速生成          | Apache 2.0            | 最快    |

FLUX.1-schnell 使用 **latent adversarial diffusion distillation** 实现高质量，允许在 **1-4 步** 内生成，而不是传统扩散所需的几十步。([Hugging Face][1])

---

## 3. 架构

它不是 Stable Diffusion XL 风格的 U-Net。

旧架构：

```
Stable Diffusion:

Text encoder
     |
     v
 U-Net
     |
     v
 latent image
```

FLUX：

```
Text tokens
     +
Image latent tokens
          |
          v
  Transformer blocks
          |
          v
  Flow matching trajectory
          |
          v
       VAE
          |
          v
       pixels
```

核心是类似 **Diffusion Transformer (DiT)** 的架构。

可以这样理解：

```
GPT transformer
+
image patches
+
flow matching
```

非常相似的哲学：

```
LLM:

token -> transformer -> next token
```

FLUX：

```
image latent token -> transformer -> next denoising direction
```

---

## 4. 硬件要求

官方模型：

* 参数：约 12B
* 默认数据类型：BF16
* 庞大的文本编码器 + transformer + VAE

([Hugging Face][1])

典型 VRAM 需求：

### RTX 4070 12GB

可能可行，但：

* 无法舒适地加载 BF16 全精度
* 需要 CPU offload
* 速度较慢

示例：

```python
pipe.enable_model_cpu_offload()
```

Hugging Face 建议使用 `pipe.enable_model_cpu_offload()` 来节省 VRAM。([Hugging Face][2])

你在 RTX 4070 上使用 FLUX.2 的体验是合理的：图像模型极其消耗内存，因为 transformer 占据了大量 VRAM。

---

## 5. 本地运行

最小化的 Diffusers 设置：

```bash
pip install diffusers transformers accelerate
```

Python：

```python
import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)

pipe.enable_model_cpu_offload()

image = pipe(
    "a cyberpunk city at night, cinematic lighting",
    guidance_scale=0,
    num_inference_steps=4
).images[0]

image.save("flux.png")
```

([Hugging Face][2])

---

## 6. 为什么工程师喜欢 FLUX

与旧版 Stable Diffusion 相比：

### 更好的提示遵循能力

示例：

```
"a red cube on top of a blue sphere,
with text saying HELLO WORLD"
```

FLUX 在以下方面表现更好：

* 物体关系
* 排版
* 复杂场景

### 更好的美学效果

* 光照
* 构图
* 真实感

FLUX 发布时，社区对比经常强调这些优势。([Reddit][3])

---

## 7. 与你 GPT 实验的关联

有趣的类比：

```
Your GPT-2 training:

15B tokens
↓
Transformer learns language distribution
↓
generate text
```

FLUX：

```
massive image-text dataset
↓
Transformer learns visual distribution
↓
generate image
```

架构趋势正在趋同：

```
CNN era
   ↓
U-Net diffusion
   ↓
Transformer diffusion
   ↓
multimodal foundation models
```

FLUX 基本上就是图像生成领域的“GPT 时刻”：

> 用大型 transformer 取代专门的视觉网络。

---

## 8. 针对你的 RTX 4070 配置

1. **FLUX.1-schnell**
   * 最佳的初次实验
   * 可行的本地使用

2. 量化版本：
   * GGUF / FP8 变体
   * 更低 VRAM 占用

3. ComfyUI 工作流：
   * 最容易用于尝试 LoRA、类似 ControlNet 的条件控制

你的 RTX 4070 12GB 实际上是一个很好的“研究工作站”GPU，用于学习这些架构，类似于人们曾经用 8-16GB 显卡学习 LLM 推理的方式。

参考链接：

[1]: https://huggingface.co/black-forest-labs/FLUX.1-schnell?utm_source=chatgpt.com "black-forest-labs/FLUX.1-schnell · Hugging Face"
[2]: https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/ebe987ee3929ae4f45d31e003ae5ee24339c12c0/README.md?utm_source=chatgpt.com "README.md · black-forest-labs/FLUX.1-schnell at ebe987ee3929ae4f45d31e003ae5ee24339c12c0"
[3]: https://www.reddit.com/r/StableDiffusion/comments/1ehh1hx?utm_source=chatgpt.com "Announcing Flux: The Next Leap in Text-to-Image Models"
