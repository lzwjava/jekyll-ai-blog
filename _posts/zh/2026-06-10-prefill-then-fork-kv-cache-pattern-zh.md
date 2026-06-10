---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预填充然后分叉KV缓存模式
translated: true
type: note
---

**问题：** nanochat 的 KV 缓存中的 `prefill` 方法是如何工作的——它的作用是什么？每一行代码在做什么？

**回答：**

## 整体思路：一次性处理提示词，采样 N 次

这是 **先预填充再分叉** 的模式。当你需要对同一个提示词进行多次采样（例如 best-of-N、pass@k 评估、强化学习中的并行 rollout）时，朴素的做法是将提示词重复 N 次送入模型。但所有 N 个样本的提示词 KV 缓存是相同的——因此 nanochat 的做法是：

```
1. 构建一个 batch_size=1 的 KV 缓存
2. 将提示词通过模型运行一次 → 填充 `other`
3. 构建第二个 batch_size=N 的缓存（即 `self`）
4. self.prefill(other)                    → 将提示词的 KV 复制/广播到所有 N 个行中
5. 并行解码 N 个样本，从相同的前缀开始分叉
```

提示词的计算量从 `O(N · prompt_len)` 降至 `O(prompt_len)`。对于一个 2000 个 token 的提示词和 16 个样本，预填充阶段节省了 16 倍的计算量。

## 逐行解释

```python
assert self.get_pos() == 0, "Cannot prefill a non-empty KV cache"
```
`self` 必须是全新的——预填充是从位置 `[0, other_pos)` 进行整体复制，而不是追加。合并到一个部分填充的缓存会破坏位置对齐。

```python
assert self.n_layers == other.n_layers and self.n_heads == other.n_heads and self.head_dim == other.head_dim
assert self.max_seq_len >= other.max_seq_len
```
几何结构必须匹配（同一个模型），并且目标缓存至少需要与源缓存相同的序列空间——通常更多，因为 `self` 在提示词之后还会继续解码。

```python
other_pos = other.get_pos()
self.k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]
self.v_cache[:, :, :other_pos, :, :] = other.v_cache[:, :, :other_pos, :, :]
```

这是核心技巧。缓存布局是五维的：

```
(batch, n_layers, seq_len, n_kv_heads, head_dim)
   │       │         │
   │       │         └── 切片到 :other_pos（仅填充的提示词区域）
   │       └── 所有层在一次赋值中复制
   └── 广播：other 的 batch=1，self 的 batch=N
```

PyTorch 的广播规则在第 0 维生效：将一个 `(1, L, P, H, D)` 的张量赋值给一个 `(N, L, P, H, D)` 的切片，**会将单个提示词缓存复制到所有 N 个 batch 行**，无需显式循环或 `repeat()`。一个融合的复制内核，一次性完成。

该机制的最小复现：

```python
import torch
N, L, T, H, D = 4, 2, 8, 2, 3
src = torch.randn(1, L, 5, H, D)        # batch=1 预填充，5 个提示词 token
dst = torch.zeros(N, L, T, H, D)        # batch=4 解码缓存
dst[:, :, :5, :, :] = src               # 在第 0 维上广播
assert (dst[0, :, :5] == dst[3, :, :5]).all()  # 每一行都得到了提示词的 KV
```

```python
self.cache_seqlens.fill_(other_pos)
```
`cache_seqlens` 是一个形状为 `(batch,)` 的逐序列长度张量——这是 FlashAttention 中 `flash_attn_with_kvcache` 的约定。它告诉注意力内核每个序列的有效 KV 结束位置，即下一个解码 token 的 K/V 应该写入的位置。将所有 N 个条目设置为 `other_pos` 意味着：每一行的"写入指针"都紧跟在提示词之后。

```python
if other.prev_embedding is not None:
    self.prev_embedding = other.prev_embedding.expand(self.batch_size, -1, -1).clone()
```
这传递了 **拖尾状态**——nanochat 会将上一个 token 的嵌入混合到当前 token 的表示中（继承自 modded-nanogpt 系列的"token 拖尾技巧"），因此解码步骤 `other_pos` 需要 token `other_pos - 1` 的嵌入。两个细节值得注意：

- `.expand(N, -1, -1)` 创建了一个 **零复制视图**，在 batch 维上步长为 0——所有 N 行共享同一块内存。
- `.clone()` 随后将其 **物化** 为 N 个独立行。这是必要的：一旦 N 个样本开始分叉，每一行的 `prev_embedding` 都会被其自身的 token 覆盖，而写入一个步长为 0 的扩展视图要么会报错，要么会悄悄破坏所有行。

`expand().clone()` 是"先广播再拥有内存"的惯用模式——比 `repeat()` 更容易理解，这里结果相同。

## 为什么一开始不直接用一个 batch=N 的缓存对象？

你可以通过将提示词重复 N 次来批量预填充，但这既浪费计算（在一次批量调用中执行 N 个相同的前向传播的 FLOPs）也浪费带宽。预填充是计算密集型的（对整个提示词进行大矩阵乘法）；解码是内存带宽密集型的（每次一个 token）。以 batch=1 运行预填充然后分叉缓存，可以让每个阶段都以低成本进行。唯一的代价是一次性的 `O(N · L · P · H · D)` 内存复制——纯带宽，无 FLOPs，在 GPU 上只需微秒级时间。

需要深刻理解的一点是：这是因为 KV 缓存 **就是** 变换器解码器的整个序列状态。复制缓存和拖尾嵌入后，N 个样本在比特级别上与各自独立处理提示词无法区分——它们只有在采样选择不同 token 时才会分叉。

**参考资料：**

- [nanochat 仓库 (karpathy/nanochat)](https://github.com/karpathy/nanochat)
- [flash_attn_with_kvcache — FlashAttention 接口](https://github.com/Dao-AILab/flash-attention/blob/main/flash_attn/flash_attn_interface.py)