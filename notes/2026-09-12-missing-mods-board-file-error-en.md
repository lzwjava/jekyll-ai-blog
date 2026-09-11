---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing MODS Board File Error
translated: false
type: note
---

**Question:** What does this new MODS error mean, and how can it be fixed?

**Answer:**

This is a **different error** from before. The GPU hardware init issue is gone — now it's a **missing file error**.

**System Info from screen:**

| Field | Value |
| --- | --- |
| MODS Version | 400.250 |
| Kernel | 4.17.4-gentoo |
| Kernel Driver | 3.87 |
| SBIOS Version | 4.6.5 |
| Hostname | tinylinux |

**The actual error:**

```
boards.js : 391/gpu_drv/r400/r400_00-626s No such file or directory
Error Code = 0000000467 (No such file or directory)
```

**What this means:**

MODS is trying to load a **board definition file** for the GT 730, specifically looking for:

```
r400/r400_00-626s
```

This is a **GPU driver profile/script file** that MODS needs to run the test. It cannot find it in the expected path.

**Possible fixes:**

1. **Wrong MODS version for this GPU**
   - MODS 400.250 may not include the correct board scripts for GK208 (GT 730)
   - Try using an **older or matching MODS version** that includes `r400_00-626s`

2. **Incomplete MODS package**
   - The MODS installation may be missing files
   - Re-download/re-extract the full MODS package and verify file integrity

3. **Check the boards directory manually:**

   ```bash
   find / -name "r400_00-626s*" 2>/dev/null
   ls ./391/gpu_drv/r400/
   ```

4. **Use correct script path flag** if the files exist elsewhere:

   ```bash
   ./mods gputest.js -skip_rm_state_init --datadir /path/to/correct/dir
   ```

---

> 💡 **Key insight:** This error means MODS is now **successfully communicating with the GPU** (progress from before!), but the test script package is incomplete or mismatched for this GPU's PCI device ID (`626s` = GT 730 variant).

**References:**

- [NVIDIA MODS Tool Overview](https://developer.nvidia.com/mods)
