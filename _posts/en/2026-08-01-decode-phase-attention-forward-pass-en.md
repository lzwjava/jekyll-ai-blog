---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decode Phase Attention Forward Pass
translated: false
type: note
---

`_decode_forward` is the decode-phase counterpart — here's the full walkthrough:

```python
def _decode_forward(self, q, context, k_cache, v_cache):
```

**Key difference from prefill:** there's no `k`/`v` argument at all. The only fresh tensor is `q` — `(batch, num_heads, head_dim)`, exactly **one query per sequence** (the single token generated this step). All K/V comes from the cache. That's the whole point of decode: pay for 1 token of compute, reuse everything else.

## 1. Warmup/fallback guard

```python
if context_lens is None or block_tables is None or k_cache is None:
    return q   # identity
```

No cache available (e.g. CUDA-graph warmup runs a dummy pass before real serving) → just pass q through unchanged. No attention is actually computed during warmup.

## 2. Gather the whole history from the paged cache

```python
seqlens = [cl.item() for cl in context_lens]
k_gathered, v_gathered = _gather_kv_from_cache(k_cache, v_cache, block_tables, seqlens, block_size)
```

- `context_lens[i]` = how many tokens sequence *i* has **including** the one just generated (its K/V was already written by `store_kvcache` in `forward()` before this ran).
- `_gather_kv_from_cache` walks each sequence's `block_tables` (the list of physical blocks), and for each position `0..seqlens[i]-1` copies `k_cache[block, offset]` into a dense tensor of shape `(batch, max_len, num_kv_heads, head_dim)`.

So the paged, scattered storage becomes a plain dense `(batch, seq, head, dim)` tensor the kernel can eat. (This is the classic *paged → dense gather*; production vLLM avoids this by feeding `block_table` directly into flash-attn's paged kernels, but this code chose the simpler gather.)

## 3. Shape gymnastics for `flash_attn_func`

```python
q_i = q.unsqueeze(1)   # (batch, heads, dim) → (batch, 1, heads, dim)
```

flash_attn_func wants `(batch, seqlen, num_heads, head_dim)`; the single decode token becomes `seqlen=1`. The gathered k/v are already in the right layout (`_gather_kv_from_cache` returns `(batch, seq, head, dim)`).

```python
if self.num_heads != self.num_kv_heads:          # GQA / MQA
    num_repeats = self.num_heads // self.num_kv_heads
    k_gathered = k_gathered.repeat_interleave(num_repeats, dim=2)
```

If the model uses grouped-query attention (e.g. 8 Q heads, 2 KV heads), each KV head is replicated `num_repeats` times so every Q head has a matching K/V head.

## 4. Why `causal=False` is safe here

```python
o = flash_attn_func(q_i, k_gathered, v_gathered, dropout_p=0.0,
                    softmax_scale=self.scale, causal=False)
```

No causal mask needed during decode — and not just because there's only 1 query row. The cache **never contains future tokens**: a token's K/V is only stored after it's generated. So the gathered keys are guaranteed to be `{pos 0 … pos t}` for a query at position `t`, never beyond. All keys are legitimate context.

## 5. Output

```python
o = o.squeeze(1)   # (batch, 1, heads, dim) → (batch, heads, dim)
return o
```

One attention output per sequence, which continues through the transformer → LM head → next token sampled. Next step, the process repeats: 1 new token, its K/V cached, full-history gather again.

## Decode vs. prefill, side by side

| | Prefill (`_prefill_forward`) | Decode (`_decode_forward`) |
| --- | --- | --- |
| q size | all prompt tokens (packed) | 1 token per seq `(batch, …)` |
| k/v source | packed tensors (or gather if prefix cached) | always gathered from cache |
| attention | over prompt (`causal=True`, bottom-right aligned for prefixes) | over full cached history (`causal=False`, safe) |
| output | first output token per seq | one new token per seq |
| cost | O(prompt_len²) once | O(context_len) per step — but cached, so only new K/V computed |

**One caveat worth knowing:** `_gather_kv_from_cache` zero-pads shorter sequences to `max_len`, and with `causal=False` the query attends to those zero rows too (they contribute 0 to the output, but they do "steal" some softmax weight, slightly distorting results when sequences in a batch have very different lengths). vLLM's production kernels avoid this with proper masking/paged attention — this is the simplified tradeoff the codebase makes.
