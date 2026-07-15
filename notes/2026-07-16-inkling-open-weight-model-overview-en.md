---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inkling Open-Weight Model Overview
translated: false
type: note
---

Question: What is Inkling, Thinking Machines Lab's new release?

Answer: It's Thinking Machines Lab's first open-weights model, released July 15, 2026. Key specs:

**Architecture**

- MoE transformer, 975B total parameters, 41B active parameters, up to 1M token context
- 256 routed experts + 2 shared experts per layer, 6 routed experts active per token, sigmoid router, aux-loss-free load balancing (DeepSeek-V3 style)
- Attention: sliding-window/global layers interleaved 5:1, 8 KV heads, uses a learned relative positional bias instead of RoPE (claims better long-context extrapolation) + short convs on QK/V and residual branches
- Pretrained on 45 trillion tokens of text, images, audio, video
- Optimizer: Muon for large matrices, Adam for the rest, tied to their modular-manifolds weight-decay/LR coupling work
- Trained entirely on NVIDIA GB300 NVL72 systems

**RL**

- Scaled RL to over 30M rollouts, log-linear reward improvement
- Controllable "thinking effort" — trained by varying system message + per-token cost during RL, so you can dial reasoning length/cost like a knob
- Noted CoT compression over training (grammar drops, stays comprehensible) — same phenomenon Cognition reported on SWE-1.7

**Variant**

- Inkling-Small (preview): 276B total, 12B active parameters, matches/exceeds full Inkling on several benchmarks — better pretrain data mix for the smaller size, full weights not released yet.

**Where it lands vs frontier**

- Solid but not SOTA. On agentic coding (Terminal Bench 2.1) roughly on par with GLM 5.2/DeepSeek V4 Pro, well behind Claude Fable 5/GPT 5.6 Sol.
- On Terminal Bench 2.1, Inkling spends 1/3 as many tokens to match Nemotron 3 Ultra — that's the real pitch: efficiency per token, not peak score.
- Multimodal: encoder-free, images as 40×40 patches through a 4-layer hMLP, audio as dMel spectrograms — no separate vision/audio encoder tower.
- Fine-tunable now on Tinker (their platform), weights on Hugging Face (`thinkingmachines/inkling`), inference support already landed in vLLM, SGLang, llama.cpp, transformers.

Given you're already running your own GPU cluster training GPT-2 760M — this is one you could actually pull weights for and fine-tune locally if you want a MoE base with native audio/vision instead of bolting on encoders yourself.

References:

- [Inkling: Our Open-Weights Model](https://thinkingmachines.ai/news/introducing-inkling/)
- [Model card](https://thinkingmachines.ai/model-card/inkling/)
- [Hugging Face weights](https://huggingface.co/thinkingmachines/inkling)
- [Tinker docs](https://tinker-docs.thinkingmachines.ai/tinker/)
