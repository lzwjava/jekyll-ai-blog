---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Open-Core and Managed Hosting
translated: false
type: note
---

Question: What's SGLang's business model — how does the open-source project monetize?

Answer: SGLang split into two tracks:

**1. Open-source core stays free, non-profit-hosted**
The repo is still hosted under LMSYS (non-profit). SGLang is currently hosted under the non-profit open-source organization LMSYS, and enterprises interested in adopting it at scale — technical consulting, sponsorship, partnerships — can contact them directly. It's also been getting grant funding rather than revenue — it received the third batch of the Open Source AI Grant from a16z in mid-2025.

**2. Commercial spinout: RadixArk**
This is the actual "business model" you're asking about. Ying Sheng and Banghua Zhu, both AI infra veterans from xAI and NVIDIA, founded RadixArk, which launched with $100M in Seed funding at a $400M post-money valuation, led by Accel and co-led by Spark Capital. Investor list is stacked with strategics: NVentures (Nvidia's VC arm), AMD, MediaTek, plus angels like Igor Babuschkin (xAI), Lip-Bu Tan (Intel CEO), John Schulman, Soumith Chintala, Thomas Wolf.

Revenue mechanics: RadixArk continues developing SGLang as open-source while also building adjacent tools like Miles (an RL framework), and has begun charging for paid hosting services — the same open-core-to-managed-service pattern you're seeing across AI infra (vLLM did the same move).

So: **open-core + managed inference hosting**, funded on the thesis that SGLang is used by companies like xAI and Cursor to accelerate inference/training, and optimizing that layer creates immediate, large savings on server costs — classic infra land-grab, monetize-the-hosting-not-the-code play, same as Databricks (Ion Stoica's other company, incidentally — SGLang originated in his Berkeley lab).

For your own agent stack (ww/iclaw/zz), this is relevant less as a business model template and more as: if you're not on RadixArk's managed hosting, you're just running the free OSS engine — no lock-in risk yet, but worth watching if they start gating perf features (PD disaggregation, large-scale EP) behind the paid tier.

References:

- [RadixArk Launches with $100M Seed — BusinessWire](https://www.businesswire.com/news/home/20260505077157/en/RadixArk-Launches-with-$100-Million-in-Seed-Funding-Led-by-Accel-to-Grow-SGLang-and-Democratize-Frontier-AI-Infrastructure)
- [TechCrunch: SGLang spins out as RadixArk, $400M valuation](https://techcrunch.com/2026/01/21/sources-project-sglang-spins-out-as-radixark-with-400m-valuation-as-inference-market-explodes)
- [sgl-project/sglang GitHub](https://github.com/sgl-project/sglang)
