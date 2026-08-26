---
audio: false
generated: true
image: false
lang: en
layout: post
title: Neil Movva's Token Factory Strategy
translated: false
type: note
---

**Question:** What were the key things Neil Movva said in his recent *Invest Like the Best* episode with Patrick O'Shaughnessy?

**Answer:**

The episode aired on **August 25, 2026**. Here's a breakdown of the major themes:

---

**1. The "Token Factory" Thesis — AI Is Optimizing for the Wrong Workload**

Movva's central argument is that the entire AI stack — from GPU kernels to data center power sourcing — has been built around interactive chatbots that demand low latency, when the real growth market is background agents that run for hours or days without supervision. For these workloads, latency is irrelevant and cost per token is everything.

Sail is building what he calls a "token factory" — an inference company designed for a future where AI agents run in the background for hours or days at a time, rather than answering a human in real time. In that world, latency matters less and cost matters more.

---

**2. The Scavenger Strategy**

Movva's strategy is explicitly a scavenger approach: buy chips that larger players ignore, rent power in facilities too small for hyperscalers, and tolerate uptime levels that would be fatal for anyone else. His company's north star is a 1,000x reduction in token cost.

On chips, he said: there are no bad chips, only bad pricing — and he's happy to buy AMD, SambaNova, Google TPUs, and Amazon Trainium, since others underestimate them. On power, he is willing to buy capacity in 1-megawatt facilities that larger players ignore, and even accept 95% uptime, because his control plane can shift workloads elsewhere when a facility goes down.

---

**3. Chips: Cerebras vs. Nvidia — It's Not Winner-Take-All**

Movva predicts a hybrid outcome, not a winner-take-all battle. Cerebras and similar chips will serve as accelerators for compute-bound layers, paired with traditional GPUs that have the off-chip DRAM capacity for attention layers and long context windows.

He also pointed to what he calls the **"original sin" of transformers**: transformers juxtapose an extremely memory-bound layer (attention) right next to a compute-bound layer (MLP), making it nearly impossible for any single chip design to be optimal for both.

---

**4. Data & Open Source**

Movva argues the internet was a "one-time subsidy" of roughly 30 trillion tokens of high-quality text, and models have already seen it many times over. The future is model self-improvement through reinforcement learning in isolated "gym" environments with verifiable tasks.

On open source, he noted that even without deliberate scraping, AI-generated content is proliferating on the internet: "We're going to have latent distillation for a long time. It seems fundamentally impossible to prevent the diffusion of information or model capabilities."

---

**5. Is This a Bubble? — The Dot-Com Comparison**

Movva draws a distinction between today's token consumption — immediate and non-speculative — and the dot-com era's speculative infrastructure build-out. His view: people buy tokens because they are immediately valuable; you don't hoard tokens, you use them immediately.

---

**6. TSMC Geopolitics — Contrarian View**

His most contrarian take is on TSMC and geopolitics: he argues that even in a worst-case scenario, Western chip fabs like Intel are "not that far behind, at worst maybe 2x worse performance per watt," and that the performance gap from one process node to the next is not as dramatic as chip-war discourse suggests.

---

**References:**

- [BigGo Finance: Neil Movva AI Inference 1000x cheaper](https://finance.biggo.com/news/29d3f76c7eeac4a2)
- [Colossus: Invest Like the Best episode listing](https://colossus.com/series/invest-like-the-best/)
- [Apple Podcasts: Episode description](https://podcasts.apple.com/us/podcast/invest-like-the-best-with-patrick-oshaughnessy/id1154105909)
- [Digg: Neil Movva Discusses AI Inference on Podcast](https://digg.com/tech/s7o4z9dq)
