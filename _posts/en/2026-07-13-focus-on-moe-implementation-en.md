---
audio: false
generated: true
image: false
lang: en
layout: post
title: Focus on MoE Implementation
translated: false
type: note
---

## Your Current Position (from evidence in your notes + portfolio)

**Done:**
- GPT-2 124M from scratch (SEC filings, RTX 4070, val loss 2.28)
- GPT-2 760M on MI300X (nanochat experiments)
- nanoGPT fork with 45 commits (dataset pipelines, training configs, shape annotations)
- Two-node DDP debugging (CPU gloo hang)
- H200 nanochat runs (device_batch=32 sweet spot on d24 model)
- SEC-EDGAR-GPT end-to-end (paper + chatbot + website in 3 days)
- CLI agents (ww, iclaw, zz) — full stack ownership
- 3B+ tokens/yr API consumption
- 10K+ blog posts + 9.7K+ AI notes

**Read about but not yet implemented:**
- MoE routing in your own code
- MLA from scratch
- FlashAttention kernel-level understanding
- Distillation pipeline (student/teacher)

**The key signal from your own notes:**

Your training log shows a loss plateau at 1.25-1.39 after 35K steps. The LR decay just started. This is important — you're *actively training models right now* and observing their behavior. Very few people do that.

---

## Answer: Focus, not breadth

Given your actual state, **don't go broad**. You already have solid breadth — MoE theory, MLA theory, agent loops, DDP debugging, kernel-level understanding. The gap is implementation depth.

Your friend was right when they said **one main axis + one supporting axis**. I'd refine it based on your actual trajectory:

### Main axis: MoE from scratch

This is your highest-leverage move because:

1. You already have `nanoGPT` forked and well-understood
2. You already wrote about DeepSeek MoE, Kimi Linear — time to own it in code
3. The skill compounds: MoE + routing → load balancing → expert collapse → inference optimization
4. Fits your hardware perfectly (only active params matter)

The concrete project:

```
nanoGPT-MoE on RTX 4070
├── Week 1-2: Implement Switch Transformer MoE FFN
│   ├── Replace dense FFN with MoE (8 experts, top-2 routing)
│   ├── Add load balancing loss
│   └── Train GPT-2 50M, compare loss curves
├── Week 3-4: Routing analysis
│   ├── Expert utilization heatmaps
│   ├── Load balancing vs no load balancing
│   └── top-1 vs top-2 vs top-k routing
├── Week 5-6: Training dynamics
│   ├── Expert collapse detection
│   ├── Capacity factor tuning
│   └── Compare dense vs MoE at same active parameter count
└── Write: "Training Small MoE from Scratch" — your own paper
```

### Supporting axis: MLA implementation

Do this second, after MoE is running. Since you already read about it:

```
nanoGPT-MLA on RTX 4070
├── Implement MultiHeadLatentAttention
│   ├── KV compression into latent space
│   ├── Compare KV cache size vs standard MHA
│   └── Benchmark: memory, speed, quality
├── Hybrid: MoE + MLA
│   └── This is exactly DeepSeek's recipe
└── Write comparison
```

### What to skip (for now)

| Direction | Skip reason |
|-----------|-------------|
| FlashAttention kernel | Important but your RTX 4070 doesn't need custom kernels — PyTorch SDPA + FlashAttn-v2 works. Come back when you hit inference bottlenecks |
| RLHF/GRPO | Poor hardware fit (needs reward model, multi-stage training). Learn later via distillation axis |
| Big model training | H200 10h bursts are fine for teacher generation. Don't make it your identity |
| Pure RL | Your advantage is systems + architecture, not theory |

---

## GPU build recommendation

Don't buy 3 machines immediately. Your current build plan should be:

**Phase 1 (now, 0 new GPUs):**
- RTX 4070 (main dev + MoE training)
- MI50 (ROCm exploration on the side)

Run MoE experiments on the 4070 for 2 months. You'll learn exactly what bottlenecks matter.

**Phase 2 (after MoE experiments reveal the bottleneck):**
- If VRAM-limited: add a used RTX 3060 12GB (~$150-200) for parallel experiments
- If compute-limited: H200 RunPod for 24-48h monthly (large MoE training)
- The MI50 is for ROCm learning, not productivity

**H200 usage pattern:**
- Monthly 24-48h burst, not weekly
- Use for: large MoE training runs (760M+), teacher generation for distillation
- Do NOT use for: daily iteration, debugging, architecture changes

---

## Your 6-month identity

Not "I study LLM."
Not "I do MoE."

Better:

> **"I train small efficient LLMs from scratch and understand every layer."**

This connects:
- Your nanoGPT work (you already own from-scratch training)
- Your planned MoE + MLA implementations
- Your hardware constraints turned into advantage
- Your ability to write + document experiments

The output is a series of concrete artifacts:

1. `nanoGPT-MoE` — trained MoE models with loss curves and expert analysis
2. `nanoGPT-MLA` — trained models with KV cache comparison
3. A published experiment log (blog posts, your existing pattern)
4. A training procedure doc that's deeper than any paper reproduction

You're already in the top 1% of people who have trained a GPT-2 from scratch on real data. Narrowing to "I train small efficient models and understand exactly what happens inside" is a genuinely differentiated position.

Start with the MoE FFN replacement in nanoGPT this week. The code change is approximately 150 lines. Everything else follows from that.
