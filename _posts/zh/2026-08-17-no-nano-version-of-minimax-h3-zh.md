---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniMax-H3 无纳米版本
translated: true
type: note
---

问题：是否存在一个开源的 **“nano”项目对应 MiniMax-H3**，类似于 `nanoGPT` / `nanochat`，可以让你研究和运行 **文本 + 图像的多模态训练/推理流程**？

答案：

**严格来说，还没有——至少目前没有。** 关键在于 **MiniMax-H3 本身更接近一个全模态的视频生成系统，而不是像 Qwen-VL 那样的多模态大语言模型**。

MiniMax 将 H3 描述为联合处理 **文本、图像、视频和音频**，其组件包括 **H3-VAE、H3-Omni Transformer、Contextual Omni Representation 和 In-Context Regeneration**。MiniMax 宣布计划发布模型权重，但并未看到官方提供类似 `nanoH3` 的极简训练实现。([MiniMax][1])

### 我认为你真正想要的是

你想要类似这样的东西：

```text
                 nanochat
                    │
          ┌─────────┴─────────┐
          │                   │
       text data          image/text data
          │                   │
       tokenizer          vision encoder
          │                   │
          └─────────┬─────────┘
                    ↓
             multimodal Transformer
                    ↓
              training loop
                    ↓
               inference
```

整个系统 **小到可以阅读和修改**，而不是试图理解一个拥有10万行代码的生产级仓库。

基于这个目的，我 **不建议从 H3 的实际实现入手**。

### 更适合学习的项目

我大致排序如下：

| 项目                      | 你学到什么                          | 类似 nano 的程度 |
| ------------------------- | ----------------------------------- | ---------------- |
| **nanochat**              | LLM 预训练 → SFT → RL → 推理        | ⭐⭐⭐⭐⭐           |
| **nanoGPT**               | 从头理解 Transformer                | ⭐⭐⭐⭐⭐           |
| **LLaVA**                 | 视觉编码器 → 投影器 → LLM           | ⭐⭐⭐              |
| **SmolVLM**               | 小巧实用的 VLM                      | ⭐⭐⭐⭐            |
| **Qwen2-VL / Qwen2.5-VL** | 现代 VLM 架构                       | ⭐⭐              |
| **MiniMax-H3**            | 全模态生成                         | ⭐                |
| **Open-Sora**             | 视频生成训练/推理                   | ⭐⭐              |

`nanochat` 仍然非常有用，因为它的整个理念正是你描述的那样：实现最小/可 hack 的代码，涵盖分词、预训练、微调、评估和推理。([GitHub][2])

### 如果你的真实目标是学习 H3

我建议你自己动手构建一个 **`nano-omni`**。

从 **图像 + 文本** 开始，而不是视频/音频：

```text
image
  │
  ▼
ViT / SigLIP
  │
  ▼
image tokens
  │
  ├──────────────┐
  │              │
text tokens   image tokens
  │              │
  └──────┬───────┘
         ▼
   Transformer
         │
         ▼
    text logits
```

然后训练目标基本就是：

```python
x = torch.cat([
    text_embedding,
    vision_projector(vision_encoder(image)),
], dim=1)

logits = model(x)

loss = cross_entropy(
    logits[:, :-1],
    labels[:, 1:]
)
```

这样你就能掌握 **多模态大语言模型的核心机制**，而不会陷入视频生成的复杂代码中。

然后逐步深入：

```text
nanoGPT
   ↓
nanochat
   ↓
nano-VLM
   ↓
nano-video
   ↓
nano-omni
   ↓
理解 H3
```

有趣的是，**H3 并非简单的“nanochat + 图像编码器”**。MiniMax 表示 H3 是一个统一的多模态表示与生成框架，横跨文本/图像/视频/音频，这是一个本质不同的东西。([MiniMax][1])

另外，要小心 GitHub 上声称是“MiniMax H3 开源”的结果。已经存在一些第三方 H3 API 封装，但那些是 **API 客户端，而非训练代码**。([GitHub][3])

如果你的具体目标是 **“我想从头实现一个 1–3B 的多模态模型，自己训练，并理解前向传播中的每一个张量”**，我建议你使用 **nanochat + 一个约 300 行的 ViT/投影器扩展**，而不是寻找一个不存在的 `nanoH3`。这将是一个很好的学习项目。

[1]: https://www.minimax.io/blog/minimax-h3?utm_source=chatgpt.com "MiniMax H3: An Open Model Breaking the Boundaries Between Tasks and Modalities - MiniMax Research | MiniMax"
[2]: https://github.com/karpathy/nanochat?utm_source=chatgpt.com "GitHub - karpathy/nanochat: The best ChatGPT that $100 can buy. · GitHub"
[3]: https://github.com/Anil-matcha/MiniMax-H3-API?utm_source=chatgpt.com "GitHub - Anil-matcha/MiniMax-H3-API: Python SDK for the MiniMax H3 API — text-to-video, image-to-video, and first/last-frame video generation via Muapi. · GitHub"
