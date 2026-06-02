---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 压缩稀疏注意力深入探讨
translated: true
type: note
---

**问题：** 深入探讨 DeepSeek-V4 中的压缩稀疏注意力（CSA）——它如何从基本原理工作，包括压缩器、闪电索引器，以及它与 V3.2 中前代稀疏注意力的比较？

**回答：**

## CSA：DeepSeek-V4 中的压缩稀疏注意力

让我从底层开始构建——从标准注意力为何在 100 万 token 时失效，到 CSA 的每个组件，再到其成本与收益。

---

### 为什么标准注意力无法扩展到 100 万 token

标准多头注意力有两个扩展问题：

1. **计算量**：每层 `O(N²·d)`——在 100 万 token 时，每次前向传播每层需要 `10¹²` 次操作。
2. **KV 缓存内存**：每层存储 `K ∈ ℝ^{N×d_k}` 和 `V ∈ ℝ^{N×d_v}`。在 100 万 token、61 层、bf16 精度下，这需要数百 GB。

在推理时，每个新 token 都需要关注整个 `N` 长度的 KV 缓存。对于长上下文智能体而言，KV 缓存是瓶颈，而非计算量。

先前的答案是**稀疏注意力**（V3.2 的 DeepSeek 稀疏注意力）：不关注所有 `N` 个位置，只关注 top-k 选中的位置。但进行选择的索引器仍然需要对所有 `N` 个 KV 条目进行评分——只是为了决定跳过哪些。选择本身是 `O(N)` 的。

CSA 的核心见解：**先压缩，再稀疏化**。索引器的搜索空间在运行前缩小了 4 倍。

---

### CSA 的三个组件

#### 1. 压缩器（4 倍序列池化）

每 4 个连续的 token 位置被折叠成一个压缩后的 KV 条目：

```
[t₁, t₂, t₃, t₄] → 一个压缩的 KV 块
```

压缩方式是**带有 softmax 门控的池化，并加入学习到的位置偏置**。具体来说，对于一个包含 4 个隐藏状态 `H ∈ ℝ^{4×d}` 的块：

```python
# 学习到的每个位置偏置（所有块共享，仅编码块内位置）
pos_bias = learned_param  # 形状: (4,)

# 通过对 4 个位置进行 softmax 得到门控权重
gates = softmax(pos_bias)  # 形状: (4,)

# 加权求和 = 一个压缩表示
compressed = einsum('p, p d -> d', gates, H)  # 形状: (d,)
```

这是一种**可训练的池化操作**——既不是平均池化，也不是最大池化。模型会学习 4-token 窗口内哪些位置对压缩包含最重要的信息。位置偏置很轻量（仅 4 个标量），但因为是共享的，所以能够泛化。

经过这一步，你的 KV 缓存条目数从 `N` 变为 `N/4`。对于 100 万 token，那就是 25 万个压缩块。

压缩器分别用于生成**压缩后的 K 和 V**。得到的 `K_c ∈ ℝ^{N/4 × d_k}` 和 `V_c ∈ ℝ^{N/4 × d_v}` 以 **FP8**（而非 bf16）格式存储，与标准精度相比，内存再次减半。

---

#### 2. 闪电索引器（FP4，ReLU 评分的块选择）

给定一个查询 `q ∈ ℝ^{d_k}`，索引器对所有 `N/4` 个压缩键块进行评分，以选出最相关的 top-k 个块。这就是“闪电”的由来——它以 **FP4** 精度运行，并使用 **ReLU 激活函数而非 softmax**：

```python
# FP4 量化的查询和压缩键
q_fp4 = quantize_fp4(q)
K_c_fp4 = quantize_fp4(K_c)  # 形状: (N/4, d_k)

# 对每个压缩块评分（多头点积）
scores = relu(q_fp4 @ K_c_fp4.T)  # 形状: (N/4,)
# 注意：使用 ReLU 而非 softmax——消除负值，保留正值，无需归一化

# 选择 top-k 个块
top_k_indices = argsort(scores)[-k:]
```

为什么索引时用 ReLU 而非 softmax？

- Softmax 会进行归一化，这意味在稀疏场景下低分仍可能“胜出”。而 ReLU 自然地会将无关块归零——如果点积为负，该块被直接排除。
- FP4 精度足以对块进行排序，而非计算最终的注意力权重。索引器是一个**粗过滤器**，而非注意力机制本身。
- 这运行得非常快——在现代硬件（H100、MI300X）上，FP4 点积比 FP8 便宜 2-4 倍，比 bf16 便宜 4-8 倍。

索引器选择 top-k 个压缩块。只有这些块对应的**原始未压缩的** KV 条目（共 4k 个原始位置）才会参与实际的注意力计算。

---

#### 3. 完整的注意力传递（带滑动窗口处理近期信息）

CSA 每层运行**两个并行分支**：

```
查询 q
  ├─ [闪电索引器] → top-k 个压缩块 → [对 k×4 个原始 KV 进行注意力计算]
  └─ [滑动窗口] → 最后 W 个 token（未压缩） → [局部注意力]

输出 = 合并(稀疏全局注意力, 局部注意力)
```

滑动窗口处理近期信息——最后 W 个位置的 token 尚未被压缩（或其压缩尚未刷新），因此需要直接注意力。这与 Longformer/Mistral 滑动窗口的局部注意力技巧相同，但在这里它是**压缩稀疏全局注意力的补充**，而非整个机制。

最终的注意力输出结合了两个分支（通常通过拼接后投影，或学习到的门控）。

---

### 对比：V3.2 稀疏注意力 vs. V4 CSA

| | V3.2 DeepSeek 稀疏注意力 | V4 CSA |
|---|---|---|
| 索引范围 | 全部 `N` 个 KV 条目 | `N/4` 个压缩块 |
| 索引器精度 | FP8 或 bf16 | **FP4** |
| 索引器激活函数 | softmax 或点积 | **ReLU** |
| KV 存储 | FP8 | FP8（压缩后），因此条目数减少 4 倍 |
| 有效搜索空间 | `N` | `N/4` |
| 缓存占用减少 | ~稀疏比例 | **~25 倍**（4 倍压缩 × 约 6 倍 FP8 相对于 bf16 GQA 基线） |

核心创新：V3.2 对原始序列进行稀疏选择。V4 对已压缩的序列进行稀疏选择。索引器本身的运行成本降低了 4 倍，且每个选定块需要物化的 KV 缓存也更小。

---

### HCA 作为另一半

CSA 与**重度压缩注意力（HCA）**交错使用——思路相同，但压缩比为 128 倍，且**无稀疏选择**（对所有 `N/128` 个块进行密集注意力）。在 128 倍压缩下，压缩后的序列足够短，以至于 `O((N/128)²)` 的密集注意力计算成本很低。

在 V4-Pro 的 61 层堆栈中，第 0-1 层为 HCA，第 2-60 层交替使用 CSA 和 HCA，最后的 MTP 块仅运行滑动窗口。

这种交错设计是有原则的：不同层在训练过程中会形成不同的注意力模式。HCA 层学习粗粒度的全局上下文。CSA 层在更粗粒度的摘要之上学习细粒度的稀疏检索。

---

### 这在数据上为你带来了什么

在 100 万 token 时，与 DeepSeek-V3.2 相比，DeepSeek-V4-Pro 仅需 27% 的单 token 推理 FLOPs，以及 10% 的 KV 缓存内存。V4-Flash 进一步将 FLOPs 降至 10%，KV 缓存降至 7%。与使用 bfloat16 且具有 8 个头的分组查询注意力相比，DeepSeek-V4 所需的缓存大小约为 2%。

2% 的 KV 缓存数据由三个独立的乘数复合而成：

- **4 倍**：来自 CSA 序列压缩
- **约 4 倍**：来自 FP8 与 bf16 存储对比
- **约 4 倍**：来自稀疏选择（仅物化 top-k 个块）

这些乘数是相乘而非相加。

---

### 完整 CSA 前向传播的最小伪代码

```python
def csa_forward(q, K_full, V_full, k_blocks=64, window=512):
    N, d = K_full.shape

    # 1. 压缩 KV 缓存：N → N/4
    K_c, V_c = compress_kv(K_full, block_size=4)  # 各为 (N/4, d)，以 FP8 存储

    # 2. 闪电索引器：使用 FP4 和 ReLU 对压缩块评分
    scores = relu(quantize_fp4(q) @ quantize_fp4(K_c).T)  # (N/4,)
    top_k_block_indices = topk(scores, k=k_blocks)         # (k_blocks,)

    # 3. 收集选定块的原始 KV（每块 4 个原始 token）
    selected_positions = expand_blocks(top_k_block_indices, block_size=4)  # (k_blocks*4,)
    K_sel = K_full[selected_positions]  # (k_blocks*4, d)
    V_sel = V_full[selected_positions]

    # 4. 对选定位置进行全局稀疏注意力
    attn_global = softmax_attention(q, K_sel, V_sel)

    # 5. 局部滑动窗口注意力（近期信息）
    K_local = K_full[-window:]
    V_local = V_full[-window:]
    attn_local = softmax_attention(q, K_local, V_local)

    # 6. 合并
    return merge(attn_global, attn_local)

def compress_kv(K, block_size=4):
    N, d = K.shape
    K_blocked = K.reshape(N // block_size, block_size, d)
    # 学习到的位置偏置（4 个标量）
    gates = softmax(learned_pos_bias)  # (block_size,)
    K_compressed = einsum('b p d, p -> b d', K_blocked, gates)
    return quantize_fp8(K_compressed)
```

---

### 值得内化的核心见解

CSA 就像一个 **两级索引**，类似 B 树或 ANN 索引——压缩得到易于搜索的摘要，搜索摘要找到候选者，然后仅检索这些候选者的全分辨率条目。创新点不在于单个组件，而在于**压缩、索引和检索形成了一个流水线，每个阶段都针对下一阶段的精度要求进行了调优**（FP4 索引器 → FP8 存储 → bf16 最终注意力）。

这在架构上类似于向量数据库中的 HNSW 或 IVF——使用粗量化进行快速近邻搜索，然后使用全精度重新排序。DeepSeek 直接将这种检索系统的直觉应用于注意力机制。

---

参考文献：

- [DeepSeek-V4：智能体可真正使用的百万 token 上下文（HuggingFace 博客）](https://huggingface.co/blog/deepseekv4)
- [DeepSeek-V4 技术报告（PDF）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
