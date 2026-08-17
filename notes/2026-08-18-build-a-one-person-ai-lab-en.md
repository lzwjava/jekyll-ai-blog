---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build a One-Person AI Lab
translated: false
type: note
---

Question: **What should I focus on over the next few months?**

Answer:

Given where you are now, I would **not** try to optimize for “more things.” You already have enough skills. The next 3–6 months should turn your scattered AI work into **public proof + leverage + optionality**.

My priority would be:

> **Build a small one-person AI lab whose output is strong enough to get you hired, attract clients, or become a company.**

### 1. August–September: go deep on LLM systems

Pick **one serious technical project** and spend ~60–70% of your technical time on it.

I would choose something around:

**LLM training → inference → serving**

For example:

```text
train a small model
      ↓
understand attention / RoPE / MoE / KV cache
      ↓
implement or modify inference
      ↓
vLLM / SGLang
      ↓
benchmark
      ↓
optimize GPU utilization
      ↓
write everything publicly
```

You already trained GPT-2 and have touched vLLM/SGLang/ROCm. Now go one layer deeper instead of jumping to another framework.

A good target:

```text
repo/
├── model/
├── train.py
├── infer.py
├── benchmark.py
├── kernels/
└── README.md
```

And produce **2–4 serious technical notes**:

* How LLM inference actually works
* KV cache + paged attention
* Prefill vs decode scheduling
* GEMM / memory bandwidth / GPU utilization
* One concrete optimization you implemented

The goal isn't the GitHub stars.

The goal is:

> **Someone technically strong looks at your repo and thinks: "This guy actually understands LLM systems."**

---

### 2. September–October: contribute upstream

Don't only build toy projects.

Pick **one ecosystem**:

* vLLM
* SGLang
* PyTorch
* Hugging Face
* ROCm

and make real PRs.

Even something small is valuable:

```text
read issue
   ↓
reproduce
   ↓
understand implementation
   ↓
patch
   ↓
benchmark
   ↓
PR
```

This is particularly valuable for you because you don't have the conventional CS degree path.

Your GitHub becomes part of your credential.

Instead of:

> "I don't have a degree."

you want the evidence to be:

> "Here are my LLM systems projects, here are my benchmarks, here are my upstream PRs, and here is the model I trained."

That's a much stronger signal.

---

### 3. Keep one commercial track alive

Don't turn the next few months into pure research.

Allocate roughly:

```text
70%  AI engineering / research / portfolio
20%  consulting / paid AI work
10%  company experiments
```

For the 20%, sell things you already know how to deliver:

```text
LLM inference deployment
GPU optimization
model fine-tuning
RAG
agent systems
private/self-hosted LLM infrastructure
```

But don't become a generic "AI consultant."

Use consulting to discover **repeated pain**.

If three customers independently ask:

> "Can you make our inference 2× cheaper?"

that's much more interesting than three unrelated consulting projects.

The repeated pain can become the company.

---

### 4. Don't spend the next months building another generic AI app

I'd actively avoid:

```text
another chatbot
another RAG demo
another AI wrapper
another agent framework
another "ChatGPT for X"
```

You already know how to ship software.

Your scarce asset now is **deep technical differentiation**.

I'd rather see you spend 6 weeks making something like:

```text
SGLang scheduler optimization
```

than 6 weeks making:

```text
AI SaaS dashboard #37
```

---

### 5. Keep the education / US path moving, but don't let it dominate

Your US/Canada exploration is useful because it creates another option.

But I wouldn't make:

> "get admitted to a school"

the primary objective of the next few months.

Treat applications as an **optionality project**.

Meanwhile continue building the technical evidence that helps regardless of what happens:

```text
                    ┌── AI job
                    │
technical portfolio ├── consulting
                    │
                    ├── startup
                    │
                    └── master's / immigration option
```

One strong technical portfolio improves all four.

---

## A concrete 90-day plan

### August

**Theme: foundations + one serious project**

* Finish a small LLM training/inference project.
* Read the core papers you're currently circling around.
* Understand the implementation rather than collecting papers.
* Start one public repo.
* Publish technical notes as you learn.
* Continue your school/application research in a separate small time block.

### September

**Theme: systems**

* Go deep into vLLM/SGLang internals.
* Work on one real optimization/feature.
* Benchmark before/after.
* Submit your first meaningful upstream PR.
* Start looking for paid LLM infrastructure work.

### October

**Theme: external validation**

You want to have:

```text
1 serious GitHub project
2–4 deep technical articles
1–3 upstream PRs
1 benchmark/optimization result
1 deployed real-world AI system
some consulting revenue
```

At that point, reassess.

---

## The bigger goal

I think your most valuable move right now is **not choosing between "job vs startup vs research."**

Instead, build something that keeps all three doors open.

Your trajectory can look like:

```text
software engineer
      ↓
LLM engineer
      ↓
LLM systems specialist
      ↓
      ┌───────────────┐
      ↓               ↓
AI company       elite AI job
      ↓               ↓
 independent research / products
```

And your existing experience is actually a good foundation for this: you've already shipped products, built backend systems, trained models, worked with GPUs, and experimented with inference stacks.

So I'd make the next few months **boringly focused**:

> **One hard technical problem. One serious repo. Real benchmarks. Real upstream contributions. A small amount of paid work. Public writing.**

That's enough.
