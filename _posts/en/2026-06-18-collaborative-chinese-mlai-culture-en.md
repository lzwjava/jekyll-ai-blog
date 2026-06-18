---
audio: false
generated: true
image: false
lang: en
layout: post
title: Collaborative Chinese ML/AI Culture
translated: false
type: note
---

**Question:** Expand on the point that the overseas Chinese ML/AI community is more collaborative than the general Chinese SWE community — with examples of key figures and what makes this subculture different.

**Answer:**

## Why the ML/AI Chinese Diaspora Is Different

The general "Chinese engineers are less collaborative" pattern breaks down sharply in the ML/AI research and open-source space. This isn't accidental — it's structural.

### The Core Reason: Career Incentives Flip

In corporate SWE, helping a fellow Chinese engineer get a job at your company is a **zero-sum** perception risk — they might compete for your promotion, your project, your visibility.

In ML/AI research and open-source, **sharing makes you more powerful, not less.** Citations, GitHub stars, course enrollments, Twitter followers — these compound. Mu Li's D2L course making you famous doesn't take anything from Song Han. The incentive structure actively rewards generosity.

This is the same reason the *Indian* network advantage doesn't extend as strongly into ML research — it's a corporate/hiring network optimized for job placement, not knowledge sharing.

---

## Key Figures and What They Actually Built

### **Andrej Karpathy**
- Stanford PhD, OpenAI founding team, Tesla AI Director, back to OpenAI
- Wrote **cs231n** (Stanford's deep learning course) — probably the most influential ML curriculum ever made public
- **nanoGPT**, **micrograd**, **llama2.c** — minimal, from-scratch implementations you yourself are studying
- YouTube lectures watched by millions
- His philosophy: *"The best way to understand something is to rebuild it from scratch in the simplest possible way."* — this is exactly your learning style
- He doesn't gatekeep. Everything is public, annotated, minimal.

### **Mu Li (李沐)**
- AWS principal scientist, CMU PhD
- **D2L.ai (Dive into Deep Learning)** — a full textbook with executable code, free, translated into multiple languages, used by hundreds of universities
- **B站 paper reading series** — he reads AI papers live on Bilibili with Chinese commentary. Demystifies frontier research for Chinese-speaking engineers globally
- His paper readings of Attention Is All You Need, ResNet, BERT are canonical
- Actively engages comments, answers questions, mentors publicly

### **Yangqing Jia (贾扬清)**
- Created **Caffe** at Berkeley — one of the first widely adopted deep learning frameworks, before TensorFlow or PyTorch
- Led AI infrastructure at Facebook, now at Alibaba Cloud
- Caffe's open release in 2014 bootstrapped an entire generation of CV researchers
- Less active publicly now but his early open-source contributions had compounding impact

### **Song Han (韩松)**
- MIT professor, co-founded **Efficient ML** group
- Invented **deep compression** (pruning + quantization + Huffman coding) — seminal work on making neural nets run on edge hardware
- **TinyML** and **MCUNet** — running inference on microcontrollers
- Extremely generous with course materials, code, and student mentorship
- His MIT 6.5940 (TinyML and Efficient Deep Learning) is fully public

### **Lianmin Zheng (郑联民)**
- PhD from UCB, core contributor to **Apache TVM**, created **Ansor** (auto-tuning for tensor programs)
- Co-created **vLLM** — the dominant open-source LLM inference engine, now used everywhere
- Co-created **Chatbot Arena / LMSYS** — the human preference benchmark that became the standard for LLM evaluation
- Ships fast, open-sources fast, collaborates with the whole community

### **Tri Dao**
- Stanford PhD, created **FlashAttention** (v1, v2, v3)
- FlashAttention is now inside every serious transformer implementation — CUDA-level rewrite of attention that's 2-4x faster and memory-efficient
- Co-founded **Together AI**
- All code open-sourced immediately. No waiting for a product moat.

### **Hao Zhang**
- Co-created **Alpa** (auto-parallelism for LLMs), **vLLM**, **SkyPilot**
- Berkeley systems + ML intersection — the most practically useful quadrant

---

## The Pattern Across All of Them

| Behavior | What It Signals |
|---|---|
| Open-source everything immediately | Fame > moat in research culture |
| Teach publicly (courses, YouTube, Bilibili) | Influence compounds via students |
| Build minimal didactic implementations | Karpathy ethos: clarity over cleverness |
| Engage with the community directly | Trust-building without corporate filter |
| Cross-collaborate (vLLM, TVM, FlashAttention all cite each other) | Network is meritocratic, not ethnic |

---

## Why This Subculture Formed

**1. Berkeley/Stanford/CMU pipeline**
A disproportionate number of Chinese ML PhDs came through these three programs in the 2012–2020 wave. They built peer relationships *before* corporate incentives kicked in. The collaboration patterns were set in grad school.

**2. The "immigrant has to prove value publicly" dynamic**
Unlike Indian engineers who could leverage an existing hiring network, Chinese ML researchers had to *publish their way* into legitimacy. Open-source and papers were the currency. This forced a culture of public contribution.

**3. China's ML ambition created a dual audience**
People like Mu Li and Song Han can reach both English-speaking researchers *and* the massive Chinese-speaking ML community. This dual leverage makes public teaching unusually high-ROI for them specifically.

**4. DeepSeek's open-weight releases changed the game**
DeepSeek (Wenfeng Liang's team) releasing R1, V3, V4 weights openly — when they had zero obligation to — is the latest and most dramatic example. A Chinese org out-openness'd OpenAI. This has ripple effects on the whole community's norms.

---

## What This Means for You Practically

You're already aligned with this subculture by instinct:

- You're studying nanoGPT (Karpathy's thing)
- You follow Wenfeng Liang and DeepSeek
- You maintain a public knowledge base and blog
- You train models from scratch rather than just calling APIs

**The moves that plug you into this network:**

1. **Write about your MI300X GPT-2 training run** — publicly, with numbers. AMD + large model + from scratch is genuinely rare. Mu Li's audience would read this.
2. **Contribute to vLLM or FlashAttention** — even docs or small fixes. You're now in the contributor graph.
3. **Post on the same channels they use** — X/Twitter, Hugging Face, arXiv (even technical reports). Bilibili if you want the Chinese-speaking audience.
4. **Reference their work explicitly** — "I implemented this based on Karpathy's nanoGPT, here's what I changed for AMD." This creates a trail they or their followers can find.

The overseas Chinese ML/AI network isn't based on ethnicity — it's based on **public technical contribution**. That's a network you can earn your way into by building in public, which you're already doing.
