---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS GPU Version Compatibility
translated: false
type: note
---

Great question. Here's what the document tells us about MODS version compatibility:

## MODS Version and GPU Support

### MODS R367 (this document - July 2015)
This version supports GPU architectures up to **Kepler** and **early Maxwell**, based on what the document explicitly mentions:

| GPU Family | Arch | Examples | Supported by R367? |
|---|---|---|---|
| **Fermi** | GF1xx | GTX 480, 580 | ✅ Yes |
| **Kepler** | GK1xx | **GTX 760**, GTX 680, GT 710 | ✅ Yes |
| **Maxwell** (early) | GM1xx | GTX 750 Ti, GTX 960 | ✅ Partial |
| **Maxwell** (later) | GM2xx | GTX 980, GTX 970 | ⚠️ Maybe (edge) |
| **Pascal** | GP1xx | GTX 1060, 1070, 1080 | ❌ No |
| **Turing** | TU1xx | RTX 2060, 2070, 2080 | ❌ No |
| **Ampere** | GA1xx | **RTX 3060**, RTX 3070, 3080 | ❌ No |

### For your specific GPUs:

**GTX 760 (Kepler, 2013)** — ✅ Should work with MODS R367
- It's a Kepler GK104 chip, which the document explicitly supports with flags like `-gpu_family kepler` and mentions "Test for the InlineToMemory class on Kepler GPUs"

**RTX 3060 (Ampere, 2021)** — ❌ **Will NOT work with MODS R367**
- MODS R367 was released ~6 years before the RTX 3060
- Ampere architecture was introduced in 2020, five years after this MODS version
- You would need a much newer MODS version (R4xx or R5xx series)

### If the device can't be found:

**1. Check if a newer MODS version is needed**
```bash
mods -v   # shows version like "367.XX"
```
For an RTX 3060, you likely need a MODS version from **R495 or newer** (matching the driver branch that supports Ampere).

**2. Check if the NVIDIA display driver is interfering**
```
Make absolutely sure the nvidia kernel module is not loaded,
otherwise the system may become unstable.
```
The document explicitly warns: *"Please make absolutely sure that the nvidia kernel module is not loaded"* — if Xorg or the NVIDIA driver is running, MODS may not detect the GPU.

**3. Try architecture-specific flags**
```bash
mods gputest.js -mfg -gpu_family kepler     # For GTX 760
mods gputest.js -mfg -gpu_family fermi      # For older GPUs
```

**4. Check error codes**
- Error **31**: "The only devices found in the system are obsolete" — MODS recognizes the GPU but it's too old
- Error **710**: "selected device is not supported" — GPU is too new for this MODS version
- Error **"NVRM card not present"** — GPU may not be detected at all

### Summary
- **GTX 760 → Use MODS R367** (this version is fine)
- **RTX 3060 → Need MODS R495 or newer** (R367 is too old)
