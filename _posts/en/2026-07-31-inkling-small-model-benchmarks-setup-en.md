---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Inkling-Small: Model, Benchmarks, Setup"
translated: false
type: note
---

Question: What is Thinking Machines Lab's Inkling-Small model — architecture, benchmarks, how to run it?

Answer:

Released July 30, 2026 (yesterday), Apache 2.0, open weights. This is TML's (Mira Murati's lab) smaller sibling to their flagship "Inkling" model.

**Architecture** — sparse MoE decoder, natively multimodal (text/image/audio in, text out):

- 42-layer decoder-only transformer with a sparse Mixture-of-Experts feed-forward backbone: each token is routed to 6 of 256 experts, plus 2 shared experts active on every token
- Attention is a hybrid of local and global layers
- images are encoded via a hierarchical patch encoder, and audio via discrete token encoding — with all modalities projected into a shared hidden space and processed jointly by the decoder
- 276B total, 12B active params — so ~4.3% sparsity ratio, similar active-param class to your GPT-2 760M scale-up experiments but MoE instead of dense.
- context window of up to 1M tokens, numerics: BF16, MXFP8 and NVFP4

**Benchmarks** (vs open-weight peers at similar active-param count, and vs closed models):

- SWE-Bench Verified: 80.2% — beats Qwen3.5-397B-A17B's 76.4% and DeepSeek-V4-Flash's 79.0%, loses to GPT-5.6-Luna's 93.0%
- Terminal-Bench 2.1 (best harness): 64.7%
- GPQA Diamond: 89.5%, tied with GPT-5.6-Luna
- ARC-AGI-2: 40.1% — notably higher than the full "Inkling" model's 36.5%, and way above Claude 4.5 Haiku's 4.0%
- SimpleQA Verified (factuality) is weak: 20.6%, worse than most peers — expected tradeoff for a small MoE optimized for agentic/reasoning over rote knowledge

Punches well above its active-param weight class on agentic coding and reasoning; factuality/knowledge recall is the weak spot, as usual for smaller MoEs.

**Running it yourself** — this is where it gets real for your stack:

```
BF16 checkpoint: 600GB+ aggregated VRAM
  - 4x B300, or 8x H200

NVFP4 checkpoint: 180GB+ aggregated VRAM
  - W4A4 on 1x B300 (needs SM100+)
  - W4A16 on 2x H200
```

Running the model directly on GPU hardware requires an inference deployment framework–either SGLang, vLLM, TokenSpeed, Unsloth, or Hugging Face

Weights on HF: `thinkingmachines/Inkling-Small` and `thinkingmachines/Inkling-Small-NVFP4`. Fine-tuning access via their Tinker platform + `tml-renderers` pip package + tinker-cookbook on GitHub.

For your MI300X setup — NVFP4 at 180GB is in range but note the W4A4 fast path is Blackwell-only (SM100+); on MI300X you'd be doing BF16 via vLLM/SGLang ROCm builds, so budget the full 600GB+ VRAM tier, or run it split across nodes.

References:

- [Inkling-Small Model Card](https://thinkingmachines.ai/model-card/inkling-small/)
- [Tinker Cookbook](https://github.com/thinking-machines-lab/tinker-cookbook)
