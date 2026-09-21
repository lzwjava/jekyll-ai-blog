---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99-QD4 Confirmed Working with ReBAR
translated: false
type: note
---

Question: **Does the Huananzhi X99-QD4 in this Chinese listing work with ReBarUEFI / Resizable BAR as shown in `ReBarUEFI#11`?**

Answer:

**Yes — this exact motherboard model is explicitly confirmed working.**

In `xCuri0/ReBarUEFI#11`, the tested entry is:

| Board                 | GPU      |       BAR | UEFIPatch |
| --------------------- | -------- | --------: | --------- |
| **Huananzhi X99-QD4** | RTX 3060 | **16 GB** | **No**    |

So this isn't an inference from "some X99 board"; **X99-QD4 itself was tested with a 16 GB BAR and did not require UEFIPatch**. ([GitHub][1])

[ReBarUEFI #11 — List of working motherboards](https://github.com/xCuri0/ReBarUEFI/issues/11?utm_source=chatgpt.com)

### What that means for the listing

The seller's board:

> 华南 x99-QD4 / Q87 / DDR4 / dual M.2

is almost certainly the **Huananzhi X99-QD4 family** referred to by the ReBarUEFI project. The project itself specifically calls out **"AliExpress X99 Tutorial"**, and says these X99 boards don't require the normal UEFIPatch procedure. ([GitHub][2])

There is also a **2026 X99-QD4-specific modded BIOS project** that explicitly lists:

* ReBarDxe injected
* overclocking lock removed
* memory tuning unlocked
* VRM current limit unlocked
* BCLK downspread removed

and reports the X99-QD4 BIOS as tested/working. ([GitHub][3])

### The important distinction

I'd separate these three things:

```text
X99-QD4 hardware
       │
       ├── ReBar capability ─────── YES, documented
       │
       ├── Stock BIOS ───────────── depends on BIOS version
       │
       └── Modded BIOS ──────────── ReBarDxe + OC possible
```

The GitHub issue proves **ReBar works on X99-QD4**, but it does **not** mean every stock BIOS revision automatically has ReBAR exposed.

For the board you're considering, I'd specifically ask the seller for:

```text
1. Exact BIOS version
2. BIOS screenshot showing Above 4G Decoding
3. Whether ReBarDxe is already injected
4. Whether CSM can be disabled
5. Whether they can provide the original BIOS dump
```

The ReBarUEFI requirements are basically **Above 4G Decoding + CSM off**, with the ReBar DXE module inserted into the firmware. ([GitHub][2])

### One more interesting point: the "鸡血 BIOS"

The seller's **2690 v3 all-core 3.5 GHz** and **1650 v3 4.4/4.5 GHz** claims are a separate BIOS-mod/CPU-microcode issue from ReBAR.

So if your goal is something like:

```text
X99-QD4
+ E5-1650 v3 @ ~4.4 GHz
+ DDR4
+ RTX 3090 / 4090 / Arc
+ ReBAR
```

then **X99-QD4 is a particularly interesting platform because we have direct ReBarUEFI evidence for this exact board.**

One caveat: the original #11 test is **RTX 3060 + 16 GB BAR**, so it establishes the firmware/platform capability, not that *every* modern GPU will behave identically. The project's current wiki says more than 200 motherboards have been tested and maintains the working-board list. ([GitHub][4])

If you tell me **which GPU you're planning to put on this X99-QD4** (especially 3090/4090/Arc A770/B580), I can check the ReBarUEFI reports for that GPU + X99 combination and tell you what BIOS modifications you'll actually need.

[1]: https://github.com/xCuri0/ReBarUEFI/issues/11 "List of working motherboards · Issue #11 · xCuri0/ReBarUEFI · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com "GitHub - xCuri0/ReBarUEFI: Resizable BAR for (almost) any UEFI system · GitHub"
[3]: https://github.com/avkila-tech/HUANANZHI-X99-QD4-2024/blob/main/README.md?utm_source=chatgpt.com "HUANANZHI-X99-QD4-2024/README.md at main · avkila-tech/HUANANZHI-X99-QD4-2024 · GitHub"
[4]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"