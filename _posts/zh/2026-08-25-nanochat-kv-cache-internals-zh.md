---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoChat KV缓存内部机制
translated: true
type: note
---

现在我完全理解了。以下是 KV cache 在 nanochat 中的工作方式：

## 存储位置

- **`KVCache` 类** — `nanochat/engine.py:82` — 状态容器
- **在注意力中使用** — `nanochat/gpt.py:108-123`（`CausalSelfAttention.forward`）和 `gpt.py:459+`（位置偏移、smear）
- **内核胶水层** — `nanochat/flash_attention.py:200`（`flash_attn_with_kvcache`，支持 FA3/FA2/SDPA 后端）

## 布局与分配

缓存预先以 FA3 原生 `(B, T, H, D)` 布局分配（无需转置）：

```python
self.k_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, device=device, dtype=dtype)
self.v_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, ...)
```

关键细节：

- **每层一个张量切片**：`get_layer_cache(layer_idx)` 返回 `self.k_cache[layer_idx]` 视图。
- **仅 KV 头**（`n_kv_head`，默认 6）：这是为 GQA 准备的——即使默认配置中 `n_head == n_kv_head`，缓存仍按 `n_kv_head` 形状分配，FA3/`enable_gqa` 会在内部为查询头复制 KV 头。
- **计算精度**（bf16），与激活精度一致，确保内核的就地缓存写入精度正确。
- **位置是逐 batch 的 `int32` 张量**：`cache_seqlens`（形状为 (B,)），不是标量——FA3 需要这种形状。

## 两阶段引擎流程（`Engine.generate`，engine.py:156）

1. **预填充，batch=1**：分配一个 `seq_len=len(tokens)` 的小型缓存，将完整提示词通过 `model.forward(ids, kv_cache=kv_cache_prefill)` 运行——一次前向，所有层写入 KV，从最后位置获取 logits。
2. **克隆到解码缓存**：`kv_cache_decode.prefill(kv_cache_prefill)` 将 KV 切片和 smear 状态复制到 `batch_size=num_samples`、大小为 `len(tokens) + max_tokens` 的缓存中。batch-1 缓存被释放。（这允许你只做一次预填充，然后基于相同前缀并行生成多个样本。）
3. **解码循环**：每次迭代仅将新采样的 token(s) `(B, 1)` 与解码缓存一起送入模型；注意力看到完整的缓存前缀，因此每个 token 的成本是 O(1) 新计算 + O(context) 注意力读取，而非 O(T²)。

## 每次前向的机制（有趣的部分）

**旋转位置编码偏移**（`gpt.py:466-468`）：缓存通过 `kv_cache.get_pos()` 知道其绝对位置，cos/sin 表按 `self.cos[:, T0:T0+T]` 切片。因此，在位置 500 处解码 1 个 token 时，会获得绝对位置 500 的旋转位置编码。

**先旋转再缓存，而非先缓存再旋转**：在 `CausalSelfAttention.forward` 中，新的 `k`（和 `q`）在内核调用*之前*使用绝对位置应用 `apply_rotary_emb`。然后已经旋转、QK-norm、缩放的 `k` 作为 `k=k` 传给内核：

```python
q, k = apply_rotary_emb(q, cos, sin), apply_rotary_emb(k, cos, sin)
q, k = norm(q), norm(k)
...
y = flash_attn.flash_attn_with_kvcache(q, k_cache, v_cache, k=k, v=v,
        cache_seqlens=kv_cache.cache_seqlens, causal=True, window_size=window_size)
```

这是正确的，因为旋转/归一化在写入时使用绝对位置只发生一次——读取时缓存的键已经处于正确形式。（FA3 也有内部的 `rotary_cos/rotary_sin` 路径；此代码手动完成，以便同一代码路径在 FA2/SDPA 回退上也有效。）

**单个内核完成写入 + 注意力**：`flash_attn_with_kvcache` 将 `k, v` 就地插入缓存中 `cache_seqlens` 位置，然后计算 `q` 对缓存中直到 `cache_seqlens + T` 位置的注意力。因果 + 滑动窗口掩码来自 `window_size`（例如，短层为 `(768, 0)`，长层为 `(-1, 0)`/`(2048, 0)`）。

**位置推进是手动的，仅在最后一层之后**（`gpt.py:122-123`）：

```python
if self.layer_idx == kv_cache.n_layers - 1:
    kv_cache.advance(T)
```

所有层在一次前向中必须看到*相同*的 `cache_seqlens`（每层写入同一位置），因此指针每次前向推进一次，而非每层推进。测试（`test_attention_fallback.py:312-330`）也做了相同的显式 `advance`，确认这些内核不会就地更新 `cache_seqlens`。

## 除 K/V 之外的额外缓存状态

- **`prev_embedding`**（engine.py:104）：前一个 token 的归一化嵌入，用于“smear”技巧（廉价的 bigram 信息）。在 `T == 1` 的解码时，模型读取它，混合 `x + gate * prev`（`gpt.py:483-492`），然后存储新 token 的嵌入。`prefill()` 也会为多样本缓存复制/扩展该值。
- **值嵌入（ResFormer）*不*缓存**——它们通过 `self.value_embeds[str(i)](idx)` 每步重新查询，这是一个廉价的嵌入收集操作。

## 成本计算

- `kv_bytes_per_token()`（gpt.py:374）：`n_layer × 2 × n_kv_head × head_dim × 2 bytes`——每个 token 的存储量。
- `kv_read_bytes(context_len)`（gpt.py:380）：每个解码步骤的读取量，且遵循滑动窗口——短窗口层只读取 `min(context, window)` 的缓存，这正是 SSSL 模式的核心：长层做完整读取，短层只读最后四分之一。

## 回退方案

SDPA 回退（`flash_attention.py:235+`）复现内核行为：在 `pos` 处就地插入 `k, v`，将缓存切片到 `end_pos`，并为滑动窗口/分块推断构建显式布尔掩码（假设统一位置：`pos = cache_seqlens[0].item()`）。

有一点值得注意：`GPT.generate()`（`gpt.py:518`）是朴素的免缓存路径——它每一步都对不断增长的序列重新运行完整前向——引擎的 `__main__` 测试断言其产生的 token 与缓存路径完全一致，因此缓存是经过真值验证的。
