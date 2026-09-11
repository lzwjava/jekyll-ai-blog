---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix MODS Error 467 (Kepler)
translated: false
type: note
---

**Question:** Now running MODS 367.56.4, but still getting Error 467 "No such file or directory" — what does this mean and how to fix it?

**Answer:**

Good progress — you switched to the 367.x version as recommended. But there's still a missing file issue. Here's the detailed analysis:

**Key info from screen:**

| Field | Value |
|---|---|
| MODS Version | **367.56.4** |
| RM Version | `rel/gpu_drv/r367/r367_00-557` |
| gputest.js | 59 entries |
| boards.js | 7 entries |
| boards.db | 3208 entries |

**The errors:**
```
Error 467 : Global.LoadGoldenValues  No such file or directory
Error 467 : Global.InitializeGpuTests  No such file or directory
```

**What this means:**

MODS is now loading correctly (r367 driver found ✅), but it cannot find the **"Golden Values"** file — this is a reference data file containing expected test results for your specific GPU board ID. Without it, MODS cannot validate the GPU test results.

**Notable observations:**
- `boards_gp102.db`, `boards_gp104.db`, `boards_gp106.db` are present → these are **Pascal** GPU board databases
- But there is **no `boards_gk208.db`** or equivalent **Kepler** board database listed
- This confirms the 367.56.4 package you have is **Pascal-focused**, not Kepler (GT 730)

**You need MODS 367.38.1 specifically**, not just any 367.x version:

| Version | GT 730 (GK208 Kepler) |
|---|---|
| **367.38.1** | ✅ Has Kepler board DB |
| **367.56.4** (current) | ❌ Pascal boards only |
| **400.x** | ❌ Wrong architecture |

**Action Steps:**

1. Find and download **MODS 367.38.1** specifically (not 367.56.4)
2. Verify after extraction that you see files like:
   ```
   boards_gk208.db  ← this must exist
   ```
3. Re-run the test with that version

> 💡 The version number matters a lot — 367.38.1 was released when Kepler was still the primary supported architecture, so it contains the correct Golden Values and board DB for GK208.

**References:**
- [Nvidia Modular Diagnostic Software - MODS (rkblog.dev)](https://rkblog.dev/posts/pc-hardware/nvidia-modular-diagnostic-software-mods/)
