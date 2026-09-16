---
audio: false
generated: true
image: false
lang: en
layout: post
title: Eight-Computer AI Sandbox
translated: false
type: note
---

This is a great question for you specifically. Let me think about what fits *your brain* — impatient, hands-on, loves AI/tech, hates boring theory, wants to build real things.

5-8 old computers running Ubuntu is actually a **perfect sandbox** for someone like you. Here's what I'd do:

---

## 1. Build Your Own AI Cluster (the obvious choice for you)

Your notes are full of AI/ML: DeepSpeed, Flash Attention, LoRA, efficient inference, Groq speed. But you probably can't afford RTX 4090s.

With 5-8 old machines:

- **Distributed LLM inference** — run Ollama/vLLM across all 8 machines. Serve one big model (like Llama 3) split across them. Learn how model parallelism, tensor parallelism, pipeline parallelism actually work.
- **Distributed training playground** — set up DeepSpeed or PyTorch DDP across your cluster. Train tiny models. Watch how communication overhead kills speed. Learn why GPUs matter by *feeling* the pain of CPU-only distributed training.
- **Build your own "poor man's TPU"** — use MPI + OpenBLAS to implement matrix multiplication across machines. This is how people understood AI before GPUs existed.

**Why this fits you:** You'll learn *deeply* because you'll hit real bottlenecks (network latency, memory bandwidth) and have to solve them. No simulator, no textbook — real hardware, real problems.

---

## 2. Build a Kubernetes Cluster & Make It Do Something Useful

Not just "install Kubernetes because everyone says so." Make it **serve something real**:

- A model API that load-balances across 5 machines
- An auto-scaling web service that spins up pods on demand
- A CI/CD runner that builds and tests your code across the cluster

**Why this fits you:** You hate slow processes. Kubernetes is slow and complex. You'll get frustrated — and then you'll *deeply understand* why distributed systems are hard. Your impatience will force you to optimize, debug, and truly learn.

---

## 3. Build a Private "AI Factory"

Set up a pipeline that your 8 machines work on together:

```
Machine 1: Web scraper → collects data
Machine 2: Data processor → cleans, deduplicates
Machine 3-5: Training workers → fine-tune small models
Machine 6: Inference server → serves the model
Machine 7-8: Evaluation/Testing → runs benchmarks
```

Then let it run 24/7, generating output for your blog, your experiments, your side projects.

**Why this fits you:** You love output (42K+ posts). You love automation. This is a system that *produces* while you sleep.

---

## 4. The "Convex Hull Rocket Landing" Project (remember your note?)

You were obsessed with the guy who built his own rocket and used convex hull algorithms for landing. Now you have 8 computers:

- **Simulate** the rocket's flight computer with one machine
- **Simulate** sensors on another machine
- Build a **distributed real-time control system**

You can't afford a real rocket. But you can build the control software, the simulation, the sensor fusion — and run it across your cluster. If you ever get access to real hardware, your code is ready.

---

## 5. Bittorrent + AI = Distributed Dataset Training

Your old machines have one advantage: **storage**. 8 machines × cheap hard drives = lots of storage.

Build a distributed system that:
- Downloads datasets via Bittorrent (fast! distributed!)
- Shares them across your cluster via NFS or GlusterFS
- Trains different parts of a model on different machines
- Syncs results

This is essentially how large AI labs work — but you'll build it yourself, from scratch.

---

## The Most Important Thing (from your own experience)

You wrote this:

> *"Do something one loves, will learn deeply. If not love something, and then forcibly do it, people will cheat."*

So the real question is: **Which of these sounds like play, not work?**

- If the AI cluster sounds fun → do that
- If the Kubernetes battle sounds fun → do that
- If building a distributed system from scratch sounds fun → do that
- If none of them excite you → don't do any of them. Sell the computers. Buy something that *does* excite you.

Your 5-8 old machines aren't a limitation. They're a constraint that forces creativity. And constraints, for a builder like you, are more interesting than unlimited resources.

---

**My pick for you:** Build a tiny AI inference cluster. Serve a model across 8 machines. Feel the latency. Optimize it. Make it fast. Your 100+ notes on speed/efficiency will suddenly have a real home. 🚀
