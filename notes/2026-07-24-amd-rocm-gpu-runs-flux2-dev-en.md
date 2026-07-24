---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm GPU Runs FLUX.2-dev
translated: false
type: note
---

Here's the full picture:

---

## ✅ GPU Confirmed — AMD ROCm

| Component | Details |
|-----------|--------|
| **GPU** | **gfx1100** (RDNA 3 arch) — likely AMD Radeon PRO W7900 or cloud-partitioned Instinct |
| **VRAM** | **48 GB** (Samsung) |
| **ROCm** | v7.2.1 (HIP 7.2.53211) |
| **Driver** | v6.16.13 |
| **PCIe** | Gen4 x16 @ 16GT/s |
| **Power** | 241W cap, currently 17W |
| **OS** | Ubuntu 24.04, Python 3.12.3 |
| **CPU** | AMD EPYC 9334 — 128 threads |
| **RAM** | 503 GB |

## 📦 PyTorch (ROCm 7.2) Available

Official PyTorch wheels with ROCm 7.2 support exist on PyTorch's index:

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm7.2
```

Available versions: `2.13.0+rocm7.2` (latest), `2.12.1`, `2.12.0`, `2.11.0`

## 🎨 Can FLUX.2-dev Run on This?

**Yes, absolutely.** Here's the breakdown:

### FLUX.2-dev VRAM Requirements

| Component | Est. Size | Notes |
|-----------|-----------|-------|
| Text Encoder (T5-XXL) | ~10 GB | Loaded once, usually fp16 |
| Transformer (flux2-dev) | ~12-16 GB | bf16 weights |
| VAE | ~1 GB | Tiny |
| **Total to run** | **~25-30 GB** | At default 1024×1024 |
| Inference overhead | ~2-4 GB | Intermediate activations |

### You Have 48 GB → ✅ More than enough

Headroom for **higher resolutions** (e.g. 1536×1536) or **larger batch sizes**.

### Expected Performance

| Hardware | Time per image at 1024×1024 (4-step schnell / 28-step dev) |
|----------|----------------------------------------------------------|
| Your GPU (RDNA 3, 48 GB) | ~3-10 sec/image (estimate, similar to RX 7900 XTX) |
| NVIDIA A100 (80 GB) | ~2-5 sec |
| CPU-only (128 cores) | Several minutes |

### ⚠️ One Catch

**FLUX.2-dev is a gated model** — you need a HuggingFace token (must accept the license on huggingface.co first) to download it.

---

Want me to **install PyTorch + diffusers** on the server and test FLUX inference? I'd need to:

1. `pip install torch --index-url https://download.pytorch.org/whl/rocm7.2`
2. `pip install diffusers transformers accelerate sentencepiece`
3. Log in with your HF token and download FLUX.2-dev
