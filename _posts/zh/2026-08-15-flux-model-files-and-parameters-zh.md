---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX模型文件与参数
translated: true
type: note
---

问题：`FLUX` 模型文件和 `sd-cli` 参数的含义是什么？有哪些可选参数？

回答：

在你的命令中，**FLUX 并不是单一的一个模型文件**，而是由多个神经网络组件组成的流水线：

```text
                    prompt
                      │
          ┌───────────┴───────────┐
          │                       │
       CLIP-L                  T5-XXL
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
               FLUX Transformer
                flux1-schnell
                      │
                      ▼
                    VAE
                      │
                      ▼
                 PNG image
```

### 1. `flux1-schnell-Q4_0.gguf`

```bash
--model flux1-schnell-Q4_0.gguf
```

这是**主要的 FLUX transformer**。

对于 FLUX.1：

* `flux1-schnell` = FLUX.1 Schnell
* `schnell` 意为**快速**
* 它被设计为使用极少的采样步数，通常为 **1–4 步**
* `Q4_0` = 4 位量化
* `.gguf` = GGUF 模型格式，常用于 `llama.cpp` 风格的 C/C++ 推理项目，包括 `stable-diffusion.cpp`

从概念上讲，这是最大/最重要的部分：

```text
text conditioning
       ↓
FLUX Transformer
       ↓
latent representation
```

Transformer 预测噪声潜变量应如何向最终图像转换。

与 FP16 相比，`Q4_0` 大幅减少了内存占用：

```text
FP16:
  ~16 bits / weight

Q8:
  ~8 bits / weight

Q4:
  ~4 bits / weight
```

代价是部分质量/精度损失。

---

### 2. `ae.safetensors`

```bash
--vae ae.safetensors
```

这是 **VAE / Autoencoder**。

对于 FLUX，`ae.safetensors` 本质上是负责在以下两者之间转换的组件：

```text
image ↔ latent
```

在生成过程中：

```text
FLUX transformer
       ↓
latent
       ↓
VAE decoder
       ↓
RGB image
```

因此，VAE **并不生成图像的语义内容**。

Transformer 决定诸如：

> cat + astronaut + rocket

而 VAE 将生成的潜变量表示转换为实际像素。

---

### 3. `clip_l.safetensors`

```bash
--clip_l clip_l.safetensors
```

这是 **CLIP-L**，即 CLIP 文本编码器。

你的 prompt：

```text
"a cat astronaut riding a rocket"
```

会被文本编码器转换为数值表示。

CLIP-L 是原始 FLUX 使用的两个文本条件系统之一。

大致过程如下：

```text
"a cat astronaut riding a rocket"
             ↓
          CLIP-L
             ↓
      text embeddings
```

---

### 4. `t5xxl_fp16.safetensors`

```bash
--t5xxl t5xxl_fp16.safetensors
```

这是第二个文本编码器：

**T5-XXL**。

FLUX 同时使用了这两者：

```text
                 prompt
                   │
          ┌────────┴────────┐
          ↓                 ↓
       CLIP-L             T5-XXL
          │                 │
          └────────┬────────┘
                   ↓
             FLUX Transformer
```

这是 FLUX 的一个重要设计选择。

T5-XXL 是一个非常庞大的语言模型/文本编码器，使 FLUX 获得比仅使用 CLIP 丰富得多的文本条件。

注意：

```text
t5xxl_fp16
```

是 **FP16**，未量化。

因此，尽管你的主 FLUX 模型是：

```text
Q4_0
```

你仍然加载了一个可能很大的 T5-XXL 模型。

如果你担心显存/内存，**T5-XXL 可能是内存占用的重要部分**。

---

# 你的生成参数

### `--cfg-scale 1.0`

```bash
--cfg-scale 1.0
```

CFG = **Classifier-Free Guidance**（无分类器引导）。

传统扩散模型通常使用类似：

```text
CFG = 5
CFG = 7
CFG = 7.5
```

更高的 CFG 通常会使图像更强烈地偏向 prompt，但可能导致伪影/过度处理。

对于 **FLUX.1 Schnell**，`1.0` 是正常的，因为 Schnell 是围绕不同的引导公式/低步数生成而设计的。

因此：

```bash
--cfg-scale 1.0
```

并不等同于“弱 prompt”。

对于这个 Schnell 设置，它是合适的。

---

### `--steps 4`

```bash
--steps 4
```

这是扩散/流积分步数。

对于 Schnell：

```text
1 step  → 极快
2 steps → 快
4 steps → 常见
```

与旧版 Stable Diffusion 进行概念对比：

```text
SD 1.5:
20–50 steps

SDXL:
20–50 steps

FLUX.1 Schnell:
~1–4 steps
```

这是 Schnell 引人注目的主要原因之一。

---

### `--width 768 --height 768`

```bash
--width 768
--height 768
```

输出分辨率：

```text
768 × 768
```

像素数：

```text
768 × 768 = 589,824 pixels
```

提高分辨率大致会随潜变量 token 数量增加计算/内存开销。

例如：

```text
768²  =   589K pixels
1024² = 1.05M pixels
```

因此 1024×1024 的像素数大约是：

```text
1.05M / 0.59M ≈ 1.78×
```

---

### `--output flux_out.png`

仅仅是输出文件名：

```bash
--output flux_out.png
```

---

### `--prompt`

```bash
--prompt "a cat astronaut riding a rocket"
```

你的文本条件。

---

# 重要的区别

将你的文件视为：

| 文件                                  | 角色                                    |
| ------------------------------------- | --------------------------------------- |
| `flux1-schnell-Q4_0.gguf`             | **主要图像生成 transformer**            |
| `t5xxl_fp16.safetensors`              | **大型文本编码器**                      |
| `clip_l.safetensors`                  | **CLIP 文本编码器**                     |
| `ae.safetensors`                      | **VAE / 图像 ↔ 潜变量转换**             |

因此，如果你删除 VAE：

```text
transformer → latent → ??? 
```

你无法将潜变量解码为图像。

如果你删除 T5：

```text
prompt → incomplete conditioning
```

FLUX 将无法在预期的配置下工作。

---

# "Schnell" 与 "Dev" 的含义

如果你正在试验 FLUX，这可能是最有用的区别。

### FLUX.1 Schnell

```text
FLUX.1-schnell
      ↓
few steps
      ↓
very fast generation
```

适用于：

* 本地推理
* 交互式应用
* 智能体
* 对延迟敏感的图像生成

### FLUX.1 Dev

```text
FLUX.1-dev
      ↓
more computation
      ↓
generally better quality / adherence
```

它通常需要比 Schnell 多得多的计算量。

因此，你当前的设置：

```bash
flux1-schnell-Q4_0.gguf
--steps 4
```

基本上优化为：

> **“在相对有限的硬件上，以极快速度生成一张不错的 FLUX 图像。”**

---

# 其他有用的 `sd-cli` 选项

具体选项取决于 `stable-diffusion.cpp` 的版本/构建，请直接检查你的二进制文件：

```bash
/mnt/data/zz/flux/sd_cpp/build/bin/sd-cli --help
```

常见控制选项包括：

```bash
--seed
--steps
--cfg-scale
--width
--height
--output
--prompt
```

为了可复现性：

```bash
--seed 12345
```

然后，相同的模型 + prompt + 参数应产生相同/相似的结果。

例如：

```bash
sd-cli \
  --model flux1-schnell-Q4_0.gguf \
  --vae ae.safetensors \
  --clip_l clip_l.safetensors \
  --t5xxl t5xxl_fp16.safetensors \
  --steps 4 \
  --cfg-scale 1.0 \
  --width 768 \
  --height 768 \
  --seed 42 \
  --output cat.png \
  --prompt "a cat astronaut riding a rocket"
```

**接下来最值得检查的是内存架构**：每个组件（`FLUX Q4`、`T5-XXL`、`CLIP-L`、`VAE`）消耗多少 RAM/VRAM，以及 `stable-diffusion.cpp` 将哪些组件放在 GPU 上、哪些放在 CPU 上。这解释了为什么量化后的 FLUX 模型可以在 12–16 GB 的 GPU 上运行，同时仍需要大量系统内存。