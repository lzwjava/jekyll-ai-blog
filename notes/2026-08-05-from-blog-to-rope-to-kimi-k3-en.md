---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Blog to RoPE to Kimi K3
translated: false
type: note
---

Question: Read and summarize/fact-check this Chinese biographical piece on Jianlin Su (苏剑林) — his path from a math-focused blog to RoPE, then to KDA and Attention Residuals in Kimi K3.

Answer:

**The narrative, stripped of the literary framing:**

Su Jianlin is a self-taught math person (BSc South China Normal, MSc pure math at Sun Yat-sen) who ran a blog called "Scientific Spaces" since age 15. He never did a PhD, never went abroad. Key technical milestones:

- **2021**: published RoPE (Rotary Position Embedding) on his blog first, then as RoFormer on arXiv. Core idea: encode absolute position as a rotation matrix so that when you take the dot product between query and key, only the *relative* rotation (angle difference) survives — you get relative position info from an absolute encoding scheme, for free, inside the attention dot product. This is why it composes cleanly with linear attention (rotation is just a norm-preserving linear map) and extrapolates better than learned/absolute embeddings.
- **2019–2022**: authored bert4keras, WoBERT/WoNEZHA — widely used Chinese NLP tooling while working at a company (追一科技) that was contracting/downsizing.
- **2023**: joined Moonshot AI (Kimi), worked remotely from Guangzhou.
- **Feb 2025**: MoBA (Mixture of Block Attention) — sparse attention for long context, released hours after DeepSeek's NSA.
- **2025**: QK-Clip, fixing "MaxLogit explosion" when scaling the Muon optimizer past ~100B params, used in Kimi K2's 15.5T-token pretrain with a reported zero loss-spike run.
- **Nov 2025**: Kimi Linear / KDA (Kimi Delta Attention) — a gated DeltaNet variant that, in fair comparison, beat full attention on short-context, long-context, *and* RL scaling. I checked the arxiv listing (2510.26692) — Su is indeed a listed author among ~59 Kimi Team authors.
- **Mar 2026**: Attention Residuals (AttnRes) — replaces fixed-weight residual summation with learned softmax attention over previous layer outputs. Confirmed on arXiv (2603.15031): Su is credited as one of the earliest co-authors alongside Guangyu Chen and Yu Zhang, with a 17-year-old high schooler (Guangyu Chen) also a lead co-author. Verified via GitHub (MoonshotAI/Attention-Residuals) and arXiv listing.
- **The "kills his own RoPE" detail**: Kimi Linear reportedly uses NoPE — no explicit position encoding — because KDA's gating is expressive enough to learn positional structure implicitly. This is a real and notable design choice; the framing that Su co-designed something that obsoletes his earlier famous invention checks out per Kimi Linear's public documentation.

**On Kimi K3 itself** — I verified independently:
- 2.8T total params, MoE with 896 experts, 16 active (~104B active params), 1M context, built on KDA + AttnRes. Kimi K3 is Kimi's most capable flagship model to date, with 2.8 trillion parameters, built on Kimi Delta Attention (KDA), a hybrid linear attention mechanism, and Attention Residuals, with native visual understanding and a 1M-token context window, positioned as the world's first open-source model in the 3-trillion-parameter class.
- Timeline: hosted launch July 16, open weights July 26–27, 2026 — weights went public July 26, 2026 at roughly 7:30 PM EDT, a day ahead of the July 27 target.
- Benchmark claim in the article checks out: Arena ranked K3 first in its Frontend Code evaluation at 1,679 points, ahead of Fable 5, in blind developer testing, though Moonshot itself says K3 still trails Claude Fable 5 and GPT-5.6 Sol overall.
- The export-control/sanctions subplot is real: White House OSTP accused Moonshot of distillation against Claude Fable 5 using restricted chips via Thailand, and Treasury Secretary Bessent warned of possible sanctions — this matches the Fable/Mythos export-control episode from earlier this summer.

**What I'd flag as unverifiable / likely embellished:** the "200 Silicon Valley companies signed a letter against sanctions" and "Wall Street called it DeepSeek 2.0" lines — plausible given the tone of coverage, but I didn't find a primary source pinning those exact numbers/quotes; treat them as color rather than fact.

The RoPE math itself, if you want the actual derivation (block-diagonal rotation matrix, why `q_m^T k_n` depends only on `m-n`), I can walk through it — you've probably already got this in your notes but happy to do the forward-pass version alongside how KDA's delta-rule gating differs from vanilla linear attention.

References:
- [Kimi K3 – Kimi API Platform](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Attention Residuals (arXiv 2603.15031)](https://arxiv.org/abs/2603.15031v1)
- [Kimi Linear (arXiv 2510.26692)](https://arxiv.org/abs/2510.26692)
- [MoonshotAI/Attention-Residuals GitHub](https://github.com/MoonshotAI/Attention-Residuals)
- [Tom's Hardware — Kimi K3 vs Claude Fable 5](https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3)