---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding SATA Power for WD10EZEX
translated: false
type: note
---

**Question:** How do I find the right power connector for the WD10EZEX hard drive?

---

**Answer:**

The WD10EZEX uses a standard **SATA power connector** — the wide, flat 15-pin plug that comes directly from your power supply unit (PSU).**How to find it in your case:**

Look inside your case for cables coming out of the PSU (power supply). You're looking for the **wide flat connector** with a distinctive L-shaped notch on one side — it only fits one way.

Your PSU will have one of two setups:

**1. Non-modular PSU** — cables are permanently attached. Trace the bundle of cables from the PSU brick; look for the wide flat SATA power plugs dangling from those cables. There may be a chain of 2–4 SATA connectors on one cable.

**2. Modular/semi-modular PSU** — you plug cables in as needed. Look for a cable labeled **"SATA"** or **"HDD"** in the box that came with your PSU, and plug it into the matching port on the PSU.

---

**Identify it visually:**

| Connector | Pins | Width | Purpose |
| --- | --- | --- | --- |
| **SATA power** ✅ | 15 pins | ~27mm wide, flat | What your HDD needs |
| Molex (old 4-pin) | 4 pins | Chunky rectangular | Older HDDs/fans |
| PCIe 6/8-pin | 6 or 8 pins | Square-ish | GPU only |

The SATA power connector is **wider and flatter** than the old Molex plug, and has an L-shaped locking notch so it can only go in one direction. Just push it firmly into the port on the back edge of the hard drive until it clicks/seats flush.

---

**If you can't find a SATA power cable:**

You can use a **Molex-to-SATA power adapter** (very cheap, ~$2–3) if your PSU only has old 4-pin Molex connectors. Plug the Molex end into the PSU cable, and the SATA end into the drive.
