---
audio: false
generated: true
image: false
lang: en
layout: post
title: "KV Cache: 2 and Layers Multiplier"
translated: false
type: note
---

**Question:** Why is there a `2` multiplier in the KV cache formula, and why multiply by `num_layers`?

**Answer:**

The `2` and `num_layers` are **two separate multipliers**, not a combined factor. Let me break it down:

```
KV cache size = batch_size × seq_len × hidden_dim × 2 × num_layers × bytes
                                                     ↑                  ↑
                                              K + V tensors      one per layer
```

## The `2`: Key and Value Tensors

In multi-head attention, you have **Q, K, V**:

```python
Q = input @ W_q  # Query: computed fresh each step
K = input @ W_k  # Key: reused across all future steps
V = input @ W_v  # Value: reused across all future steps
```

During inference, you only cache **K and V**, not Q. Why?

- **Q is computed only from the current token**, so it's small and ephemeral
- **K and V must be stored for all previous tokens** in the sequence, because:

  ```
  attention(Q_new, K_all, V_all) = softmax(Q_new @ K_all.T / sqrt(d)) @ V_all
  ```

  When predicting token 100, you need K and V from tokens 1-99. So the `2` accounts for both K and V.

## The `× num_layers`: Every Attention Layer Stores Its Own Cache

A transformer model has many layers (e.g., 40 for 13B), and **each layer has independent K and V caches**:

```
Layer 1: K_cache_1 (batch, seq_len, hidden_dim)
         V_cache_1 (batch, seq_len, hidden_dim)
Layer 2: K_cache_2 (batch, seq_len, hidden_dim)
         V_cache_2 (batch, seq_len, hidden_dim)
...
Layer 40: K_cache_40 (batch, seq_len, hidden_dim)
          V_cache_40 (batch, seq_len, hidden_dim)
```

Total = `2 * 40 = 80` cache tensors.

## Concrete Example

For a **13B model** (typically ~5120 hidden_dim, ~40 layers):

```python
batch_size = 32
seq_len = 4096
hidden_dim = 5120
num_layers = 40
bytes = 2  # fp16

# Per layer: batch × seq × hidden = 32 × 4096 × 5120 = 671M elements
# K cache per layer: 671M × 2 bytes = 1.3 GB
# V cache per layer: 671M × 2 bytes = 1.3 GB
# Both per layer: 2.6 GB
# Total × 40 layers: 104 GB
```

So when you see **52 GB** (my earlier example), it's actually the full KV cache across all layers for one batch.

## Why This Matters

This is why KV cache becomes the **hard limit** on batch size during inference:

```python
max_batch_size ≈ available_memory / (2 × num_layers × seq_len × hidden_dim × bytes)
```

On MI300X (192 GB):

```
max_bsz ≈ 192GB / (2 × 40 × 4096 × 5120 × 2 bytes)
        ≈ 192GB / 3.3GB per token position
        ≈ ~58 batch size at full sequence
```

This is why **MQA (Multi-Query Attention)** and **GQA (Grouped-Query Attention)** help—they reduce `hidden_dim` in the cache:

```
# Standard MHA: K and V are (batch, seq, hidden_dim)
# GQA: K and V are (batch, seq, hidden_dim // num_groups)
# MQA: K and V are (batch, seq, hidden_dim // num_heads)  [extreme case]
```

Reducing the cache size by 8-12x lets you fit much larger batches.
