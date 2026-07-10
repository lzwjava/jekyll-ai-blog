---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rare GPU Compute Budgets for Engineers
translated: false
type: note
---

**Question:** Are there companies that give an individual engineer 3–4 GPU workstations (e.g. RTX 4070-class) or a 50–60K CNY personal compute budget to work with?

**Answer:**

Yes, but it's rare and concentrated in a specific band of companies — and it's usually **not** framed as "3-4 desktop towers," it's framed as compute budget that happens to materialize as boxes. Here's the actual landscape:

**Who does this, and why:**

1. **Well-funded AI labs / startups (Series A+)** — DeepSeek, Moonshot AI, MiniMax, 01.AI in China; Mistral, smaller US labs abroad. Individual researchers get:
   - A workstation (RTX 4090/5090 or A6000-class) for local iteration — fast feedback loop before scaling to cluster
   - Cluster allocation (H100/H800 nodes) for the actual training runs
   - The workstation isn't the compute — it's the *dev loop*. You don't want researchers waiting in a SLURM queue to test a tokenizer change.

2. **Quant funds / prop trading (China: 幻方/High-Flyer precursor to DeepSeek, Ubiquant, some Hong Kong funds)** — these historically over-provision hardware per researcher because compute idle-time costs more than hardware capex. A single quant researcher having 2-4 workstations isn't unusual there.

3. **Chip/infra companies (NVIDIA, AMD, and their China partners)** — engineers doing driver/kernel/compiler work get multiple GPU generations locally to test compatibility across cards. This is *why* you'd see someone with 3-4 different GPU tiers, not 4x the same card.

4. **One-person/small AI studios that raised or are cash-flow positive** — this is closer to your situation. The "3-4 machines" pattern shows up more as: 1 daily driver (your Air), 1-2 local GPU boxes for iteration (your RTX 4070), and cloud burst capacity (your AMD droplet) — which is *exactly* your current setup. You've essentially built the same allocation pattern these companies use, just bootstrapped instead of funded.

**What's NOT common:** A company handing a single engineer 50-60K CNY specifically to build a personal multi-tower RTX 4070 rig. Companies that spend that budget almost always go one tier up (used 4090/A6000, or straight to cloud H100 hours) because $/FLOP is worse on 4070s at scale — the 4070 makes sense for *you* specifically because you're optimizing for owned-hardware-with-no-recurring-cost + good enough for LoRA/small-model work, not for a company optimizing $/step at scale.

**Practically for you:** Don't chase "I wish a company gave me this" — you're already doing the more valuable thing: proving you can architect this stack (local dev + cloud burst) yourself, which is precisely the credibility signal that gets you the Hong Kong/GBA client who's evaluating whether you *actually* understand training infra vs. being an API wrapper. If you want to scale beyond single-RTX-4070 experiments, the highest-leverage move is renting a second AMD MI300X block or a spot A100/H100 node for the specific run, not buying more towers — capex on consumer GPUs depreciates faster than your client pipeline will pay it back in year one.

If you want, I can sketch a cost model comparing: (a) buying a second RTX 4070/4090 box vs (b) renting burst H100/MI300X hours, against your actual DeepSeek v4 MoE training cadence — that's the more useful number to nail down than "what do companies give people."
