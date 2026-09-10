---
audio: false
generated: true
image: false
lang: en
layout: post
title: Budget GPU Repair Test Bench PC
translated: false
type: note
---

Question: Is this ¥208 B75 + Xeon E3-1260L desktop a good machine to buy for learning GPU repair?

Answer: **Yes — at ¥208, I think it’s a pretty good cheap GPU-repair test machine**, with a few caveats.

### Why it works well

* **B75 platform** → cheap, simple, DDR3, plenty of used parts.
* **E3-1260L, 4C/8T** → totally sufficient for GPU diagnostics. CPU performance isn't important here.
* **8 GB DDR3** → enough for Windows/Linux + GPU tools.
* **160 GB SSD** → enough for drivers, Linux, MATS/Tserver, diagnostic software, etc.
* **PCIe x16 slot** → the important part. You can repeatedly install/remove GPUs.
* **Integrated graphics** → potentially useful for troubleshooting a discrete GPU that doesn't output video.
* **¥208 including case + PSU** → low enough that you don't need to baby the machine.

For a repair bench, this is basically a **sacrificial host PC** rather than a performance machine.

### But check these 3 things before buying

**1. Verify the exact motherboard and PCIe slot**

The listing is inconsistent:

> "华硕B75台式主机"
> but configuration says "华南B75主板"

I would specifically ask for a photo of the motherboard. You want a normal **PCIe x16 physical slot**.

**2. Be suspicious of "Intel HD Graphics P1000"**

That's not the normal integrated GPU name for an E3-1260L. The E3-1260L itself has **Intel HD Graphics P3000**, not "P1000."

So the seller's specification is probably sloppy.

**3. PSU is the biggest unknown**

For GPU repair, the included PSU is actually more important than the CPU.

If it's some no-name 250–350 W PSU, I'd probably **replace it with a known-good PSU** before testing 3060/3070/3080/3090-class cards.

Don't use a questionable PSU to diagnose a questionable GPU.

### How I'd use this machine

I'd build the bench roughly like:

```text
B75 + E3-1260L
       │
       ├── iGPU → monitor
       │
       └── PCIe x16
             │
        ┌────┴────┐
        │ GPU under│
        │   test   │
        └─────────┘
```

Then:

```bash
lspci | grep -i vga
lspci -nn
nvidia-smi
dmesg | grep -i nvidia
```

You can also use it for:

* GPU BIOS flashing
* driver testing
* PCIe enumeration testing
* checking whether a card reaches POST
* Linux `lspci` diagnostics
* MATS/Tserver work
* testing repaired cards
* stress testing after repair
* oscilloscope/multimeter work alongside the PC

### My verdict

**¥208: 8.5/10 for a GPU-repair bench.**

I would **not** buy it because it's a powerful computer. I'd buy it because it's a **cheap disposable PCIe test platform**.

If the motherboard has a proper x16 slot and the PSU isn't complete garbage, **¥208 is cheap enough that I'd seriously consider it.**