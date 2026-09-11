---
audio: false
generated: true
image: false
lang: en
layout: post
title: Headless GPU MODS Init Failure
translated: false
type: note
---

**Question:** Could the hardware initialization failure be because the system is using the integrated GPU for video output, while MODS is trying to test the dedicated GPU (GK208)?

**Answer:**

**Yes, exactly! That is very likely the correct explanation.**

This is a classic scenario in GPU manufacturing/testing environments:

---

**What's happening:**

```
System Video Output → Integrated GPU (iGPU)
MODS Test Target   → Dedicated GPU (GK208 / discrete)
```

- The dedicated GPU (GK208) has **no display connected** to it
- It is running in a **headless** state
- MODS tries to initialize the GPU's display/user interface (`EnableUserInterface`) and **fails** because there's no active display on that GPU

---

**This explains the specific error:**

```
Error 0x00000000237 : Global.EnableUserInterface unable to set mode
```

This error is about **display mode setting**, which fails on a headless discrete GPU.

---

**What you should try:**

1. **Add `-notest` with headless flag** — some MODS versions support headless mode
2. **Use `-oca` or `-oqa` mode** which may skip display init
3. **Try running without `-skip_rm_state_init`** to let RM fully initialize the discrete GPU:

```bash
./mods gputest.js -mfg
```

4. **Check if MODS has a headless/no-display option** in its help:

```bash
./mods --help
```

In manufacturing test environments, it is **completely normal** to output video through the iGPU while stress-testing a discrete GPU — MODS should support this configuration.

**References:**

- [NVIDIA MODS Documentation](https://developer.nvidia.com/mods)
