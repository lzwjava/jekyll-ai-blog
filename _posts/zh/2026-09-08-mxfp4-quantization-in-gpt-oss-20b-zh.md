---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-OSS-20B 中的 MXFP4 量化
translated: true
type: note
---

**GPT-OSS-20B 中的 MXFP4 是什么意思？**

答案：**MXFP4 是 GPT-OSS 用于 MoE 权重的原生 4 位浮点量化格式。**

拆解这个名称：

* **M** = Microscaling / 块缩放格式
* **XF** = 微软的 **MX** 微缩放系列
* **P4** = **4 位浮点**值

重要的是，**它并非简单的“处处都是 FP4”。** MXFP4 使用：

```text
                 MXFP4 tensor
                      │
          ┌───────────┴───────────┐
          │                       │
     FP4 values              block scale
     4 bits each              shared scale
          │                       │
          └───────────┬───────────┘
                      ↓
             actual FP value
```

对于 GPT-OSS-20B，OpenAI 将 **MoE 线性投影权重** 量化为 MXFP4。其他主要张量——attention、embeddings 等——保持 **BF16**。（[GitHub][1]）

### 为什么需要块缩放？

假设你有 32 个权重：

```text
W = [0.02, -0.7, 1.2, -2.8, ...]
```

直接用 4 位来表示每个数字会带来极差的动态范围。

相反，MXFP4 大致这样做：

```text
                 shared scale
                     ↓
W[0:32] ────────> [FP4, FP4, FP4, ... FP4]
```

每个小块共享一个缩放因子。

概念上：

```python
# simplified, NOT the actual implementation

scale = max(abs(W_block)) / FP4_MAX

q = round(W_block / scale)
q = clamp(q, FP4_MIN, FP4_MAX)

# store:
#   q     -> 4-bit values
#   scale -> block scale
```

在 GEMM 过程中，内核实际上会重建：

```text
W ≈ FP4_values × block_scale
```

这就是为什么与朴素的 4 位量化相比，你能获得更好的数值表现。

### 为什么称为 4.25 位？

这是 GPT-OSS 的一个特别重要的细节。

OpenAI 将 MXFP4 报告为 **每个参数 4.25 位**，而不是正好 4 位，因为你还需要存储块缩放因子。（[OpenAI Deployment Safety Hub][2]）

对于 GPT-OSS：

```text
FP4 value        = 4 bits
scale overhead   ≈ 0.25 bits / parameter
────────────────────────────────────
effective         ≈ 4.25 bits / parameter
```

因此，20.9B 参数并不需要：

```text
20.9B × 4 bits
```

正好这么多。缩放元数据会增加一些开销。

这就是为什么已发布的 GPT-OSS-20B checkpoint 约为 **12.8 GiB**，而不是约 10.5 GB。（[OpenAI Deployment Safety Hub][2]）

### 这对 MoE 尤其有用

GPT-OSS-20B 实际上有：

```text
total parameters:       20.91B
active parameters:       3.61B
experts:                    32
experts selected/token:     4
```

因此，对于每个 token，router 只激活 4 个专家，但**专家权重仍然需要存在于内存中**。（[OpenAI CDN][3]）

MXFP4 使这些庞大的专家矩阵变得更小。

架构大致如下：

```text
                    token
                      │
                      ▼
                   Router
                      │
              select 4 / 32 experts
                 ┌────┼────┐
                 ▼    ▼    ▼
               E7    E13   E27 ...
                │     │     │
                │ MXFP4     │
                ▼     ▼     ▼
                 └────┼─────┘
                      │
                      ▼
                    output
```

这就是为什么 **GPT-OSS-20B 可以在约 16 GB 内存中运行**，尽管总参数约为 21B。OpenAI 特别指出，MoE 权重占参数数量的 90% 以上，并已量化为 MXFP4。（[OpenAI Deployment Safety Hub][2]）

### 有趣的 GPU/内核部分

这直接与你一直在问的 Triton 问题相关。

模型不一定会这样做：

```text
MXFP4 → BF16
       ↓
    BF16 GEMM
```

那样会浪费大部分内存带宽优势。

相反，专门的 **MXFP4 GEMM 内核** 可以直接消费打包的 FP4 权重和缩放因子。

OpenAI 大致将张量存储为：

```text
tensor.blocks
    ↓
packed FP4 values
(two FP4 values / uint8)

tensor.scales
    ↓
block scaling factors
```

并且支持 MXFP4 的内核直接在这种表示上进行操作。（[GitHub][1]）

所以你看到的栈大致是：

```text
GPT-OSS-20B
     │
     ├── Attention ───────── BF16
     │
     ├── Embeddings ──────── BF16
     │
     └── MoE
          │
          ├── Router ─────── BF16
          │
          └── Experts
                │
                └── MXFP4
                     │
                     ├── packed FP4
                     ├── block scales
                     │
                     ▼
               MXFP4 Triton/CUDA kernel
                     │
                     ▼
                    GEMM
```

**一句话总结：** MXFP4 是一种**块缩放 FP4 表示**，它让 GPT-OSS 能够以大约 **4.25 位/参数** 的规模存储其庞大的 MoE 专家权重，同时保留比朴素 FP4 更好的数值范围。

参考资料：

* [OpenAI GPT-OSS 模型卡](https://deploymentsafety.openai.com/gpt-oss/tacit-knowledge-and-troubleshooting?utm_source=chatgpt.com)
* [OpenAI GPT-OSS GitHub README](https://github.com/openai/gpt-oss/blob/main/README.md?utm_source=chatgpt.com)
* [Hugging Face MXFP4 文档](https://huggingface.co/docs/transformers/quantization/mxfp4?utm_source=chatgpt.com)

我还可以详细讲解**实际的 32 元素 MXFP4 编码（E2M1 + E8M0 缩放）以及 Triton 内核如何将其转化为矩阵乘法**，这是有趣的底层部分。

[1]: https://github.com/openai/gpt-oss/blob/main/README.md?utm_source=chatgpt.com "gpt-oss/README.md at main · openai/gpt-oss · GitHub"
[2]: https://deploymentsafety.openai.com/gpt-oss/tacit-knowledge-and-troubleshooting?utm_source=chatgpt.com "gpt-oss-120b & gpt-oss-20b Model Card - OpenAI Deployment Safety Hub"
[3]: https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf?utm_source=chatgpt.com "forward pass), and gpt-oss-20b with 24 layers (20.9B total and 3.6B active parameters). Table 1 shows a full breakdown of the parameter counts."