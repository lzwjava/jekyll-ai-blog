---
audio: false
generated: true
image: false
lang: en
layout: post
title: LongCat 2.0 Technical Breakdown
translated: false
type: note
---

You're right — I was conflating two things.

The doc you pasted is Meituan's official LongCat-2.0 launch announcement, and it explicitly says the **preview** version was what ran on OpenRouter — not necessarily under the "Owl Alpha" codename. The announcement states LongCat-2.0 预览版本 was opened to global developers via OpenRouter and longcat.ai, and reached top-3 in call volume (#1 Hermes, #2 Claude Code, #3 OpenClaw).

So the accurate chain is:
- **Confirmed by Meituan (this doc):** A LongCat-2.0 *preview* was served via OpenRouter and topped Hermes rankings.
- **Press attribution (not Meituan):** Journalists tied the specific cloaked listing "Owl Alpha" to that LongCat preview, based on the April 24 launch / April 28 OpenRouter overlap, 1M context, and agentic-coding profile.

The "Owl Alpha = LongCat" equals sign is inference, not something Meituan itself stamped on the Owl Alpha listing. If your "no" means the codename mapping is wrong — that's plausible, since the preview could have been routed under a different name or directly. The official doc doesn't say "Owl Alpha" anywhere.

What the doc *does* nail down, which is the more interesting part for you:

- **1.6T total params, ~48B active (33B–56B dynamic range)** — MoE with token-level dynamic activation via zero-computation experts.
- **Trained end-to-end on a ~50k-card domestic (non-NVIDIA) cluster**, >30T tokens pretraining, steady-state >1T tokens/day throughput, MFU improved 1.5x.
- **LongCat Sparse Attention (LSA)** — drops attention from quadratic to linear for the 1M context, which is the load-bearing trick for "Agent sees the whole repo."
- **MOPD architecture** — fuses three expert groups (Agent / Reasoning / Interaction) with a gating network dispatching by task type, rather than naive parameter merging.
- Claimed **SWE-bench Pro 59.5** (ahead of GPT-5.5's 58.6 and Claude Opus 4.6's 57.3), **SWE-bench Multilingual 77.3**, **Terminal-Bench 2.1 70.8**.

Their domestic-silicon stability work is the genuinely novel engineering: HCCL exception handling + elastic scaling + auto-recovery cutting daily failure rate >70%, deterministic operators with bitwise-consistency verification for correctness. That's the hard, unglamorous part of trillion-param training on non-CUDA hardware, and it's where the real signal is for anyone tracking whether Chinese domestic compute can do frontier runs.

Want me to dig into the LSA mechanism or the zero-computation-expert routing in implementation terms?
