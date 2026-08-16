---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳开源文本到图像学习项目
translated: true
type: note
---

问题：**学习文本到图像生成（包括模型架构、训练和推理），有哪些最佳的开源项目？**

答案：

如果你的目标是 **“我想了解整个 T2I 技术栈，而不仅仅是使用 ComfyUI”**，我会建议按以下顺序学习：

### 1. Hugging Face Diffusers — 最佳综合入门项目

[Duffusers GitHub](https://github.com/huggingface/diffusers?utm_source=chatgpt.com)

这是最值得入手开始学习的项目，因为它几乎暴露了每一个组件：

```text
文本
 │
 ▼
分词器 / 文本编码器
 │
 ▼
文本嵌入
 │
 ├──────────────────┐
 ▼                  │
噪声潜变量         │
 │                  │
 ▼                  │
┌─────────────────┐ │
│ UNet / DiT      │◄┘
│ 以文本为条件    │
│ 进行控制        │
└─────────────────┘
 │
 ▼
调度器 / 去噪
 │
 ▼
VAE 解码器
 │
 ▼
图像
```

它同时包含了 **推理管道和实际的训练代码**，涵盖文本到图像、DreamBooth、LoRA、ControlNet 等。([Hugging Face][1])

例如，实际可以阅读：

```text
diffusers/
├── src/diffusers/
│   ├── models/
│   │   ├── unets/
│   │   ├── transformers/
│   │   ├── autoencoders/
│   │   └── ...
│   ├── schedulers/
│   └── pipelines/
└── examples/
    └── text_to_image/
        └── train_text_to_image.py
```

该训练示例特意设计得相当可读，它暴露出预处理和训练循环，而不是将所有内容隐藏在庞大的框架背后。([Hugging Face][1])

**对你来说，这可能是首选。**

---

### 2. Stable Diffusion — 学习原始的潜在扩散架构

[Stable Diffusion GitHub](https://github.com/CompVis/stable-diffusion?utm_source=chatgpt.com)

这可能是从 **“我理解 Transformer”** 过渡到 **“我理解 T2I”** 的最佳概念桥梁。

其重要理念是 Stable Diffusion 不直接在像素上操作：

```text
图像
  │
  ▼
 VAE 编码器
  │
  ▼
潜在变量 z
  │
  + 噪声
  │
  ▼
UNet(z, 文本嵌入, 时间步)
  │
  ▼
预测噪声
  │
  ▼
去噪迭代
  │
  ▼
潜在变量
  │
  ▼
VAE 解码器
  │
  ▼
图像
```

与当今 20B/30B+ 规模的 T2I 系统相比，原始的 Stable Diffusion 实现相对易于理解。

Hugging Face 的实现也记录了其架构：一个图像 VAE、CLIP 文本编码器、条件 UNet 和调度器。([Hugging Face][2])

---

### 3. FLUX — 学习现代 T2I Transformer 架构

[Black Forest Labs FLUX GitHub](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)

这是我会在 **学习 Stable Diffusion 之后** 研究的一个项目。

其中有趣的转变是：

```text
Stable Diffusion

文本 → CLIP
         │
         ▼
潜在变量 → UNet → 潜在变量
```

对比现代系统如 FLUX：

```text
文本嵌入
       │
       ▼
┌───────────────────┐
│ Transformer        │
│                   │
│ 图像 token        │
│       +           │
│ 文本 token        │
└───────────────────┘
       │
       ▼
   图像潜在变量
```

因此，如果你已经熟悉 GPT 风格的 Transformer，**FLUX 更接近你已有的思维模型**。

官方仓库包含了最简的本地推理代码，并支持不同的推理后端和精度，包括 BF16/FP8/FP4 TensorRT 路径。([GitHub][3])

我会特别研究：

```text
flux/
├── model.py
├── modules/
├── sampling.py
├── cli.py
└── ...
```

并追踪：

```python
提示词
  -> 文本编码器
  -> token 嵌入
  -> Transformer
  -> 流匹配 / 去噪
  -> VAE
  -> 图像
```

---

### 4. PixArt-α — 理解 DiT 的优秀项目

[PixArt-α GitHub](https://github.com/PixArt-alpha/PixArt-alpha?utm_source=chatgpt.com)

如果你的兴趣点是 **“如何构建一个类似 GPT 的 Transformer 来生成图像？”**，那么这个项目尤其适合。

其架构基本上是这样的：

```text
图像
 ↓
VAE
 ↓
潜在图块/token
 ↓
DiT Transformer
 ↑
文本条件
 ↓
预测噪声 / 速度
```

这是一个在你理解了原始 Stable Diffusion UNet 之后非常有用的阅读项目。

其概念发展路径变为：

```text
CNN/UNet 扩散
       ↓
   DiT
       ↓
现代多模态 Transformer
```

---

### 5. Sana — 学习高效的 T2I

[Sana GitHub](https://github.com/NVlabs/Sana?utm_source=chatgpt.com)

我会专门关注 Sana 的 **效率方面**。

它之所以有趣，是因为现代图像生成不仅仅是：

> “制造一个巨大的 Transformer。”

你还需要考虑：

```text
潜在空间压缩
+
高效注意力机制
+
高效文本编码器
+
扩散 / 流训练
+
知识蒸馏
+
量化
```

这更接近你可能喜欢的那种系统工程问题。

---

### 6. ComfyUI — 理解推理流程图的好工具

[ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI?utm_source=chatgpt.com)

我不建议从这里开始学习模型本身。

但对于理解一个真实的 T2I 推理管道是如何组装起来的，它非常有用：

```text
CLIP
  ↓
条件控制
  ↓
KSampler ← 调度器
  ↓
UNet / DiT
  ↓
潜在变量
  ↓
VAE
  ↓
图像
```

节点图使得 **模型的组成** 变得非常清晰。

---

## 我建议实际阅读的项目

基于你的背景，我会推荐：

| 顺序 | 项目                  | 你能学到什么                                      |
| ---- | --------------------- | ------------------------------------------------- |
| 1    | **Diffusers**         | 完整的生态系统 + 训练                             |
| 2    | **Stable Diffusion**  | 潜在扩散 + UNet + VAE                             |
| 3    | **PixArt-α**          | DiT / Transformer 图像生成                        |
| 4    | **FLUX**              | 现代多模态 Transformer + 流匹配                   |
| 5    | **Sana**              | 高效的现代 T2I                                    |
| 6    | **ComfyUI**           | 生产级推理组合                                    |

关键在于 **不要只是运行演示程序**。

---

## 你应该理解的训练代码

从 Diffusers 的文本到图像训练示例开始：

[Diffusers text-to-image training](https://huggingface.co/docs/diffusers/training/text2image?utm_source=chatgpt.com)

概念上，核心的训练循环出奇地简洁：

```python
# 图像 -> 潜在变量
z = vae.encode(image).latent_dist.sample()

# 随机时间步
t = torch.randint(0, T, (B,), device=device)

# 随机高斯噪声
eps = torch.randn_like(z)

# 正向扩散
z_t = scheduler.add_noise(z, eps, t)

# 文本 -> 嵌入
c = text_encoder(tokens)

# 预测噪声
eps_hat = unet(
    z_t,
    t,
    encoder_hidden_states=c,
).sample

# 扩散目标
loss = F.mse_loss(eps_hat, eps)

loss.backward()
optimizer.step()
```

这是我会建议你首先自己实现的内容。

官方的 Diffusers 文档明确暴露了这个训练管道，并说明代码旨在可以被适配，而不是被视为黑盒。([Hugging Face][1])

并且重要的是，**一块 24 GB 的 GPU 配合梯度检查点和混合精度，足以用于 SD 级别的文本到图像训练**，尽管更大/更快的训练需要更多的显存。([Hugging Face][4])

因此，你的 4070 级别机器实际上对于学习这个很有用——不仅仅是用于推理。

---

## 然后学习流匹配

这是我建议超越旧有 Stable Diffusion 思维模型的地方。

不要仅仅思考：

```text
x0 = 图像
xT = 噪声

x0 → x1 → x2 → ... → xT
```

并学习在离散时间步预测噪声，现代模型可以将生成过程表述为学习一个 **速度场**：

```text
x(t) = (1 - t) * x_数据 + t * x_噪声

vθ(x(t), t, 文本) ≈ dx(t)/dt
```

训练大致变成了：

```python
t = torch.rand(B, device=device)

x = (1 - t) * 图像潜在变量 + t * 噪声

目标速度 = 噪声 - 图像潜在变量

预测速度 = model(x, t, 文本)

loss = F.mse_loss(预测速度, 目标速度)
```

这个公式上的微小改变会将你引向 **FLUX 风格的现代图像生成**。

因此，我不会花几个月时间只学习旧的 DDPM 实现。而是学习：

```text
DDPM
 ↓
潜在扩散
 ↓
UNet
 ↓
DiT
 ↓
流匹配
 ↓
FLUX 风格的 T2I
```

在 2026 年，这会是更好的学习路径。

### 我推荐的小型项目

鉴于你已经从零训练过 GPT-2/nanoGPT，我建议你实际上自己构建一个小型的 **nano-diffusion**：

```text
nano-t2i/
├── tokenizer.py
├── text_encoder.py
├── vae.py
├── dit.py
├── flow_matching.py
├── train.py
└── sample.py
```

从极其微小的规模开始：

```text
64×64 图像
↓
8×8 潜在变量
↓
微小 DiT
↓
微小文本 Transformer
↓
1万–10万 图像/文本对
```

然后将你的实现与 Diffusers 进行对比。

这将比通过 UI 操作 Stable Diffusion 教会你多得多的东西。

[Diffusers training overview](https://huggingface.co/docs/diffusers/training/overview?utm_source=chatgpt.com) [Diffusers text-to-image guide](https://huggingface.co/docs/diffusers/v0.28.2/training/text2image?utm_source=chatgpt.com)

参考资料：

* [Hugging Face Diffusers](https://github.com/huggingface/diffusers?utm_source=chatgpt.com)
* [Stable Diffusion](https://github.com/CompVis/stable-diffusion?utm_source=chatgpt.com)
* [FLUX](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)
* [PixArt-α](https://github.com/PixArt-alpha/PixArt-alpha?utm_source=chatgpt.com)
* [Sana](https://github.com/NVlabs/Sana?utm_source=chatgpt.com)
* [ComfyUI](https://github.com/comfyanonymous/ComfyUI?utm_source=chatgpt.com)

[1]: https://huggingface.co/docs/diffusers/training/overview?utm_source=chatgpt.com "Overview · Hugging Face"
[2]: https://huggingface.co/docs/diffusers/en/api/pipelines/stable_diffusion/text2img?utm_source=chatgpt.com "Text-to-image · Hugging Face"
[3]: https://github.com/black-forest-labs/flux/blob/main/docs/text-to-image.md?utm_source=chatgpt.com "flux/docs/text-to-image.md at main · black-forest-labs/flux · GitHub"
[4]: https://huggingface.co/docs/diffusers/v0.28.2/training/text2image?utm_source=chatgpt.com "Text-to-image · Hugging Face"