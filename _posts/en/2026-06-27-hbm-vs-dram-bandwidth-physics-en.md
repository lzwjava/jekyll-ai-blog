---
audio: false
generated: true
image: false
lang: en
layout: post
title: "HBM vs DRAM: Bandwidth Physics"
translated: false
type: note
---

Question: Compare DRAM and HBM.

Answer:

Same DRAM cells underneath — the difference is packaging and the memory bus, which is what dominates bandwidth.

**Core distinction**

| | DDR/GDDR (planar DRAM) | HBM |
|---|---|---|
| Topology | Discrete chips on PCB, beside the processor | DRAM dies stacked vertically (4–16 high), beside the die on a silicon interposer |
| Interconnect | Wide PCB traces, ~16–32 bit/chip | TSVs (through-silicon vias) + microbumps; **1024-bit bus per stack** |
| Bus width | DDR5: 64-bit/channel; GDDR6: 32-bit/chip | 1024-bit/stack × N stacks |
| Clock | High per-pin (GDDR6 ~16–20 Gbps/pin) | Low per-pin (~6.4 Gbps for HBM3) but enormously wide |
| Bandwidth | DDR5 ~50 GB/s; GDDR6X ~1 TB/s | HBM3 ~3.35 TB/s/stack; **HBM3E ~1.2+ TB/s/stack** |
| Capacity/footprint | High capacity, large area | High density in tiny area |
| Power/bit | Higher | ~3–4× lower pJ/bit (short, wide, slow) |
| Cost | Cheap, commodity | Expensive (interposer, TSV, stacking yield) |

**The physics that matters**

HBM's win is the *wide-and-slow* strategy. Bandwidth = bus_width × transfer_rate. GDDR pushes transfer rate up per pin (signal integrity nightmare, power-hungry). HBM goes the other way: keep per-pin rate modest, but make the bus absurdly wide (1024 bits/stack) by physically stacking dies and connecting them with TSVs over a silicon interposer — distances measured in millimeters, not centimeters. Short traces → lower capacitance → less energy per bit → you can run more bits in parallel without melting the chip.

**Your MI300X case**

The 192 GB HBM3 you're training GPT-2 760M on is 8 stacks. Aggregate bandwidth ~5.3 TB/s. For LLM training, you're bandwidth-bound on the backward pass and optimizer states far more than compute-bound at that scale — which is exactly why HBM exists. A 760M model with Adam (params + 2 moment buffers + grads, fp32 ≈ 760M × 16 bytes ≈ 12 GB) fits trivially; the bandwidth is what lets you keep the MFU up.

Quick mental model for why GPUs moved to HBM:

```
roofline: perf = min(compute_peak, bandwidth × arithmetic_intensity)
```

Transformer training/inference sits at modest arithmetic intensity (especially decode, which is memory-bound — every token re-reads the KV cache and weights). So the bandwidth term dominates, and HBM is the only way to feed thousands of FLOP units without starving them. This is also why GDDR-based consumer cards (your RTX 4070, ~504 GB/s GDDR6X) hit a wall on large-model inference long before they run out of FLOPs.

**When DDR still wins:** capacity at low cost (CPUs with TB of DDR5), where you don't need the bandwidth and can't pay the interposer tax.
