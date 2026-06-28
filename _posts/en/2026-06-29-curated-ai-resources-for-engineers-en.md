---
audio: false
generated: true
image: false
lang: en
layout: post
title: Curated AI Resources for Engineers
translated: false
type: note
---

Let me find what's currently active and worth your time.The search surfaced mostly hardware vendor SEO. Those aren't worth your time. Here's a curated list of sites that actually compound for someone training models and building agents.

**Question:** What are hot/interesting AI and GPU websites worth following for a deep-technical, AI-first engineer?

**Answer:**

**Training internals & deep technical writing**

- **[Karpathy's blog + nanochat/nanoGPT repos](https://github.com/karpathy/nanochat)** — you're already here, but his GitHub Discussions and issues are where the real teaching happens. Watch the nanochat repo activity.
- **[Lil'Log (Lilian Weng)](https://lilianweng.github.io/)** — the canonical deep-dives on attention, diffusion, RLHF, reward hacking. Math-heavy, exactly your register.
- **[Jay Alammar](https://jalammar.github.io/)** — illustrated transformer/LLM internals. Visual but not shallow.
- **[Sebastian Raschka's Ahead of AI](https://magazine.sebastianraschka.com/)** — best signal-to-noise newsletter on LLM training, fine-tuning, and architecture papers. He ships actual PyTorch implementations (his `LLMs-from-scratch` repo pairs with the posts).
- **[Eleuther AI blog](https://blog.eleuther.ai/)** — GPT-NeoX, scaling laws, the people who actually train open models from scratch.

**GPU / CUDA / kernels**

- **[GPU MODE](https://github.com/gpu-mode)** (formerly CUDA MODE) — Discord + YouTube + repos. The community for kernel writing, Triton, FlashAttention internals. This is the single best place for your CUDA/inference-optimization trajectory.
- **[Horace He / "Making Deep Learning Go Brrrr From First Principles"](https://horace.io/brrr_intro.html)** — memory-bound vs compute-bound, the mental model for all GPU optimization.
- **[Modal blog](https://modal.com/blog)** and **[Together AI blog](https://www.together.ai/blog)** — practical inference/training infra, FlashAttention authorship lives near Together.
- **[vLLM blog](https://blog.vllm.ai/)** and **[llm-d](https://llm-d.ai/blog)** (surfaced above) — PagedAttention, prefix caching, distributed inference. The recent llm-d posts on precise prefix-cache aware scheduling report large throughput gains by giving the scheduler direct introspection into distributed vLLM KV cache.

**MoE / frontier architecture (your DeepSeek v4 interest)**

- **[DeepSeek's GitHub + tech reports](https://github.com/deepseek-ai)** — read the actual papers (DeepSeek-V3, MLA, MoE load balancing). Their open infra repos (FlashMLA, DeepEP, DeepGEMM) are gold for kernel-level MoE.
- **[Tri Dao's blog](https://tridao.me/)** — FlashAttention, Mamba, state-space models from the source.

**Aggregators worth the noise**

- **[Hacker News](https://news.ycombinator.com/)** — filter for AI/GPU submissions; comment threads often beat the articles.
- **[r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)** — the pulse for open-weight models, quantization, single-GPU experiments. Aligns with your RTX 4070 / MI300X tinkering.
- **[The Gradient](https://thegradient.pub/)** and **[Sebastian Ruder's NLP newsletter](https://newsletter.ruder.io/)** — research-adjacent depth.

**For your idol-tier matching**

- **[Yin Wang's site](https://www.yinwang.org/)** — you know it; worth re-reading his compiler/PL essays for the first-principles discipline.
- **[Simon Willison's blog](https://simonwillison.net/)** — prolific, build-in-public, LLM tooling and CLI agents. Closest spiritually to your `ww`/`iclaw`/`zz` workflow.

If I had to pick three to start: **GPU MODE** (kernels/CUDA), **Sebastian Raschka** (training-from-scratch with code), and **DeepSeek's repos** (MoE at the frontier). Those three map directly onto your MI300X training, nanochat work, and DeepSeek v4 MoE exploration.

**References:**

- [Lil'Log](https://lilianweng.github.io/)
- [Ahead of AI — Sebastian Raschka](https://magazine.sebastianraschka.com/)
- [GPU MODE](https://github.com/gpu-mode)
- [Making DL Go Brrrr — Horace He](https://horace.io/brrr_intro.html)
- [DeepSeek AI GitHub](https://github.com/deepseek-ai)
- [vLLM blog](https://blog.vllm.ai/)
- [llm-d blog](https://llm-d.ai/blog)
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)
