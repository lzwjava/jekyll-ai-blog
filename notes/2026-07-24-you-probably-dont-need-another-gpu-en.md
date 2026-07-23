---
audio: false
generated: true
image: false
lang: en
layout: post
title: You Probably Don't Need Another GPU
translated: false
type: note
---

**Question: Do I need to buy another GPU?**

**Answer:**

Based on your current trajectory (training GPT-2 scale models, running FLUX/Qwen experiments, exploring ROCm/MI300X, LLM infra), the answer is:

**Probably not yet. Buy another GPU only when you hit a specific bottleneck.**

Your current RTX 4070 (12GB VRAM) is actually enough for many valuable experiments:

| Task                               | RTX 4070 12GB | Need another GPU? |
| ---------------------------------- | ------------: | ----------------- |
| Train GPT-2 124M/64M from scratch  |             ✅ | No                |
| Fine-tune 7B with LoRA/QLoRA       |             ✅ | No                |
| Run Qwen3-8B quantized             |             ✅ | No                |
| Learn CUDA/Triton kernels          |             ✅ | No                |
| Build agents/RAG/apps              |             ✅ | No                |
| Train 1B+ dense model from scratch |     ❌ painful | Maybe             |
| Full fine-tune 7B/14B              |             ❌ | Yes               |
| FLUX.2-dev BF16 inference          |             ❌ | Yes               |
| Large multimodal models            |             ❌ | Yes               |

Your recent FLUX issue is the main thing pushing you toward more VRAM:

```
FLUX.2-dev transformer:
~60GB BF16
```

A single 4070 cannot realistically handle that. But buying a GPU just for FLUX is probably not the best ROI.

---

### The next useful upgrade is not "more compute", it is "more VRAM"

Your current limitation:

```
RTX 4070
  12GB VRAM
      |
      +-- model weights
      +-- KV cache
      +-- activations
      +-- optimizer states
```

Modern AI workloads are memory-bound.

A 24GB card changes your world:

```
12GB:
  small models
  LoRA
  learning

24GB:
  QLoRA 7B/14B
  larger diffusion
  serious local inference

48GB:
  professional experimentation

80GB:
  frontier research
```

---

### Options ranked by value

#### Option 1 — Keep RTX 4070 + rent GPUs

Probably best for you.

Example workflow:

Local:

```
RTX 4070
 |
 +-- coding
 +-- experiments
 +-- small training
```

Cloud:

```
MI300X / H100 / A100
 |
 +-- big models
 +-- benchmarking
 +-- production tests
```

You already use AutoDL/RunPod/cloud, so this fits.

---

#### Option 2 — Buy RTX 3090 24GB (used)

Probably the sweet spot.

Why:

```
RTX 3090:
24GB VRAM
936 GB/s memory bandwidth
cheap used market
CUDA ecosystem
```

Compared with 4070:

```
VRAM:
12GB -> 24GB  (2x)

Memory bandwidth:
504 GB/s -> 936 GB/s (~1.85x)
```

For LLM work, this is a huge jump.

You can keep:

```
RTX 4070
+
RTX 3090
```

Then:

* 4070: daily desktop
* 3090: AI box

---

#### Option 3 — RTX 4090

Great but expensive.

```
4090:
24GB
much faster
Ada architecture
```

Better for inference/training, but price/performance is worse than used 3090.

---

#### Option 4 — Pro cards / datacenter cards

Only if you have a concrete reason:

* MI50
* Radeon Pro VII
* A6000
* H100

These are interesting technically but increase friction.

Your goal is shipping AI products, not collecting GPUs.

---

My recommendation for your situation:

```
Now:
RTX 4070
+
cloud GPUs

Next purchase:
used RTX 3090 24GB

Do not buy:
another 12GB card
```

The biggest jump is:

```
12GB → 24GB
```

not:

```
4070 → 4070 Super
```

Your current experiments are already beyond the "need more FLOPS" stage. The constraint you keep hitting is **VRAM capacity**. A 24GB card would remove many artificial limits.

References:

* NVIDIA GeForce RTX 3090 specifications: [https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090/](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090/)
* NVIDIA GeForce RTX 4070 specifications: [https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070/](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070/)
* Hugging Face QLoRA paper: [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)