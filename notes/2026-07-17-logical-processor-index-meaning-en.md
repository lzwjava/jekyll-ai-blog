---
audio: false
generated: true
image: false
lang: en
layout: post
title: Logical Processor Index Meaning
translated: false
type: note
---

Question: What does "12 (AMD EPYC 7443 24-Core Processor)" mean?

Answer: That's a line from `/proc/cpuinfo` or `lscpu -e` — `12` is the **logical processor index** (0-based), and the string is the `model name` field for that logical CPU.

```bash
# see it yourself
grep -A0 "^processor\|^model name" /proc/cpuinfo | head -30
# or cleaner
lscpu -e
```

Context on the EPYC 7443:

- **24 physical cores / 48 threads (SMT2)** — Zen 3, 7nm
- Base clock 2.85 GHz, boost 4.0 GHz
- 128 MB L3 cache
- 8 CCDs disabled down to fewer... actually 7443 has 4 CCDs × 6 cores, 32MB L3 per CCD region shared
- TDP 200W, PCIe 4.0, 8-channel DDR4-3200

So processor index `12` is just the 13th logical CPU (thread) on that socket — with SMT on, cores 0–23 map to physical cores 0–23 and 24–47 are their sibling threads (or interleaved, depends on topology — check `lscpu -e` for the actual `CORE` column to see which physical core owns thread 12).

If you're pinning training/inference workloads, useful command:

```bash
lscpu -e=CPU,CORE,SOCKET,ONLINE
numactl --hardware   # check NUMA node mapping before pinning threads
```

7443 is a solid CPU for host-side dataloading / preprocessing alongside MI300X — just make sure you pin dataloader workers to cores on the same NUMA node as the GPU's PCIe root complex to avoid cross-node memory traffic.
