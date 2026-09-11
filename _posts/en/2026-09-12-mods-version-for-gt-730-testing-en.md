---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS Version for GT 730 Testing
translated: false
type: note
---

**Question:** Which MODS version should be used for testing the GT 730 (GK208)?

**Answer:****Question:** Which MODS version should be used to test the GT 730 (GK208/Kepler)?

**Answer:**

Based on research, here is the version compatibility breakdown:

**Recommended: MODS 367.38.1**

There are two publicly available versions — **367.38.1** (full package with all tools and documentation) and **400.184** (partial, containing only `mods` and `mats` tools). The 367.38.1 version does not support Turing cards, so for older Kepler cards like the GT 730, **367.38.1 is the correct and complete version to use.**

**Why your current MODS 400.250 is failing:**

The error you saw:
```
391/gpu_drv/r400/r400_00-626s  No such file or directory
Error Code = 467
```

MODS 400.x was designed primarily for **newer GPU architectures (Turing/Ampere)**. The board script `r400_00-626s` for the GK208 (GT 730) is either missing or incompatible in version 400.250.

**Version Compatibility Summary:**

| MODS Version | GT 730 (Kepler GK208) | GTX 16xx / RTX (Turing+) |
|---|---|---|
| **367.38.1** | ✅ Full support | ❌ Not supported |
| **400.184 / 400.250** | ❌ Missing board scripts | ✅ Supported |

**Action Steps:**

1. Download **MODS 367.38.1** (search on GPU repair forums or Russian hardware sites)
2. Create a bootable flash drive using Rufus with FreeDOS, extract the MODS zip and copy contents onto it
3. Re-run the GPU test — the `r400_00-626s` board script should be present in 367.38.1

**References:**
- [Nvidia Modular Diagnostic Software - MODS (rkblog.dev)](https://rkblog.dev/posts/pc-hardware/nvidia-modular-diagnostic-software-mods/)
- [NVIDIA MODS Kernel Driver (GitHub)](https://github.com/NVIDIA/mods-kernel-driver)
