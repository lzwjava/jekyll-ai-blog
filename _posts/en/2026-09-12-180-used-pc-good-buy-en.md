---
audio: false
generated: true
image: false
lang: en
layout: post
title: "¥180 Used PC: Good Buy?"
translated: false
type: note
---

Question: Is this ¥180 used PC a good buy?

Answer: **Yes — at ¥180, this is a very cheap basic PC, assuming it actually works.** I’d buy it if you need a disposable/light-duty machine.

Specs:

* **i5-3470** — 4C/4T, Ivy Bridge, old but still perfectly usable for Linux, office, downloads, lightweight servers, etc.
* **8GB DDR3-1600** — adequate for basic use; probably the first thing to upgrade.
* **120GB SSD + 500GB HDD** — useful, although both drives are old enough that SMART health matters.
* **H61 motherboard** — ancient, but fine for this CPU.
* **¥180 without GPU** — excellent price.
* **GT 705 + ¥80** — **skip it**. The GT 705 is extremely weak and adds basically no useful compute value. The i5-3470's integrated graphics can handle ordinary display output.

### The real things I'd check

The CPU/motherboard aren't the risk at this price. **Power supply and disks are.**

Before paying, run:

```bash
sudo smartctl -a /dev/sda
sudo smartctl -a /dev/sdb
```

or on Windows use CrystalDiskInfo.

Also check:

* Does it boot reliably?
* SSD health / reallocated sectors
* HDD health / bad sectors
* PSU brand + model
* CPU temperature under load
* USB/network/audio all work
* RAM is actually 8GB
* No random freezes/reboots

**PSU model is particularly important.** If it's some no-name 15-year-old PSU, I'd mentally price the machine at ¥180 **minus the cost of replacing the PSU**.

### My price judgment

| Price        | Verdict                                      |
| ------------ | -------------------------------------------- |
| ¥180 bare PC | 🟢 **Very good**                             |
| ¥260 + GT705 | 🟡 Still okay, but don't bother with the GPU |
| ¥300–350     | 🟡 Reasonable only if condition is excellent |
| ¥400+        | 🔴 I'd look for newer hardware               |

If you're buying it specifically to **run an agent/server/Linux box**, I'd actually consider this more interesting than it looks: ¥180 for a complete x86 machine is hard to beat, provided the PSU and storage aren't dying.

If you send me the **PSU model + a photo of the inside/spec sticker**, I can tell you whether there are any red flags before you buy.

I can also compare this against a few ¥200–500 used-PC configurations and tell you what I'd hunt for instead.
