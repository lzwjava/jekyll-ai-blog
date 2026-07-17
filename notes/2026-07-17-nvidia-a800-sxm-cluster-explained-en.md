---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA A800 SXM Cluster Explained
translated: false
type: note
---

Question: What is an "SXM A800 cluster" (a800集群)?

Answer: It's a multi-node GPU cluster built from NVIDIA A800 GPUs in the SXM form factor — the export-compliant version of the A100 that NVIDIA made specifically for the China market after the Oct 2022 US export controls.

**What A800 actually is:**

- Same silicon as A100 (GA100, 80GB HBM2e, 2.0 TB/s mem bandwidth, ~312 TFLOPS FP16 dense)
- Only real change: NVLink cut from 600 GB/s on the A100 down to 400 GB/s on the A800 — this was the deliberate throttle to stay under the export threshold of chip I/O bandwidth ≥ 600 GB/s combined with a performance-density formula
- FP64/compute performance unchanged, unlike H800 which also zeroed out FP64

**SXM vs PCIe matters here:** NVLink is available in SXM GPUs via HGX server boards, combined with NVSwitch, letting A800 GPUs interconnect at up to 400 GB/s per link — PCIe A800 cards need an NVLink bridge and don't get the same topology. A "SXM A800 cluster" almost always means HGX A800 8-GPU baseboards (like HGX A100 boards but relabeled), each node with NVSwitch fabric, then InfiniBand/RoCE between nodes.

**Why it matters for your workload (multi-node LLM training):** the 33% NVLink cut hits all-reduce/all-gather heavy collectives hardest — large model training efficiency drops because GPU-to-GPU data transmission bandwidth is reduced by a third. You'll feel it most in tensor-parallel (TP) communication within a node; data-parallel/pipeline-parallel across nodes is bottlenecked by your IB fabric anyway so less impact there. If you're training GPT-2 760M-scale, TP isn't even needed — DP + ZeRO is fine and the NVLink cut barely matters. It starts to bite once you go multi-node TP for 30B+ models.

Quick way to inspect topology on an actual node:

```bash
nvidia-smi topo -m
nvidia-smi nvlink -s
```

Since you're already on MI300X (2B tokens/mo), worth noting: MI300X uses Infinity Fabric not NVLink, so this A800 constraint is NVIDIA-cluster-specific — doesn't apply to your current AMD setup.

References:

- [NVIDIA A800 vs A100 — Lenovo Press](https://lenovopress.lenovo.com/lp1813-thinksystem-nvidia-a800-pcie-gpu)
- [Nvidia AI Chips comparison — FiberMall](https://www.fibermall.com/blog/nvidia-ai-chip.htm)
- [GPU Data Sheets — arthurchiao.art](https://arthurchiao.art/blog/gpu-data-sheets/)
