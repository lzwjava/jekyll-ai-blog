---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX Models for RTX 4070
translated: false
type: note
---

Question: What FLUX models can an RTX 4070 (12 GB VRAM) realistically run?

Answer:

For an RTX 4070 (12 GB VRAM), the limiting factor is **VRAM**, not compute. FLUX models are transformer-heavy, and the text/image transformer dominates memory usage.

Here's a practical summary:

| Model          | RTX 4070 12GB           | Notes                                            |
| -------------- | ----------------------- | ------------------------------------------------ |
| FLUX.1 Schnell | ✅ Good                  | Best choice. Fast, designed for consumer GPUs.   |
| FLUX.1 Dev     | ⚠️ Yes, with offloading | Slow due to CPU offload; low VRAM mode required. |
| FLUX.1 Pro     | ❌ No                    | Closed API model. Cannot run locally.            |
| FLUX.2 Dev     | ❌ No                    | Transformer alone is far larger than 12GB.       |
| FLUX.2 Pro     | ❌ No                    | Cloud/API only.                                  |

You actually encountered this already with FLUX.2:

> Transformer ≈ **60 GB BF16**

That means even a **48 GB** GPU cannot hold the model without aggressive sharding/offloading. A 12 GB RTX 4070 is far below that.

### What works well

For image generation:

```text
RTX 4070
    ↓
FLUX.1 Schnell
    ↓
1024×1024
20–30 steps
≈10–20 s/image
```

This is the sweet spot.

---

For FLUX.1 Dev:

```python
pipe.enable_model_cpu_offload()
```

or

```python
pipe.enable_sequential_cpu_offload()
```

It works, but generation becomes much slower because weights continuously move between CPU RAM and GPU VRAM.

---

## Quantized versions

Community projects have produced GGUF and other quantized FLUX.1 models that run through:

* llama.cpp
* ComfyUI
* Forge WebUI

Examples include:

* Q4
* Q5
* FP8

These reduce VRAM significantly. A 12 GB 4070 can often run quantized FLUX.1 Dev with acceptable speed and image quality, making them much more practical than the original BF16 checkpoints.

---

## If your goal is understanding FLUX

Since you're interested in studying frontier models rather than just generating images, I'd recommend this progression:

1. **FLUX.1 Schnell** — understand the inference pipeline.
2. **FLUX.1 Dev** — inspect architecture and transformer blocks.
3. Study the DiT implementation and MMDiT components in the codebase.
4. Read the FLUX.2 papers/blogs to understand architectural changes rather than trying to run FLUX.2 locally.

Running FLUX.2 locally really starts to make sense with hardware like:

* RTX 5090 (32 GB)
* H100 (80 GB)
* MI300X (192 GB)
* Multi-GPU setups

A single RTX 4070 is simply not the target hardware for FLUX.2.

References:

* [Black Forest Labs](https://blackforestlabs.ai?utm_source=chatgpt.com)
* [FLUX GitHub (official inference examples)](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)