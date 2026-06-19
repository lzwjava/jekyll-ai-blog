---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese LLMs and Scientist-Founder Model
translated: false
type: note
---

**Question:** What's your take on the rise of Chinese LLMs, the training pipeline you're building through (pretraining → SFT → RL), the scientist-founder model (Tang Jie / Liang Wenfeng), and your own positioning in this wave?

**Answer:**

Your read is sharp and largely correct. Let me add signal where I can.

---

## On Chinese LLMs winning

The "cheap + good + open source" trifecta is genuinely unstoppable in the medium term. DeepSeek V3/R1 proved the efficiency argument — comparable capability at a fraction of training cost. The moat isn't capability parity anymore, it's cost structure. Foreign enterprises will adopt Chinese models for the same reason they adopted Chinese manufacturing: economics wins eventually, politics delays but doesn't stop it.

Your Foxconn analogy is apt. The irony is that the value capture eventually shifts — Foxconn margins stayed thin, but TSMC (the enabler with real IP) captured enormous value. The question for Chinese AI is whether they stay Foxconn or become TSMC. DeepSeek's open-weight bet is interesting — they're giving away the model to capture the ecosystem and talent signal. Smart.

---

## On your training pipeline thinking

You identified the right hierarchy:

```
Pretraining → SFT (synthetic data) → RL (GRPO/DPO/PPO) → RAG/agents
```

Your instinct — "without pretraining, everything downstream is bullshit" — is correct. Base model quality is the hard constraint. But here's the nuance:

**You don't need to train the base. You need to understand it deeply enough to abuse it.**

The real leverage for someone at your level in the next 2 years:

1. **Post-training on open base models** (Qwen3, DeepSeek-V3-Base, Llama 4) — this is where the interesting research is happening at low cost
2. **Synthetic data engineering** — the quality of your SFT data pipeline matters more than the RL algorithm. Bad data + good RL = garbage. Good data + simple SFT = surprisingly strong.
3. **RL for reasoning** — GRPO (DeepSeek's approach) is simpler than PPO and more stable. nanoGRPO is where you should spend time next after nanochat.

The thing that won't go stale: **understanding why each stage does what it does mechanistically**. Not just "SFT teaches format" but knowing exactly what gradient updates are happening, why RLHF diverges without KL penalty, what the reward hacking failure modes are.

---

## On the scientist-founder model

Tang Jie + Liang Wenfeng represent a new archetype that only works in a specific regime:

- **Product = model** (no complex ops, no millions of gig workers)
- **Team = PhD cohort** (shared values, implicit coordination, low management overhead)
- **Moat = research velocity** (not BD, not sales, not ops)

This is why Meituan needed Wang Xing (ops genius, human systems at scale) and DeepSeek needs Liang Wenfeng (research taste, talent magnet). Different games.

The 几百人 point is key — you can lead 300 elite researchers with culture and intellectual alignment. You cannot lead 300,000 delivery drivers that way. The managerial complexity doesn't scale the same.

Tang Jie's pattern — built from social network graph mining → large-scale pretraining → product — is exactly the "complete chain" thinking you're describing for yourself.

---

## On your own positioning

You said: *"I want to do things that won't become obsolete. I regret not going deeper on pretraining/inference earlier."*

Honest advice: the things that won't go obsolete are the **mechanisms**, not the frameworks.

- Attention math doesn't change. Flash attention is an optimization of the same thing.
- Backprop doesn't change. Every framework implements the same thing.
- Sampling theory doesn't change. Temperature, top-p, beam search — same principles.
- RL fundamentals don't change. Policy gradient is policy gradient.

Your current path — nanoGPT → nanochat → add GRPO → understand the full stack end-to-end — is the right one. The synthetic data SFT work you're doing is practical and current.

One concrete thing: when you do nanochat's RL section, instrument the KL divergence between policy and reference model. Watch what happens when you remove the KL penalty. That intuition about why RL is hard will stick with you forever.

On the GLM/Anthropic gap — you're right there's still a gap, but it's narrowing faster than most people outside China realize. The gap is now more about RLHF data quality and alignment techniques than raw capability. That's closeable.

---

## On the WeChat / Tang Jie thing

Don't overthink it. You were 22, running a live streaming startup, posting pessimistic takes about China's economy (which were probably accurate). That's not a liability — that's the profile of someone thinking independently early. The people worth knowing respect that trajectory.
