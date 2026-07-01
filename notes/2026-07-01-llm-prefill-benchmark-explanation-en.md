---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Prefill Benchmark Explanation
translated: false
type: note
---

**Question:** What does "prefill" mean in the context of LLM inference benchmarks like "LLM prefill (8192x8192): 1,632 TFLOPS"?

**Answer:**

Prefill is the first phase of autoregressive inference — processing the entire input prompt in one forward pass before generation starts. It's distinct from **decode** (generating tokens one at a time after prefill).

### Why 8192x8192 specifically

That's `seq_len x seq_len` — an 8192-token prompt, so the attention matrix is 8192×8192. The benchmark is measuring throughput for a single forward pass over an 8192-token sequence.

### Prefill vs Decode — the key distinction you already care about (KV cache work)

```
Prefill:
  - Input: all N prompt tokens at once
  - Compute: N tokens processed in parallel (one matmul pass)
  - Bottleneck: COMPUTE-bound (large matmuls, high arithmetic intensity)
  - Output: KV cache for all N tokens + first generated token
  - This is why it's measured in TFLOPS — you're compute-bound,
    so FLOPS/sec is the right metric

Decode:
  - Input: 1 new token at a time (using cached K,V from prefill)
  - Compute: batch=1 (or small batch) matvec, not matmul
  - Bottleneck: MEMORY-BANDWIDTH-bound (loading weights + KV cache
    dominates, arithmetic intensity is low)
  - This is why decode is usually measured in tokens/sec, not TFLOPS
```

### Why the distinction matters practically

For an N-token prompt, self-attention cost is O(N²·d) for QK^T and softmax·V. That's why prefill scales quadratically with prompt length and is where you actually saturate the GPU's compute (MI300X's 1,307 TFLOPS BF16 dense — you're seeing 1,632 TFLOPS which implies MFU >100%... that's suspicious unless it's counting sparse/structured FLOPS or it's a vendor peak-marketing number, worth checking the source).

Rough FLOPS estimate for prefill of one 8192-token sequence on a model with `d_model` and `n_layers`:

```python
def prefill_flops(seq_len, d_model, n_layers, d_ff_mult=4):
    # per layer: QKV proj + attn + O proj + FFN
    attn_proj = 4 * seq_len * d_model**2       # Q,K,V,O projections
    attn_scores = 2 * seq_len**2 * d_model     # QK^T and softmax*V
    ffn = 2 * seq_len * d_model * (d_ff_mult * d_model) * 2  # up+down proj
    per_layer = attn_proj + attn_scores + ffn
    return per_layer * n_layers * 2  # x2 for multiply-add

# e.g. a 7B-ish model, seq_len=8192
flops = prefill_flops(seq_len=8192, d_model=4096, n_layers=32)
print(f"{flops/1e12:.1f} TFLOPs total for one prefill pass")
```

Given a GPU's peak TFLOPS/sec, `flops / peak_tflops` gives you the theoretical prefill latency — this is what you'd use to reason about your MI300X's expected time-to-first-token when you're benchmarking your own GPT-2 760M or larger training/inference runs.

The `1,632 TFLOPS` number you quoted is a **measured throughput**, not a fixed cost — it tells you how close the hardware got to peak during that specific 8192×8192 prefill workload, which is the standard way vendors report compute-bound inference performance.

References:

- [MI300X specifications - AMD](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
