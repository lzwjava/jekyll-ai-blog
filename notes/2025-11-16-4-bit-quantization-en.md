---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: 4-bit Quantization for Efficient LLMs
translated: false
type: note
---

### What is 4-bit quantization (in the context of QLoRA or GPTQ)?

4-bit quantization is a technique to dramatically reduce the memory footprint of large language models (LLMs) by storing each weight using only 4 bits instead of the usual 16-bit (FP16/BF16) or 32-bit (FP32) precision.

Normal (full-precision) models:

- FP32: 4 bytes per parameter → 7B model ≈ 28 GB
- FP16/BF16: 2 bytes per parameter → 7B model ≈ 14 GB

4-bit quantization:

- ~0.5 bytes per parameter → 7B model ≈ 3.5–4 GB (roughly 1/4 to 1/8 the original size depending on the exact method)

There are two major 4-bit approaches you commonly see today:

| Method   | Full name                  | Main paper / year | Typical use case                  | Key characteristics                                                                 |
|----------|----------------------------|-------------------|-----------------------------------|---------------------------------------------------------------------------------------|
| GPTQ     | GPTQ                       | 2023              | Post-training quantization (inference only) | One-shot, very accurate, no retraining needed. Rounds weights to 4-bit after training. |
| QLoRA    | Quantized Low-Rank Adaptation | 2023 (Jun)     | Efficient fine-tuning / instruction tuning | Combines 4-bit storage + LoRA adapters + paged optimizers. Allows fine-tuning 65B+ models on a single 24–48 GB GPU. |

#### QLoRA in more detail (the one people usually mean when they say “4-bit QLoRA”)

QLoRA does four clever things at once:

1. 4-bit NormalFloat (NF4) quantization
   - A special 4-bit data type optimized for normally distributed weights (most LLM weights are ≈ Gaussian after training).
   - Better than plain INT4; theoretically optimal for normally distributed data.

2. Double quantization
   - Even the quantization constants (scaling factors) are quantized from FP16 → 8-bit, saving a few more MB.

3. Paged optimizers
   - Optimizer states (AdamW moments) are stored in CPU RAM and paged to GPU with NVIDIA unified memory. Prevents OOM during training.

4. LoRA adapters
   - Only trains small low-rank matrices (r=64 or less) while the base 4-bit model stays frozen.

Result: You can fully fine-tune a 65B Llama/Mistral model on one 48 GB RTX A6000 or even a 70B model on a single 80 GB A100 with QLoRA, whereas normal full fine-tuning would need 8×A100s or more.

#### GPTQ (the inference-focused one)

- Done after training is finished.
- Uses second-order (Hessian) information to minimize rounding error when compressing weights to 4-bit.
- Extremely accurate — usually <0.1 perplexity degradation vs FP16.
- Popular with tools like AutoGPTQ, ExLlama, vLLM, and llama.cpp (GGUF also has GPTQ-style modes).

### Gradient Checkpointing (also called “activation checkpointing”)

A completely separate memory-saving technique used during training.

How it works:

- Normally, backpropagation needs to store all intermediate activations from the forward pass → memory grows linearly with model depth/batch size/sequence length.
- Gradient checkpointing trades compute for memory:
  - During forward pass, it only saves a few “checkpoint” activations.
  - During backward pass, it re-computes the missing activations on the fly.

Typical memory savings: 50–80% of activation memory, at the cost of ~20–30% slower training.

It is almost always used together with QLoRA or any large-model fine-tuning because even with 4-bit weights, activations still blow up GPU memory.

### TL;DR Summary

“4-bit quant (QLoRA-style or GPTQ) + gradient checkpointing” is the modern recipe for:

- Running or fine-tuning huge models (33B, 70B, 405B) on consumer or single-enterprise GPUs.
- QLoRA-style 4-bit → fine-tuning with very low GPU memory.
- GPTQ-style 4-bit → fast inference with very low GPU memory.
- Gradient checkpointing → makes the actual backward pass possible on long sequences without OOM.

Together they are why you see people fine-tuning Llama-3-70B on a single 3090/4090 today.
