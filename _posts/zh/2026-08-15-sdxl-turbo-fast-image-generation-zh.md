---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SDXL Turbo 快速图像生成
translated: true
type: note
---

问题：`sdxlturbo_example` 图像模型简介

答案：

`sdxlturbo_example` 通常指基于 **SDXL Turbo** 构建的示例，SDXL Turbo 是 Stability AI 发布的快速文本到图像扩散模型。它演示了如何运行 **SDXL Turbo 推理**，通常使用 Hugging Face Diffusers 库。

![Image](https://images.openai.com/static-rsc-4/CPDeoZigLPBXgghVzfTpsGt-XPNYy1dB678aDgvGoLnzkCdDWxLl84qSp_4T8ditNXcv0VBrTfaX6bdG3zWTyNrwLWO-cYGo_jgUwMFBqCZyRd1HgAkW88rIkNiFoiNJ-SHjnM9F3P54XAec7havHwpt5GsSrDoeNiIyVjwntT6pSLVCLojRMwIU_svnuPeu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/n0x65uRCxGKioCrsygs90DxHmRH6uYxdM_jvDjsYPoqWC1nMpJWuL-yS24KI4Bi44b7ppeIjErRO3tSXX765gPJBG9yszeQMN-sYsAFh5T-gVPNmJwxEpgrtZAN9S6vTRoXTU7nlz4uQHbyTZ9J_cgcn3wcGOi1bCwxAhLzKqVUzaOpZS8onFFJC-mT-fBJE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WRokY3KVg07yjnT6ujOP-6CeGK5U61vayqbvsXfl2NfNq7rTENK9EU7wQKRTZE6IXMCLGQteW7eJV6ItAXdTz3eVP5rcOqgrWrh-dxry0bL8IBczjxFpGBbcXWprbwL0M_Jut66bKPWKgY7glilkRbLw4WxrGgHWVDy4kU4m2jLcsu2SFz5-ray4mb3FcTdU?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MgEhKftEFSaWebu0ORgwDcJXw0_dqXCUJ63i1UPVyXeCzxDFgkkTDjt7kbtafy0UUWklQ7-KlAQ8ei2C256urNaTjm4bimlu9wXIGfeb8SWyIzbBo02n-OyejlZmXYpWw6I9NeJYNf6XBS2okB4AnHfRWfNFIoq0-pDRKz9N7AmlJPEu9NNWo323s7VmxMF_?purpose=fullsize)

## SDXL Turbo 是什么？

SDXL Turbo 是一种**针对实时生成优化的文本到图像扩散模型**。

普通 Stable Diffusion：

```
噪声
  |
  |  20-50 步去噪
  v
图像
```

SDXL Turbo：

```
噪声
  |
  |  1-4 步去噪
  v
图像
```

关键技术是**对抗性扩散蒸馏 (ADD)**。

SDXL Turbo 不是训练模型逐步进行多步去噪，而是将大型扩散模型的知识蒸馏成一个更小的模型，该模型能够在极少步数内生成优质图像。

---

## 模型架构

SDXL Turbo 基于 SDXL：

```
文本提示
    |
    v
CLIP 文本编码器
    |
    v
条件嵌入
    |
    v
UNet / 类扩散 Transformer 去噪器
    |
    v
VAE 解码器
    |
    v
图像
```

主要组件：

* **文本编码器**

  * 基于 CLIP
  * 将提示转换为嵌入

* **UNet**

  * 预测去噪方向

* **VAE**

  * 潜在空间 ↔ 像素

模型不直接生成像素：

```
1024x1024 图像

        |
        v

潜在张量

4 x 128 x 128

        |
        v

UNet 在此处操作
```

---

## 示例代码

典型的 Diffusers 用法：

```python
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
)

pipe.to("cuda")

prompt = "a cyberpunk city at night, cinematic lighting"

image = pipe(
    prompt=prompt,
    num_inference_steps=1,
    guidance_scale=0.0
).images[0]

image.save("output.png")
```

重要参数：

```python
num_inference_steps=1
```

SDXL Turbo 可以在 1 步中工作。

```
步数：
1   最快
2-4 更好质量
20+ 不必要
```

---

## 硬件要求

大致范围：

| GPU              | 体验                          |
| ---------------- | ----------------------------- |
| RTX 4090 24GB    | 极佳                          |
| RTX 3090 24GB    | 良好                          |
| RTX 4070 Ti 12GB | 可通过优化实现                |
| RTX 4060 8GB     | 困难                          |
| Apple M 系列     | 可行但较慢                    |

内存：

* FP16：推理时约 6-8GB VRAM
* 更高分辨率需要更多

您的 RTX 4070 Ti 12GB 可以轻松运行 SDXL Turbo。

---

## 与其他图像模型比较

| 模型                | 质量     | 速度          | 用途                    |
| ------------------- | -------- | ------------- | ----------------------- |
| SDXL                | 更高     | 慢            | 通用生成                |
| SDXL Turbo          | 良好     | 极快          | 交互式生成              |
| Stable Diffusion 1.5 | 较低     | 快            | 旧生态系统              |
| FLUX.1              | 非常高   | 更慢          | 前沿质量                |
| Midjourney          | 高       | 仅 API        | 消费产品                |

SDXL Turbo 不是最高质量的模型。它的优势在于延迟。

---

## 为何在技术上重要

SDXL Turbo 是**模型压缩/蒸馏**的一个例子：

教师模型：

```
大型扩散模型

50 步
10B+ 计算单元

        |
        | 蒸馏
        v

学生模型：

SDXL Turbo

1 步
成本低得多
```

这一理念在现代 AI 中无处不在：

* LLM 蒸馏
* 推理模型压缩
* 扩散加速
* 移动 AI 部署

权衡：

```
更少计算
     |
     v
采样灵活性降低
     |
     v
质量略微下降
```

---

参考资料：

* [SDXL Turbo 模型卡](https://huggingface.co/stabilityai/sdxl-turbo?utm_source=chatgpt.com)
* [Diffusers SDXL Turbo 文档](https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl_turbo?utm_source=chatgpt.com)
* [对抗性扩散蒸馏论文](https://arxiv.org/abs/2311.17042?utm_source=chatgpt.com)
