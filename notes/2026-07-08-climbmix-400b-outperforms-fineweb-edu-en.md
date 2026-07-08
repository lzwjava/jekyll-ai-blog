---
audio: false
generated: true
image: false
lang: en
layout: post
title: ClimbMix-400B outperforms FineWeb-Edu
translated: false
type: note
---

Question: Is ClimbMix-400B better than FineWeb-Edu for pretraining?

Answer:

Short answer: yes, on the benchmarks the CLIMB authors report, and it's now battle-tested outside the paper too — Karpathy switched nanochat's default pretraining corpus from FineWeb-Edu to ClimbMix.

**The paper's own claim:**
Models trained on Nemotron-ClimbMix significantly outperform those trained on existing datasets — Nemotron-CC, SmolLM-corpus, DCLM-baseline, and FineWeb-Edu — under an equal token budget. A 1B model continuously trained on 400B ClimbMix tokens exceeds Llama-3.2-1B by 2.0% averaged across 12 downstream reasoning benchmarks, and this is explicitly a head-to-head against FineWeb-Edu at matched token count, not just against raw web crawl.

**Independent real-world signal (more relevant to you, since you're doing nanoGPT/nanochat-scale runs on MI300X):**
NanoChat's GPT-2-capability training time dropped from ~3 hours to ~2 hours on an 8×H100 node, driven primarily by switching the pretraining dataset from FineWeb-edu to ClimbMix, plus FP8. Critically: alternative datasets including OLMo, FineWeb, and DCLM produced regressions when swapped in, while ClimbMix worked out of the box — meaning it's not just marginally better, it's specifically the one drop-in replacement that didn't need re-tuning of hyperparameters to realize the gain. That's the strongest practical signal for your use case: you don't have to re-tune LR/schedule to benefit.

**Why it wins mechanically (not just "more filtered"):**
FineWeb-Edu's advantage comes from LLM-classifier-based educational-quality filtering on top of FineWeb — a single quality axis. ClimbMix instead optimizes the *mixture ratio* across 20 semantic clusters (drawn from Nemotron-CC + smollm-corpus) using CLIMB-search, a proxy-model-driven bootstrapping loop — closer to hyperparameter search over data composition than a filter threshold. That's why it generalizes better across the 12-benchmark suite instead of winning on one axis (e.g. FineWeb-Edu's edu-scored data helps Science slightly but doesn't move Commonsense/NLI, per other mixture studies).

**One caveat worth knowing before you commit ClimbMix as your default:** since it draws from Nemotron-CC + smollm-corpus rather than raw FineWeb, it inherits whatever synthetic/curated bias those sources have (smollm-corpus is synthetic-heavy). If your downstream target is code/agent-heavy tasks rather than the 12 general-reasoning benchmarks in the paper, that's an empirical question worth a quick val_bpb ablation on your own MI300X setup rather than assuming the paper's gains transfer 1:1 — same caveat Karpathy notes when OLMo/DCLM regressed on drop-in.

**Practical move for your GPT-2-760M runs:**

```bash
# same swap Karpathy made — just point prepare.py at ClimbMix instead of fineweb-edu
uv run prepare.py --dataset karpathy/climbmix-400b-shuffle
uv run train.py   # 300s baseline run, compare val_bpb against your current fineweb-edu checkpoint
```

Given you're already deep in nanochat, this is a near-zero-cost swap to test on your own val_bpb metric before trusting the paper's 12-benchmark number for your specific downstream targets.

References:

- [Nemotron-CLIMB paper — arXiv:2504.13161v2 (Figure 1: ClimbMix vs FineWeb-Edu/DCLM/etc.)](https://arxiv.org/html/2504.13161v2)
- [NVIDIA CLIMB Research page](https://research.nvidia.com/labs/lpr/climb/)
- [Karpathy's NanoChat: FineWeb-edu → ClimbMix switch, 2-hour GPT-2 training](https://blockchain.news/ainews/karpathy-s-nanochat-hits-2-hour-gpt-2-training-on-8x-h100-fp8-and-nvidia-climbmix-boost-throughput-2026-benchmark-analysis)
- [karpathy/climbmix-400b-shuffle on Hugging Face](https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle)
