---
audio: false
generated: true
image: false
lang: en
layout: post
title: GT 730 MODS Golden File Missing
translated: false
type: note
---

**Question:** Why does MODS fail when testing a GT 730 GPU?

**Answer:**

The error is clear from Image 3:

```
Failed to open file gldGK208S.bin – No such file or directory
Error 0000000000011 : Global.LoadGoldenValuesHelper file does not exist
Error Code = 0000000000011 (file does not exist)
```

### Root Cause

MODS is looking for a **Golden Values file** named `gldGK208S.bin` for your GPU. From Image 2, the GPU Device ID is `GK208S` (GT 730 uses the GK208 chip). This `.bin` file contains reference/baseline test values for that specific GPU die, and **it's missing from your MODS installation**.

### Why This Happens

| Reason | Detail |
|---|---|
| **MODS version too new** | MODS 455.127 may have dropped legacy Kepler (GK208) golden files |
| **Incomplete MODS package** | The `gldGK208S.bin` was never included or was deleted |
| **Wrong MODS build** | Some MODS builds are GPU-family specific |

### How to Fix

1. **Get the correct MODS package** that includes Kepler GPU support — older MODS releases (pre-R450) more reliably include GK208 golden files
2. **Manually obtain `gldGK208S.bin`** from NVIDIA and place it in the MODS working directory
3. **Run MODS with `-skipGoldenCheck`** flag if you only want functional tests without golden value comparison:
   ```bash
   ./mods gputest.js --skipGoldenCheck
   ```
4. **Contact NVIDIA** — MODS is an internal/partner tool; the GK208S golden file may require a direct request

### Note on Hardware

The GT 730 (GK208) is a **Kepler-generation GPU (2014 era)**. MODS support for legacy Kepler may be limited in newer driver branches like r455.

---

References:
- [NVIDIA MODS Overview](https://developer.nvidia.com/mods)
- [GK208 / GT 730 Architecture Info](https://www.techpowerup.com/gpu-specs/nvidia-gk208b.g186)
