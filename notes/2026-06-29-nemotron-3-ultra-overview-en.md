---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nemotron 3 Ultra Overview
translated: false
type: note
---

Let me verify this — "Nemotron 3 Ultra" with those specific specs (550B total / 55B active, hybrid Transformer-Mamba MoE, 1M context) doesn't match anything I can confirm from training, and the numbers are specific enough to check.Question: Give me an intro to NVIDIA Nemotron 3 Ultra.

Answer:

Confirmed — this is real. NVIDIA open-sourced **Nemotron 3 Ultra** on June 4, 2026. Here's the technically grounded intro, going one layer deeper than the OpenRouter blurb you pasted.

## What it actually is

A **550B-total / 55B-active MoE**, NVIDIA's largest open model to date, built for long-running agents (planning, tool use, multi-turn reasoning, deep research). It's the strongest Western open-weight model on Artificial Analysis' Intelligence Index right now — scoring 48, on-par accuracy with the top open models while being much cheaper to run. Released under NVIDIA's new Open Model, Weights & Data License, with weights, training recipe, code, and most of the data published.

## The architecture is the interesting part

This is **not a pure Transformer**. It's a **hybrid Mamba-Attention MoE**, which is the whole reason for its throughput advantage. The pattern, per the technical report and model card:

- **Mamba-2 layers** do most of the sequence mixing. SSMs scale **sub-quadratically** in sequence length and carry a fixed-size recurrent state instead of a growing KV cache. For a 1M-token agent context, that's the difference between a bounded state and an O(n) KV cache that eats your VRAM.
- **A sparse set of Attention layers** are interleaved for **precise recall** — Mamba's compressed state is lossy for exact retrieval ("what was the variable name 400K tokens ago"), so you keep a few attention layers to recover needle-in-haystack precision. Mamba handles long sequences with sub-quadratic scaling; a few attention layers are kept for precise recall over large contexts.
- **LatentMoE** — the MoE layers operate in a compressed latent space (Nemotron's variant), interleaved with the Mamba-2 blocks.
- **Multi-Token Prediction (MTP)** layers for faster decode + quality, same as DeepSeek-style MTP.

The mental model: Mamba = cheap bulk context processing, Attention = expensive precise lookup, MoE = sparse capacity, MTP = decode speedup. It's the same family idea as Jamba/Zamba but scaled to frontier size.

## Why it's fast (the part that matters for your agent pipelines)

It achieves 5.9×, 4.8×, and 1.6× higher inference throughput vs GLM-5.1-754B-A40B, Kimi-K2.6-1T-A32B, and Qwen-3.5-397B respectively on an 8K-input / 64K-output setting, at on-par accuracy. That long-output regime is exactly where attention KV cache cost dominates — so the Mamba layers pay off most in agent loops that generate a lot (reasoning traces, tool-call chains). It also reports the highest non-hallucination score in its comparison set, 78.7 on AA-Omniscience.

## Quantization / deployment

It's **pretrained natively in NVFP4** (4-bit), not post-hoc quantized — ~20 trillion tokens of NVFP4 pretraining. The shipped checkpoint mixes NVFP4 routed experts, FP8 for shared experts and Mamba linears, and BF16 for attention layers — NVIDIA found accuracy saturated below this precision budget. Practical payoff: the W4A16 path fits on a single 8-GPU H100 node with room for MTP weights, whereas an FP8 checkpoint would span two nodes. One NVFP4 checkpoint runs across Ampere/Hopper/Blackwell.

## Post-training

Centered on Multi-teacher On-Policy Distillation (MOPD), distilling 10+ specialized teachers into one model — then SFT on synthetic code, math, science, tool-calling, structured output, and instruction data.

## For your setup

You can't run the full thing on the 4070 or the MI300X comfortably at full precision (550B), but it's relevant to you on two fronts:

1. **Run it locally via GGUF** — Unsloth has dynamic quants down to 1-bit at 189GB disk, and a 3-bit UD-IQ3_XXS that fits on a 256GB device. Your MI300X (192GB HBM3) is in range for the aggressive low-bit quants — this is the one machine you have that could actually serve it.
2. **It's the architecture worth studying** if you're tracking where MoE is going post-DeepSeek-v4. The hybrid Mamba-Attention + LatentMoE + MTP stack is a different bet than DeepSeek's pure-attention MLA approach. Worth reading both technical reports side by side.

If you want, I can pull the actual layer pattern (Mamba:Attention:MoE ratio) and head/expert dimensions from the technical report and sketch the forward pass in ~50 lines, or set up an OpenRouter call against the free endpoint to benchmark it against your deepseek-v4-flash baseline.

References:

- [Nemotron 3 Ultra Technical Report (NVIDIA Research)](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)
- [NVIDIA Technical Blog — Nemotron 3 Ultra](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/)
- [MarkTechPost coverage](https://www.marktechpost.com/2026/06/04/nvidia-ai-releases-nemotron-3-ultra-an-open-550b-mixture-of-experts-hybrid-mamba-transformer-for-long-running-agents/)
- [NVIDIA build.nvidia.com model card (NVFP4)](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b/modelcard)
- [Unsloth — run Nemotron 3 Ultra locally (GGUFs)](https://unsloth.ai/docs/models/nemotron-3-ultra)
