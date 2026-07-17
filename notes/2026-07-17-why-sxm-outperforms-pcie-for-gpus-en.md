---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why SXM Outperforms PCIe for GPUs
translated: false
type: note
---

Question: Why is PCIe form-factor worse than SXM for GPUs (e.g. H100/H200/MI300X)?

Answer:

Core reasons, in order of actual impact:

**1. Interconnect bandwidth (the big one)**
- SXM exposes NVLink (or Infinity Fabric for MI300X) directly through the socket to a NVSwitch backplane.
- H100 SXM: 900 GB/s NVLink bidirectional per GPU, all-to-all via NVSwitch.
- H100 PCIe: NVLink bridge (if present) only gives ~600 GB/s and only pairs adjacent GPUs (2-GPU bridge, not full mesh). No NVSwitch fabric.
- Without NVLink bridge, PCIe cards fall back to PCIe Gen5 x16 = 64 GB/s bidirectional for GPU-to-GPU traffic — routed through the CPU root complex/PLX switches, adding latency and contending with host traffic.
- For tensor-parallel or pipeline-parallel training (your GPT-2 760M runs, and anything bigger), all-reduce / all-gather cost dominates. 14x bandwidth difference (900 vs 64 GB/s) directly bottlenecks scaling efficiency past 2-4 GPUs.

**2. Power delivery**
- SXM socket delivers power directly from board (up to 700W for H100 SXM, 1000W for B200 SXM).
- PCIe form factor capped by slot + power connectors, typically 300-350W (H100 PCIe is 350W vs SXM's 700W) — meaning lower sustained clocks, less compute.

**3. Cooling**
- SXM modules are designed for HGX baseboards with direct liquid/vapor-chamber cooling engineered per-system.
- PCIe cards use blower-style air cooling in a standard chassis slot — thermal throttling under sustained all-core load is common.

**4. Topology / all-to-all**
- SXM + NVSwitch = full non-blocking all-to-all topology, every GPU talks to every other GPU at full NVLink speed.
- PCIe multi-GPU = tree/star topology through PCIe switches and CPU, asymmetric bandwidth depending on which GPUs communicate.

**Practical number for you:** on 8x H100 SXM, all-reduce for a 7B-param gradient sync takes ~single-digit ms. Same op on 8x H100 PCIe (no NVLink bridge) can be 5-10x slower, directly cutting into MFU (model FLOPs utilization) — this is why cloud providers doing serious pretraining (and why your MI300X boxes matter) default to SXM/OAM baseboards, and PCIe cards are positioned for inference or single/dual-GPU inference workloads where interconnect isn't the bottleneck.

MI300X specifically ships as OAM (Open Accelerator Module, AMD's SXM-equivalent) with Infinity Fabric — same story: 896 GB/s per-GPU aggregate bandwidth vs a hypothetical PCIe MI300X (AMD doesn't actually ship one) which would be capped by Gen5 x16.

References:
- [NVIDIA H100 Datasheet](https://www.nvidia.com/en-us/data-center/h100/)
- [NVIDIA NVLink and NVSwitch](https://www.nvidia.com/en-us/data-center/nvlink/)
- [AMD Instinct MI300X Datasheet](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
