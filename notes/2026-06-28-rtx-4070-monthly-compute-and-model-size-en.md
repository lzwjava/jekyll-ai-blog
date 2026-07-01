---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Monthly Compute and Model Size
translated: false
type: note
---

Question: If an RTX 4070 runs continuously for a month, how much total compute does it produce, and what size model could it train from scratch?

Answer:

Let me work this from first principles — FLOPs budget → Chinchilla token budget → trainable model size.

## 1. Raw compute budget

RTX 4070 (AD104) specs that matter:

| Metric | Value |
| -------- | ------- |
| FP16/BF16 dense (Tensor) | ~29 TFLOP/s (no sparsity) |
| FP16 with 2:4 sparsity | ~58 TFLOP/s (marketing number) |
| TF32 | ~15 TFLOP/s |
| FP8 (Ada supports it) | ~58 TFLOP/s dense |
| VRAM | 12 GB |
| Memory BW | 504 GB/s |

The marketing "~120 AI TOPS" is INT8 with sparsity — irrelevant for training. For BF16 training, your **realistic sustained** number is the killer: kernel efficiency on a single consumer card for transformer training (nanoGPT-style) lands around **35–45% MFU**. Call it 40% of ~29 TFLOP/s ≈ **12 TFLOP/s effective**.

Month of wall-clock:

```python
seconds = 30 * 24 * 3600          # 2,592,000 s
peak_bf16 = 29e12                  # FLOP/s, dense, no sparsity
mfu = 0.40
effective = peak_bf16 * mfu        # 11.6e12 FLOP/s

total_flops = effective * seconds
print(f"{total_flops:.2e} FLOPs")  # ≈ 3.0e19
```

**~3 × 10¹⁹ FLOPs in a month** of nonstop training. (Theoretical peak ceiling, 100% MFU, would be ~7.5e19 — you will never see it.)

## 2. Convert FLOPs → model size (the C ≈ 6ND rule)

The standard training-compute approximation:

$$C \approx 6 \cdot N \cdot D$$

where N = params, D = training tokens. The 6 = 2 (forward) + 4 (backward), per param per token.

Chinchilla-optimal says **D ≈ 20·N**. Substitute:

$$C \approx 6 \cdot N \cdot (20N) = 120 N^2$$

Solve for N:

```python
C = 3.0e19
N = (C / 120) ** 0.5
print(f"{N/1e6:.0f}M params")   # ≈ 500M
D = 20 * N
print(f"{D/1e9:.0f}B tokens")   # ≈ 10B tokens
```

So **compute-optimally, ~500M params on ~10B tokens** is what a month buys you. That's roughly GPT-2 Large (760M) territory but slightly under, trained Chinchilla-style instead of GPT-2's heavily under-tokened regime.

## 3. The real constraint isn't FLOPs — it's the 12 GB VRAM

This is where the AMD MI300X (your other box) and the 4070 diverge hard. Compute-optimal ≠ trainable on the card. Memory for Adam training, per param:

| Buffer | Bytes/param (mixed precision) |
| -------- | ------------------------------- |
| BF16 weights | 2 |
| BF16 grads | 2 |
| FP32 master weights | 4 |
| Adam m | 4 |
| Adam v | 4 |
| **Total** | **~16 bytes/param** |

```python
vram = 12e9
overhead = 0.85          # activations, fragmentation, CUDA context, cuDNN workspace
usable = vram * overhead
N_max = usable / 16
print(f"{N_max/1e6:.0f}M params")  # ≈ 640M (states only, zero activations)
```

But that leaves **nothing for activations**, which for a transformer at seq_len 1024, decent batch, scale with batch×layers×seq×hidden. In practice on a 4070:

- **Naive Adam, no tricks:** ~150–250M params is the comfortable ceiling.
- **8-bit Adam (`bitsandbytes`)**: optimizer states 8→2 bytes, pushes you to ~400–500M.
- **Activation checkpointing + grad accumulation**: lets you actually hit the ~500M FLOP-optimal target, trading ~30% extra compute for memory. This is the combination you'd need.

So the FLOP budget (500M) and the memory budget *can* be reconciled — but only with 8-bit Adam + activation checkpointing + tiny micro-batches + grad accumulation. Without those, you're memory-bound at ~200M and your month of FLOPs goes underutilized.

## 4. Practical recommendation

The honest answer: **a 4070 for a month comfortably trains a ~300–500M dense model to a respectable loss, GPT-2-class.** This is exactly the nanoGPT / Karpathy regime — you've already been in GPT-2 760M territory on the MI300X, so think of the 4070 as "one notch down, and you must fight memory the whole way."

Config that actually fits and uses the month well:

```python
# nanoGPT-style, tuned for 4070 12GB
model = dict(
    n_layer=24, n_head=16, n_embd=1024,   # ~350M params
    block_size=1024, vocab_size=50304,
)
train = dict(
    micro_batch_size=2,
    grad_accum_steps=32,        # effective batch 64
    optimizer="adamw8bit",      # bitsandbytes
    grad_checkpoint=True,
    dtype="bfloat16",
    compile=True,               # torch.compile, ~20-30% throughput on Ada
)
# Target ~7-10B tokens over the month → Chinchilla-ish
```

For anything 760M+ or MoE (DeepSeek-style), the FLOP math alone says months, and the VRAM math says it won't fit at all without offload (ZeRO-Offload/`deepspeed`), which tanks throughput on a single consumer card. **That's MI300X work** — your 192 GB box is where 760M+ and MoE experiments belong. Use the 4070 for fast 100–350M iteration loops where you tune architecture/data and turn experiments around in hours, not for the big runs.

## Summary table

| | FLOP-optimal | Memory-realistic (4070) |
| --- | --- | --- |
| Total compute / month | ~3e19 FLOPs | same |
| Model size | ~500M | ~300–500M (with 8-bit Adam + ckpt) |
| Tokens | ~10B | ~7–10B |
| Without memory tricks | — | ~150–250M ceiling |

References:

- [Training Compute-Optimal LLMs (Chinchilla)](https://arxiv.org/abs/2203.15556)
- [nanoGPT](https://github.com/karpathy/nanoGPT)
- [Reducing Activation Recomputation (activation checkpointing math)](https://arxiv.org/abs/2205.05198)
- [8-bit Optimizers via Block-wise Quantization](https://arxiv.org/abs/2110.02861)
