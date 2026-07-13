---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 coil whine and benchmark anomaly
translated: false
type: note
---

Question: (1) Why does an MI50 whine on a 300W PSU but not a 400W one? (2) Local shop has a "Radeon Pro VII" (crossflashed MI50) scoring 1617 in 鲁大师 — good deal or not?

Answer:

**1. Coil whine at 300W vs 400W**

This isn't really about the PSU's *rated* wattage, it's about **transient current headroom on the 12V rail feeding the 8-pin(s)**. MI50 stock is ~200-225W, but the common "满血" (full-power) BIOS/registry mod pushes it to 300W. Under that load:

- HBM2 + VRM draw fast current spikes that a marginal PSU can't source cleanly → the PSU's own inductors/MOSFETs start switching harder to compensate → audible 啸叫 (whine), not damage, just noise from voltage regulation working overtime.
- A "400W-rated" PSU isn't inherently better per-watt — it's just giving you more **rail headroom**, so at 300W draw you're not near its transient limit anymore.
- Confirmed pattern from Chinese MI50 forums: power limiting the GPU to reduce wattage removed the whine entirely — same mechanism, inverse direction (they reduced W instead of increasing PSU capacity).

Practical fix if you're stuck on a 300W PSU: cap power via `rocm-smi --setpoweroverdrive` or the AMD MPT tool to ~250W. Or just use native 8-pin cables straight from the PSU (not daisy-chained from one connector, not molex adapters) — bad cabling is the other #1 cause of this exact symptom.

**2. The shop's "Radeon Pro VII" — is it legit, is 1617 believable?**

This card is almost certainly an MI50 crossflashed to the Radeon Pro VII (or V420) vBIOS — that's the standard mod to unlock the miniDP output, confirmed by since only this BIOS enables the miniDP port on the MI50. Legitimate practice, not a scam by itself — MI50 and Radeon Pro VII/V420 share the same Vega 20 silicon and PCB.

But **1617 as a 鲁大师 total score is a huge red flag**. A healthy MI50/Radeon Pro VII scores around 400,000 (40万) points on 鲁大师. 1617 is off by ~250x. Two possibilities:

- **It really is the total score** → card is broken: PCIe link degraded (running x1 instead of x16), bad vBIOS flash causing fallback clocks, driver not actually loaded (Windows showing generic "Microsoft Basic Display Adapter"), or memory throttled/damaged. Walk away or demand a live re-test in front of you.
- **It's actually the core clock in MHz, not a benchmark score** — MI50 base clock is 1625 MHz, so 1617 lines up almost exactly. If the seller/shop conflated "clock speed" with "跑分", the card may be totally fine.

Don't guess — make them run it live:

```bash
# on the spot, before paying
rocm-smi --showclocks --showtemp --showmeminfo vram
lspci -vv | grep -A2 "LnkSta:"   # confirm PCIe x16 Gen3/4, not x1/x4
```

or on Windows, GPU-Z showing core clock ~1625-1725MHz, 16GB HBM2, PCIe x16.

Also physically check per known scam pattern: the MI50's outer label and ECC chip prove it hasn't done mining duty — mining-flogged cards get reflowed and lose the graphene thermal pad (brittle, cracks on disassembly), so ask if it's ever been opened.

90°C after 10min burn is roughly normal for stock MI50 cooling under full load (throttle/beep threshold is ~95-100°C junction) — not a red flag by itself, but plan better cooling if you'll run sustained training jobs.

**Bottom line**: don't pay until they show you a live rocm-smi/GPU-Z read with real clocks and a fresh 鲁大师 run in front of you. If 1617 is genuinely the benchmark total, it's a dud.

References:

- [MI50本地部署DeepSeek交流（上） - 知乎](https://zhuanlan.zhihu.com/p/23351570033)
- [MI50 32G版vbios汇总及通用驱动安装办法 - CSDN](https://blog.csdn.net/dwd112358/article/details/153295770)
- [不到600元的苏妈专业卡对标4060 - CSDN](https://blog.csdn.net/minge89/article/details/148349350)
- [ATX3.0 psu's and coil whine - Overclockers UK](https://forums.overclockers.co.uk/threads/atx3-0-psus-and-coil-whine.18967019/)
