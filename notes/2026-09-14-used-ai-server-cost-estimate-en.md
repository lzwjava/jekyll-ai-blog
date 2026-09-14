---
audio: false
generated: true
image: false
lang: en
layout: post
title: Used AI Server Cost Estimate
translated: false
type: note
---

**Question:** How much would a dual-socket Broadwell server (48 threads, 62 GiB RAM, 2× Tesla P100 12 GB) cost if purchased on the open market?

**Answer:**

This system has three cost components. Here's a breakdown based on current market data (September 2026):

---

### 1. Base Server (Dual-Socket Broadwell, ~48 threads, ~64 GB RAM)

A typical Dell PowerEdge R730 or HP DL380 Gen9 matching this spec (dual Xeon E5-2600 v4 Broadwell, ~64 GB RAM) is widely available used. Dual-socket Intel servers with 64 GB RAM on eBay currently range from roughly **$200–$550** for refurbished units, depending on specific CPU model, drive config, and condition. A clean R730/DL380 Gen9 with 48 threads + ~64 GB lands around **$250–$400**.

---

### 2. Two × Tesla P100 (12 GB each)

As of September 14, 2026, the Tesla P100 16 GB can be found used on eBay from around **$99**, and new from ~$94 on Newegg. The 12 GB SXM2 variant (typically found in DGX-1s) is rarer, but PCIe 12 GB versions are priced similarly or slightly lower. Budget roughly **$80–$120 each**, so **~$160–$240 for the pair**.

---

### 3. Estimated Total

| Component | Estimated Cost |
| --- | --- |
| Dual-socket Broadwell server (~64 GB RAM) | $250–$400 |
| 2× Tesla P100 (12 GB each) | $160–$240 |
| **Total** | **~$400–$650** |

---

### Worth Noting

The P100 is considered good for 14B parameter models; running 30B models requires aggressive quantization, and its older Pascal architecture may have limited compatibility with newer inference stacks. For a complete AI workstation, you may also want to budget for NVMe storage (the 32 GB root disk is tight) and a compatible PCIe riser/bracket if the P100s aren't already seated in the server chassis.

So all-in, you're looking at roughly **$400–$700** assembled from used parts — an excellent value for a 24 GB combined VRAM GPU compute node.

---

**References:**

- [Tesla P100 16GB Used Price & History (Sep 2026) — GPUDojo](https://gpudojo.com/tesla-p100)
- [Intel Computer Servers 64 GB RAM 2 Processors — eBay](https://www.ebay.com/b/Intel-Computer-Servers-64-GB-RAM-2-Processors/11211/bn_42004041)
- [Used Server GPUs for Local LLMs — CraftRigs](https://craftrigs.com/guides/used-server-gpus-tesla-p40-a100-ebay/)
