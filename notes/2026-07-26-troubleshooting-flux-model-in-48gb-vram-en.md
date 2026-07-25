---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting FLUX Model in 48GB VRAM
translated: false
type: note
---

Great question. Here's a breakdown of the problems we hit and how we solved them:

---

## 🔧 What went wrong & what we fixed

### 1. ❌ `pipe.to('cuda')` — OOM crash

**Problem:** The entire model is **~54 GB in bfloat16**. Moving all of it to GPU at once (`pipe.to('cuda')`) tries to cram it into **48 GB VRAM** → instant OOM.

```
HIP out of memory. Tried to allocate 18.00 MiB.
GPU 0 has a total capacity of 47.98 GiB of which 0 bytes is free.
```

**Fix:** Use `pipe.enable_sequential_cpu_offload()` — this keeps most weights in CPU RAM and only moves individual submodules to GPU right before they're needed for computation, then offloads them again.

### 2. ❌ `pipe.enable_model_cpu_offload()` — still OOM

**Problem:** Even with per-module offloading, the **transformer alone** (~20 GB) + its **intermediate activations** (attention states, feed-forward hidden layers) during a 1024×1024 forward pass exceeds 48 GB total.

**Fix:** Also lowered resolution from **1024×1024 → 512×512**. This dramatically reduces activation memory:
- Attention: O(n²) in sequence length — 1024² → 512² is 4× less memory
- Latent channels: proportionally smaller

### 3. ⚠️ APEX JIT compilation (20s each run)

**Problem:** Each run recompiled `fused_layer_norm_cuda` from scratch because the `.so` wasn't cached between runs.

**Fix:** It compiled once (first run took 20s), then cached (`ninja: no work to do.` on second run → 0.7s).

### 4. 🔌 Network: HuggingFace unreachable

**Problem:** Server is in China, `huggingface.co` is blocked. Direct connections timed out.

**Fix:** Used `hf-mirror.com` (HF mirror) as `HF_ENDPOINT`. Without this, we couldn't even check model metadata.

### 5. 🔐 Model is gated

**Problem:** FLUX models require license acceptance + HF token.

**Fix:** User provided a valid token. We saved it to `~/.cache/huggingface/token`.

---

## 🤯 What makes FLUX hard to run

### A. Model is enormous

| Component | Size (bf16) |
|-----------|------------|
| Transformer (DoubleStreamBlock) | ~20 GB |
| T5 text encoder | ~9 GB |
| CLIP text encoder | ~2 GB |
| VAE + AE | ~1 GB |
| **Total** | **~54 GB** |

You can't just load and run — you need **CPU offloading** or **quantization** (8-bit/4-bit). Even 48 GB VRAM isn't enough.

### B. FLUX's architecture is memory-hungry

FLUX uses a **DoubleStreamBlock** architecture where text and image features interact throughout the entire transformer. This means:
- The full transformer must be loaded for every denoising step
- Attention over 4096+ token sequences is O(n²) memory
- No cross-attention separation like Stable Diffusion (which could swap text encoder out)

### C. ROCm still has rough edges

- `flash_attn` doesn't work on ROCm → falls back to PyTorch native SDPA (slower)
- APEX ops need JIT compilation at first run
- `aiter` backend warnings about NUMA balancing
- `amdgpu-coerce-illegal-types=1` flag incompatibility with newer clang

### D. CPU offloading makes it slow

With sequential offload, each step requires:
1. Move transformer weights **CPU → GPU** (PCIe bottleneck)
2. Run forward pass
3. Move results **GPU → CPU**
4. Repeat for next step

That's why 4 steps took **60 seconds** instead of the ~2 seconds it would take on a single H100 with everything in VRAM.

---

## 🏆 Final result: working despite all this

```
Prompt: "A cute cat sitting on a desk, digital art style"
4 steps, 512×512 → 60.3 seconds ✅
```

If you want **faster generation**, we could:
1. Install `bitsandbytes` for 8-bit/4-bit quantization (fits more in VRAM)
2. Use `torch.compile` to fuse operations
3. Disable APEX aiter backend (`USE_ROCM_AITER_ROPE_BACKEND=0`) to avoid the slow path
