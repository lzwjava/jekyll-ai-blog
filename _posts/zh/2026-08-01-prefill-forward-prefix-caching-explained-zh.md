---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预填充前向前缀缓存详解
translated: true
type: note
---

以下是对该 Markdown 文本的简体中文翻译：

以下是 `_prefill_forward` 的逐行解释。首先，你需要了解两个关键事实：

**事实 1——“打包”的张量。** q、k、v 是*打包*的：批次中的序列被拼接成一个扁平张量，`cu_seqlens_q` / `cu_seqlens_k`（累积序列长度）告诉你每个序列的起始/结束位置。例如 `cu_seqlens_q = [0, 4, 9]` 表示序列 0 = tokens 0–3，序列 1 = tokens 4–8。

**事实 2——q 和 k 的长度可以不同。** 在带有前缀缓存的预填充过程中，每个序列包含：

- `seqlen_k` = 缓存的前缀 tokens + 新 tokens（所有将被关注的 tokens）
- `seqlen_q` = 仅新 tokens（我们计算输出的对象）

你可以在 `prepare_prefill` 中看到这一点：`seqlen_q = seq.num_scheduled_tokens`，`seqlen_k = end = start + seqlen_q`。

## 两个分支

```python
if context.block_tables is not None and k_cache is not None:
```

`block_tables` 仅在 `cu_seqlens_k[-1] > cu_seqlens_q[-1]` 时设置——即 **存在缓存的前缀**。因此，这个条件分为：

### 分支 1——前缀缓存（K/V 已在分页缓存中）

```python
seqlens  = 每个序列的完整 KV 长度（前缀 + 新 tokens）
q_lens   = 每个序列的新 token 长度
k_gathered, v_gathered = _gather_kv_from_cache(...)   # 从分页块中读取前缀 + 新 K/V
k_flat = torch.cat([k_gathered[i, :seqlens[i]] ...])  # 重新展平为打包格式
```

过程如下：

1. *新* tokens 的 K/V 已通过 `forward()` 中的 `store_kvcache` 写入分页缓存（在此函数运行之前）。
2. `_gather_kv_from_cache` 从块中读取**整个** K/V 序列——共享前缀和刚写入的新 tokens——并将其放入密集张量。
3. 它们被重新展平为打包形式，因此 `k_flat` 每个序列为 `[prefix_0, new_0, new_1, ...]`。
4. q 保持不变：它仅是新 tokens。

然后关键记录行：

```python
cached_len_per_seq = [(seqlens[i] - q_lens[i], q_lens[i], seqlens[i]) ...]
#                    (  cached_len,             q_len,    kv_len  )
```

对于每个序列：`cached_len = kv_len − q_len` = 查询之前的缓存前缀 tokens 数量。

### 分支 2——标准预填充（无现有缓存）

```python
q_lens  = 新 token 长度
kv_lens = 完整提示长度
cached_len_per_seq = [(kv_lens[i] - q_lens[i], q_lens[i], kv_lens[i]) ...]
```

这里每个 token 都是新的，因此对于每个序列，`kv_len == q_len` 且 `cached_len = 0`。q/k/v 是整个提示，直接使用。

## 神奇之处：因果掩码如何处理前缀

两个分支都调用了 `_flash_attention(q, k, v, self.scale, causal=True, cached_len_per_seq=...)`。由于列表非空，它使用具有**独立** `cu_seqlens_q` 和 `cu_seqlens_k` 的 `flash_attn_varlen_func`（这就是为什么 q 和 k 的长度可以不同）。

关键行为在 flash-attn 本身中有文档记录——**因果掩码与右下角对齐**：

```
如果 seqlen_q = 2 且 seqlen_k = 5：
    1 1 1 1 0
    1 1 1 1 1
```

因此，查询位置 `i` 关注键位置 `j` 当且仅当 `j ≤ i + (kv_len − q_len) = i + cached_len`。

思考这对前缀缓存意味着什么：键位置 `0..cached_len−1` 是前缀，键位置 `cached_len + i` 是查询 `i` *之后* 的新 token。掩码表明：

- 查询 `i` 关注**所有前缀 tokens**（位置 `0..cached_len−1`）✓
- 加上更早的新 tokens（`cached_len..cached_len + i`）✓
- 但**不**关注未来的新 tokens（位置 `> cached_len + i`）✓（因果）

这正是正确的语义：每个新 token 可以看到完整的历史，而不是未来。无需自定义掩码代码——右下角对齐自动实现了这一点。

## 输出结果

`o` 是**仅新 tokens**（`total_q_tokens` 行）的打包注意力输出。它向上流向 Transformer 的其余部分；每个序列的最后一个 token 最终到达 LM 头 → 第一个输出 token。同时，新的 K/V 已经位于分页缓存中，因此后续的解码步骤可以关注它们。

另一个细微差别：在分支 1 中，K/V *进入* 缓存（`store_kvcache`），然后*读回*（`_gather_kv_from_cache`），以便可以在完整序列上计算注意力——这是通过分页缓存的往返。在分支 2（无前缀）中，直接使用 q/k/v。而在 `forward()` 中，还有一个 CUDA 图捕获快捷方式（`torch.cuda.is_current_stream_capturing()`），它完全跳过所有缓存操作，因为在图捕获期间不允许使用 `.item()` 调用和张量条件语句。