---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ship FinGPT Experiment
translated: false
type: note
---

Based on your notes from the last 24 hours, here's what I see you've been deep-diving on and what makes sense to do today:

---

## Your Recent Focus (Last 24h)

1. **Financial LLMs** — BloombergGPT vs FinGPT deep dive
2. **LoRA fine-tuning** — contrarian truths, practical limits
3. **RTX 4070 compute budget** — what you can actually train (300-500M params)
4. **Blog infrastructure** — Jekyll/GitHub Pages migration constraints
5. **SGLang/Triton** — getting inference working on your workstation
6. **CC BY 4.0 licensing** — for your notes knowledge base

---

## What To Do Today

### 1. **Ship the FinGPT-style experiment on your RTX 4070** (Highest Priority)

Your notes already laid out the exact recipe — take Qwen or Llama-3-8B, build a small financial sentiment instruction set from headlines, QLoRA-tune on your 4070. This is the portfolio piece that bridges your banking domain + AI engineering transition. You already have SGLang serving working, so you can test immediately after training.

```bash
# Start on your workstation
ssh lzw@192.168.1.36
# Clone FinGPT, adapt their pipeline to your hardware
```

### 2. **Fix the SGLang/Triton segfault** (Unblock Inference)

You hit a Triton 3.5/3.6 segfault on Ada architecture. Your notes say Triton 3.3.1 + cu126 avoids it. Make sure `~/sglang-env` is stable so you can serve models after fine-tuning.

### 3. **Register `lzwjava.com`** ($10/yr)

Your notes concluded: owning the apex domain is worth it for portability. You have 400+ posts and 8,000 notes — being locked to `*.github.io` is unnecessary risk. This is a 10-minute task.

### 4. **Apply CC BY 4.0 to your notes**

You researched the license. Now apply it — add a LICENSE file to your notes repo with CC BY 4.0. Quick win.

### 5. **Set up rsync backup to Mini M4**

Your notes mention rsync 2.6.9 drops on big transfers but re-run resumes. Run `mini-backup.sh` to huarong@192.168.1.54 — get your 25GB backup current.

---

## The Bigger Picture

Your notes show you're building the exact stack that matters: **training** (nanoGPT/LoRA), **serving** (SGLang), **domain expertise** (financial LLMs), and **infrastructure** (GPU machines, backups). The FinGPT experiment is the highest-leverage thing because it produces a tangible artifact that demonstrates all four.

What do you want to tackle first?
