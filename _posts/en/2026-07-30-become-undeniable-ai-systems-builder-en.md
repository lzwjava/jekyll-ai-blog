---
audio: false
generated: true
image: false
lang: en
layout: post
title: Become Undeniable AI Systems Builder
translated: false
type: note
---

**Question: What should I do in the next few months?**

Given your current trajectory (AI engineer transition, already training LLMs, building agents, running consulting, blog/community, and having strong backend experience), I would optimize for **becoming visibly undeniable as an AI systems builder** rather than collecting more knowledge.

The next 3–6 months should be:

## 1. Build a public AI engineering portfolio (highest ROI)

You already have rare experience:

* trained GPT-2 124M from scratch on RTX 4070
* trained nanochat-scale models
* debugged CUDA / FlashAttention / vLLM
* built agents
* ran production systems

Most "AI engineers" cannot show this.

Turn it into artifacts.

### Project A: "Train LLM from scratch" series

Repo:

```
github.com/lzwjava/llm-from-scratch
```

Structure:

```
01-tokenizer
02-nanogpt-baseline
03-pretraining-gpt2-124m
04-distributed-training
05-eval
06-inference-engine
```

Write blog posts:

* "I trained GPT-2 124M on RTX 4070"
* "What happens inside the transformer forward pass"
* "Building vLLM-like inference from scratch"

This attracts:

* AI startups
* recruiters
* researchers

---

## 2. Build one serious AI agent product

Don't build another chatbot.

Build something with business value.

Examples:

### Option 1: AI coding agent

Like a mini Claude Code:

Architecture:

```
User
 |
CLI
 |
Agent loop
 |
+-- planner
+-- tool executor
+-- code search
+-- git operations
+-- test runner
 |
LLM
```

Your advantage:

* Java/backend experience
* Linux
* infra
* LLM knowledge

Possible repo:

```
ww-agent
```

Features:

```
ww fix bug
ww explain repo
ww refactor module
ww generate tests
```

---

### Option 2: AI consulting demo

Create:

```
AI Enterprise Agent Platform
```

Demo:

```
PDF
 |
RAG
 |
Agent
 |
ERP/CRM/API tools
 |
approval workflow
```

Target:

* Chinese enterprises
* Singapore companies
* overseas SMBs

You can sell this.

---

## 3. Learn inference deeply (next frontier)

You already touched training.

The industry value is moving toward:

```
Training
   |
   v
Inference systems
   |
   v
Agents
   |
   v
AI products
```

Spend 1–2 months understanding:

### vLLM internals

Implement:

```
PagedAttention
KV cache
continuous batching
scheduler
tensor parallel
```

Minimal version:

```
tokens
 |
scheduler
 |
KV cache manager
 |
attention kernel
 |
GPU
```

Your background fits this very well.

---

## 4. Improve your English technical presence

Your advantage is unusual:

Chinese + English + AI engineering.

Write English posts:

Examples:

```
I trained GPT-2 124M on a $600 GPU.
Here is what I learned.
```

```
Understanding vLLM by implementing it from scratch.
```

```
Building an AI coding agent in Python.
```

Post:

* GitHub
* Hacker News
* Reddit r/MachineLearning
* X/Twitter

One viral technical post can create opportunities.

---

## 5. Don't spend too much time on fundamentals now

You already passed the beginner stage.

Avoid:

* watching endless courses
* reading random papers
* trying every new model

Your bottleneck is not knowledge.

Your bottleneck:

```
knowledge
   |
   v
artifact
   |
   v
users
   |
   v
money/opportunities
```

---

## Suggested timeline

### August 2026

Goal: portfolio

```
finish:
- GPT training repo
- 3 technical blogs
- GitHub cleanup
```

---

### September

Goal: inference

```
implement:
- mini vLLM
- KV cache
- batching
```

Publish.

---

### October

Goal: product

Ship:

```
AI coding agent
or
enterprise AI agent demo
```

Find first users.

---

### November-December

Convert:

```
portfolio
    |
    v
job offers / consulting clients / startup revenue
```

---

## One strategic observation

Your current profile is actually closer to:

```
Karpathy-style builder
+
Chinese startup engineer
+
production backend engineer
```

The missing piece is **public proof**.

A person who says:

> "I know LLMs"

is common.

A person who says:

> "I trained GPT-2 on my RTX 4070, implemented attention, built an inference engine, and shipped agents used by customers"

is rare.

Your next months should maximize that gap.
