---
audio: false
generated: true
image: false
lang: en
layout: post
title: "OptiPlex 5050: Good Buy? GPU Upgrade?"
translated: false
type: note
---

**Question:** Is this Dell OptiPlex 5050 desktop (565 CNY) a good buy, and can you upgrade the GPU?

---

**Answer:**

## Is it a Good Buy?

**At 565 CNY (~$78 USD), it's a reasonable deal** for light office/media use, but with notable caveats.

### ✅ What's Good
- **E3-1240 v5** is a solid 4-core/8-thread Xeon (Skylake, 3.5GHz) — equivalent to an i7-6700
- **256GB SSD + 500GB HDD** combo is practical
- **16GB DDR4** visible in CPU-Z (though listing says 8GB — clarify this before buying)
- Small form factor, all accessories included
- Temps look acceptable (51–64°C under load)

### ⚠️ Concerns
- **AMD R5 240** is extremely weak — barely usable for anything beyond display output
- **Small Form Factor (SFF) case** severely limits GPU upgrades (see below)
- DDR4 running at 2133MHz, not full speed
- No discrete GPU worth keeping

---

## Can You Plug in a GPU?

**This is where it gets tricky.** The Dell OptiPlex 5050 comes in multiple form factors:

| Form Factor | PCIe Slot | Max GPU Size | Power |
|---|---|---|---|
| **Mini Tower (MT)** | Full-length x16 | Full-size GPU | 6-pin possible |
| **Small Form Factor (SFF)** | Half-height x16 | Low-profile only | ~75W max (no extra power connector) |
| **Micro** | None | ❌ No GPU | — |

**From the image, this appears to be SFF**, which means:
- You **can** add a GPU, but only **low-profile** cards
- Power is limited to ~75W (PCIe slot only, no 8-pin connector)
- Good low-profile options: **RX 6400 LP, GTX 1650 LP, Arc A310 LP**

---

## Verdict

> **Buy it if:** you need a cheap office PC and won't game. The price is fair.
> **Skip it if:** you want meaningful GPU gaming — the SFF chassis kills that potential.

**Clarify with seller:** Is it SFF or Mini Tower? Is RAM actually 16GB or 8GB?

---

**References:**
- [Dell OptiPlex 5050 Specs (Official)](https://www.dell.com/support/home/en-us/product-support/product/optiplex-5050-desktop/overview)
- [Intel Xeon E3-1240 v5 Specs](https://ark.intel.com/content/www/us/en/ark/products/88170/intel-xeon-processor-e3-1240-v5-8m-cache-3-50-ghz.html)
- [Best Low-Profile GPUs for SFF PCs](https://www.techpowerup.com/gpu-specs/?form_factor=Low+Profile&sort=name)
