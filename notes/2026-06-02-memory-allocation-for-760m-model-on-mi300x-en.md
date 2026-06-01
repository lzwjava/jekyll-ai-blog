---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Allocation for 760M Model on MI300X
translated: false
type: note
---

The 760M model is just small for this GPU. Here's the math:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Where the 63.5 GB goes (760M model, bf16)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model weights (bf16):     760M × 2B  =  1.5 GB
Gradients (bf16):         760M × 2B  =  1.5 GB
Adam states (fp32 m+v):   760M × 8B  =  6.1 GB
Master weights (fp32):    760M × 4B  =  3.0 GB
                           ─────────────────────
Model subtotal:                         ~12 GB

Activations (batch=32, seq=1024, 24 layers):
  Per layer stores attention + FFN intermediates
  for backprop. ~24 layers × 32 × 1024 × 1536 × ...
  Estimated:                          ~30-40 GB

PyTorch compile buffers, HIP runtime, fragmentation:
                                      ~10-15 GB
                           ─────────────────────
Total:                              ~55-65 GB  ✓ matches rocm-smi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MI300X capacity:  192 GB
Used:              63.5 GB  (33%)
Headroom:         128.5 GB  (67%)
```

Why so low? The MI300X is designed for 70B+ models. A 760M model is ~0.4% of the parameter count that fills this GPU. The main VRAM consumers are:

1. **Model weights** — only 1.5 GB for 760M params
2. **Activations** — this is the dominant cost, proportional to batch_size × seq_len × n_layers × n_embd
3. **Optimizer states** — ~4× the model weight size (Adam needs m, v, master weights)

What you could do with the headroom:

- **Increase batch_size** — currently 32 (32K tokens/step). Could go to 64 or 128, which would improve MFU by reducing the ratio of optimizer overhead to compute
- **Train a larger model** — 1.5B, 3B, even 7B would fit comfortably
- **Longer sequences** — increase block_size from 1024 to 2048 or 4096
- **Gradient accumulation** — already at 1, could increase effective batch size

The current 760M config was sized conservatively. If you want to push the hardware harder, bumping batch_size to 64 would be the simplest win — same model, better GPU utilization, faster training per token.