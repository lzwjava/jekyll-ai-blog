---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 + 4070 Training Limits
translated: false
type: note
---

Question: **With 2–3× NVIDIA M40 cards and 1× RTX 4070, how far can you go for training models?**

---

Answer:

This is a nuanced setup — lots of VRAM on paper, but with serious caveats. Here's a full breakdown:

---

## ⚠️ Critical Warning: M40 PyTorch Support Is Ending NOW

As of September 4, 2026, PyTorch announced that **PyTorch 2.14 is the last release to ship any CUDA 12.6 wheels**. Starting with PyTorch 2.15, Maxwell (SM 5.0), Pascal (SM 6.0), and Volta (SM 7.0) are **fully dropped**.

The M40 is Maxwell (SM 5.2). This means: **you must pin to PyTorch ≤ 2.14 + CUDA 12.6** to use the M40 at all. Modern frameworks (Unsloth, newer HuggingFace TRL versions, etc.) may stop working.

---

## GPU Spec Comparison

| | M40 (×2 or ×3) | RTX 4070 |
| --- | --- | --- |
| Architecture | Maxwell (SM 5.2) | Ada Lovelace (SM 8.9) |
| VRAM each | 24 GB GDDR5 | 12 GB GDDR6X |
| FP32 | ~7 TFLOPS | ~29 TFLOPS |
| Tensor Cores (FP16/BF16) | ❌ None | ✅ Yes (~116 TFLOPS) |
| Memory Bandwidth | 288 GB/s | 504 GB/s |
| PyTorch support | ⚠️ Ends at 2.14 | ✅ Fully current |

The M40 has **no Tensor Cores**, so all training runs in FP32 — roughly 4–8× slower than a modern GPU doing BF16 with tensor acceleration.

---

## VRAM Math

The answer varies by a factor of ~16× depending on whether you use full fine-tuning, LoRA, or QLoRA.

7B QLoRA needs ~12GB VRAM; 70B QLoRA needs ~41–46GB VRAM; and a Qwen 3 30B-A3B MoE runs at only ~17.5GB QLoRA despite its 30B parameter count.

---

## What Each Setup Can Train

### RTX 4070 Alone (12 GB, modern/fast)

| Task | Possible? |
| --- | --- |
| 7B QLoRA (Llama, Mistral, Qwen) | ✅ Comfortable |
| 13B QLoRA | ✅ Yes |
| 7B LoRA | ❌ Too tight (~14–18 GB needed) |
| Any full fine-tuning | ❌ No |

**Best use**: Fast, modern QLoRA fine-tuning. Uses Tensor Cores, BF16, current PyTorch.

---

### 2× M40 (48 GB combined, with PyTorch ≤ 2.14)

| Task | Possible? |
| --- | --- |
| 7B full fine-tuning (gradient checkpointing) | ✅ Tight but doable |
| 13B QLoRA / LoRA | ✅ Yes (even one M40) |
| 30B QLoRA | ✅ Yes |
| 70B QLoRA | ✅ Yes (41–46 GB fits) |
| 70B LoRA or full FT | ❌ No |

### 3× M40 (72 GB combined, with PyTorch ≤ 2.14)

| Task | Possible? |
| --- | --- |
| 13B full fine-tuning (distributed) | ✅ Yes |
| 70B QLoRA | ✅ Comfortably |
| 70B LoRA | ✅ Possible (~45–55 GB) |
| 70B full fine-tuning | ❌ Needs 140+ GB |

---

## Can You Combine M40 + RTX 4070 in One Training Job?

**Practically: No. Don't try it.**

- Different architectures (SM 5.2 vs SM 8.9) can technically run DDP, but are extremely inefficient
- The RTX 4070 will sit idle waiting for M40s (~4× slower)
- No NVLink on either card means all inter-GPU comms are over slow PCIe

**Run them as separate workers** (different training jobs or CPU-offloaded inference on M40s while training on RTX 4070).

---

## Practical Recommendation

| Priority | Use this GPU | For this task |
| --- | --- | --- |
| **1st choice** | RTX 4070 | All QLoRA fine-tuning of 7B–13B models, fast iteration |
| **2nd choice** | 2–3× M40 | 70B QLoRA or 13B LoRA, pinned to PyTorch 2.14 |
| **Avoid** | Mixed M40 + 4070 | Single distributed training job |

The M40 trio gives you **raw VRAM capacity** for big models, but the **RTX 4070 is your real workhorse** for any training that needs speed, modern frameworks, or Tensor Core acceleration. Plan for the M40s to become unsupported soon and factor that into your workflow design.

---

References:

- [PyTorch Maxwell/Pascal support dropped — CUDA 12.6 wheels ending at PyTorch 2.14](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432.md)
- [GPU VRAM Requirements for LLM Fine-Tuning 2026](https://www.spheron.network/blog/gpu-vram-requirements-fine-tune-llm-2026/)
- [LLM Hardware Requirements Guide — VRLA Tech, June 2026](https://vrlatech.com/llm-hardware-requirements-guide/)
- [Best GPU for Fine-Tuning LLMs in 2026](https://packet.ai/blog/best-gpu-fine-tuning-llm)
- [PyTorch Issue #157517 — Maxwell/Pascal/Volta deprecation](https://github.com/pytorch/pytorch/issues/157517)
