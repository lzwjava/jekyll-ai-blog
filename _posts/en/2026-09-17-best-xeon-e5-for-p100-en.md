---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Xeon E5 for P100
translated: false
type: note
---

Question: **Which CPU should you pair with the Huananzhi X99-BD4 for a Tesla P100?**

Answer: Go with a **Xeon E5 v4**, especially if this is an AI/compute node.

### My picks

| CPU            | Cores / Threads |  TDP | Why                               |
| -------------- | --------------: | ---: | --------------------------------- |
| **E5-2683 v4** |         16 / 32 | 120W | **Best cheap choice**             |
| **E5-2690 v4** |         14 / 28 | 135W | Higher clocks                     |
| **E5-2697 v4** |         18 / 36 | 145W | More CPU throughput               |
| E5-2680 v4     |         14 / 28 | 120W | Cheap alternative                 |
| E5-2699 v4     |         22 / 44 | 145W | Maximum cores, usually poor value |

For **1× P100**, I'd buy the **E5-2683 v4**.

```text
X99-BD4
   │
   └── E5-2683 v4
          │
          ├── 16C / 32T
          ├── 40 PCIe 3.0 lanes
          └── 120W
                  │
                  └── Tesla P100 16GB
```

The key thing for your setup is **PCIe lanes**, not CPU FLOPS. The E5-2683 v4 gives you plenty of PCIe connectivity for a P100 + NVMe + NIC.

### If you're building 2× P100

I'd still use:

**E5-2683 v4 → excellent cheap option**

or

**E5-2697 v4 → if you actually have CPU-side workloads.**

I wouldn't spend money on an E5-2699 v4 just to feed GPUs. The P100 is going to dominate the compute workload.

### One caveat

These Chinese X99 boards can be picky about BIOS/CPU compatibility. **E5-2683 v4 is Broadwell-EP**, so verify that the particular BD4 BIOS supports v4 CPUs before buying a large batch.

If you're buying **200 X99-BD4 boards**, I'd actually test:

```bash
lscpu
lspci -nn
nvidia-smi
```

with **E5-2683 v4 + P100 + 128GB DDR4** on one board before committing to the whole batch.
