---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 滑动窗口注意力架构
translated: true
type: note
---

此代码库中的滑动窗口注意力机制分为三层：首先在 `gpt.py` 中将**模式字符串**转换为每层的窗口大小，然后通过 `flash_attention.py` 在注意力核中**实际执行**。

## 1. 窗口分配位置（gpt.py）

`Config` 中定义 `window_pattern: str = "SSSL"`（gpt.py:39），其中 `L` 代表完整上下文，`S` 代表四分之一上下文。`_compute_window_sizes`（gpt.py:287）将其转换为每层的 `(left, right)` 元组：

```python
long_window  = config.sequence_len                          # L: 完整 2048
short_window = -(-long_window // 4 // 128) * 128            # S: 约四分之一，向上取整到 128（FA3 块大小）
char_to_window = {"L": (long_window, 0), "S": (short_window, 0)}
# 跨层平铺模式："SSSL" -> S,S,S,L, S,S,S,L, ...
window_sizes[-1] = (long_window, 0)   # 最后一层始终为完整上下文
```

因此，模式会在 `n_layer` 层上平铺，每个 `Block` 接收 `window_sizes[i]`，并将其转发到 `flash_attn.flash_attn_func(...)` / `flash_attn_with_kvcache(...)`（gpt.py:110, 119）。

**窗口语义**：`(left, right)` 是一个基于距离的带状区域，而非“最后 N 个位置”。每个查询 Token 可以关注其背后距离 ≤ `left` 的键——以及自身。`right = 0` 加上 `causal=True` 意味着不关注未来；`left = -1` 则表示无限制。此处 `left` 始终是具体的窗口大小（或完整的 `sequence_len`），不会是 `-1`。

## 2. `flash_attention.py` —— 调度层

该文件本身未实现滑动窗口，而是作为一个**统一封装器**，将 `window_size` 元组转发给当前激活的后端，共有三种情况：

### FA3（Hopper）——透传

```python
return _fa3.flash_attn_func(q, k, v, causal=causal, window_size=window_size)
```

FA3 CUDA 核接收 `(left, 0)`，并在核内部原生执行带状掩码——每个查询块仅加载窗口内的键/值块，这正是 FLOP/内存节省的来源。

### FA2——近似透传

```python
return _fa2.flash_attn_func(q, k, v, dropout_p=0.0, causal=causal, window_size=_fa2_window_size(window_size))
```

FA2 的核原生支持相同的 `(left, right)` 带状注意力。`_fa2_window_size` 将无限制的 left 映射为 FA2 的 `(-1, -1)` 哨兵值（在此模型中 right 始终为 0，因此大部分情况直接透传）。

### SDPA 回退 —— 手动模拟（`_sdpa_attention`，实质内容）

PyTorch 的 `scaled_dot_product_attention` 没有带状窗口概念，因此根据不同情况通过三种方式模拟：

**a) 完整上下文，等长**（`window < 0 或 window >= Tq`，且 `Tq == Tk`）：

```python
return F.scaled_dot_product_attention(q, k, v, is_causal=True, ...)
```

窗口涵盖了所有内容，因此直接使用普通因果 SDPA（快速路径）。

**b) 单 Token 解码**（`Tq == 1`）——巧妙技巧：

```python
start = max(0, Tk - (window + 1))
k = k[:, :, start:, :]   # 仅保留最后 window+1 个键
v = v[:, :, start:, :]
return F.scaled_dot_product_attention(q, k, v, is_causal=False, ...)
```

查询关注宽度为 `window` 的带状区域，只需要 KV 缓存的**尾部**，因此直接将 `k/v` 切片为最后 `window + 1` 个键。完全不需要掩码——由于查询位于最后位置，这在数学上等同于带状注意力。

**c) 分块推理 / 预填充**（`Tq != Tk`，且两者都大于 1）：此时查询是序列内部的块，因此相关的键包括缓存尾部以及块内更早的 Token。需要构建显式的布尔掩码：

```python
row_idx = (Tk - Tq) + torch.arange(Tq)          # 查询行的绝对位置
col_idx = torch.arange(Tk)                       # 键列的绝对位置
mask = col_idx <= row_idx                        # 因果：键位置 <= 查询位置
if window >= 0 and window < Tk:
    mask = mask & ((row_idx - col_idx) <= window)  # 滑动：回看距离 <= 窗口
return F.scaled_dot_product_attention(q, k, v, attn_mask=mask, ...)
```

`row_idx` 偏移量 `(Tk - Tq)` 将查询行映射到其在缓存中的真实位置，从而在绝对位置上计算因果性和距离带状，而不是使用相对偏移。

## 关键观察

- **节省源于核本身，而非掩码。** 使用 FA3/FA2 时，带状区域是一种核级别的优化：窗口外的键块永远不会被加载，因此每层的注意力 FLOP 随窗口大小而非完整上下文缩放。使用 SDPA 回退时，仅通过掩码/切片实现——结果正确但无速度提升。
- **KV 缓存仍然无界增长。** `engine.py` 中的 `KVCache` 仅不断追加（`cache_seqlens += num_tokens`）；不存在驱逐机制。此处的滑动窗口只限制**注意力**，并不限制缓存内存。（gpt.py:107 的注释——`(N, 0)` 用于滑动窗口——确认仅使用左侧带状。）
- **每个位置的有效上下文**为 `min(position, window+1)` 个 Token——具有 `S` 的层获得约四分之一上下文的局部注意力，与完整上下文的 `L` 层交替出现，最后一层始终看到全部内容，从而形成滑动窗口 LLM 典型的廉价“局部性 + 全局回顾”混合模式（例如 Longformer/BigBird 风格混合体）。
- SDPA 窗口检查 `window >= Tq` 将“窗口至少与查询运行长度相等”视为完整上下文——这是一个重要的边缘情况，因为在解码过程中 `Tq` 很小（通常为 1），即使“短”窗口（如 512）在生成早期也涵盖了查询迄今为止看到的所有内容。
