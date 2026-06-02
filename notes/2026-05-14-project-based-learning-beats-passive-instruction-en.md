---
audio: false
generated: true
image: false
lang: en
layout: post
title: Project-Based Learning Beats Passive Instruction
translated: false
type: note
---

Question: Is project-based learning (like training nanoGPT hands-on) more effective than certifications or school for deep, lasting understanding?

Answer:

## Yes — And There's Strong Evidence Why

The short answer: **project-based learning beats passive instruction for retention, depth, and real skill transfer.** Here's why, grounded in both learning science and what you're actually doing with nanoGPT.

---

## What You Just Did (and Why It Stuck)

Training nanoGPT wasn't abstract. You hit **real problems**:

- Why does the corpus say 140B but training only sees 10B?
- Why did the downloader produce more than expected?
- What does `BYTES_PER_TOKEN = 4.0` actually mean in practice vs theory (~2.85)?

These aren't textbook exercises. **The confusion was real. The debugging was real. The resolution required you to connect 3 separate files across a codebase.** That's exactly what makes it stick.

---

## The Science Behind It

### 1. Desirable Difficulty (Bjork, 1994)
Learning that feels hard *in the moment* produces stronger long-term retention. Struggling to figure out why `max_iters = 19073` only covers 7% of your corpus is harder than reading a slide — and **10× more memorable**.

### 2. Encoding Specificity
Memory is context-dependent. You don't just remember a fact — you remember **the situation you learned it in**. Years from now, `bytes_per_token` will trigger the memory of debugging that exact discrepancy.

### 3. Transfer Learning (Human Edition)
School teaches you to solve problems that look like the ones you practiced. Projects teach you to **navigate ambiguity** — the actual skill senior engineers use daily.

### 4. Interleaving & Retrieval Practice
A real project forces you to jump between concepts: distributed systems → tokenization → memory layout → training loops. That interleaving is cognitively taxing but **dramatically improves transfer** to new problems.

---

## What Certifications Get Wrong

| Certification / School | Project-Based |
|---|---|
| Teaches to the test | Teaches to the problem |
| Clean, solved examples | Messy, unsolved reality |
| Passive absorption | Active construction |
| Forgotten in 6 months | Remembered for years |
| Validates you learned *about* something | Proves you can *do* something |

Certifications are **signals**, not skills. A hiring manager might use one to filter résumés. But in the room, they'll ask you to debug something — and that's where project learning wins.

---

## The nanoGPT Case Is Especially Good Because

- **Scale is real** — 140B tokens, 263 GB, real shards, real GPU budgets
- **The bugs are real** — `BYTES_PER_TOKEN` being off by 30% is a production-class estimation error
- **The architecture is canonical** — nanoGPT is essentially GPT-2. Understanding it means understanding the transformer backbone of almost every LLM in production
- **The decisions have tradeoffs** — why sample randomly vs sequentially? Why 100M tokens per shard? These aren't arbitrary — and now you know why

---

## The Honest Caveat

Projects alone have one weakness: **you can develop wrong mental models with no one to correct them.** School and books serve as a foundation and error-correction layer. The ideal path:

```
Solid fundamentals (books/courses, fast)
        ↓
Real project (slow, painful, unforgettable)
        ↓
Read theory again (now it all makes sense)
        ↓
Repeat
```

Andrej Karpathy (nanoGPT's author) literally embodies this — deep theory + obsessive hands-on building. That's the model worth copying.

---

## Bottom Line

The lesson you learned today about corpus sizing, token sampling, and training budgets will outlast any ML certification by **years** — because you didn't read it. You lived it.

References:

- [Bjork Learning and Forgetting Lab — Desirable Difficulties](https://bjorklab.psych.ucla.edu/research/)
- [nanoGPT by Karpathy](https://github.com/karpathy/nanoGPT)
- [FineWeb Dataset — HuggingFace](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
