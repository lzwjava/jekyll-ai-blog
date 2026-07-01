---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V4 Memory Demand Impact
translated: false
type: note
---

**Question:** What does DeepSeek V4's dramatically lower memory requirement imply for the memory industry (Samsung, SK Hynix, Micron, etc.)?

**Answer:****Question:** What does DeepSeek V4's dramatically lower KV cache / memory requirement imply for Samsung, SK Hynix, Micron, and the broader memory industry?

**Answer:**

This is a fascinating macro question — software architecture decisions at DeepSeek ripple all the way to fab investments in Pyeongtaek and Incheon. Here's the full picture:

---

## First: Understand What Was Driving Memory Demand

The AI inference boom created a **memory supercycle** unlike anything before:

Memory companies are now posting gross margins above TSMC's — something unthinkable two years ago. Samsung's memory division and SK Hynix delivered gross margins of roughly 63–67% in Q4 2025, compared to TSMC's guided 60%. The HBM market is controlled by three companies: SK Hynix (~57% share), Samsung (~22%), and Micron (~21%). All three have sold out capacity through 2026.

The shortage has caused 200–400% price increases in DRAM and NAND flash. OpenAI alone consumes ~40% of global DRAM supply.

The bottleneck was always the KV cache — it scales linearly with context length and sits in HBM (the most expensive, highest-bandwidth memory). Every token you process writes and reads from HBM. That's the core cost driver.

---

## The DeepSeek V4 Shock: 10% KV Cache = 90% Less HBM Per Request

The intuition: if V4 needs only 10% of the KV cache at 1M tokens versus V3.2, then **you can serve 10x more concurrent long-context sessions on the same GPU cluster**. Or equivalently, you need 10x fewer H100s to hit the same throughput.

That's a direct hit on HBM demand — at least per-unit-of-useful-work.

An aggressive reduction in the KV cache footprint isn't just some abstract software milestone; it carries massive implications for the actual memory supply chain. The industry is currently locked in a DRAM supercycle driven by insatiable demand for HBM.

---

## But: Jevons Paradox Is the Counter-Force

After the original DeepSeek shock, HBM demand actually climbed even more steeply. This is explained by Jevons Paradox — when technological efficiency lowers the cost of a resource (in this case, inference), total usage explodes rather than contracts.

The historical pattern with every compute efficiency gain in AI:

- Cost per token drops → more applications become economically viable → aggregate token volume explodes → total HBM demand goes **up**, not down.

This is what happened after DeepSeek R1 (Jan 2025), after FlashAttention, after quantization. Each time, analysts panicked about memory demand collapsing. Each time, they were wrong.

---

## What the Memory Companies Are Actually Doing

They are not scared. They are building more:

Samsung is looking to expand HBM production capacity by around 50% in 2026, while SK Hynix has announced plans to increase infrastructure investment by more than four times the previously announced figure. Both are constructing new fabs in South Korea — Samsung's P5 facility in Pyeongtaek expected operational by 2028, SK Hynix's M15X by mid-2027.

Samsung's memory chief warned that "significant shortages" across memory products are expected to continue through at least 2027. Demand fulfillment rates have fallen to record lows as customers rush to secure future supply.

---

## The Deeper Structural Shift: Where Memory Is Going

DeepSeek V4 introduces another wrinkle — the **Engram architecture**:

Engram reduces reliance on expensive HBM by offloading static knowledge to system DRAM, lowering costs and enabling frontier-level performance on more accessible hardware configurations. By allocating 75–80% of sparse model capacity to dynamic reasoning and 20–25% to static lookups via deterministic hash-based retrieval, it separates static knowledge from dynamic computation.

This is architecturally significant: **not all memory is equal**. HBM is fast and expensive (for activations, KV cache, weights being computed). System DRAM is slower and cheaper (for cold weights, static lookups). If models increasingly route static knowledge to DRAM, that's a demand shift — less HBM per GPU, more system DRAM per node.

---

## Industry Implications Summary

| Dimension | Effect |
| --- | --- |
| **HBM demand per GPU** | ↓ per inference request (CSA/HCA compression) |
| **Total HBM demand** | ↑ (Jevons Paradox — more models, more deployments) |
| **HBM price/margins** | Still high, shortages continue through 2027 |
| **System DRAM demand** | ↑ new (Engram-style architectures offload to DRAM) |
| **GPU count needed per workload** | ↓ (1M context fits on fewer H200s) |
| **Democratization** | ↑ smaller players can now run 1M-context models |
| **Samsung/Hynix stock reaction** | Short-term fear (like DeepSeek R1 shock), but fundamentals remain strong |

HBM market TAM is projected to reach $100B by 2028, up from $35B in 2025 — a ~40% CAGR. HBM4 is entering production in 2026, with 16-Hi stacks targeting Q4 2026.

---

## The Real Signal for the Industry

The efficiency gains don't reduce memory demand — they change **what kind of memory** and **at what tier** in the hierarchy. The long-term trend is clear: AI is consuming memory at every level of the stack (HBM → LPDDR5 → NAND), and software efficiency gains just accelerate the diffusion of AI into more products and use cases, expanding the total addressable market for all memory types.

Samsung, Hynix, Micron aren't worried about DeepSeek V4. They're worried about building fabs fast enough.

**References:**

- [Samsung & SK Hynix warn of shortages through 2027 (Tom's Hardware)](https://www.tomshardware.com/tech-industry/artificial-intelligence/samsung-and-sk-hynix-warn-ai-driven-memory-shortages-could-last-until-2027-and-beyond)
- [Why KV Cache Drives AI Economics (Data Gravity)](https://www.datagravity.dev/p/why-kv-cache-and-memory-drive-ai)
- [The AI Memory Supercycle (Introl)](https://introl.com/blog/ai-memory-supercycle-hbm-2026)
- [How the Hunger for Memory Is Starving the Rest of Tech (CipherTalk)](https://ciphertalk.substack.com/p/how-the-hunger-for-memory-is-starving)
- [TurboQuant/DeepSeek Fear Analysis — Seoul Economic Daily](https://en.sedaily.com/news/2026/03/29/tokens-kv-cache-turboquant-decoding-ai-jargon-and-its)
