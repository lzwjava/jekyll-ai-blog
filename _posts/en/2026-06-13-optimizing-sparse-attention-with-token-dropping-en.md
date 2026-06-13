---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Sparse Attention with Token Dropping
translated: false
type: note
---

**Question:** Explain deeply the techniques described in this document — Output-Aware Token Dropping (OAM-based), Dynamic Load Balancing for Attention Kernels on Blackwell, and INT8 KV Cache Quantization schemes.

**Answer:**

---

## 1. The Core Problem: Sparse Attention and What "Token Dropping" Means

In full attention, every query attends to every key: O(n²) complexity. For 128K context, that's 128K × 128K = 16B pairs per layer. Impractical at inference time.

**Sparse attention** fixes this by only computing attention for a *subset* of tokens. The question is: **which tokens do you keep?**

---

## 2. Traditional Token Selection: Q×K Score (The Problem)

Classic sparse attention ranks tokens by their attention logit:

```
score(q, k_i) = q · k_i / sqrt(d_k)
```

Then you take the top-K tokens by this score. Simple, but this has a **fundamental flaw**:

> The Q×K score is a *routing probability* — it measures geometric alignment between query and key. It does **not** measure how much that token's *value* contributes to the output.

Concretely: the attention output is

```
out = sum_i [ softmax(q · k_i / sqrt(d)) * v_i ]
```

A token with a high `q · k_i` score might have `v_i ≈ 0` (tiny value vector). You kept it for nothing. Conversely, a token with moderate `q · k_i` might have a massive `|v_i|` — dropping it destroys output quality.

---

## 3. OAM: Output-Aware Metric — The Fix

The key insight: **score each token by its actual contribution to the output**, not just its key-query alignment.

The contribution of token `i` to the output is approximately:

```
contribution_i ≈ softmax(q · k_i) * |v_i|
```

Or in log-space (more numerically stable):

```
log_contribution_i = (q · k_i) + log|v_i|
```

This is the **BetaMax-based log evaluation** referenced in the doc. "BetaMax" likely refers to a max-normalized log-softmax approximation — instead of computing full softmax (which requires all tokens), you use a local approximation:

```python
# Pseudocode for OAM score
def oam_score(q, k_i, v_i):
    routing_score = q @ k_i / sqrt(d_k)          # standard attention logit
    value_magnitude = torch.log(v_i.norm() + eps) # |v_i| contribution
    return routing_score + beta * value_magnitude  # beta is a learned or fixed weight
```

Then you drop tokens with the **lowest OAM score** instead of lowest `q·k` score.

**Why this is principled:** You're approximating the upper bound of each token's output contribution before actually computing softmax. This is closely related to the idea behind **Reformer** (LSH attention) and **Mamba's selective state spaces** — the selector should know *what matters downstream*, not just *what looks similar*.

---

## 4. The "Slim" Implementation Result

The 3.6x throughput on 128K inputs makes sense:

- At 128K sequence length, full attention = 128K² ops per head
- If OAM drops 90% of tokens → effective context = 12.8K per query
- Compute reduction: ~10x in attention, less in practice due to overhead
- 3.6x end-to-end is realistic because attention is only one bottleneck (FFN, memory bandwidth also matter)

---

## 5. Dynamic Load Balancing for Attention Kernels (Blackwell / H20)

### The Problem: Thread Divergence from Variable Sequence Lengths

In batched inference, sequences have different lengths. When you tile the KV cache across thread blocks (CTA/SM), one sequence might be 128K tokens while another is 512. The CTA handling the long sequence does 250x more work — all other CTAs finish and **sit idle** (warp stall).

This is the **load imbalance problem** in attention kernels, well-known from FlashAttention-2 → FlashAttention-3 evolution.

### Split-KV Approach

The fix: **Split the KV dimension across multiple CTAs**, then reduce:

```
Sequence of length L → split into N chunks of L/N
Each chunk handled by one CTA
Final output = online softmax reduction across chunks (log-sum-exp trick)
```

This is exactly what **FlashAttention-3** does with its "persistent kernel + work stealing" scheduler, and what **vAttention/PagedAttention** variants implement.

The reduction still uses the numerically stable online softmax:

```python
# Online softmax across splits
m_new = max(m_prev, m_chunk)
exp_sum = exp(m_prev - m_new) * exp_sum_prev + exp(m_chunk - m_new) * exp_sum_chunk
out = (exp(m_prev - m_new) * out_prev * exp_sum_prev + out_chunk * exp_sum_chunk) / exp_sum
```

Result: **1.5x kernel speedup**, 1% end-to-end. The small end-to-end gain means attention wasn't the dominant bottleneck for their workload (likely compute-bound at shorter contexts, memory-bound at longer ones).

---

## 6. INT8 KV Cache Quantization: Two Schemes

### Why INT8 KV Cache?

KV cache is the memory bottleneck at long context. For a 70B model with 128K context:

```
KV cache size = 2 * n_layers * n_heads * d_head * seq_len * bytes_per_element
             = 2 * 80 * 64 * 128 * 128000 * 2 (BF16)
             ≈ 210 GB  ← doesn't fit on one B200 (192GB HBM3)
```

INT8 halves this to ~105 GB. Worth it if accuracy holds.

### Per-Tensor Static Quantization (Baseline — The Problem)

```
q_val = round(val / scale)   # scale is a single float per tensor
val_reconstructed = q_val * scale
```

One `scale` for the entire Q, K, or V tensor. Fast (one multiply to dequantize), but **catastrophic for long context**:

- At 128K tokens, the *range* of K/V values spans many orders of magnitude
- A single scale can't represent both small and large values accurately
- Quantization error accumulates over 80 layers → agent tasks fail (they maintain long history)

### Scheme A: Fine-Grained QK (Best Accuracy, Some Cost)

```
Per-token-partition quantization for Q and K:
  Each "partition" (e.g., 64 or 128 tokens) gets its own scale
  scale[i] = max(|k[i*chunk:(i+1)*chunk]|) / 127

V uses per-tensor (one global scale)
```

Why Q and K are most sensitive: the `softmax(QK^T)` is exponential — small errors in Q or K get amplified. V enters linearly, so coarser quantization is tolerable.

### Scheme B: Coarser KV (Near-Zero Perf Loss)

```
Q: per-token-partition (fine)
K: per-tensor (coarse)
V: per-tensor (coarse)
```

Trades some accuracy for performance. Both schemes are "essentially lossless" because INT8 with properly calibrated scales has ~0.4% relative error — within noise for most benchmarks.

### The Accuracy/Throughput Tradeoff Visualized

```
Scheme          | Q scale    | K scale    | V scale    | Accuracy | Perf
----------------|------------|------------|------------|----------|------
Baseline INT8   | per-tensor | per-tensor | per-tensor | degraded | fastest
Scheme B        | per-token  | per-tensor | per-tensor | good     | ~baseline
Scheme A        | per-token  | per-token  | per-tensor | best     | ~5-15% slower
BF16 (full)     | n/a        | n/a        | n/a        | perfect  | 2x memory
```

---

## 7. How These Three Fit Together

```
Inference request (128K context)
         │
         ▼
OAM Token Dropping ──► reduce effective KV to attend over (3.6x compute reduction)
         │
         ▼
INT8 KV Cache ──────► halve memory bandwidth for KV reads
         │
         ▼
Split-KV Load Balance ► evenly distribute remaining KV work across SMs
         │
         ▼
Output
```

They're orthogonal optimizations that stack: OAM reduces *which* tokens you process, INT8 reduces *how expensive* each token read is, and Split-KV reduces *idle time* from imbalance.

---

## Connections to What You're Already Working On

Given you're training on MI300X and studying DeepSeek v4 MoE:

- **OAM is directly relevant to MoE inference**: in MoE, token routing also uses a score that doesn't consider output magnitude. The same argument applies — you could weight expert routing by the expert's output norm, not just gate score. This is an open research direction.
- **INT8 KV quantization**: when you run 128K context inference on your RTX 4070 (12GB), this is *why* it OOMs — unquantized KV. Try `llama.cpp` with `-cache-type-k q8_0 -cache-type-v q8_0` for Scheme B equivalent on local models.
- **Split-KV**: FlashAttention-3's `tile_scheduler` does exactly this. Worth reading the FA3 paper alongside this.
