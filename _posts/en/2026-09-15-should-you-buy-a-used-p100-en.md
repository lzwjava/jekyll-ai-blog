---
audio: false
generated: true
image: false
lang: en
layout: post
title: Should You Buy a Used P100?
translated: false
type: note
---

**Question:** Someone on Xianyu (Chinese secondhand marketplace) is selling a P100 GPU, claiming it works normally, ran compute loads up to 240W stably, but says you need to handle cooling — they ran the fans at 100% blowing directly at it. Should you buy it?

**Answer:**

This is a pretty reasonable deal on paper, but there are a few things worth understanding:

**About the Card Itself**

The NVIDIA Tesla P100 (16GB HBM2) is a data center GPU with no onboard cooling — it's designed for server chassis with managed airflow. The seller's comment about running fans at 100% is completely normal for this card used outside a rack environment; it's not a red flag, it's just the reality of using passive/blower server GPUs in an open-air setup.

The P100 features 16 GB of HBM2 memory with 732 GB/s memory bandwidth, delivers 9.3 TFLOPS of FP32 performance, and has a 250W TDP. So "stable up to 240W" is right in line with normal operation — that's expected behavior, not a claim to be suspicious about.

**Pricing Reality**

Used P100 units are widely available in the secondhand market, typically priced between $83–$200, offering around $5/GB of VRAM — significantly cheaper than T4 or V100. The lowest average tracked price is currently around $76 on platforms like eBay. So compare what the Xianyu seller is asking against those benchmarks.

**Things to Watch Out For**

- **Cooling is your responsibility.** This card *will* throttle or die without active airflow. You'll need a direct fan blowing on it, or mount it in a case with good airflow. The seller's 100% fan approach is the correct one.
- **PCIe vs SXM2 form factor** — confirm which one it is. The SXM2 version requires a special mezzanine board, while PCIe plugs into a standard motherboard.
- **Power delivery** — at 250W TDP, you need an 8-pin (or dual 8-pin depending on variant) and a PSU with headroom.
- Pascal architecture may have limited software support with some newer inference stacks — check CUDA compatibility for your intended use case.
- **No display output** — this is a compute-only card.

**Bottom Line**

If the price is reasonable (under ~$150 USD equivalent) and the seller has a credible track record, it's a solid budget compute card. The thermal handling story they gave is legitimate and honest, which is actually a good sign.

---

References:
- [NVIDIA Tesla P100 Specs & Pricing – GPUpoet](https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100)
- [Tesla P100 Used Price & History – GPUDojo](https://gpudojo.com/tesla-p100)
- [P100 Cloud Pricing & Specs – gpus.io](https://gpus.io/en/gpus/teslap100)
- [P100 Buying Guide for AI/Home Labs – Alibaba Electronics](https://electronics.alibaba.com/product/nvidia-tesla-p100)
