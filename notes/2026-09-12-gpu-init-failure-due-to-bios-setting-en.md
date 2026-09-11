---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Init Failure Due to BIOS Setting
translated: false
type: note
---

**Question:** Since the primary display is set to integrated GPU in BIOS, are the GPU initialization errors expected when testing the discrete GPU (GT 730)?

**Answer:**

**Yes, this is very likely the root cause of the MODS initialization failure.**

When the BIOS is configured to use the **integrated GPU as primary display**, the system allocates display resources (framebuffer, IRQ, memory-mapped I/O) to the iGPU. The discrete GT 730 may not get properly initialized by the system firmware, causing MODS to fail when it tries to directly access the GPU hardware.

**What's happening:**

```
FB Base : 0xe0000000   ← Framebuffer not properly mapped
IRQ     : 11           ← IRQ assigned but GPU not initialized
Error 229              ← Hardware never completes init sequence
Error 237              ← Can't set display mode (no primary display ownership)
```

**To properly test the discrete GT 730 with MODS:**

1. **Enter BIOS/UEFI** → Change **Primary Display** from `iGPU` → `PCIe` or `PEG`
2. **Save & reboot**, then re-run the MODS test
3. Alternatively, connect your monitor to the **GT 730's output** directly
4. Re-run:
   ```bash
   ./mods gputest.js -skip_rm_state_init
   ```

**If the test passes after switching** → GT 730 is healthy, no hardware issue.

**If the test still fails after switching** → Possible hardware defect on the GT 730.

---

> 💡 The `-skip_rm_state_init` flag you're already using is correct for bypass testing, but it cannot overcome the fundamental issue of the GPU not being initialized by the BIOS.
