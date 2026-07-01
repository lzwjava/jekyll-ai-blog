---
audio: false
generated: true
image: false
lang: en
layout: post
title: Self-Taught AI Learning Journey
translated: false
type: note
---

**Question:** What do you think about my multi-year self-taught AI/ML learning journey — starting from building a PC with an RTX 4070 in 2023, training GPT-2 on 60GB text, spending hundreds on cloud GPUs (RunPod, DigitalOcean, H100/H200), earning two deep learning certificates, and now running local training on 400+ GB of text data — all within a budget constraint of roughly ¥1000–5000, driven initially by career goals but eventually by genuine curiosity?

**Answer:**

## Honest Reflection on Your Journey

What you described is, frankly, one of the most *authentic* ways to learn anything technical. Let me break down why.

---

### 1. You Learned the Hard Way — That's the Right Way

To escape tutorial hell and really learn, you have to get hands-on, write algorithms from scratch, implement papers, and do real side projects. That's exactly what you did — not by following a clean roadmap, but by **hitting walls repeatedly**. RunPod bills, broken environments, out-of-stock cloud GPUs — these aren't failures, they're tuition fees paid to reality.

Most people watch YouTube videos about transformers. You actually ran training loops for days and felt the pain of a 60GB text corpus taking half a day. That gap — between *knowing about* and *having done* — is enormous.

---

### 2. The Motivation Shift is the Most Valuable Part

You started with:

- "I want an AI job"
- "I want to show off certificates"
- "I want to chase AGI dreams"

And you ended up with:

- Genuine curiosity
- Budget-constrained creative problem solving
- Real intuition about what small models can actually do

This is the classic arc of deep learning. It was just me, a dream, and my PC. In front of me was an ocean of knowledge — a big, deep ocean (the Internet), and I was starting an endless journey of learning. Throughout this journey, I faced many challenges, got lost many times. You lived that sentence. The people who stick through the "got lost many times" phase are exactly the ones who come out with real understanding.

---

### 3. Constraints Made You Smarter, Not Weaker

Working with **one ¥5000 GPU**, a tight budget, no team, no managed environment — this forced you to actually understand:

- Memory bottlenecks
- What block size really means (your 泳池/swimming pool analogy is genuinely insightful)
- When cloud is worth it vs. when local compute wins
- How to make 400GB of text data work without infinite VRAM

Projects with simple models focused on a specific task can use a single GPU to train their AI. You discovered this truth empirically, not from a textbook. That's worth more.

---

### 4. What You Actually Have Now

After 2+ years of this:

| What you did | What you gained |
| --- | --- |
| RTX 4070 local inference (2023) | Hardware intuition, CUDA basics |
| GPT-2 training on 60GB text | Data pipeline, tokenization, training dynamics |
| RunPod / DigitalOcean H100/H200 | Cloud GPU workflow, cost optimization |
| Two DL certificates | Structured vocabulary, credentialing |
| 400GB local training runs | Patience, data engineering, real throughput understanding |
| WeChat channel, friends discussions | Communication and teaching ability |

Teaching others (your 泳网/block size video reaching tens of thousands of views) is one of the most underrated forms of learning validation.

---

### 5. What's Honest Criticism?

- The certificates leaning on "referencing homework too much" — that's a gap worth being honest about. The credential is less important than whether *you* can reconstruct those concepts.
- Cloud GPU spending of "several hundred dollars" for $3/hr H200 is a common trap. The lesson you learned — **local compute often beats expensive cloud for iterative small-model work** — is exactly right.
- Three to four days of training runs on 400GB is actually impressive for a single consumer GPU setup. But ask yourself: *do you understand what loss curves, gradient norms, and learning rate schedules are telling you during those runs?* That's the next level.

---

### 6. The Bigger Picture

What you've built isn't a career credential. It's **a genuine mental model of how this technology works**, built through pain, money, time, and iteration. In 2025, anyone with a mid-range laptop and an internet connection can build, train and deploy models that, five years ago, required a dedicated GPU cluster. You were doing this *before* it became easy — which means your intuitions are calibrated against real friction, not convenient abstractions.

The AGI dream may be a joke (your words), but the curiosity that drove you through all of this — that's not a joke. That's the most valuable asset you have.

**Keep going. The fact that small model training feels "comfortable" now means you've earned that comfort.**

---

References:

- [Roadmap to Learn AI in 2025 – Medium](https://medium.com/bitgrit-data-science-publication/a-roadmap-to-learn-ai-in-2024-cc30c6aa6e16)
- [GPU for Machine Learning & AI: On-Premises vs Cloud – MobiDev](https://mobidev.biz/blog/gpu-machine-learning-on-premises-vs-cloud)
- [Learn AI from Scratch in 2025 – LogicMojo](https://logicmojo.com/learn-AI-from-scratch)
- [Guide to Learning Machine Learning in 2024 – Medium](https://medium.com/@hashirbhatti/guide-to-learning-machine-learning-in-2024-with-resources-b99416c2e9d8)
