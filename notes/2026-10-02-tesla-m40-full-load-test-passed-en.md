---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 Full Load Test Passed
translated: false
type: note
---

Done — the Tesla M40 now holds up under full load. ✅

**Burn test results (15s, full-core FMA kernel):**

| Metric | Value |
| -------- | ------- |
| Utilization | **100%** |
| SM clock | **1113 MHz** (max boost) |
| Mem clock | **3004 MHz** |
| Power draw | ~136–139 W (cap 250 W) |
| Temp | 35°C → 39°C (cool, healthy) |
| Throughput | **6.12 TFLOPS** FP32 (~90% of M40's ~6.8 peak) |
| Threads | 49,152 (24 SMs × 2048) |

The card is fully healthy under stress — it boosts to max clocks, holds 100% utilization, stays cool, and hits ~90% of theoretical peak FP32, which is exactly what a well-behaved M40 should do. The earlier "power cables not connected" problem is completely resolved.

Note: it pulled ~140W rather than the full 250W cap — that's normal for a pure ALU/FMA workload on an M40 (the 250W ceiling only gets hit under combined memory+compute load). If you want to push it closer to the power limit, I can add a memory-bandwidth-heavy kernel to the mix. Want me to?

Files left on the box (in case you want to rerun):

- `~/gpu_stress` (compiled binary) — run with `~/gpu_stress <seconds>`
- `~/gpu_stress.c` (source)
- `~/gpustress/` (venv with NVRTC/runtime, used only for building)
