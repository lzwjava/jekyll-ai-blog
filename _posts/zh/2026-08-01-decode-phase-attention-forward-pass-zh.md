---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解码阶段注意力前向传播
translated: true
type: note
---

`_decode_forward` 是解码阶段的对应函数——以下是完整解读：

```python
def _decode_forward(self, q, context, k_cache, v_cache):
```

**与预填充的关键区别：** 完全没有 `k`/`v` 参数。唯一的新张量是 `q` —— `(batch, num_heads, head_dim)`，每个序列恰好 **一个查询**（即当前步骤生成的那个单一 token）。所有 K/V 都来自缓存。这正是解码的核心：只支付 1 个 token 的计算量，复用其余所有内容。

## 1. 预热/降级保护

```python
if context_lens is None or block_tables is None or k_cache is None:
    return q   # 恒等映射
```

没有可用缓存（例如 CUDA 图预热在实际服务前会先运行一次虚拟传递）→ 直接原样返回 q。预热期间不实际计算注意力。

## 2. 从分页缓存中收集完整历史

```python
seqlens = [cl.item() for cl in context_lens]
k_gathered, v_gathered = _gather_kv_from_cache(k_cache, v_cache, block_tables, seqlens, block_size)
```

- `context_lens[i]` = 序列 *i* 到目前为止的 token 数量，**包括**刚生成的那个（它的 K/V 已经在 `forward()` 中的 `store_kvcache` 执行之前写入了）。
- `_gather_kv_from_cache` 遍历每个序列的 `block_tables`（物理块列表），对于位置 `0..seqlens[i]-1`，将 `k_cache[block, offset]` 复制到形状为 `(batch, max_len, num_kv_heads, head_dim)` 的密集张量中。

因此，分散的分页存储变成了一个普通的密集 `(batch, seq, head, dim)` 张量，可供内核直接使用。（这是经典的 *分页 → 密集收集*；生产环境中的 vLLM 通过将 `block_table` 直接传入 flash-attn 的分页内核来避免这一步，但此代码选择了更简单的收集方式。）

## 3. 为 `flash_attn_func` 进行形状调整

```python
q_i = q.unsqueeze(1)   # (batch, heads, dim) → (batch, 1, heads, dim)
```

flash_attn_func 期望 `(batch, seqlen, num_heads, head_dim)`；单个解码 token 对应 `seqlen=1`。收集到的 k/v 已经是正确的布局（`_gather_kv_from_cache` 返回 `(batch, seq, head, dim)`）。

```python
if self.num_heads != self.num_kv_heads:          # GQA / MQA
    num_repeats = self.num_heads // self.num_kv_heads
    k_gathered = k_gathered.repeat_interleave(num_repeats, dim=2)
```

如果模型使用分组查询注意力（例如 8 个 Q 头、2 个 KV 头），每个 KV 头会复制 `num_repeats` 次，以便每个 Q 头都有对应的 K/V 头。

## 4. 为什么这里 `causal=False` 是安全的

```python
o = flash_attn_func(q_i, k_gathered, v_gathered, dropout_p=0.0,
                    softmax_scale=self.scale, causal=False)
```

解码期间不需要因果掩码——不仅仅是因为只有一行查询。缓存**从不包含未来的 token**：一个 token 的 K/V 只有在生成之后才会被存储。因此，对于位置 `t` 的查询，收集到的键保证是 `{位置 0 … 位置 t}`，绝不会超出。所有键都是合法的上下文。

## 5. 输出

```python
o = o.squeeze(1)   # (batch, 1, heads, dim) → (batch, heads, dim)
return o
```

每个序列得到一个注意力输出，它会继续通过 transformer → LM 头 → 下一个 token 采样。下一步，过程重复：1 个新 token，其 K/V 被缓存，再次收集完整历史。

## 解码 vs. 预填充，并排对比

| | 预填充（`_prefill_forward`） | 解码（`_decode_forward`） |
| --- | --- | --- |
| q 大小 | 所有提示词 token（打包） | 每个序列 1 个 token `(batch, …)` |
| k/v 来源 | 打包张量（如果前缀缓存则收集） | 总是从缓存中收集 |
| 注意力 | 覆盖提示词（`causal=True`，前缀右下对齐） | 覆盖完整缓存历史（`causal=False`，安全） |
| 输出 | 每个序列的第一个输出 token | 每个序列一个新 token |
| 成本 | 一次 O(prompt_len²) | 每步 O(context_len)——但已缓存，因此只计算新 K/V |

**一个值得了解的注意事项：** `_gather_kv_from_cache` 会将较短的序列零填充到 `max_len`，并且由于 `causal=False`，查询也会关注那些零行（它们对输出贡献为 0，但确实会“窃取”一些 softmax 权重，当批次中序列长度差异很大时，会轻微扭曲结果）。vLLM 的生产内核通过适当的掩码/分页注意力避免了这一点——这是代码库所做的简化权衡。
