---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Inference Cost and Speed Breakthroughs
translated: false
type: note
---

Good — the video is confirmed: **"Tri Dao: The End of Nvidia's Dominance, Why Inference Costs Fell & The Next 10X in Speed"** — Tri Dao, Chief Scientist at Together AI and Princeton professor, creator of FlashAttention and Mamba, discusses inference optimization and cost reduction. Let me fetch more content.I found detailed content from Tri Dao. Now let me also look for a transcript or detailed notes from the specific podcast episode.Good. I now have enough to give you a solid answer. The specific video is from the **Redpoint Ventures "Unsupervised Learning"** podcast. I can't pull a direct transcript, but I've pieced together the key substance from the description, related interviews, and Tri Dao's other statements around the same period.

---

**Question:** What does Tri Dao say in this talk? (<https://www.youtube.com/watch?v=xlSaoP0b90A>)

**Answer:**

The video is the **Redpoint Ventures "Unsupervised Learning" podcast episode** titled *"The End of Nvidia's Dominance, Why Inference Costs Fell & The Next 10X in Speed"*, released September 10, 2025. Tri Dao is Chief Scientist at Together AI and Princeton professor, creator of FlashAttention and Mamba.

Here's what the episode covers, reconstructed from the description, related interviews, and Tri Dao's documented positions around this time:

---

### 1. Inference costs dropped ~100× since ChatGPT launch

Tri Dao discusses how inference optimization has driven costs down 100× since ChatGPT's launch. This is the macro setup. The 100× isn't just from hardware — a significant fraction came from software/algorithmic improvements: FlashAttention, better batching (continuous batching, PagedAttention), quantization (FP8 → FP4), and speculative decoding.

---

### 2. Why the 100× happened — it's memory-bound, not compute-bound

This is the core mental model Tri Dao brings everywhere. During inference, which is the dominant workload nowadays, you're mostly using the memory subsystem. This is the same insight behind FlashAttention: attention was I/O-bound, not compute-bound. The hardware looked busy but was mostly waiting on HBM reads.

Speculative decoding exploits this directly: the total amount of compute to generate five tokens is the same, but you only had to access memory once, instead of five times. You trade idle FLOPs for fewer memory round-trips.

---

### 3. Software algorithms can match custom silicon

This is a key thesis of Together AI's work in 2025. "The software and algorithmic improvement is able to close the gap with really specialized hardware. We were seeing 500 tokens per second on these huge models that are even faster than some of the customized chips."

The compounding stack Together uses: FP4 quantization (80% speedup over FP8 baseline), static speculative decoding (+80-100% on top), then adaptive speculative decoding on top. Each layer compounds.

---

### 4. The "Next 10X" — Adaptive Speculative Decoding (ATLAS)

This is where Together AI's research work lands. The problem with static speculators: "Companies we work with generally, as they scale up, they see shifting workloads, and then they don't see as much speedup from speculative execution as before. These speculators generally don't work well when their workload domain starts to shift."

The fix is ATLAS (AdapTive-LeArning Speculator System) — a dual-model architecture with a static heavyweight speculator providing a baseline, and a lightweight adaptive speculator that learns continuously from live traffic. You can view it as an intelligent way of caching, not storing exactly, but figuring out some patterns that you see... we can then predict what the big model is going to say, and we just get better and better at predicting that.

---

### 5. Nvidia's Dominance — thesis

The "end of Nvidia's dominance" framing connects to inference being a different regime than training:

- Training: batch, throughput-bound, CUDA moat is real, H100/B200 win
- Inference: latency-sensitive, memory-bandwidth-bound, software-defined optimizations matter more, alternative hardware (Groq LPUs, Cerebras) can compete

Tri Dao's position (reflected across his public statements) is that **software-first inference optimization on commodity Nvidia hardware can rival specialized chips** — which undercuts the specialized chip narrative while simultaneously arguing inference is where the real optimization frontier is.

---

### 6. Workload drift is the hidden scaling tax

"Maybe they started using AI for chatbots, but then they realized, hey, it can write code, so they start shifting to code. Or they realize these AIs can actually call tools and control computers and do accounting and things like that."

RL training is another hard case for static speculators: the policy distribution shifts during training, so any fixed speculator goes stale. Adaptive systems are necessary at scale.

---

### What Tri Dao Believes (distilled thesis)

| Claim | Evidence |
|---|---|
| Inference is now the dominant workload | Eclipsed training in share of total compute |
| Inference is memory-bound, not compute-bound | FlashAttention was the proof case |
| Software closes the gap with custom silicon | 500 tok/s on DeepSeek-V3.1 on B200, matching Groq |
| Static speculators degrade under workload drift | Verified at Together AI enterprise customers |
| Next 10× comes from adaptive, learned optimization | ATLAS system |
| Nvidia's CUDA moat weaker in inference than training | Hardware-agnostic software wins |

---

### What You Should Take Away (for your work)

- **FlashAttention's insight generalizes**: IO-boundedness is the key mental model for any GPU optimization. Check your bottleneck before assuming you need faster compute.
- **Speculative decoding is production-ready** and compounding — if you're serving models at scale, this is table stakes now.
- **Workload drift** is a real problem for any inference-optimization system you build — static assumptions break.
- **FP4 quantization** (80% gain over FP8 baseline, Together AI's claim) is the next quantization frontier to understand; you're running on MI300X which has strong FP8/FP4 support worth exploring.

---

**References:**

- [Tri Dao: The End of Nvidia's Dominance — YouTube](https://www.youtube.com/watch?v=xlSaoP0b90A)
- [Together AI ATLAS Adaptive Speculator — VentureBeat](https://venturebeat.com/ai/together-ais-atlas-adaptive-speculator-delivers-400-inference-speedup-by)
- [Redpoint Unsupervised Learning Podcast Episode Page](https://www.redpoint.com/content-hub/video/chief-scientist-of-togetherai-tri-dao-on-the-end-of-nvidias-dominance-why-inference-costs-fell-the-next-10x-in-speed/)
