---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose One Main LLM Research Axis
translated: false
type: note
---

Question: Based on my current AI progress, how should I choose the next LLM research focus? Should I go broad (MoE, RL, KL, MLA, Flash Attention, etc.) or focus on one/two directions?

Answer:

Looking at your current trajectory, your friend is correct: **the main risk is not lack of knowledge, but too many interesting directions without a research identity.**

Your current profile is actually unusual:

* You already built software systems for 10+ years.
* You have trained GPT-style models yourself (nanoGPT, GPT-2 scale experiments).
* You have touched real GPUs (H200, MI300X, RTX 4070). ([Zhiwei Li][1])
* You write and document aggressively. ([Zhiwei Li][2])
* You prefer open source and source-code-level understanding.

So your advantage is **not competing with PhD researchers doing pure theory**. Your advantage is:

> "I can read papers → modify code → run experiments → debug kernels/systems → publish engineering insights."

I would choose a direction where this advantage compounds.

---

## My recommendation: choose one main axis + one supporting axis

### Main axis: Efficient LLM architecture + inference systems

Specifically:

**MoE + MLA + Attention optimization + small-scale reproduction**

Why?

Because this matches your hardware and engineering background.

DeepSeek-V2 is exactly this area: MoE + MLA. DeepSeek-V2-Lite has 16B total parameters but only 2.4B activated parameters, making it a good research target. ([Hugging Face][3])

The questions are very engineering-heavy:

* How does routing work?
* How does expert imbalance happen?
* How does KV cache reduction work?
* Why does MLA reduce memory bandwidth?
* How do you implement efficient inference?
* How do you modify vLLM / kernels?

These are closer to your strengths.

A good 6-month identity:

> "Open-source LLM efficiency researcher: reproducing and improving MoE/MLA inference."

---

## Second axis: RL / alignment, but not as primary

Your friend mentioned KL divergence and online policy distillation.

This is valuable, but I would not make it your main research.

Reason:

RLHF/RLVR requires:

* reward models
* large-scale experiments
* distributed training
* evaluation infrastructure

The barrier is higher.

Learn it enough:

* KL divergence
* PPO
* DPO
* GRPO
* rejection sampling
* online distillation

But use it as a tool.

Example:

"I improved MoE reasoning model efficiency using RL distillation."

Better than:

"I study RL."

---

# Your current list ranked

## Tier 1: Do deeply

### 1. MoE

★★★★★

Do:

* implement Switch Transformer MoE
* reproduce DeepSeekMoE idea
* train tiny MoE from scratch

Example:

```
GPT-2 124M
      |
      |
replace FFN
      |
      v

MoE GPT-2
8 experts
top-2 routing
load balancing loss
```

Measure:

* training speed
* activated params
* quality
* expert utilization

---

### 2. MLA

★★★★★

Very aligned.

Understand:

Normal attention:

```
K = X Wk
V = X Wv

KV cache:
[layer]
[token]
[key,value]
```

Problem:

Long context:

```
KV cache memory ↑↑↑
```

MLA:

```
KV
 |
compress
 |
latent vector
 |
store smaller cache
```

DeepSeek's MLA reduces KV cache pressure by compressing KV into latent space. ([Hugging Face][3])

Implementation project:

Take nanoGPT:

replace:

```
CausalSelfAttention
```

with:

```
MultiHeadLatentAttention
```

Train.

That is a very strong portfolio project.

---

### 3. Flash Attention

★★★★☆

Learn.

But don't spend 3 months here.

Understand:

Normal:

```
QK^T
 |
softmax
 |
PV
```

Problem:

materializes N×N attention matrix.

Flash:

```
Q block
 K block
  |
 online softmax
  |
 V block
```

Focus:

* IO complexity
* SRAM/HBM
* CUDA/Triton implementation

---

## Tier 2: Learn but don't become identity

### KL divergence

Learn mathematically:

```
KL(P||Q)
=
Σ P(x) log(P(x)/Q(x))
```

Why LLM cares:

Old model:

```
P_old
```

New model:

```
P_new
```

Prevent:

```
P_new drifting too far
```

Loss:

```
RL objective

reward
-
β KL(old,new)
```

Useful everywhere.

But KL itself is not a research direction.

---

### Muon optimizer

Interesting but niche.

Learn after fundamentals.

---

# What I would do if I were you

## Next 3 months:

### Project 1

"nanoGPT-MoE"

Fork Karpathy nanoGPT.

Implement:

```
Dense FFN

       |
       v

MoE FFN

8 experts
top-k router
aux loss
```

Train:

```
GPT-2 50M
GPT-2 100M
```

Dataset:

FineWeb / TinyStories.

Write:

* architecture explanation
* training curves
* routing visualization

---

### Project 2

"nanoGPT-MLA"

Implement:

```
Multi-head Attention

        ↓

Multi-head Latent Attention
```

Compare:

```
memory usage
speed
quality
KV cache
```

---

### Project 3

Inference engineering

Modify:

* vLLM
* llama.cpp
* Triton kernels

Examples:

```
why MLA needs special kernel
why MoE routing costs latency
```

---

# About companies

Your friend gave two paths:

## Path A: company-driven

Examples:

Want DeepSeek-style companies:

Focus:

```
MoE
MLA
distributed training
CUDA/Triton
vLLM
```

Want OpenAI/Anthropic-style:

Focus:

```
reasoning
RL
post-training
eval
agents
```

---

## Path B: frontier idea

Your idea:

> simplify Transformer and attention

Actually interesting.

A possible research theme:

"Small efficient foundation models"

Examples:

```
Can a 1B model achieve 7B quality?

through:

MoE
better attention
distillation
RL
```

This matches your hardware constraints.

---

# My suggested personal research statement for you

Not:

> "I study LLM."

Too broad.

Better:

> "I build and optimize efficient open-source LLM architectures, focusing on MoE, latent attention, and inference efficiency."

That connects:

* DeepSeek
* NVIDIA ecosystem
* open source
* your GPU experiments
* your coding background

---

Your next step should probably **not** be reading 100 papers.

Do:

1. Read DeepSeek-V2 paper.
2. Implement one component.
3. Train a small model.
4. Write results.
5. Repeat.

You already have the "builder loop"; now narrow the research loop. ([GitHub][4])

References:

* DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model ([GitHub][4])
* DeepSeek-V2-Lite model overview ([Hugging Face][3])
* Hardware-Centric Analysis of DeepSeek's Multi-Head Latent Attention ([arXiv][5])

[1]: https://lzwjava.github.io/resume-en?utm_source=chatgpt.com "Resume"
[2]: https://lzwjava.github.io/?utm_source=chatgpt.com "Zhiwei Li"
[3]: https://huggingface.co/deepseek-ai/DeepSeek-V2-Lite/blob/refs%2Fpr%2F11/README.md?utm_source=chatgpt.com "README.md · deepseek-ai/DeepSeek-V2-Lite at refs/pr/11"
[4]: https://github.com/deepseek-ai/DeepSeek-V2?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepSeek-V2: DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
[5]: https://arxiv.org/abs/2506.02523?utm_source=chatgpt.com "Hardware-Centric Analysis of DeepSeek's Multi-Head Latent Attention"
