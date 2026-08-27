---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GLM-5.3-Flash：320B MoE，18B活跃参数
translated: true
type: note
---

## 问题：zai-org/GLM-5.3-Flash 介绍

## 回答：

Z.ai 的 **GLM-5.3-Flash** 是 GLM-5 系列中的新一代 **Mixture-of-Experts (MoE) 多模态大语言模型**。其核心理念是：

> **总参数量 320B，仅约 18B 激活参数 → 前沿能力，推理成本大幅降低。**（[Hugging Face][1]）

可以将其视为 GPT-5 类推理模型、Claude Opus 类编码模型等的中国对标产品，但在高效服务方面进行了深度优化。

---

## 1. 架构

重要的架构变化：

### 1. MoE 稀疏激活

传统方式：

```
Transformer layer

all 100B+ parameters participate
          ↓
huge compute cost
```

GLM-5.3-Flash：

```
320B parameters stored

token
 |
router
 |
 +--> expert A  \
 +--> expert B   ---> only ~18B activated
 +--> expert C  /
```

因此：

* memory requirement ≈ full model size
* compute requirement ≈ 18B model

这与以下模型的方向一致：

* Mixtral
* DeepSeek-V3
* Qwen MoE models

---

### 2. 混合注意力

论文/模型卡中提到了一种混合架构：

* sparse attention
* linear attention

问题：

标准 Transformer 注意力：

$$
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
$$

复杂度：

$$
O(n^2)
$$

其中 `n` 为上下文长度。

在 10 万以上 token 时，KV 缓存变得巨大。

GLM-5.3-Flash 尝试结合：

```
short-range precise attention
+
long-range efficient linear attention
```

以降低长上下文服务成本。（[Hugging Face][1]）

---

### 3. mHC（流形约束超连接）

另一个有趣的部分。

标准残差：

```
x
 |
Layer
 |
x + Layer(x)
```

mHC 改变了残差路径，允许更丰富的信息路由，同时保持训练稳定。

直观理解：

不再是单条高速公路：

```
hidden state
     |
     v
  transformer
     |
     v
 hidden state
```

而是有多条可学习的通信路径。

这类似于提问：

“我们能否在避免巨大 Transformer 优化问题的前提下扩展深度？”

---

## 2. 多模态

GLM-5.3-Flash 是首个设计为**原生多模态**的 GLM-5 系列模型。它可以处理：

* text
* images
* reasoning tasks
* coding tasks
* agents

Hugging Face 实现通过 `AutoProcessor` 支持图像-文本输入和多模态生成。（[Hugging Face][2]）

---

## 3. 模型大小

Hugging Face 列出：

```
GLM-5.3-Flash

~321B parameters
FP8 weights
MIT license
Chinese + English
```

（[Hugging Face][3]）

内存估算：

### BF16：

$$
321B \times 2 bytes
$$

≈

```
642 GB VRAM
```

未计算 KV 缓存。

### FP8：

$$
321B \times 1 byte
$$

≈

```
321 GB VRAM
```

因此实际部署：

```
4x H100 80GB
8x A100 80GB
MI300X cluster
```

或激进的量化/卸载。

---

## 4. 为什么叫“Flash”？

并不仅仅因为 Flash Attention。

其理念：

```
big model
+
small active compute
+
optimized attention
+
cheap serving
```

类似于：

```
DeepSeek-V3:
671B total
37B active

GLM-5.3-Flash:
320B total
18B active
```

目标：

> “以极低的推理成本获得接近前沿的智能。”

---

## 5. 本地运行

使用 vLLM 的示例：

```bash
pip install vllm

vllm serve zai-org/GLM-5.3-Flash
```

它暴露了兼容 OpenAI 的 API：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

response = client.chat.completions.create(
    model="zai-org/GLM-5.3-Flash",
    messages=[
        {
          "role":"user",
          "content":"Explain CUDA kernel optimization"
        }
    ]
)

print(response.choices[0].message.content)
```

（[Hugging Face][2]）

---

## 6. 针对你的硬件实验

鉴于你的配置：

* RTX 4070 12GB
* 本地 Qwen/vLLM 实验
* GPT-2 训练
* 对分布式推理感兴趣

这个模型很有趣，因为它展示了未来的方向：

```
Old scaling:

bigger dense model
       |
       v
more GPUs


New scaling:

huge sparse model
       |
       +--> MoE
       +--> quantization
       +--> offload
       +--> smarter attention
```

瓶颈从：

> “我们能训练更大的模型吗？”

转变为：

> “我们能高效地路由、缓存、压缩和服务一个巨大模型吗？”

这与你之前的实验直接相关：

* multi-GPU
* offload
* KV cache
* local inference
* GPU hardware repair

因为未来的 AI 基础设施越来越依赖于**系统工程**，而不仅仅是模型架构。

---

参考：

* [GLM-5.3-Flash on Hugging Face](https://huggingface.co/zai-org/GLM-5.3-Flash?utm_source=chatgpt.com)
* [GLM-5.3-Flash README](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/README.md?utm_source=chatgpt.com)
* [GLM-5.3-Flash-BF16 model card](https://huggingface.co/zai-org/GLM-5.3-Flash-BF16?utm_source=chatgpt.com)

[1]: https://huggingface.co/zai-org/GLM-5.3-Flash-BF16?utm_source=chatgpt.com "zai-org/GLM-5.3-Flash-BF16 · Hugging Face"
[2]: https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/README.md?utm_source=chatgpt.com "README.md · zai-org/GLM-5.3-Flash at main"
[3]: https://huggingface.co/zai-org/GLM-5.3-Flash?utm_source=chatgpt.com "zai-org/GLM-5.3-Flash · Hugging Face"