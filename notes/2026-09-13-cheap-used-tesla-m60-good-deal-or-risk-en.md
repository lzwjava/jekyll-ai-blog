---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Cheap Used Tesla M60: Good Deal or Risk?"
translated: false
type: note
---

**Question:** Is 288 CNY a good price for a used NVIDIA Tesla M60 16GB GPU?

**Answer:**

288 CNY (~$40 USD) is **on the low end of the market** — which is both good and worth being cautious about.

**Market context:**
According to eBay and Chinese secondhand market data, normal used Tesla M60 prices range roughly from **472 to 3,800 CNY**, so 288 CNY sits well below average. That said, it's not impossible for a legitimate unit to sell this cheap — the M60 is aging hardware and supply from decommissioned data centers is abundant.

**Why it's so cheap:**
The M60 is an 8-year-old model with high power draw (~300W), and the secondhand market is oversupplied. Its FP32 compute is only ~8.1 TFLOPS — far behind even entry-level modern cards like the RTX 5060.

For AI hobbyists in 2026, more recommended options in the budget segment include the Tesla V100 16G (800–1,000 CNY) or RTX 2080 Ti 22G modified cards (1,700–1,900 CNY), which offer meaningfully better performance for LLM inference.

**Verdict on this listing:**

| Factor | Assessment |
| --- | --- |
| Price (288 CNY) | 🟡 Below market — suspiciously low, but possible |
| "Almost brand new" from pull | 🟡 Common claim; verify with photos |
| No video output (compute only) | ✅ Legitimate M60 trait |
| Requires server-grade hardware | ⚠️ Real constraint — needs proper airflow/PSU |
| Pre-sale testing claimed | ✅ Good sign if verifiable |

**Bottom line:** At 288 CNY, the price is tempting, but it's low enough to warrant caution. Ask for GPU-Z screenshots, real close-up photos, and confirm the VBIOS hasn't been modified. If it checks out, it's a reasonable deal for light inference or virtualization experiments — just don't expect competitive deep learning performance vs. modern cards.

**References:**

- [Tesla M60 market price analysis (CSDN)](https://blog.csdn.net/WSSWWWSSW/article/details/149631536)
- [2026 AI GPU buying guide for hobbyists (CSDN)](https://blog.csdn.net/d1z878/article/details/159496691)
