---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training vs Running Bonsai 2 27B
translated: false
type: note
---

**Question:** What device or FLOPS are needed to train a model like Ternary Bonsai 2 27B?

**Answer:**

This is an important distinction: **Bonsai 2 27B was not trained from scratch — it is a post-training quantization of Qwen3.8-27B**, meaning the original pre-training compute belongs to Alibaba's Qwen team. There are two separate compute questions here.

---

## 1. Pre-Training the Base Model (Qwen3.8-27B) — Done by Alibaba

The Qwen3.8-27B launch does not include a model-specific technical report, training-token count, dataset inventory, or training-compute figure, so exact numbers are not public. However, we can estimate using the standard formula.

**The Kaplan/Chinchilla formula for pre-training FLOPs:**
> `FLOPs ≈ 6 × N × D`
> where N = parameters, D = training tokens

A 27B model trained on ~10–15 trillion tokens (typical modern "over-trained" scale, following LLaMA 3 style) works out to roughly:

| Token budget | Estimated FLOPs |
| --- | --- |
| 540B tokens (Chinchilla-optimal, 20×N) | ~8.7 × 10²³ FLOPs |
| 5T tokens (moderate over-train) | ~8.1 × 10²⁴ FLOPs |
| 15T tokens (LLaMA 3-scale) | ~2.4 × 10²⁵ FLOPs |

**Hardware to do this realistically:**

Training LLaMA 70B at BF16 on 512 H100 GPUs takes about 109 days per 1 trillion tokens. A 27B model is roughly ~40% the compute per token of a 70B, so a 5T-token run on 512 H100s would take on the order of **~90–120 days**. In practice, frontier labs use clusters of **512–2048 H100/H200 GPUs** to keep wall-clock time to weeks, not months.

A realistic minimum cluster for a serious 27B pre-training run:

- **Minimum viable:** 64–128 × H100 80GB (months of wall-clock time)
- **Practical:** 256–512 × H100 80GB (~4–8 weeks)
- **Fast:** 1024+ × H100/H200 (~1–2 weeks)

---

## 2. Prism ML's Work: Ternary Quantization (Post-Training)

Prism ML's contribution is **quantization-aware training / PTQ (Post-Training Quantization)** on top of the existing Qwen3.8-27B weights — converting FP16 weights into {−1, 0, +1} ternary values with Hadamard rotation. This is far less compute-intensive than pre-training:

- You don't retrain from scratch on trillions of tokens
- You run calibration/fine-tuning passes on a much smaller dataset
- The Hadamard rotation is applied offline and folded into the stored weights

A rough estimate for this stage: **tens to a few hundred H100 GPU-hours**, compared to millions of GPU-hours for pre-training. Prism ML has not published exact figures for this stage.

---

## Summary Table

| Stage | Who | Hardware | Estimated FLOPs | Wall-clock |
| --- | --- | --- | --- | --- |
| Pre-training Qwen3.8-27B | Alibaba | ~256–2048 H100s | ~10²⁴–10²⁵ | Weeks–months |
| Ternary quantization (Bonsai) | Prism ML | Tens–hundreds H100s | ~10²¹–10²² | Days |
| **Running inference** | **You** | **Single M5 Pro / RTX 4090** | **N/A** | **~47 tok/s** |

The bottom line: **running** Bonsai 2 27B is accessible to anyone with a modern laptop or a single consumer GPU. **Reproducing the base model pre-training** is a multi-million dollar, multi-hundred GPU endeavor.

---

**References:**

- [Bonsai 2 27B Model Card — Hugging Face](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- [Cost to Train a 70B LLM From Scratch (2026) — Spheron](https://www.spheron.network/blog/cost-to-train-70b-parameter-llm-from-scratch-2026/)
- [NVIDIA NeMo LLaMA 3.1 Training Benchmarks](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/dgxc-benchmarking/resources/nemo-llama31-dgxc-benchmarking-g)
- [Chinchilla Scaling Laws — Hoffmann et al.](https://arxiv.org/abs/2203.15556)
