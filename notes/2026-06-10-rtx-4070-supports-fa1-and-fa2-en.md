---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Supports FA1 and FA2
translated: false
type: note
---

**Question:** Can the RTX 4070 run FlashAttention 1 or 2?

**Answer:**

Yes — both. The RTX 4070 is Ada Lovelace, compute capability **sm_89**, and FlashAttention-2 officially supports Ampere (sm_80/86), Ada (sm_89), and Hopper (sm_90). Only FlashAttention-**3** is out of reach (Hopper-only, uses TMA/WGMMA which Ada lacks).

Two important details for your nanochat setup:

**1. You may already be running FA2 without installing anything.** PyTorch's SDPA (`F.scaled_dot_product_attention`) ships with FlashAttention-2 kernels built in. The "SDPA fallback" message in your log just means the `flash-attn` *package* isn't installed — but SDPA will still dispatch to its internal FA2 kernel if conditions are met (fp16/bf16, head_dim ≤ 256, CUDA tensor, no incompatible mask). Verify what kernel you're actually hitting:

```python
import torch
from torch.nn.attention import SDPBackend, sdpa_kernel

q = torch.randn(1, 6, 1024, 128, device="cuda", dtype=torch.bfloat16)  # (B, H, T, hd) — d12: 768/6 = 128
with sdpa_kernel([SDPBackend.FLASH_ATTENTION]):
    out = torch.nn.functional.scaled_dot_product_attention(q, q, q, is_causal=True)
print("FA2 kernel works on this GPU:", out.shape)
```

If that runs without error, you're getting flash attention already. If your model runs in fp32, that's the real blocker — switch to bf16 (autocast), which you want for training throughput anyway.

**2. Installing the standalone `flash-attn` package** (gives you `flash_attn_func`, varlen support, slightly newer kernels):

```bash
# Avoid the multi-hour source build — use prebuilt wheels
pip install flash-attn --no-build-isolation

# If it tries to compile from source and you have limited RAM:
MAX_JOBS=4 pip install flash-attn --no-build-isolation
```

The compile-from-source path needs `nvcc` (CUDA toolkit matching your PyTorch CUDA version) and can take 30+ min and tens of GB of RAM on your 62 GB box — fine, but check for a matching prebuilt wheel first (they're keyed to torch version + CUDA version + cxx11abi + Python version).

Then in nanochat-style code:

```python
from flash_attn import flash_attn_func
# q, k, v: (B, T, H, head_dim) — note layout differs from SDPA's (B, H, T, hd)
out = flash_attn_func(q, k, v, causal=True)
```

**Practical take for your d12 run:** the gap between PyTorch SDPA's internal FA2 and the standalone package is small (a few %) at 286M scale with T≈1024–2048. The bigger wins are bf16 autocast + `torch.compile`. I'd confirm SDPA is dispatching to the flash backend (snippet above), enable bf16 if not already, and only bother installing `flash-attn` if you profile attention as a real bottleneck.

One caveat: FA1/FA2 head_dim must be ≤ 256 (and on some older FA1 builds, ≤ 128 for sm_89 backward). Your d12 config (768 dim / 6 heads = 128 head_dim) is fine.
