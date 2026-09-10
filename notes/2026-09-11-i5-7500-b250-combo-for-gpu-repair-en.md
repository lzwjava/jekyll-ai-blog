---
audio: false
generated: true
image: false
lang: en
layout: post
title: i5-7500 B250 Combo for GPU Repair
translated: false
type: note
---

Question: Is this ¥288 i5-7500 + ASUS B250M-A combo worth buying?

Answer: **Yes — ¥288 for both is a pretty good price**, assuming the seller's “functional” claim is true.

* **i5-7500**: 4C/4T, 3.4 GHz base / 3.8 GHz turbo. Still perfectly usable for a **GPU repair/test bench**.
* **ASUS B250M-A**: B250 + LGA1151 is a good match. No overclocking needed.
* **DDR4**: Your DDR4-2666 stick should work, though on this platform it will normally run at the platform's supported speed rather than necessarily 2666 MHz.
* **For GPU repair:** this is actually more useful than a very old platform. You get PCIe x16, iGPU from the 7500, and a reasonably modern test platform.
* **¥288 shipped**: I would consider that **cheap enough to buy if the board/CPU are confirmed working**. The CPU alone has meaningful resale/test value.

### The important part

For your use case, I'd value this mainly as a **dedicated GPU diagnostic machine**:

```text
i5-7500
   │
B250M-A
   ├── iGPU → motherboard HDMI/DVI/VGA → display
   │
   └── PCIe x16 → GPU under test
                       │
                       ├── normal GPU → test
                       ├── no display → diagnose
                       └── MATS/MODS later
```

That's a much better setup than using your main 13900KF machine every time you want to test a questionable GPU.

**One caveat:** before paying, ask for a photo/video showing it actually POSTs into BIOS, ideally with **one DDR4 DIMM + iGPU output**. “No repair, no hidden problem” in a Xianyu listing isn't evidence by itself.

I can also help you compare this **¥288 B250 + i5-7500 against the H81 test platform you're considering**, specifically for GPU repair.