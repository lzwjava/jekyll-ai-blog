---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Learning NanoGPT: Run First Then Study"
translated: false
type: note
---

Question: Is a good approach to learning NanoGPT training to start running it on a home server with an RTX 4070 (or similar GPU), and then study the details by reading papers?

Answer:

Yes — this is actually one of the best ways to learn. Here's why it works, and how to structure it.

---

## The "Run First, Read Later" Learning Loop

The excerpt you shared reflects expert intuition that only comes from *having trained models before*. The goal is to build that intuition yourself.

### Why Starting with Hardware Makes Sense

- **You get grounded feedback immediately** — loss curves, GPU utilization, OOM errors, training time estimates are all real and tangible
- **Papers become meaningful** — when you read "cosine LR decay," you've already *seen* what happens at the end of a run; the paper is now explaining something you observed, not something abstract
- **Debugging builds intuition faster than reading** — figuring out why your val loss is noisy teaches more than a paragraph about regularization

---

## Practical Learning Path

### Phase 1 — Just Run It (Week 1)
```bash
# Clone and run the Shakespeare char-level demo first
git clone https://github.com/karpathy/nanoGPT
python data/shakespeare_char/prepare.py
python train.py config/train_shakespeare_char.py
```
- Watch the loss curve drop in real time
- Note when it flattens
- Try intentionally breaking things (huge LR, tiny batch) to see what happens

### Phase 2 — Scale to Your Hardware (Week 2)
On an RTX 4070 (12GB VRAM), reasonable configs:

| Model Size | Batch Size | Context | Approx Time |
|---|---|---|---|
| 124M (GPT-2 small) | 12–16 | 1024 | ~20–40h on full data |
| 50M custom | 32 | 512 | ~8–12h |
| Shakespeare char | 64 | 256 | ~15 min |

Start small, validate your setup, then scale.

### Phase 3 — Read the Papers (Parallel, not after)
Read *while* a run is in progress. Good order:

1. **Attention Is All You Need** (2017) — the Transformer architecture you're training
2. **GPT-2 paper** (Radford et al., 2019) — exactly the model nanoGPT implements
3. **Chinchilla** (Hoffmann et al., 2022) — teaches you *why* the token/parameter ratio in your run matters
4. **The Karpathy "Let's build GPT" video** — bridges code ↔ paper perfectly

### Phase 4 — Interpret Your Runs
Now re-read your own training logs with paper knowledge:
- Why did loss flatten at step 12k?
- Was your run compute-optimal (Chinchilla ratio)?
- What would a 350M run realistically cost you?

---

## What the Excerpt Is Teaching You

The reasoning in that block is a masterclass in **applied ML economics**:

| Concept | What It Means Practically |
|---|---|
| Sunk cost reasoning | 46 GPU-hours already spent; marginal cost of finishing is only 14h |
| Baseline discipline | Never compare future runs to an incomplete reference |
| LR decay completion | A half-decayed cosine schedule gives a noisier, pessimistic val loss |
| Experiment sequencing | Lock in cheap baselines before committing to expensive runs |

You will only *feel* this reasoning after you've killed a run early and regretted it, or compared two runs where one had a clean decay and one didn't.

---

## Bottom Line

> **Run → Observe → Break → Read → Repeat**

The RTX 4070 is genuinely capable for this learning loop. 124M parameter models are within reach. The papers will transform from abstract math into explanations of things you've already seen happen on your screen. That's the fastest path to real understanding.
