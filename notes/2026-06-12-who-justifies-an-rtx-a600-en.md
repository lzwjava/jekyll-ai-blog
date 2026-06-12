---
audio: false
generated: true
image: false
lang: en
layout: post
title: Who Justifies an RTX A600
translated: false
type: note
---

**Question:** What kind of user actually justifies buying an RTX A6000 (or any ~¥50k GPU) to self-host LLMs at home for "unlimited" use of a reasonably good model?

**Answer:**

Run the numbers first, because for most people the math kills the idea immediately.

**The break-even calculation**

```python
gpu_cost_cny = 50_000          # ~$6,900
power_w = 300                  # A6000 TDP, 24/7 serving
elec_cny_kwh = 0.6
elec_per_year = power_w / 1000 * 24 * 365 * elec_cny_kwh  # ≈ ¥1,580/yr

# What 48GB buys you: ~70B dense @ Q4, or a 30-40B class model at high quality
# Comparable API: deepseek-v4-flash tier, roughly ¥1-3 per 1M tokens blended
api_cost_per_1M = 2.0
tokens_to_break_even = gpu_cost_cny / api_cost_per_1M * 1_000_000
print(f"{tokens_to_break_even/1e9:.0f}B tokens")  # → 25B tokens
```

At your own consumption rate (~1B tokens/month), ¥50k of hardware equals roughly **two years of API tokens** — except the API gives you frontier models (DeepSeek v4 full, Claude), while the A6000 caps you at ~30B models in FP16 or 70B-class models at 4-bit quantization in 48GB. And the hardware depreciates: used A6000s already sit around $2,500 on the workstation market, so buying new at ¥50k is buying instant depreciation. Cloud rental makes the comparison worse: A6000 on-demand averages ~$0.71/hr — ¥50k buys ~9,700 rental hours, over a year of 24/7.

So pure cost-per-token **never** justifies it. The users it actually makes sense for:

1. **Privacy/compliance-bound users.** Lawyers, doctors, finance people (your bank context!), anyone processing data that contractually cannot leave the premises. Here API is not an option at any price, so the comparison is "local vs nothing."

2. **24/7 background-agent users.** Someone running continuous pipelines — synthetic data generation, codebase indexing, log analysis, agent loops grinding all night. If you'd genuinely burn 50-100B+ tokens/year on tasks where a 32-70B model is *good enough*, marginal cost ≈ electricity wins. A 70B Q4 runs at ~18-25 tok/s on an A6000; a 32B-class model at Q5 fits in ~26GB and is tuned for multi-hour autonomous agent loops — fine for batch, painful for interactive coding.

3. **People learning inference infrastructure as the product.** If the goal is to *become* good at vLLM, quantization, KV-cache tuning, speculative decoding — the GPU is tuition, not a token vending machine. (This is the only category you partially fit.)

4. **Latency/offline-critical users.** Home automation, voice assistants, air-gapped setups.

**For you specifically: don't buy it.** You already own a 4070 for small-scale experiments and rent MI300X at $2/hr — ¥50k is ~3,500 MI300X hours, which is vastly more training compute than an A6000 ever delivers (Ampere, no FP8, 768 GB/s bandwidth vs 5.3 TB/s HBM3). Your usage pattern (frontier-model coding agents + occasional training bursts) is the textbook case for *renting*. The only scenario where I'd reverse this: if your bank work spawns a side business needing private inference, or you decide inference-serving engineering is your next deep-dive — then buy **used** (¥18-25k for a used A6000, or wait for 48GB Blackwell workstation cards) rather than ¥50k new.

One quantization-era caveat: the "quite good model" bar keeps moving. MoE models with small active params (GPT-OSS-120B-style, ~5GB active) increasingly favor *high RAM + moderate VRAM* boxes (Mac Studio, Strix Halo) over a single 48GB card for home serving — worth checking before committing ¥50k to a 2020-architecture GPU.

**References:**

- [RTX A6000 Cloud Pricing — getdeploying.com](https://getdeploying.com/gpus/nvidia-a6000)
- [GPU Shortage 2026: Should You Buy Now for LLM?](https://bestgpuforllm.com/articles/gpu-shortage-2026-llm-buying-guide/)
- [Best Local LLM for RTX A6000 (2026)](https://openclawdc.com/blog/best-local-llm-rtx-a6000/)
- [48GB GPU Server Hosting benchmarks](https://www.gpu-mart.com/vram/48gb-gpu-server)
