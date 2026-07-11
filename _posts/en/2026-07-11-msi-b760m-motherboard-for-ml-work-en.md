---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Motherboard for ML Work
translated: false
type: note
---

## Question: What is the MSI MAG B760M MORTAR WIFI?

## Answer

It's a micro-ATX motherboard built around Intel's B760 chipset, targeting LGA1700 socket CPUs. Relevant to your setup since you're doing GPU/ML workloads on a workstation — here's the spec breakdown with what matters for AI/dev work:

**CPU/Platform**

- Supports Intel Core 14th/13th/12th Gen, Pentium Gold, and Celeron processors on LGA1700
- B760 is the mid-range non-overclocking-focused chipset (no CPU multiplier OC, but memory OC is supported)

**Memory** — this is the part that matters most for local LLM inference/training on CPU or with CPU offload

- 4x DDR5 slots, max capacity 256GB, dual-channel
- Supports OC speeds up to 7200+ MHz depending on DIMM population (1DPC 1R gets the highest 7200+ MT/s, 2DPC 2R drops to 5600+ MT/s)
- 256GB max is genuinely useful if you want to run larger quantized models (GGUF) via CPU/RAM for MoE-style sparse inference where you can't fit everything in VRAM

**PCIe/Expansion** — this is the constraint that actually matters for your RTX 4070 setup

- 2x PCI-E x16 physical slots but only x16/x4 electrical — the primary slot runs PCIe 5.0 x16 from the CPU, a third slot in the layout is PCIe 3.0 x1 from chipset, and there's a PCIe 4.0 x4 slot from chipset
- So single-GPU only really — if you were hoping to add a second GPU for more VRAM pooling, the second x16 physical slot only gets x4 electrical (chipset-routed), which will bottleneck a second GPU hard for anything bandwidth-sensitive (tensor parallel across cards, fast data loading). Fine for a second card doing something less bandwidth-hungry (e.g. a dedicated small-model inference card), not fine for NVLink-less multi-GPU training.

**Storage**

- 2x M.2 slots — one PCIe 4.0 x4 from CPU, one PCIe 4.0 x4/SATA from chipset — plus 4x SATA 6G
- Supports RAID 0/1/5/10 for SATA drives

**Networking**

- Realtek 2.5Gbps LAN plus Intel Wi-Fi 6E with Bluetooth 5.3

**USB/IO**

- Rear ports include 4x USB 2.0, 3x USB 10Gbps Type-A, 1x USB 20Gbps Type-C, plus HDMI 2.1 and DisplayPort 1.4

### Bottom line for your use case

If you're speccing this for a home ML box: the single x16 PCIe 5.0 slot is fine for one RTX 4070 (which only needs PCIe 4.0 x16 bandwidth anyway, so no bottleneck there), and 256GB DDR5 headroom is genuinely attractive for running llama.cpp-style CPU-offloaded MoE inference (e.g. DeepSeek-distilled models) alongside the GPU. But this board is not a multi-GPU training rig — if your DeepSeek v4 MoE work scales toward needing 2+ GPUs, you'd want a board with dual x8/x8 PCIe lanes (usually requires a higher-end chipset like Z790, or HEDT/Threadripper platforms with more CPU PCIe lanes).

References:

- [MAG B760M MORTAR WIFI Specification](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification)
