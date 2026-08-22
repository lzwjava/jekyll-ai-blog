---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA CMP HX Series for Mining
translated: false
type: note
---

**Question:** What GPUs has NVIDIA released specifically for mining (like the GA100-based cards), and what are the key models?

---

**Answer:**

NVIDIA's dedicated mining GPU line is called the **CMP (Cryptocurrency Mining Processor) HX Series**, launched in 2021. These cards have **no display outputs** and are purpose-built for mining — not gaming. Here's the full lineup:

---

### NVIDIA CMP HX Series — Mining-Dedicated Cards

| Model | Architecture / GPU | Memory | Hashrate (Ethash) | TDP |
|---|---|---|---|---|
| **CMP 30HX** | Turing / TU116 | 6 GB GDDR6 | ~26 MH/s | ~125W |
| **CMP 40HX** | Turing / TU106 | 8 GB GDDR6 | ~36 MH/s | ~185W |
| **CMP 50HX** | Turing / TU102 | 10 GB GDDR6 | ~45 MH/s | ~250W |
| **CMP 90HX** | Ampere / GA102 | 10 GB GDDR6X | ~86–92 MH/s | ~320W |
| **CMP 170HX** | Ampere / **GA100** | 8 GB HBM2e | ~160–164 MH/s | ~250W |
| **CMP 220HX** | Ampere | — | Higher tier | — |

The CMP 30HX, 40HX, and 50HX are all based on the Turing architecture (12nm silicon). The 50HX uses TU102, the 40HX uses TU106, and the 30HX uses TU116.

The flagship CMP 170HX uses the full GA100 die — the same silicon found in the A100 datacenter GPU — but configured specifically for mining: no NVLink interface, and PCIe Gen4 optimized for sustained Ethash performance under continuous operation.

The CMP 170HX features 8 GB of HBM2e memory at 1.4 GHz, delivering up to 1.5 TB/s of bandwidth, a 250W TDP, and a 160+ MH/s hashrate.

All CMP cards are "headless" — they have no display outputs — and are designed to take strain off GeForce gaming GPUs by giving miners a dedicated product line.

---

### Important Notes

- **Bitcoin mining:** GPUs are generally less efficient than ASICs for Bitcoin mining. They are better suited for mining other cryptocurrencies like Ethereum Classic, Kaspa, or Ravencoin.
- **Consumer alternatives:** As of late 2025, the RTX 5090 is considered the best consumer card for mining, though it comes with a high upfront cost and up to 580W power draw.
- The CMP line was discontinued after 2021 as Ethereum moved to Proof-of-Stake, killing most GPU-based ETH mining demand.

---

**References:**
- [NVIDIA CMP HX Official Page](https://www.nvidia.com/en-us/cmp/)
- [CMP 170HX — Tom's Hardware](https://www.tomshardware.com/news/nvidias-cmp170hx-in-the-wild-with-164-mhps-ethereum-mining-performance)
- [CMP Architecture Details — WCCFtech](https://wccftech.com/nvidias-cmp-crypto-mining-gpus-detailed-90hx-based-on-ampere-ga102-while-50hx-40hx-30hx-based-on-turing-gpus/)
- [CMP 170HX Guide — ScreenRant](https://screenrant.com/nvidias-cmp-170hx-gpu-price-availability-hash-rate/)
