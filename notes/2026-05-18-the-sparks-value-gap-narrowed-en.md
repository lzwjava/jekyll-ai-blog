---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Spark's Value Gap Narrowed
translated: false
type: note
---

**Question:** I researched the DGX Spark and AMD Ryzen AI Max+ 395 mini PCs two months ago, and back then the cost difference between the two was around ¥10,000 (RMB). Now the AMD 395 machines have gone up to ¥25,000 — does that make the DGX Spark the better deal now?

**Answer:**

You're essentially correct — the value gap between the two options has narrowed significantly, and here's why:

## What Happened to Prices

**NVIDIA DGX Spark** also got more expensive. NVIDIA raised the DGX Spark's MSRP from $3,999 to $4,699 — an 18% increase — citing worldwide constraints in memory supply. So it's not just AMD machines that went up; the Spark is also suffering from the same LPDDR5X shortage.

**AMD Ryzen AI Max+ 395 mini PCs** with 128GB have been hit hard. As of March 24, 2026, 128GB AMD 395 machines range from $2,399 (Bosgame M5) to $3,810 (MINIX ER939-AI), with popular options like Framework Desktop at $2,851, Corsair AI Workstation 300 at $2,499, and GMKtec EVO-X2 at $3,000. RAM prices are the main culprit — prices for RAM and storage have been skyrocketing in recent months, which has put these already-expensive computers even further out of reach.

## Is DGX Spark Now the Better Value?

**Not necessarily — it depends on your use case.** Here's the breakdown:

**DGX Spark advantages:**
- The GB10 Grace Blackwell Superchip delivers up to 1 petaFLOP of AI inferencing performance (FP4), with 128GB of LPDDR5X coherent unified memory, plus a ConnectX 7 NIC running at up to 200 Gbps.
- It comes preloaded with the NVIDIA AI software stack (CUDA, TensorRT-LLM), which provides a polished day-one experience with extensive documentation and pre-configured playbooks.
- A CES 2026 software update delivered up to 2.5x performance improvements on select workloads through TensorRT-LLM optimizations and NVFP4 quantization.

**AMD 395 mini PC advantages:**
- Even at elevated prices, the cheapest 128GB AMD 395 machines (Corsair at ~$2,499, Bosgame at ~$2,399) are still noticeably cheaper than the DGX Spark at $4,699.
- The AMD Strix Halo platform offers better token-generation throughput per dollar — the Framework Desktop at $2,566 (December 2025 pricing) offered more tokens per second per dollar than the DGX Spark at $4,000.
- AMD 395 machines run standard Windows or Linux, giving more flexibility for general workloads beyond AI.

**Performance nuance:**
On heavy models like GPT-OSS 120B, DGX Spark excels at prompt processing (compute-bound) but struggles with token generation (memory-bound), where the LPDDR5X bandwidth of 273 GB/s becomes a bottleneck.

## Summary

If the cheapest AMD 395 options (Corsair, Bosgame) at ~$2,400–2,500 are no longer available in your market and prices have genuinely risen to DGX Spark territory, then yes — at ¥25,000 for AMD vs a comparable price for DGX Spark, the Spark starts to look more reasonable because you get the CUDA ecosystem, better AI software support, and a more "turnkey" experience. But if you can still find AMD 395 options at ¥18,000–20,000, the value advantage for AMD remains, especially for flexible, general-purpose AI work.

**References:**

- [NVIDIA DGX Spark price increase — Tom's Hardware](https://www.tomshardware.com/desktops/mini-pcs/nvidia-dgx-spark-gets-18-percent-price-increase-as-memory-shortages-bite-founders-edition-now-usd4-699-up-from-usd3-999)
- [AMD 395 mini PC price roundup — Liliputing (March 24, 2026)](https://liliputing.com/more-ryzen-ai-max-395-mini-pcs-with-128gb-are-now-available-if-you-can-afford-one/)
- [DGX Spark vs AMD Strix Halo benchmark & value analysis — AIMultiple](https://aimultiple.com/dgx-spark-alternatives)
- [NVIDIA DGX Spark specs & price history](https://www.aitooldiscovery.com/ai-infra/nvidia-dgx-spark-explained)
