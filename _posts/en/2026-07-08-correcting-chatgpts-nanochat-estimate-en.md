---
audio: false
generated: true
image: false
lang: en
layout: post
title: Correcting ChatGPT's nanochat estimate
translated: false
type: note
---

Question: Is the ChatGPT-generated estimate for training a nanochat-760M-scale model to 7.6B/14B tokens on an RTX 4070 correct?

Answer:

Mostly right in structure, wrong on two numbers that matter. Let me show you where, with real nanochat data pulled from Karpathy's own discussion threads.

## Error 1: RTX 4070 tensor peak is ~58 TFLOPS FP16, not 29

29 TFLOPS is the RTX 4070's **CUDA-core FP32/FP16** shader throughput. The **4th-gen Tensor Core dense FP16** peak (what actually matters for `torch.compile`'d transformer training) is roughly double that:

```
184 tensor cores × 256 FLOP/cycle × 2.475 GHz ≈ 58.3 TFLOPS (dense, no sparsity)
```

Using 29 TFLOPS as "peak" and then applying an MFU discount on top of an already-halved number double-penalizes the estimate.

## Error 2: nanochat's real d20 checkpoint is 561M params, not 760M

There's no official 760M nanochat depth. Pulling actual numbers from Karpathy's GitHub discussions:

```
d20: 560,988,160 params | 3.491758e9 FLOPs/token | 11.2B tokens | 3.92e19 total FLOPs
d32: 1,879,048,192 params | 1.207960e10 FLOPs/token | 37.6B tokens | 4.54e20 total FLOPs
```

That gives an empirical FLOPs/token-per-param ratio of `3.49e9 / 561e6 ≈ 6.22`, consistent with the standard `C ≈ 6N` per-token training FLOPs approximation. Using that ratio, a 760M model (closest real depth ≈ d22) needs:

```python
ratio = 3.491758e9 / 560_988_160  # 6.224 FLOPs/token per param, from real d20 run
n_params = 760e6
flops_per_token = ratio * n_params  # 4.73e9

for tokens in [7.6e9, 14e9]:
    total_flops = flops_per_token * tokens
    peak = 58.29e12  # dense FP16 tensor peak, RTX 4070
    for mfu in [0.15, 0.35]:
        eff = peak * mfu
        secs = total_flops / eff
        print(f"{tokens/1e9:.1f}B tok, mfu={mfu:.0%}: {secs/3600:.0f}h ({secs/86400:.1f}d)")
```

```
7.6B tok, mfu=15%:  1143h (47.6d)
7.6B tok, mfu=35%:   489h (20.4d)
14.0B tok, mfu=15%:  2105h (87.7d)
14.0B tok, mfu=35%:  902h (37.6d)
```

So realistically: **~20–48 days for 7.6B tokens, ~38–88 days for 14B tokens** — the MFU assumption is the dominant uncertainty, not the tokens/params math, and I'd anchor toward the low end (15-20%) rather than 35% for a single consumer card with gradient accumulation and small microbatches. A real single-GPU data point from the nanochat discussion threads: someone running on a DGX Spark (newer, faster silicon than a 4070) only hit **5.6% MFU** at 17.5k tok/sec — small-batch, VRAM-constrained single-GPU training on this codebase runs well below the 50%+ MFU Karpathy gets on tuned 8×H100 clusters. If your actual measured tok/sec ends up nearer that, add another 2-3x to both ranges above.

## Error 3: the VRAM/quantization framing is borrowed from the wrong model size

Your own d32 post correctly says the 1.9B d32 model needs 4-bit quant tricks to fit in 12GB — but a 760M model doesn't need that:

```
BF16 weights:  760M × 2B = 1.52 GB
Gradients:     760M × 2B = 1.52 GB
AdamW m+v:     760M × 8B = 6.08 GB
-----------------------------------
states total: ~9.1 GB, leaves ~2.9 GB for activations on a 12GB card
```

That's tight but workable with gradient checkpointing + a small microbatch (e.g. 4×2048) and grad accumulation — no need to drop to 4-bit pretraining (which isn't really how nanochat trains anyway; that framing in the earlier answer was conflating QLoRA-style fine-tuning quantization with from-scratch pretraining, which don't use the same numerics).

## Bottom line

| Tokens | Corrected estimate (RTX 4070, BF16, no quant needed) |
| --- | --- |
| 7.6B | ~3–7 weeks |
| 14B | ~5–13 weeks |

Same conclusion as the original ("4070 + nanochat = viable for a single meaningful run, iterate on H100/MI300X for anything requiring many ablations") but the arithmetic underneath had a 2x peak-FLOPs error and borrowed VRAM-pressure numbers from the wrong model size.

References:

- [$1000 tier nanochat run · karpathy/nanochat Discussion #8](https://github.com/karpathy/nanochat/discussions/8)
- [NVIDIA Spark training thread · karpathy/nanochat Discussion #28](https://github.com/karpathy/nanochat/discussions/28)
- [NVIDIA GeForce RTX 4070 AI Performance Specs — WareDB](https://www.waredb.com/processor/nvidia-geforce-rtx-4070)
- [Training nanochat d32 on RTX 4070 — lzwjava.github.io](https://lzwjava.github.io/nanochat-d32-rtx4070-en)
