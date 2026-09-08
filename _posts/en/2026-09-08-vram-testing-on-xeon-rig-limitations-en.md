---
audio: false
generated: true
image: false
lang: en
layout: post
title: "VRAM Testing on Xeon Rig: Limitations"
translated: false
type: note
---

I've read the PDF (《显存测试软件使用手册》 / "VRAM Testing Software Manual", 25 pages, revised Sept 2012, with 2021 updates). Here's the bottom line:

## It can work, but there are several limitations to note

This manual is a **usage guide for GPU repair/VRAM testing tools (MATS/MODS)**, used to detect damaged video memory on discrete graphics cards (running commands like `./mats -e 10`, `./mods gputest.js`, then checking report.txt to see if FBI0A0 reports a fail).

### Comparing against the machine you described (Xeon E5-2673 v3 + X99-A), point by point

| Manual requirement | This machine's situation | Met? |
| --- | --- | --- |
| Recommends ASUS B85/B150/H170, must support Legacy boot | X99-A motherboard supports Legacy/CSM boot, can enter the menu and pick a system | ✅ Basically met |
| 8GB+ RAM (some tests require RAM > VRAM) | 8GB DDR3 1600 | ✅ Barely sufficient (not enough to test 8GB-VRAM cards) |
| 250GB+ SATA SSD | Only a 120GB SSD | ⚠️ Too small; you'd need a 250GB+ drive to install the test image (5 partitions totaling ~225GB) |
| Supports Multi-GPU, use iGPU to display output when testing a non-displaying dGPU | **The E5-2673 v3 is a Xeon — it has no integrated GPU** | ❌ Not met |

### Main issues

1. **No integrated GPU**: The manual's recommended "iGPU + dGPU" dual-card testing method (set Primary Display to CPU Graphics in BIOS) can't be done on this machine — the E5 v3 series has no integrated graphics. You can only test with the dGPU driving the display itself; if the card doesn't output video, you're stuck.
2. **The seller's "1GB basic display card" is not a test target**: Cards like that (GT710/GT1030 types) have essentially no testing value. The manual targets gaming/mining cards (NVIDIA up to RTX 3090, AMD up to RX 6900).
3. **The 120GB SSD isn't big enough**: The image needs to be restored into 5 partitions (20+20+65+50+70GB), so you'd need a separate 250GB+ SATA drive.

### Conclusion

- This machine **can serve as a test bench** (it can host the image, supports Legacy boot, and 8GB RAM is enough to test cards with ≤4GB VRAM) — usable for GPU testing on the side while doing office work/renting out as a multi-task rig.
- But it **cannot replace the ASUS motherboard setup recommended in the manual**, especially since it has no iGPU — the most common use case, testing "dead/black-screen" graphics cards, won't work.
- One correction: this is a **desktop** (29×29×9cm compact case), not a laptop. The parts of the manual about laptop UEFI boot don't apply to it.
