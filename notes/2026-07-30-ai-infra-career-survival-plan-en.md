---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Infra Career Survival Plan
translated: false
type: note
---

Question: **Given my situation (AI infra transition, no formal degree, 900k CNY mortgage, leaving bank contractor job tomorrow), how should I survive and plan my career?**

Answer:

First: **do not think of yourself as a fresh AI engineer.** Your position is unusual.

You have:

* 11 years engineering experience
* backend/distributed systems experience
* cloud/Linux/Kubernetes
* real LLM training experience:

  * GPT-2 124M from scratch
  * nanoGPT/nanochat experiments
  * vLLM exploration
  * GPU debugging
  * CUDA/ROCm exposure
* shipped products before

The problem is not capability. The problem is **market signaling**.

A degree is a filter for HR. It is not the core requirement for AI infra.

But with 900k mortgage, you cannot make a romantic "quit everything and research AI" move. You need a **two-track strategy**.

---

## 1. Next 3 months: survival mode

Your priority:

**Cash flow > perfect AI job**

Do not burn runway.

Your target:

* Maintain income: 20k-40k RMB/month
* Move toward AI infra every month

Possible paths:

### Path A: AI Infra Engineer (best)

Roles:

* LLM Platform Engineer
* Inference Engineer
* ML Infrastructure Engineer
* AI Backend Engineer
* Agent Infrastructure Engineer

Your existing backend background maps well.

The pitch:

> "Backend engineer transitioning into LLM infra. Built and trained GPT models, deployed inference systems, optimized GPU workloads."

Not:

> "I have no degree and want to learn AI."

---

### Path B: AI consulting / outsourcing

You already have an advantage.

Many companies need:

* RAG systems
* private LLM deployment
* agent workflows
* internal AI tools

A small company may pay:

* 30k-80k RMB/project

Your engineering background is valuable here.

---

### Path C: Keep a bridge job

A mistake would be:

```
bank contractor
     |
     v
unemployed
     |
     v
study AI 6 months
     |
     v
job hunting
```

Mortgage makes this dangerous.

Better:

```
bank contractor
      |
      +---- freelance AI projects
      |
      +---- AI infra portfolio
      |
      v
AI infra job
```

---

# 2. Your AI infra roadmap

Do not learn more models.

You already know enough theory.

Now build production evidence.

## Month 1

Build:

### Project 1: Mini vLLM clone

Implement:

```
prompt
 |
tokenizer
 |
KV cache
 |
continuous batching
 |
scheduler
 |
CUDA kernel
 |
generation
```

Even a toy version.

Repository:

```
github.com/lzwjava/my-vllm
```

README:

```
Implemented:
- PagedAttention
- KV cache management
- batching scheduler
- tensor parallel inference
```

This signals AI infra.

---

## Month 2

Build:

### Production LLM serving stack

Example:

```
Client
 |
FastAPI
 |
Ray
 |
vLLM
 |
NVIDIA GPU
 |
Prometheus
 |
Grafana
```

Add:

* autoscaling
* monitoring
* latency benchmark

Measure:

```
tokens/sec
TTFT
GPU utilization
memory usage
```

---

## Month 3

Contribute upstream.

Targets:

* vLLM
* llama.cpp
* PyTorch
* Triton

Even small PRs.

A single merged PR can replace a degree signal.

---

# 3. Degree problem

The reality:

Large companies:

```
Google
Meta
OpenAI
Anthropic
NVIDIA
```

often use degree filters.

But AI infra ecosystem is different.

Many teams care about:

```
Can you make GPU cheaper?
Can you increase throughput?
Can you debug CUDA?
Can you deploy models?
```

Your advantage:

Most people who have degrees cannot do what you already did.

A person with CS PhD but no production experience may not know:

```
nvidia-smi failure
CUDA mismatch
flash-attn build
distributed training
Linux kernel issues
```

You do.

---

# 4. Financial plan with 900k mortgage

Assume:

Mortgage:

900k RMB

Don't optimize for maximum salary first.

Optimize for:

```
survival probability
```

Your hierarchy:

## Level 1

Stable income:

20k+/month

↓

## Level 2

AI transition

↓

## Level 3

30k-50k/month AI infra

↓

## Level 4

Consulting/startup

---

Avoid:

* buying more GPU hardware
* spending 6 months only reading papers
* chasing PhD-level theory
* quitting without income

You already have enough compute.

Your RTX 4070 is enough for portfolio work.

---

# 5. Your story matters

Your background is actually a strong founder/engineer story:

```
self taught programmer
 |
mobile/backend engineer
 |
built products
 |
learned deep learning
 |
trained GPT models locally
 |
building AI infra
```

This is closer to:

* Karpathy style
* independent researcher-engineer

than traditional graduate student.

Use it.

---

# 6. My recommended next 12 months

```
Aug-Sep 2026

Get income bridge
+
build vLLM-like project


Oct-Dec 2026

Apply:
- AI infra engineer
- LLM platform engineer
- AI backend engineer

Contribute OSS


2027

Choose:

A:
Senior AI infra engineer

or

B:
AI consulting company

or

C:
AI startup
```

---

The key decision tomorrow is not "should I leave the bank job?"

The key question is:

**After leaving, how many months of runway do you have?**

Calculate:

```
cash savings / monthly family expense
```

If runway < 6 months:

Get income immediately while transitioning.

If runway > 12 months:

You can aggressively build AI infra portfolio.

Given your mortgage, I would personally optimize for **income + AI transition simultaneously**, not pure exploration. You are already past the beginner stage; the next step is turning your AI ability into market proof.
