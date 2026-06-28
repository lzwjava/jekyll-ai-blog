---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V4 Pro DSpark Speculative Decoding
translated: false
type: note
---

**Question:** What is `deepseek-ai/DeepSeek-V4-Pro-DSpark` on Hugging Face?

**Answer:**

The `-DSpark` suffix is the key. DeepSeek-V4-Pro-DSpark is not a new model — it's the same DeepSeek-V4-Pro checkpoint with an additional speculative decoding module attached. The name is a play on "DeepSeek + Spark" (speculative). Reference implementation lives in their [DeepSpec](https://github.com/deepseek-ai/DeepSpec) repo.

So this repo = base weights + a draft/predictor head for **self-speculative decoding** (akin to Medusa/EAGLE-style multi-token prediction), to accelerate inference without changing model quality. The draft module proposes several future tokens, the full model verifies them in one forward pass, and accepted tokens are committed — turning multiple sequential decode steps into one verified batch. That's why the repo shows extra tensor types (`F8_E8M0`, `I8`, etc.) — the spec module ships alongside the main FP4+FP8 weights.

**The model itself (DeepSeek-V4 series):**

This is the **V4 preview** — a generational jump from V3.2. Two MoE variants, both 1M-token context:

| Model | Total | Activated | Precision |
|---|---|---|---|
| V4-Flash | 284B | 13B | FP4+FP8 |
| V4-Pro | 1.6T | 49B | FP4+FP8 |

The architecturally interesting parts, given your MoE/attention focus:

1. **Hybrid attention (CSA + HCA)** — Compressed Sparse Attention combined with Heavily Compressed Attention. At 1M-token context, V4-Pro needs only 27% of single-token inference FLOPs and 10% of the KV cache compared to V3.2. This is the natural successor to V3.2's DSA (DeepSeek Sparse Attention) — they've split the attention budget into two compression regimes rather than one. The 10% KV cache number is the headline for long-context serving economics.

2. **Manifold-Constrained Hyper-Connections (mHC)** — a strengthening of conventional residual connections to improve stability of signal propagation across layers while preserving expressivity. This reads as a constrained variant of the Hyper-Connections work (replacing the single residual stream with learnable multi-stream connections), with a manifold constraint to keep training stable at 1.6T scale.

3. **Muon optimizer** — they've moved off AdamW for the main training. Muon is used for faster convergence and greater training stability. Consistent with the Kimi/Moonshot direction; notable that DeepSeek adopted it at trillion-param scale.

4. **Training + post-training:** pre-trained on 32T+ tokens, with a two-stage post-training paradigm — independent cultivation of domain-specific experts via SFT and GRPO RL, then unified consolidation through on-policy distillation. So they train specialist experts separately, then distill them on-policy back into one model. That's a cleaner take on the "merge specialists" problem than naive weight averaging.

**Three reasoning modes** (Non-think / Think High / Think Max), with Max needing ≥384K context window and a special system prompt. On benchmarks, V4-Pro-Max leads on LiveCodeBench (93.5) and Codeforces rating (3206), trading blows with Opus-4.6, GPT-5.4, and Gemini-3.1-Pro elsewhere — strongest open model on coding, still behind Gemini on raw knowledge (SimpleQA).

For your use: if you're serving V4 locally or benchmarking, **DSpark is the repo you want for throughput** — the spec module is what makes 49B-activated / 1M-context decode tolerable on your hardware budget. Recommended sampling is `temperature=1.0, top_p=1.0`.

**References:**

- [deepseek-ai/DeepSeek-V4-Pro-DSpark](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark)
- [DeepSeek-V4 Technical Report (arXiv 2606.19348)](https://arxiv.org/abs/2606.19348)
- [DeepSpec repo](https://github.com/deepseek-ai/DeepSpec)
