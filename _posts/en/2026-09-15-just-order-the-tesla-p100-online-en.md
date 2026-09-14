---
audio: false
generated: true
image: false
lang: en
layout: post
title: Just Order the Tesla P100 Online
translated: false
type: note
---

Good — now I have a clear picture. The "P100" at 400 CNY is almost certainly the **NVIDIA Tesla P100 16GB GPU** (a data center compute card), popular in China's secondhand market (闲鱼/Xianyu) for AI/ML hobby use. Here's my answer:

---

**Question:** Should I drive to Guangzhou to buy a Tesla P100 GPU for ¥400 CNY, or just order it delivered — and is it worth bringing my computer to test it on-site?

---

**Answer:**

**Just get it delivered — no need to drive.**

The Tesla P100 at ~¥400 CNY is a well-known secondhand GPU circulating on China's 闲鱼 (Xianyu) market. According to a 2026 guide on second-hand AI cards for Chinese hobbyists, the Tesla P100 16GB is specifically praised as a great-value deep learning card, and sellers ship these regularly. Here's the breakdown:

**Delivery is fine because:**

- Sellers on 闲鱼 and Taobao ship P100s constantly — it's a commodity item in this market. Multiple Chinese Bilibili reviewers have bought P100s around the 300–400 CNY range and reviewed them for gaming and LLM inference, all via online purchase.
- The card is passive-cooled with no moving parts, so it ships safely without special handling.
- At ¥400, the gas and time cost of driving to Guangzhou likely isn't worth it unless you're already going.

**On-site testing only makes sense if:**

- You're buying from a private seller who refuses refunds and has no return policy — then testing before paying in cash makes sense.
- The seller is offering a "modified" desktop version (魔改版 with added fans), which has more variables worth checking.
- If buying from a reputable 闲鱼 store with a return window, just buy online.

**Things to verify when it arrives:**

- It's a **passive card** (no fans, meant for server airflow) — you'll need to add fans or a custom cooler for desktop use, which adds ~¥100–200.
- Check that it's the **PCIe version** (not SXM2, which needs an expensive adapter board).
- Run a quick GPU burn test (e.g., `nvidia-smi` + furmark or a simple CUDA workload) to confirm HBM2 health.

**On the price:** The Tesla P100 remains a popular "budget" AI accelerator in 2026, valued for its high VRAM-to-price ratio. Current used pricing sits around $80 USD globally, which puts ¥400 CNY (~$55 USD) at the lower-mid range — a decent deal if the card is healthy.

---

**References:**

- [2026 个人 AI 爱好者显卡选购完全指南 (CSDN)](https://blog.csdn.net/d1z878/article/details/159496691)
- [Tesla P100 Used Price & History — GPUDojo](https://gpudojo.com/tesla-p100)
- [398元 Tesla P100 测评：打游戏和LLM推理到底行不行 (Bilibili)](https://www.bilibili.com/video/BV1WLBTY8Ee9/)
