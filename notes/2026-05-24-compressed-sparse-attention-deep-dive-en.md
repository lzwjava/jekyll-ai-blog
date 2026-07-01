---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compressed Sparse Attention Deep Dive
translated: false
type: note
---

**Question:** Deep-dive into Compressed Sparse Attention (CSA) from DeepSeek-V4 — how does it work from first principles, including the compressor, lightning indexer, and how it compares to the predecessor sparse attention in V3.2?

**Answer:**

## CSA: Compressed Sparse Attention in DeepSeek-V4

Let me build this from the ground up — from why standard attention breaks at 1M tokens, through every component of CSA, to what it costs and saves.

---

### Why Vanilla Attention Can't Scale to 1M Tokens

Standard multi-head attention has two scaling problems:

1. **Compute**: `O(N²·d)` per layer — at 1M tokens, that's `10¹²` operations per layer per forward pass.
2. **KV cache memory**: For each layer you store `K ∈ ℝ^{N×d_k}` and `V ∈ ℝ^{N×d_v}`. At 1M tokens, 61 layers, bf16 — this is hundreds of GBs.

At inference, every new token attends over the full `N`-length KV cache. The KV cache is the binding constraint for long-context agents, not compute.

The prior art answer was **sparse attention** (V3.2's DeepSeek Sparse Attention): don't attend to all `N` positions, only top-k selected ones. But the indexer that does the selection still has to score against all `N` KV entries — just to decide which ones to skip. Selection is itself `O(N)`.

CSA's key insight: **compress first, then sparsify**. The indexer's search space shrinks 4x before it ever runs.

---

### CSA in Three Components

#### 1. The Compressor (4x sequence pooling)

Every 4 consecutive token positions are collapsed into a single compressed KV entry:

```
[t₁, t₂, t₃, t₄] → one compressed KV block
```

The compression is **softmax-gated pooling with a learned positional bias**. Concretely, for a block of 4 hidden states `H ∈ ℝ^{4×d}`:

```python
# Learned per-position bias (shared across all blocks, just encodes intra-block position)
pos_bias = learned_param  # shape: (4,)

# Gating weights via softmax over the 4 positions
gates = softmax(pos_bias)  # shape: (4,)

# Weighted sum = one compressed representation
compressed = einsum('p, p d -> d', gates, H)  # shape: (d,)
```

This is a **trainable pooling operation** — not mean pooling, not max pooling. The model learns which positions within a 4-token window carry the most information for compression. The positional bias is lightweight (just 4 scalars) but shared, so it generalizes.

After this step, your KV cache has `N/4` entries instead of `N`. For 1M tokens, that's 250K compressed blocks.

The compressor is applied to produce **compressed K and V** separately. The resulting `K_c ∈ ℝ^{N/4 × d_k}` and `V_c ∈ ℝ^{N/4 × d_v}` are stored in **FP8** (not bf16), which halves memory again relative to standard precision.

---

#### 2. The Lightning Indexer (FP4, ReLU-scored block selection)

Given a query `q ∈ ℝ^{d_k}`, the indexer scores all `N/4` compressed key blocks to pick the top-k most relevant ones. This is where the "lightning" comes from — it runs in **FP4** precision with **ReLU activation instead of softmax**:

```python
# FP4 quantized query and compressed keys
q_fp4 = quantize_fp4(q)
K_c_fp4 = quantize_fp4(K_c)  # shape: (N/4, d_k)

# Score each compressed block (multi-head dot product)
scores = relu(q_fp4 @ K_c_fp4.T)  # shape: (N/4,)
# Note: ReLU not softmax — kills negatives, keeps positives, no normalization needed

# Pick top-k blocks
top_k_indices = argsort(scores)[-k:]
```

Why ReLU instead of softmax for indexing?

- Softmax normalizes, which means low scores can still "win" in a sparse field. ReLU naturally zeros out irrelevant blocks — if the dot product is negative, the block is simply excluded.
- FP4 is enough precision to rank blocks, not to compute final attention weights. The indexer is a **coarse filter**, not the attention mechanism itself.
- This runs extremely fast — FP4 dot products on modern hardware (H100, MI300X) are 2-4x cheaper than FP8, and 4-8x cheaper than bf16.

The indexer selects top-k compressed blocks. Only those blocks' corresponding **original uncompressed** KV entries (4k original positions) participate in the actual attention computation.

---

#### 3. The Full Attention Pass (with sliding window for recency)

CSA runs **two parallel branches** per layer:

```
Query q
  ├─ [Lightning Indexer] → top-k compressed blocks → [Attention over k×4 original KVs]
  └─ [Sliding Window] → last W tokens (uncompressed) → [Local Attention]

Output = combine(sparse_global_attn, local_attn)
```

The sliding window handles recency — tokens in the last W positions aren't compressed yet (or their compression hasn't been flushed), so they need direct attention. This is the same local attention trick from Longformer/Mistral sliding window, but here it's a **complement** to the compressed sparse global attention, not the whole mechanism.

The final attention output combines both branches (typically via concatenation then projection, or learned gating).

---

### Contrast: V3.2 Sparse Attention vs. V4 CSA

| | V3.2 DeepSeek Sparse Attention | V4 CSA |
| --- | --- | --- |
| Index over | Full `N` KV entries | `N/4` compressed blocks |
| Indexer precision | FP8 or bf16 | **FP4** |
| Indexer activation | softmax or dot | **ReLU** |
| KV storage | FP8 | FP8 (compressed), so 4x fewer entries |
| Effective search space | `N` | `N/4` |
| Cache footprint reduction | ~sparse fraction | **~25x** (4x compression × ~6x from FP8 vs bf16 GQA baseline) |

The core innovation: V3.2 did sparse selection over the raw sequence. V4 does sparse selection over an already-compressed sequence. The indexer itself becomes 4x cheaper to run, and the KV cache that needs to be materialized per selected block is smaller.

---

### HCA as the Other Half

CSA is interleaved with **Heavily Compressed Attention (HCA)** — same idea but 128x compression and **no sparse selection** (dense attention over all `N/128` blocks). At 128x, the compressed sequence is short enough that `O((N/128)²)` dense attention is cheap.

In V4-Pro's 61-layer stack, layers 0–1 are HCA, layers 2–60 alternate CSA and HCA, and the MTP block at the end runs sliding-window only.

This interleaving is principled: different layers develop different attention patterns during training. HCA layers learn coarse, global context. CSA layers learn fine-grained sparse retrieval over that coarser summary.

---

### What This Buys You in Numbers

At 1M tokens, DeepSeek-V4-Pro requires 27% of single-token inference FLOPs compared with DeepSeek-V3.2, and 10% of the KV cache memory. V4-Flash drops these to 10% of the FLOPs and 7% of the KV cache. Compared against grouped query attention with 8 heads in bfloat16, DeepSeek-V4 requires roughly 2% of the cache size.

The 2% KV cache figure compounds from three independent multipliers:

- **4x** from CSA sequence compression
- **~4x** from FP8 vs bf16 storage
- **~4x** from sparse selection (only materializing top-k blocks)

These multiply, not add.

---

### Minimal Pseudocode for the Full CSA Forward Pass

```python
def csa_forward(q, K_full, V_full, k_blocks=64, window=512):
    N, d = K_full.shape

    # 1. Compress KV cache: N → N/4
    K_c, V_c = compress_kv(K_full, block_size=4)  # (N/4, d) each, stored FP8

    # 2. Lightning indexer: score compressed blocks in FP4 with ReLU
    scores = relu(quantize_fp4(q) @ quantize_fp4(K_c).T)  # (N/4,)
    top_k_block_indices = topk(scores, k=k_blocks)         # (k_blocks,)

    # 3. Gather original KV for selected blocks (4 original tokens per block)
    selected_positions = expand_blocks(top_k_block_indices, block_size=4)  # (k_blocks*4,)
    K_sel = K_full[selected_positions]  # (k_blocks*4, d)
    V_sel = V_full[selected_positions]

    # 4. Global sparse attention over selected positions
    attn_global = softmax_attention(q, K_sel, V_sel)

    # 5. Local sliding window attention (recency)
    K_local = K_full[-window:]
    V_local = V_full[-window:]
    attn_local = softmax_attention(q, K_local, V_local)

    # 6. Combine
    return merge(attn_global, attn_local)

def compress_kv(K, block_size=4):
    N, d = K.shape
    K_blocked = K.reshape(N // block_size, block_size, d)
    # Learned positional bias (4 scalars)
    gates = softmax(learned_pos_bias)  # (block_size,)
    K_compressed = einsum('b p d, p -> b d', K_blocked, gates)
    return quantize_fp8(K_compressed)
```

---

### The Key Insight Worth Internalizing

CSA is a **two-level index** like a B-tree or ANN index — compress to get a cheap-to-search summary, search the summary to find candidates, then retrieve the full-resolution entries for those candidates only. The innovation isn't any single component; it's that **compression, indexing, and retrieval form a pipeline where each stage is tuned to the next stage's precision requirements** (FP4 indexer → FP8 storage → bf16 final attention).

This is architecturally analogous to HNSW or IVF in vector databases — coarse quantization for fast neighbor search, then rerank with full precision. DeepSeek applied this retrieval systems intuition directly to the attention mechanism.

---

References:

- [DeepSeek-V4: a million-token context that agents can actually use (HuggingFace Blog)](https://huggingface.co/blog/deepseekv4)
- [DeepSeek-V4 Technical Report (PDF)](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
