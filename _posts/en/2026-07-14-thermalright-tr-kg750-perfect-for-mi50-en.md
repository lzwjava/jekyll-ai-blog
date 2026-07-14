---
audio: false
generated: true
image: false
lang: en
layout: post
title: Thermalright TR-KG750 Perfect for MI50
translated: false
type: note
---

Question: Is the Thermalright TR-KG750 (750W, 80+ Gold, ATX3.1, native PCIe5.1, full modular, Japanese caps, 14cm compact) a good fit?

Answer: Yes, this works well. Checked the actual cable manifest for this unit — it ships with 2x CPU 4+4-pin cables, 1x 12VHPWR PCIe 5.1 cable, 2x PCIe 6+2-pin cables, and 2x SATA cables. That gives you exactly the 2 native 8-pin PCIe connectors the MI50 needs — no daisy-chaining, no adapters.

Checks against your build:

- **750W** — right in the 650-750W target range for your ~400-440W sustained load, good headroom without over-provisioning
- **2x native 8-pin PCIe** — direct match for MI50's dual 8-pin requirement, this was the one non-negotiable
- **80+ Gold** — meets the efficiency bar for a sustained-load workload like inference/training
- **ATX3.1** — fully backward compatible with your setup; the extra transient-response spec (designed for spiky modern GPU loads) doesn't hurt anything on an older card, it's just unused headroom
- **The 12VHPWR cable is dead weight for you** — MI50 doesn't use it, just leave it unplugged and coiled in the case, no downside to it being there
- **14cm compact body** — fits mATX cases without clearance issues, good match for the B550M board

One thing to sanity check yourself since spec sheets don't list it: confirm 80+ Gold efficiency curve numbers (20%/50%/100% load) if you want hard data, but at 750W rated / ~430W actual draw you're sitting around 55-58% load, which is the efficiency sweet spot for any Gold-rated unit regardless of brand.

Verdict: **buy it.** No changes needed to your parts list.

References:

- [TR-KG750 official cable/packing list](https://mall.icw.buaa.edu.cn/SzhtShop/detail/jd/100188730172)
- [TR-KG750 spec sheet — ZOL](https://detail.zol.com.cn/2125/2124585/param.shtml)
