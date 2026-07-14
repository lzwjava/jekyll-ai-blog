---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best DDR4 for Ryzen 5 5600 Build
translated: false
type: note
---

Question: What DDR4 memory should I pair with the R5 5600 + Colorful B550M-GAMING WIFI6E V14 + MI50 16GB build?

Answer:

This board is a budget mATX B550, which almost certainly means **2 DIMM slots**, not 4 — confirm on the box/manual before buying a 4-stick kit, since dual-rank 2-DIMM configs behave differently than quad-DIMM boards for OC stability.

**Speed target: DDR4-3600, not higher.**

Zen3 (5600) runs Infinity Fabric Clock (FCLK) and Memory Clock (MCLK) in 1:1 mode up to ~1800MHz FCLK = DDR4-3600. Above that, most chips drop to 2:1 mode, which adds latency and usually nets you *worse* real-world performance despite the higher rated speed — this is a known Zen3 platform quirk, not board-specific. So:
- DDR4-3600 CL16-18 = sweet spot, stays 1:1
- DDR4-3200 CL16 = safe fallback if you get a bad IMC sample or the 3600 kit won't post
- DDR4-4000+ = don't bother, you're paying more for a kit that likely runs slower net-net on this CPU

**Capacity: 2x16GB (32GB) minimum, 2x32GB (64GB) if budget allows.**

The MI50 16GB does its own compute in HBM2 — system RAM isn't in the inference hot path unless you're doing CPU offload for models that don't fit in 16GB VRAM (common with llama.cpp `--n-gpu-layers` partial offload). If you plan to run anything bigger than what fits in 16GB VRAM with partial CPU offload, or run multiple docker containers / agents alongside inference, go 64GB. If this box is dedicated to one inference workload at a time, 32GB is enough.

**Buy dual-rank if the kit lists it** (usually 16GB single-stick kits are dual-rank; check "1Rx8" vs "2Rx8" on the spec sheet) — dual-rank improves bandwidth and stability on AM4 boards over single-rank, at negligible cost difference.

**Concrete pick:** 2x16GB DDR4-3600 CL18 (e.g. Kingston Fury Beast or Crucial Ballistix equivalents at that speed/timing), dual-rank if available. Skip RGB/premium tiers — no performance difference, just cost.

References:
- [Zen3 FCLK:MCLK 1:1 vs 2:1 memory scaling](https://www.cpu-monkey.com/en/compare_cpu-amd_ryzen_5_7500f-vs-amd_ryzen_5_5600)
- [MI50 real deployment notes on BIOS/hardware requirements](http://wtarreau.blogspot.com/2025/12/amd-radeon-instinct-mi50-32gb-best-ai.html)
