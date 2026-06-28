---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nemotron 3 Ultra 550B Hybrid MoE
translated: false
type: note
---

**Question:** What is the model at `huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16`?

**Answer:**

This is NVIDIA's largest open-weight model yet — the BF16 (full-precision) instruct/chat checkpoint of **Nemotron 3 Ultra**. It's frontier-scale and the architecturally interesting part is what's *not* a standard dense transformer.

**The numbers**

- 55B active, 550B total parameter Mixture-of-Experts hybrid Mamba-Transformer model — so ~10% activation ratio, similar density to DeepSeek-V3-class MoEs.
- Pre-trained with around 20T tokens, supports up to 1M context length.
- Post-training data cutoff May 2026, pre-training cutoff September 2025.

**The architecture — this is the part worth your attention**

It's not a pure transformer. The model employs a hybrid Latent Mixture-of-Experts (LatentMoE) architecture, utilizing interleaved Mamba-2 and MoE layers, along with select Attention layers. Three things stacked together:

1. **Mamba-2 + Attention hybrid** (Nemotron-H lineage). Most layers are Mamba-2 SSM blocks — linear-time, constant-state-size sequence mixing — with only a few full self-attention layers interleaved. This is what makes 1M context tractable: you're not paying O(n²) KV cache on every layer. The Mamba state is fixed-size regardless of sequence length, which is why Unsloth's pitch is that it can preserve long agent state, logs, and plans across sustained sessions.

2. **LatentMoE** — the novel routing trick. Tokens are projected into a smaller latent dimension for expert routing and computation, improving accuracy per byte. Instead of routing/computing experts in the full model dim, you compress to a latent space first (conceptually adjacent to MLA's KV compression in DeepSeek, but applied to the MoE FFN path).

3. **MTP (Multi-Token Prediction)** — includes MTP layers for faster inference through native speculative decoding. Same idea DeepSeek-V3 popularized: extra prediction heads let the model self-speculate, so you get free draft tokens without a separate draft model.

**NVFP4 pre-training** — notable. The Ultra model is pre-trained using an NVFP4 recipe — a quantization-aware pre-training approach. They trained in 4-bit floating point (NVFP4) from the start, not just quantized post-hoc. That's the compute-efficiency play and is the direction the field is moving.

**Post-training pipeline:** SFT, RL, and Multi-teacher On-Policy Distillation (MOPD) — the MOPD piece (distilling from multiple teacher models on-policy) is the differentiator from a standard SFT+RLHF stack.

**Practically for you**

This specific BF16 repo is the full-precision weights — the heavy one. The BF16 model cache ranges from ~1.1–1.7 TB; minimum GPU requirement is 4×GB200/B200/B300 or 8×H100. Your **MI300X (192GB)** won't hold BF16 alone, and the NVFP4 variant is CUDA/Blackwell-oriented. Your realistic local paths:

- **MI300X**: try the NVFP4 checkpoint via vLLM (ROCm), or an FP8/GGUF route. Even NVFP4 cache is ~330 GB, so it won't fit a single 192GB card — you'd need 2× MI300X or aggressive quant.
- **Unsloth GGUFs**: dynamic 1-bit takes 189GB disk; 3-bit needs ~256GB RAM, 4-bit ~300GB — CPU/offload territory, not your 62GB workstation.
- **Cheapest to just try it**: OpenRouter has a free tier ($0 in/out), paid is $0.50/M input, $2.20/M output.

If you want to actually study the architecture rather than run the 550B, grab the **Nano** sibling — same LatentMoE + Mamba-2 hybrid recipe at a size that fits your hardware, and the full training recipe is open in the NVIDIA Nemotron Developer Repository. That's the high-leverage move for someone mapping DeepSeek-V4 MoE internals: Nemotron 3 gives you the Western open counterpart with Mamba hybridization + NVFP4 pretraining that DeepSeek doesn't do.

**References:**

- [NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 · Hugging Face](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)
- [NVIDIA Nemotron 3 Ultra research page](https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/)
- [NIM Day-0 Get Started guide](https://docs.nvidia.com/nim/large-language-models/latest/day-0/get-started-nemotron-3-ultra.html)
- [Unsloth: Run Nemotron 3 Ultra Locally](https://unsloth.ai/docs/models/nemotron-3-ultra)
- [OpenRouter — Nemotron 3 Ultra pricing](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b)
