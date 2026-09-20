---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheap X99 Boards for M40 and P100
translated: false
type: note
---

Question: What are some cheap motherboard options compatible with M40 / P100 and the E5-2676 v3?

Answer:

Here's the practical breakdown, sorted from cheapest to slightly more expensive. All keep your E5-2676 v3 CPU.

---

## 💸 Cheap Chinese X99 Boards (~$30–80)

These are the most wallet-friendly options, but **Above 4G Decoding support is hit-or-miss** depending on the specific board revision and BIOS version.

**Huananzhi X99-TF** — *Best bang for buck if you want DDR3 carry-over*

This is actually the closest upgrade from your current Huanan X99-HD3 — it supports **both DDR3 and DDR4** on the same board (different slots), so you can reuse your existing Kingston DDR3 sticks. Community users have reported Above 4G Decoding is accessible after disabling CSM in BIOS. Users running Chinese X99 boards have confirmed that the "above 4G decoding" option does appear in these boards — you just need to enable it and disable CSM. It has 2 PCIe 3.0 x16 slots and NVMe M.2 support.

- Price: ~$50–70 (AliExpress/Taobao)
- DDR3 + DDR4 hybrid slots ✅ (keep your RAM!)
- Above 4G: ⚠️ Present but needs CSM disabled
- Socket: LGA 2011-3

**Huananzhi X99-F8** — *DDR4, more slots, better BIOS*

A step up from the TF — DDR4 only, but has a cleaner BIOS with Above 4G Decoding more consistently reported. It uses the C612 chipset (same as Supermicro server boards), giving it better stability and ECC RDIMM support. Two PCIe 3.0 x16 slots and NVMe M.2.

- Price: ~$120–150 (board only)
- Above 4G: ✅ More reliably present
- DDR4 ECC RDIMM support ✅
- Socket: LGA 2011-3

**Machinist X99 MR9A Pro / MR9D** — *ATX, widely available*

Popular on AliExpress and eBay. The MR9D has 3 PCIe 3.0 x16 slots, 8 DDR4 DIMM slots (up to 256GB), and 10 SATA ports. Above 4G Decoding is present in BIOS on most recent firmware versions. A well-documented option in the Chinese budget X99 community.

- Price: ~$70–100
- Above 4G: ⚠️ Present on newer firmware, verify before buying
- DDR4 ECC + non-ECC ✅
- Socket: LGA 2011-3

---

## ⚠️ The Key Risk with All Cheap Chinese X99 Boards

Even when Above 4G Decoding is enabled and CSM is disabled, some Chinese X99 clone boards still clamp the BAR size somewhere in the PCI Bus / Host Bridge — meaning the GPU is still not fully functional for large-BAR cards. Results vary by board **revision** and BIOS date, not just model name. Always check the seller's BIOS version and look for community reports for that specific revision (V1.0, V1.2, V2.0, etc.) before buying.

---

## Quick Comparison

| Board | Price | DDR | Above 4G | Risk | Note |
|---|---|---|---|---|---|
| Huananzhi X99-TF | ~$50 | **DDR3+DDR4** | ⚠️ | Medium | Reuse your RAM |
| Machinist MR9A/MR9D | ~$80 | DDR4 | ⚠️ | Medium | Widely available |
| Huananzhi X99-F8 | ~$140 | DDR4 ECC | ✅ | Low | C612 chipset |
| ASUS X99-E WS (used) | ~$120 | DDR4 | ✅ | Very Low | Best proven option |

---

**Bottom line:** If keeping your DDR3 RAM matters, the **Huananzhi X99-TF** is the only cheap option that lets you do that. If you're okay moving to DDR4, the **X99-F8** or a used **ASUS X99-E WS** gives you much more reliable Above 4G Decoding for only a little more money. The cheap Machinist boards can work, but it's a gamble on the specific revision.
