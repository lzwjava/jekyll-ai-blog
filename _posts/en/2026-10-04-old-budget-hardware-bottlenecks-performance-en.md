---
audio: false
generated: true
image: false
lang: en
layout: post
title: Old Budget Hardware Bottlenecks Performance
translated: false
type: note
---

Here's what's inside that machine — and yes, the hardware itself is the reason it's slow:

## Hardware findings

| Component | Spec | Verdict |
|-----------|------|---------|
| **CPU** | AMD **Athlon X4 850** Quad Core (2015) | ❌ Weak budget CPU |
| **RAM** | **8 GB DDR3-1333** (2×4 GB, ECC) | ❌ Old, slow, small |
| **OS disk** | WD Green **120 GB SSD** (`/`) | ⚠️ OK, but low-end SSD |
| **2nd disk** | Seagate **500 GB HDD** (7200rpm, 2010-era) | idle/unused |

## Why it's slow

**1. CPU — AMD Athlon X4 850 (the main culprit)**
- Released **2015**, a budget FM2+ socket chip (Steamroller architecture, 28nm)
- 4 cores @ 3.2 GHz, **only 4 MB L2 cache and no L3 cache at all**
- No AVX2 (which is why we installed mihomo's "compatible" build)
- Single-thread performance is roughly **~10× slower** than a modern mid-range CPU. Even a Raspberry Pi 5 beats it in many tasks.

**2. RAM — 8 GB DDR3-1333**
- DDR3 at 1333 MT/s is ~2010-era memory speed
- 8 GB is enough for a lightweight server, but combined with the weak CPU it bottlenecks desktop use

**3. Storage (this part is actually fine)**
- Ubuntu is correctly installed on the **120 GB WD Green SSD**, not the old 500 GB HDD — so disk isn't the main problem. Though the WD Green is a DRAM-less budget SSD (slow writes under load).

## Current status
- Load average was **3.32** right after boot (14 min uptime — likely from mihomo's rule-provider downloads + my install work), but CPU is now ~97% idle and RAM has ~5.6 GB free. So it's not overloaded right now — it's just **fundamentally an old 2015 budget desktop**.

## Bottom line
This is a ~2015 entry-level desktop platform (FM2+). It can't be meaningfully upgraded — FM2+ has no fast CPUs, and DDR3 is obsolete. It's fine as a lightweight **headless server** (running mihomo as a LAN proxy is a perfect use), but it will always feel slow as an interactive Ubuntu desktop.

Would you like me to check what (if anything) is actively consuming resources, or slim down Ubuntu (disable snap/animations/services) to squeeze out what it's got?