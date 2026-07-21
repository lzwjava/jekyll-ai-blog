---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BFL：FLUX背后的实验室
translated: true
type: note
---

问题：黑森林实验室（BFL）简介——FLUX 模型背后的实验室

答案：

黑森林实验室（Black Forest Labs，简称 BFL）是一家专注于**视觉智能**的德国 AI 研究实验室——致力于构建能理解并生成图像（最终拓展到更广泛的视觉世界）的基础模型。其口号“赋能无处不在的视觉智能”所指向的目标，是超越简单的图像生成，迈向能感知、推理并创造视觉内容的系统。（[黑森林实验室][1]）

重要发展历程：

```
潜在扩散研究
        |
        v
Stable Diffusion (2022)
        |
        v
黑森林实验室 (2024)
        |
        v
FLUX.1 / FLUX.2 模型
```

创始团队来自最初的 Stable Diffusion 研究生态，包括 Robin Rombach、Andreas Blattmann 和 Patrick Esser 等研究人员。他们此前曾致力于潜在扩散模型的研究，这些模型成为了 Stable Diffusion 的基础。（[黑森林实验室][1]）

## 为何 BFL 至关重要

在 FLUX 出现之前，主要的开源图像生成玩家包括：

* Stable Diffusion / SDXL
* Midjourney
* DALL·E

BFL 于 2024 年携 FLUX.1 进入市场，并显著提升了图像生成质量，尤其是在以下方面：

* 提示词遵循
* 人体解剖结构
* 字体/文本渲染
* 复杂场景
* 照片级真实感

FLUX.1 模型采用 **12B 参数的混合扩散 Transformer 架构**，基于流匹配（flow matching）思想，而非较老的 U-Net 风格扩散流水线。（[黑森林实验室][2]）

高层架构：

```
文本提示
    |
    v
文本编码器
    |
    v
条件嵌入
    |
    v
扩散 Transformer (DiT)
    |
    v
潜在图像表示
    |
    v
VAE 解码器
    |
    v
生成图像
```

类似于 LLM 的演进：

```
GPT:
tokens -> Transformer -> next token

FLUX:
噪声潜在表示 -> Transformer -> 去噪潜在表示 -> 图像
```

核心思想同样是 Transformer 扩展，只不过模型预测的是图像潜在表示的去噪轨迹，而非预测 token。

---

## FLUX 模型家族

原始 FLUX.1：

| 模型              | 用途                                 |
| ----------------- | ------------------------------------ |
| FLUX.1 [pro]      | 最佳质量，API/商用                    |
| FLUX.1 [dev]      | 开源权重，研究/非商用                 |
| FLUX.1 [schnell]  | 快速本地推理                         |

（[黑森林实验室][2]）

对于本地 GPU 用户：

```
FLUX.1-schnell
    |
    +-- RTX 4090 / 3090 可行
    +-- 12GB VRAM 困难
    +-- 量化/卸载有帮助

FLUX.1-dev
    |
    +-- 重得多
    +-- 通常需要 24GB+ VRAM
```

你的 RTX 4070 12GB 可以通过优化运行 FLUX，但非常勉强。常用技巧：

```bash
--cpu-offload
--vae-cpu-offload
fp8 权重
量化 Transformer
```

---

## BFL vs OpenAI / Google / Midjourney

粗略对比：

| 公司                | 主要视觉 AI                          |
| ------------------- | ------------------------------------ |
| OpenAI              | DALL·E / GPT 视觉生态系统             |
| Google DeepMind     | Imagen, Gemini 视觉                   |
| Midjourney          | 封闭式创意图像模型                    |
| Stability AI        | Stable Diffusion                     |
| **黑森林实验室**    | **FLUX 视觉基础模型**                 |

BFL 的独特定位在于：

```
学术研究
       +
开放模型理念
       +
初创公司执行力
       =
FLUX 生态系统
```

他们在文化上更接近早期的 OpenAI 和早期的 Stability AI：发布强有力的研究，推出可用的模型，吸引开发者。（[黑森林实验室][2]）

---

## AI 工程师为何关注

对于 LLM 从业者来说，FLUX 之所以有趣，是因为它展示了相同的扩展趋势：

LLMs：

```
Transformer
+
更多参数
+
更多数据
+
更好的对齐
=
GPT 级别模型
```

视觉模型：

```
扩散 Transformer
+
更多图像/视频数据
+
更好的条件控制
+
更大的算力
=
视觉智能模型
```

BFL 的长期愿景不仅仅是“生成图片”：

```
图像生成
        |
        v
图像编辑
        |
        v
视频生成
        |
        v
世界理解
        |
        v
具身 AI / 机器人
```

他们将自身目标描述为构建视觉智能的基础设施，而不仅仅是创意工具。（[黑森林实验室][1]）

---

参考文献：

* 黑森林实验室 — 关于 ([黑森林实验室][1])
* 宣布黑森林实验室 / FLUX.1 发布 ([黑森林实验室][2])
* 黑森林实验室 B 轮融资公告 ([黑森林实验室][3])
* FLUX 模型概述 ([docs.bfl.ml][4])

[1]: https://bfl.ai/about?utm_source=chatgpt.com "关于 | 黑森林实验室"
[2]: https://bfl.ai/blog/24-08-01-bfl?utm_source=chatgpt.com "宣布黑森林实验室 | 黑森林实验室"
[3]: https://bfl.ai/blog/our-300m-series-b?utm_source=chatgpt.com "为视觉智能奠定基础——我们的 3 亿美元 B 轮融资 | 黑森林实验室"
[4]: https://docs.bfl.ml/?trk=public_post_main-feed-card-text&utm_source=chatgpt.com "欢迎来到 BFL 文档！ - 黑森林实验室"