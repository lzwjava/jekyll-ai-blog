---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Stability AI图像模型介绍
translated: true
type: note
---

问题：Stability AI 图像模型简介

答案：

![Image](https://images.openai.com/static-rsc-4/tQ-e95Wvn-WA5b4l91HYdrn_blXKteFffX7HGDkn00jJRb5eAWoS6AllKK2256hmyGX3-ASq2pJER6DwsXbfAZYHjxuCjG7oX_ZmpiPO4WKbc_YayIeX1fKqW3S_51B0a2oru5f0oHPNtRF9xVBvzv_wdKBvcVjKQZxtNELMuzndkZf94SH492TEg-usdcF3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pDNn1-0rRuClKspbkb0_12iqyVgFJPXjmzNp_0e7vodSKnAVIrQovmvK2gQk-vPlRhhzv3i03I816dn-7Dpd7O1WAHiXf_A-4nmHHJslXQCFIN9bMpn5W_pog1MObWUymWNk0k53iVxs8Lc9cOaWma0JliWKlj-rm3L3XHSimDITPRZBnIvUUEHA0EakhwYr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DSuXA7xXXlXiYahmYRyH0VJjC47wBXFJojPYOrt7MyL1yDlv__8jsf15xmOXVPiFv2iIJmo_X_aYx0IflmsU4ipGDaorIg5hGro12YRqKlrooxEpEb6hhtEcyfTKKxkbRKr3ctbh4JExldZVhYR66Ka10WeTc5HZ63N47UuFpXEh6F-zQ9ZjNqU8JkSRb2Ut?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Dzp2HlIHgUnOF9bwYH4yFve0ExE_Kx9LOQUwNPvzCtomjWI_YjHxIqsUmH3gQ7519I9P-rZxgijDXHudIDT9aey5CrESxoCrV0QYBNm692156TZ-qhs4vu7U7R7NiPzZ1BKTDdMGhS60okaugXL8BvGEgXtgd1qIBxTbX_BMmGbSmF8Zqf_UvmYVQm0_3l60?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/uOevt2wXn6acXlqWDYoYXnzJN37riFWAnJFgx6JIG2ydfHGd1ijaAF6oIqghwKMRFVi1rro05MRf5B63TChK3uItJ66JeA3b0LH220fhnYtFdYzme8jXhfCOCD65jWuMBxtu0So0CxgpbaokH-m9YS6HXWYTlMpoq2mRCZ8RKOeWeQMcROsMMIScxX63IRXo?purpose=fullsize)

**Stability AI** 是开放生成式图像模型领域最具影响力的公司之一。其旗舰技术是 **Stable Diffusion**，它使高质量 text-to-image 生成得以面向研究者、开发者和本地用户。

核心思想：

> Stable Diffusion 并非直接生成像素，而是学习从压缩的图像表示中去除噪声。

数学上：

```
random noise z_T
      |
      v
 U-Net / DiT denoiser
      |
      v
clean latent image z_0
      |
      v
VAE decoder
      |
      v
RGB image
```

---

## 1. 历史

### Stable Diffusion 之前

早期的图像生成：

* GANs (2014-2020)

  * StyleGAN
  * BigGAN

问题：

* 训练困难
* 控制有限
* mode collapse

随后，diffusion models 出现了。

重要论文：

* Denoising Diffusion Probabilistic Models
* High-Resolution Image Synthesis with Latent Diffusion Models

Latent diffusion 是重大突破。

---

## 2. Stable Diffusion（2022）

原始模型：

Stability AI 发布了：

* Stable Diffusion 1.0
* Stable Diffusion 1.5

架构：

```
Text prompt
    |
CLIP text encoder
    |
text embedding
    |
    v
+----------------+
| U-Net          |
| diffusion      |
| model          |
+----------------+
    |
latent image
    |
VAE decoder
    |
image
```

示例：

提示词：

```
a robot walking in Tokyo at night,
cinematic lighting
```

模型执行以下步骤：

```
noise image

step 1:
noise -> slightly recognizable shapes

step 20:
objects appear

step 50:
details appear
```

---

## 3. 为什么 Stable Diffusion 改变了世界

之前：

```
AI image generation
=
big company API only
```

Stable Diffusion 之后：

```
AI image generation
=
download model
+
run locally
+
fine tune yourself
```

这催生了：

* ComfyUI ecosystem
* LoRA fine-tuning
* DreamBooth
* ControlNet
* 成千上万个社区模型

---

## 4. 主要的 Stability 模型

### Stable Diffusion 1.x

参数量：

~860M

优势：

* 轻量
* 庞大的生态系统
* 可在消费级 GPU 上运行

示例：

RTX 3060/4060：

```
512x512 generation
possible
```

---

### Stable Diffusion XL (SDXL)

2023 年发布。

规模大得多：

```
SD 1.5:
~860M params

SDXL:
~3.5B params
```

改进：

* 更好的构图
* 更好的文字排版
* 更高分辨率
* 更准确的人体结构

流程：

```
Prompt
 |
Dual CLIP encoders
 |
Base diffusion model
 |
Refiner model
 |
VAE
 |
Image
```

---

### SDXL Turbo

一项重大优化。

常规 diffusion：

```
50 steps
```

Turbo：

```
1-4 steps
```

使用：

* Adversarial Diffusion Distillation (ADD)

权衡：

```
speed ↑↑↑
quality slightly ↓
```

适用于：

* 实时应用
* 交互式生成

---

### Stable Diffusion 3 / 3.5

新一代模型。

架构正转向：

```
U-Net
  |
  v
Transformer diffusion (DiT style)
```

与以下方向类似：

* OpenAI Sora
* FLUX
* Imagen

特性：

* 更强的文本理解
* 更好的提示词遵循能力
* 改进的文字排版

---

## 5. 训练原理

简化说明：

取一张图像：

x0 = real image

添加噪声：

x_t = sqrt(alpha)*x0 + sqrt(1-alpha)*epsilon

其中：

epsilon = random Gaussian noise

训练模型：

输入：

(noisy image, timestep, text)

预测：

noise epsilon

损失：

L = ||epsilon - epsilon_theta(x_t,t,c)||^2

模型学习的是：

“给定带噪声的图像和文本，我应该去除什么噪声？”

---

## 6. 生态系统

最大的影响不仅仅在于基础模型。

### ComfyUI

基于节点的工作流：

```
Checkpoint
    |
CLIP
    |
Sampler
    |
ControlNet
    |
LoRA
    |
VAE
    |
Output
```

它成为了图像生成领域的“Linux 终端”。

---

### LoRA

小型适配器：

基础模型：

```
3.5B parameters
```

LoRA：

```
10MB-200MB
```

训练：

* 新风格
* 新角色
* 新产品

而无需完整微调。

---

### ControlNet

增加控制：

输入：

* 边缘图
* 姿态
* 深度
* 草图

输出：

相同构图，但风格为生成风格。

---

## 7. 与其他图像模型的比较

| 模型             | 公司                | 优势                     |
| ---------------- | ------------------- | ------------------------ |
| Stable Diffusion | Stability AI        | 开放生态系统             |
| SDXL             | Stability AI        | 质量 + 社区              |
| SD3.5            | Stability AI        | 更好的理解能力           |
| FLUX             | Black Forest Labs   | 非常高的质量             |
| Midjourney       | Midjourney          | 艺术质量                 |
| Imagen           | Google              | 照片级真实感             |
| DALL-E           | OpenAI              | 指令遵循能力             |

---

## 8. 为什么工程师喜欢 Stable Diffusion

对于 AI 工程师：

它类似于 Linux。

封闭模型：

```
call API
```

Stable Diffusion：

```
download checkpoint
inspect architecture
modify scheduler
train LoRA
build pipeline
deploy locally
```

你可以实验：

* attention
* VAE
* samplers
* quantization
* distillation
* inference optimization

---

## 9. 当前趋势

该领域正在演进：

```
GAN
 |
v
Diffusion U-Net
 |
v
Latent Diffusion
 |
v
Diffusion Transformer (DiT)
 |
v
Multimodal foundation models
```

Stable Diffusion 标志着图像生成成为开放工程生态系统的转折点。

对于已经在使用 LLM 的人来说，一个有趣的关联是：

```
LLM:
token space -> transformer -> next token

Image diffusion:
latent space -> transformer/U-Net -> denoise step
```

两者都是大规模表示学习系统；只是预测目标不同。

参考链接：

* [Stable Diffusion paper (Latent Diffusion Models)](https://arxiv.org/abs/2112.10752?utm_source=chatgpt.com)
* [Stable Diffusion 3 paper](https://arxiv.org/abs/2403.03206?utm_source=chatgpt.com)
* [Stability AI official site](https://stability.ai?utm_source=chatgpt.com)
* [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI?utm_source=chatgpt.com)