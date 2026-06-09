---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep MAX_JOBS at 32
translated: false
type: note
---

Question: Can we set `MAX_JOBS` even larger than 32 to speed up the compilation further?

Answer: **No, you should not increase `MAX_JOBS` any further.** Keeping it at 32 (or even dropping it back down slightly) is the safest choice.

While your RAM has plenty of headroom (149 GB free), increasing `MAX_JOBS` further will not make the build faster, and it may actually slow it down or crash it due to **CPU over-subscription** and **process thrashing**.

Here is why your build speed is dropping, and why a higher number won't help.

---

## Why Setting It Higher Won't Help

### 1. You have 20 vCPUs, but 66 Compiler Processes are already running

Look closely at this line from your log:

> `32 GB RAM used, 149 GB free — no memory pressure. 66 hipcc processes running.`

Even though you set `MAX_JOBS=32`, Python's build system spawning `hipcc` (the AMD compiler frontend) often creates multiple child processes per job (e.g., preprocessing, compiling, and assembling).
Because your AMD cloud instance only has **20 vCPUs**, having 66 active processes means your CPU is heavily over-subscribed. The CPU cores are spending more time context-switching (swapping tasks back and forth) than doing actual math.

### 2. The "Later Kernels" Bottleneck

As your automation agent (Hermes) correctly noted: **"Later kernels are just bigger."**
The compilation process doesn't handle identical files from start to finish.

* The first 93 files were small, simple helper objects (which is why they finished in 1 minute).
* The subsequent files contain the massive, heavily-templated **Composable Kernel (CK) attention blocks**.

Each individual file now takes much longer to compile. Forcing a 20-vCPU machine to process more than 32 of these massive files simultaneously will saturate the CPU instruction pipelines completely.

---

## What Happens if You Push it Higher?

If you try to set `MAX_JOBS=64` or higher:

* **The build time might increase:** The CPU will choke on context switching, leading to a state called *thrashing*.
* **GNU Make Internal Errors:** Pytorch/HIP source builds can throw internal segmentation faults or pipeline errors if the process table gets completely flooded.

---

## Summary Strategy

Your current pace (**~35 to 50 minutes remaining**) is entirely normal and expected when compiling FlashAttention from scratch for a high-performance target like `gfx942` (MI300X).

Let the current build finish. The good news is that **you only have to do this once**. Once the `.whl` package or installation is complete, FlashAttention will run at native speed on your MI300X GPU without needing to compile anything again.
