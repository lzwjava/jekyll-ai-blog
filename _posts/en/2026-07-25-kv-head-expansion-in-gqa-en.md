---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV head expansion in GQA
translated: false
type: note
---

Question: What does `k_i = k_i.repeat_interleave(num_repeats, dim=2)` do in GQA/MQA attention, given the comment `(1, kv_len, 16, 128)`?

Answer:

This is expanding KV heads to match Q heads in **Grouped Query Attention (GQA)**. The shape tells the story: `(batch, seq_len, num_heads, head_dim)`.

**The problem:** you trained/inference with fewer KV heads than Q heads to save KV-cache memory. E.g. 16 query heads but only 4 KV heads (`num_repeats = 16/4 = 4`). Each KV head is shared across a *group* of 4 Q heads.

**Before repeat_interleave**, `k_i` shape is `(1, kv_len, 4, 128)` — 4 KV heads.

**repeat_interleave(4, dim=2)** turns each KV head into 4 identical copies, contiguous:

```python
import torch

kv_heads = 4
num_repeats = 4
k_i = torch.arange(kv_heads).view(1, 1, kv_heads, 1)  # fake KV head ids
print(k_i.squeeze())
# tensor([0, 1, 2, 3])

out = k_i.repeat_interleave(num_repeats, dim=2)
print(out.squeeze())
# tensor([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3])
```

So KV head 0 gets duplicated into Q-head slots [0,1,2,3], KV head 1 into [4,5,6,7], etc. This matches how the Q heads are laid out (not interleaved) — Q head index `h` uses KV head `h // num_repeats`.

**Why not `.repeat()` instead:** `repeat` would tile the whole sequence `[0,1,2,3,0,1,2,3,...]` — wrong grouping. `repeat_interleave` gives `[0,0,0,0,1,1,1,1,...]` — correct, because each Q head group needs the *same* KV head repeated, not the whole KV head sequence retiled.

**After the op:** `k_i` shape becomes `(1, kv_len, 16, 128)` — now every Q head has a corresponding (duplicated) K/V head, so you can do plain multi-head attention (matmul Q·Kᵀ per head) without special GQA-aware kernels.

**Cost:** this materializes memory — `num_repeats` copies. Real inference engines (vLLM, FlashAttention-2 GQA kernels) avoid this by broadcasting KV heads virtually inside the kernel instead of physically expanding them. `repeat_interleave` here is the naive/reference implementation — fine for correctness checks, bad for a serving hot path.

**Alternative without extra memory** (broadcast via view + expand, no copy until matmul forces it):

```python
k_i = k_i.unsqueeze(3).expand(1, kv_len, kv_heads, num_repeats, 128).reshape(1, kv_len, 16, 128)
```

Still materializes on `.reshape()` for non-contiguous cases, but at least the intent (broadcast, not repeat) is explicit, and some autograd/kernel paths can fuse it.

If you're writing this for training (not serving), `repeat_interleave` is fine — it's just prepping tensors for a standard `scaled_dot_product_attention` call in eager/GQA-naive mode.
