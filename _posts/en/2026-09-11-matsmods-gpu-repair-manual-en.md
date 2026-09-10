---
audio: false
generated: true
image: false
lang: en
layout: post
title: MATS/MODS GPU Repair Manual
translated: false
type: note
---

Question: How useful is the uploaded **显卡测试命令手册** for GPU repair, especially **MATS/MODS**?

Answer: **Very useful for your GPU-repair setup.** It is essentially a practical MATS/MODS/Tserver field manual, not just a generic GPU benchmark guide.

The most valuable parts for you are:

* **NVIDIA MATS** — memory testing. The manual shows commands such as `./mats -e 10` and `./mats -n 1 -e 5`, and explains how `report.txt` identifies memory errors. 
* **MODS** — initializes/tests the GPU environment before MATS. The manual explicitly says that if the environment cannot reach PASS, you may have a power/core/hardware problem and cannot proceed normally to MATS. 
* **Faulty VRAM localization** — it maps MATS results such as `A0` to the physical VRAM organization on the board. That's exactly the kind of information useful when deciding which memory chip to inspect/replace. 
* **Core vs VRAM differentiation** — it also documents an additional MODS test (`gputest.js ... -matsinfo`) to help distinguish a GPU-core problem from a memory problem. 
* **AMD support** — it covers RX 400/500, Vega, RX 5000/6000 and Radeon VII, with AMD's `tserver`/`memfa` workflow. 

### This changes my view of the ¥208 B75 machine

The manual itself recommends a relatively simple Intel platform, **8 GB+ RAM**, and importantly a board capable of **Multi-GPU**, so that the motherboard iGPU can provide display while the defective discrete GPU is tested. 

So your proposed setup:

```text
B75
E3-1260L
8 GB DDR3
160 GB SSD
        │
        ├── motherboard video → monitor
        │
        └── PCIe x16 → GPU under repair
                         │
                    MATS / MODS
```

is conceptually **exactly the kind of setup this manual is describing**.

One important limitation: the manual's documented NVIDIA support goes **up to RTX 3090**, and its instructions are based on a particular collection of older MODS/MATS versions.  So don't assume it will automatically handle every newer GPU.

For your repair-learning path, I'd rank the tools:

**multimeter → PSU/test platform → oscilloscope → MATS/MODS → microscope/BGA equipment**

MATS/MODS is particularly valuable because it lets you move from **"this GPU doesn't work"** to something much more actionable like **"the memory test reports A0 errors → identify the corresponding VRAM chip → inspect power/data lines → replace/reball → retest."**

That's a big step toward actual board-level GPU repair rather than simply swapping parts.