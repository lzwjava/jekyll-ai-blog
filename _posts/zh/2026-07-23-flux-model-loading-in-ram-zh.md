---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flux模型加载到RAM中
translated: true
type: note
---

## 问题：解释这个 `stable-diffusion.cpp` Flux 模型加载日志

这是一个 **使用 stable-diffusion.cpp / ggml 后端的 FLUX.1-schnell 推理日志**。它显示：

1. 检测到的模型架构
2. 加载的量化权重
3. 加载的文本编码器
4. 加载的 VAE
5. 加载的 Flux 变换器
6. 开始采样

有趣的部分：**整个 Flux 模型主要在 RAM 中运行，而不是 VRAM**。

---

## 1. 权重类型统计

```
Conditioner weight type stat:          f16: 196
Diffusion model weight type stat:     q4_0: 776
VAE weight type stat:                  f32: 244
```

FLUX 管道有三个主要组件：

```
Prompt
 |
 v
Text Encoder (CLIP + T5)
 |
 v
Flux Transformer (denoiser)
 |
 v
VAE Decoder
 |
 v
Image
```

### Conditioner

```
f16: 196
```

这是文本条件模型。

通常包括：

* CLIP-L
* T5-XXL（可选）

这里加载了：

```
clip_l.safetensors
```

---

### Diffusion model

```
q4_0: 776
```

这是大型 Flux 变换器。

原始模型：

```
FLUX.1-schnell
约 12B 参数
```

正常情况下：

```
BF16:
约 23-24 GB
```

这里采用了：

```
Q4_0 量化
```

意味着：

* 4 位权重
* ggml 格式
* 内存小得多

近似计算：

```
12B * 4 bits
=
6 GB
```

匹配结果：

```
diffusion_model 6389.02MB
```

这是主要的内存节省点。

---

### VAE

```
f32: 244
```

VAE 解码器很小。

内存：

```
160 MB
```

它将潜在空间转换：

```
latent tensor
      |
      v
 VAE decoder
      |
      v
 RGB image
```

---

# 2. 警告

```
t5xxl text encoder not found!
Prompt adherence might be degraded.
```

很重要。

完整的 FLUX 使用：

```
CLIP-L
+
T5-XXL
```

架构：

```
Prompt
 |
 +--> CLIP-L
 |
 +--> T5-XXL
          |
          v
       Flux transformer
```

你只有：

```
CLIP-L
```

缺少：

```
T5-XXL
```

影响：

* 图像质量仍然可用
* 提示遵循能力变差
* 复杂描述效果更差

示例：

提示：

> "A red dragon flying above a medieval city, cinematic lighting, detailed scales"

没有 T5：

可能得到：

```
dragon + city
```

有 T5：

更可能得到：

```
red dragon
medieval architecture
lighting
scale details
composition
```

---

# 3. Flux 架构

```
flux:
depth = 19
depth_single_blocks = 38
guidance_embed = false
context_in_dim = 4096
hidden_size = 3072
num_heads = 24
```

这描述了变换器。

类似于 LLM：

```
Input tokens
    |
    v
Transformer blocks
    |
    v
latent image tokens
```

---

## hidden_size

```
hidden_size = 3072
```

相当于 LLM 的嵌入维度。

作为对比：

GPT-2 1.5B：

```
hidden=1600
```

Llama 7B：

```
hidden=4096
```

Flux：

```
3072
```

---

## 注意力头数

```
num_heads=24
```

每个头：

```
3072 / 24

=128 dimensions/head
```

与 LLM 模式相同。

---

## 深度

```
depth=19
depth_single_blocks=38
```

总变换器块数：

```
19 double blocks
+
38 single blocks
```

非常深的网络。

---

# 4. 内存分配

重要的一行：

```
total params memory size =
6784.08MB

VRAM 0.00MB
RAM 6784.08MB
```

含义：

```
GPU:
0 MB

CPU RAM:
6.8 GB
```

你的模型不在 GPU 上。

后端正在进行 CPU 推理。

架构：

```
CPU RAM
 |
 | weights
 |
Flux Q4 model
 |
CPU compute
 |
image
```

没有 CUDA 加速。

---

# 5. Flux FLOW 模式

```
running in Flux FLOW mode
```

FLUX 使用不同的扩散过程。

经典 Stable Diffusion：

```
noise
 |
UNet
 |
noise prediction
 |
many steps
 |
image
```

Flux：

```
noise
 |
Transformer
 |
flow matching
 |
few steps
 |
image
```

流匹配：

```
x(t)
=
(1-t)*noise + t*image
```

模型学习速度：

```
dx/dt
```

而不是噪声。

---

# 6. 图像生成

```
generate_image 1024x1024
```

分辨率：

```
1024 × 1024

= 1,048,576 pixels
```

---

# 7. Flux 调度器

```
image_seq_len=16384
steps=4
mu=3.230
```

有趣。

对于 Flux：

图像变成 token。

1024x1024：

潜在大小：

```
128x128
```

Flux 分块：

```
128*128
=
16384 tokens
```

所以：

```
image_seq_len=16384
```

是变换器的序列长度。

类似于 LLM：

```
text tokens:
8192 tokens

image tokens:
16384 tokens
```

---

# 8. Euler 采样

```
sampling using Euler method
```

数值 ODE 求解器。

流匹配：

模型预测：

```
velocity v(x,t)
```

Euler：

```
x_next =
x + step * v(x,t)
```

只有：

```
4 steps
```

因为：

```
FLUX.1-schnell
```

针对速度进行了优化。

---

# 9. 提示词 token 化

```
"a cyberpunk street at night, neon reflections"
```

CLIP BPE：

```
[
a</w>,
cyberpunk</w>,
street</w>,
at</w>,
night</w>,
,
neon</w>,
reflections</w>
]
```

CLIP 词汇表：

```
vocab size: 49408
```

这是 OpenAI CLIP tokenizer。

---

# 10. 加载 CLIP

```
loading 196/196 tensors

clip_l.safetensors

112.36MB/s
```

已加载：

```
235 MB RAM
```

时间：

```
2 seconds
```

---

# 11. 加载 Flux 变换器

```
loading 776/776 tensors

flux1-schnell-Q4_0.gguf
```

内存：

```
6389 MB
```

时间：

```
0.4 seconds
```

非常快，因为：

```
GGUF mmap + sequential read
```

---

# 12. 计算缓冲区

```
flux compute buffer size:
2361.25 MB
```

这是临时工作内存。

推理过程中：

```
weights:
6.4GB

+
activation:
2.3GB

+
VAE:
160MB

+
text:
235MB

----------------

~9GB RAM
```

---

# 整体架构

你的设置：

```
                 Prompt
                   |
                   v
              CLIP-L f16
              235MB RAM
                   |
                   |
                   v
        Flux Transformer Q4_0
        12B params
        6.4GB RAM
                   |
                   |
                   v
             VAE decoder
             160MB
                   |
                   v

              1024x1024 image
```

---

# 为什么这能在小型硬件上运行

因为：

原始模型：

```
FLUX.1-schnell BF16

~24GB VRAM
```

你的版本：

```
Q4_0

~6.4GB RAM
```

权衡：

|          | BF16       | Q4                |
| -------- | ---------- | ----------------- |
| 内存     | 巨大       | 小                |
| 速度     | 更快 GPU   | 更慢 CPU          |
| 质量     | 最佳       | 略低              |
| 硬件     | H100/4090  | 笔记本/服务器 CPU |

---

考虑到你的 RTX 4070（12GB），这个 Q4 模型实际上很合适。如果使用 CUDA ggml 后端，可能可以将以下部分移到 GPU：

```
Flux weights:
6.4GB

+
compute:
2.3GB

≈ 9GB VRAM
```

并为 VAE/CLIP 留出空间，因此如果你的构建启用了 CUDA，GPU 加速应该是可行的。
