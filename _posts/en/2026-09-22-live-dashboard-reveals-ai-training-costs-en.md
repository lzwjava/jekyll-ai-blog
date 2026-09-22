---
audio: false
generated: true
image: false
lang: en
layout: post
title: Live Dashboard Reveals AI Training Costs
translated: false
type: note
---

**Question:** What does the MiMo-V2.6 RL dashboard actually show?

**Answer:**

The dashboard exposes an unusually detailed live picture of a large-scale AI training run. Here's a breakdown of everything it displays:

---

### 📈 Training Progress

The page shows metrics from two runs — `mimo-v2.6-pro` and `mimo-v2.6-flash` — both started on September 15, 2026. As of September 17, the pro run had completed 13 RL steps (processing 27.6 billion tokens) and the flash run had completed 15 steps (35.2 billion tokens). Each step consumes about 2.5 billion tokens.

---

### 💰 Running Cost Counter

A live counter shows about **$1.23 million USD** spent across both runs: roughly $853,000 on pro and $378,000 on flash — accumulated in just about two days.

---

### 🏆 Reward Curves (Model Quality)

The headline metric, `dynsam/avg@n`, averages reward scores across each prompt's rollouts. It had reached **0.624 for pro** (+0.059 since step 1) and **0.596 for flash** (+0.083) — meaning the models are slowly but measurably getting better at each RL step.

---

### 🧪 Mid-Training Benchmark Scores

The team periodically scores training checkpoints on **DeepSWE v1.1**, Datacurve's benchmark of 113 long-horizon software engineering tasks. The latest plotted results were **63.72 for pro** at step 10 and **60.77 for flash** at step 12.

---

### ⚙️ How the Training Works (Internals)

The dashboard reveals unusually detailed internals:

- **Long episodes**: average rollout context was ~100,000 tokens; average episode ran 65 turns on pro and 57 on flash.
- **Step duration**: a single step took 2 hours 36 minutes on pro and 2 hours 5 minutes on flash — half of that time just generating rollouts.
- **Sandboxes**: ~23,700 environments running for pro and ~37,800 for flash.
- **Batch shape**: both runs use 1,568 prompts per batch, with 16 rollout attempts per prompt.

---

### 📂 Task Mix

The sampler's per-dataset targets list **50 datasets in five groups**: code, visual, general, cybersecurity, and chat. **Code datasets make up about two-thirds** of the targets; visual and general tasks are ~13% and ~12% each; cybersecurity ~4%; chat ~3%.

---

### 🚨 Live Infrastructure Problems

The dashboard even shows problems as they happen in real time. One notice said the pro run was "restarting due to a VRAM issue on one node." Another said the flash run was restarted from step 15 because "a type of infrastructure error on one of the datasets was not correctly detected over the past ~3 hours." A separate chart tracks the rate of infrastructure errors per sequence.

---

### 🔍 Why It Matters

Frontier labs usually report post-training results only after training is finished. Here, researchers can see in real time what a production RL run on agentic coding costs (over $1 million in ~2 days), how slowly the reward curve rises, and how much engineering work goes into rollout infrastructure rather than the learning algorithm itself.

---

**References:**

- [Xiaomi Streams MiMo-V2.6 RL Runs Live – NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/xiaomi-mimo-v2-6-live-rl-dashboard)
- [MiMo V2.6 Live Dashboard – Xiaomi](https://mimo.xiaomi.com/rl/)
