---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash Attention 3 Requires Hopper GPUs
translated: false
type: note
---

**Question:** Why isn't Flash Attention 3 available on my setups, and do I need an H100/H200 (or RTX 4070) to get it working?

**Answer:**

## The Hardware Requirement

Flash Attention 3 is optimized for Hopper GPUs (H100/H800) with CUDA >= 12.3. This isn't arbitrary—the entire algorithm depends on SM90-specific features:

- **Warp specialization** — splitting producer/consumer warps to overlap compute and data movement asynchronously
- **TMA (Tensor Memory Access)** — Hopper's async memory prefetch unit
- **Async pipeline hardware** — FP8 block quantization with incoherent processing

**Your RTX 4070 is Ada Lovelace (SM89), not Hopper (SM90).** FA3's warp specialization and async data pipelining require Hopper's SM90 architecture; the flash-attn package installs on A100 (SM80) and L40S (SM89) without errors, but the FA3 compute path does not activate.

Even worse for macOS: Apple Silicon (M2) doesn't support CUDA at all—you get PyTorch's Metal Performance Shaders (MPS) fallback, which uses standard `scaled_dot_product_attention` without any Flash variant.

## What You Actually Have

| GPU | Architecture | Flash Support | Status |
| ----- | -------------- | --------------- | -------- |
| M2 MacBook | Apple Silicon | None (MPS SDPA) | CPU/fallback only |
| RTX 4070 | Ada (SM89) | **Flash Attention 2** | Full support ✓ |
| MI300X | RDNA3 | **Flash Attention 2** | Via ROCm composable_kernel ✓ |

## Flash Attention 2 vs 3 Trade-offs

You **don't need** FA3 for productive nanochat training. Here's why:

- **FA2 gains**: 2x speedup over standard attention, 5-20x memory savings
- **FA3 over FA2**: 1.5-2x additional speedup (on H100 only), mainly useful for 200K+ context windows

For 4K-8K context (what nanochat uses), FA2 on RTX 4070 is excellent. You're limited by:

1. VRAM (12GB) → batch size/sequence length
2. PCIe bandwidth, not attention kernel efficiency

## Practical Path Forward

**Don't chase FA3.** Instead:

### On RTX 4070 — enable Flash Attention 2

```bash
# Install flash-attention for Ada
pip install flash-attn --no-build-isolation

# In nanochat training config, ensure:
# - attn_impl="flash_attention_2"
# - PyTorch >= 2.2
# - CUDA >= 12.0
```

Check it works:

```python
import torch
print(torch.backends.cuda.is_available())

# Check attention backend
from torch.nn.functional import scaled_dot_product_attention
# FA2 activates automatically on Ada GPUs in PyTorch 2.2+
```

### On MI300X — ROCm Flash Attention 2

```bash
# In ROCm PyTorch container:
pip install flash-attn

# ROCm uses composable_kernel backend (not FA3)
# Still gives 2x speedup, perfect for 192GB HBM3
```

### On M2 MacBook — accept the limitation

```bash
# torch.backends.mps.is_built() = True, but no Flash kernels
# MPS SDPA is memory-efficient enough for inference/small finetuning
# For serious training → use RTX 4070 or MI300X
```

## Why FA3 Still Matters (Future Context)

Flash Attention 2 achieves only 35% utilization on the H100 GPU, while Flash Attention 3 achieves 75-85% utilization on the same hardware. This becomes critical if you:

- Train 1M-token context models
- Run inference with batched 128K+ sequences
- Need sub-ms latency at scale

For now on your RTX 4070: **FA2 is the ceiling**. If you need FA3's perf, you'd need H100/H200 access (rent via Lambda Labs, Modal, or use AMD Dev Cloud which you already have).

## Recommendation for nanochat

Your AMD MI300X is actually better positioned than RTX 4070 for this project—192GB HBM3 + FA2 support means you can train 7B-13B models with 8K context without VRAM pressure. Use that for pretraining/SFT, keep RTX 4070 for experimentation.

---

**References:**

- GitHub: Dao-AILab/flash-attention (official implementation)
- Spheron Blog: FlashAttention 2 vs 3 (2026 migration guide)
- Tri Dao's blog: FA3 design rationale
