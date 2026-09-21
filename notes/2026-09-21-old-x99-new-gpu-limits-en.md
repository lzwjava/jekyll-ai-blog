---
audio: false
generated: true
image: false
lang: en
layout: post
title: Old X99, New GPU Limits
translated: false
type: note
---

Question: Is the Huanan X99-AD4 + E5-2697v3 combo suitable for 4G Decoding and Resizable BAR, and will it work with a P100 or M40 GPU?

Answer:

**Short answer: Partially — with significant limitations.**

---

### 🔧 Platform Overview

The **Huanan X99-AD4** is a budget Chinese X99 motherboard paired with the **Intel Xeon E5-2697v3** (Haswell-EP). This is a **2014-era LGA2011-v3 platform**.

---

### 4G Decoding (Above 4G Decoding)

| Item | Status |
| ------ | -------- |
| X99 chipset support | ⚠️ **Inconsistent** |
| Huanan X99-AD4 specifically | ⚠️ **Depends on BIOS version** |
| Required for P100/M40 | ✅ Recommended but not always mandatory |

- Many Huanan X99 boards **do have an "Above 4G Decoding" option** in BIOS (often under PCIe settings), but it varies by BIOS revision.
- You should **check your specific BIOS** — look under `Advanced → PCIe Configuration`.
- Without it, large-BAR GPUs may have instability or fail to initialize properly.

---

### Resizable BAR (ReBAR)

| Item | Status |
| ------ | -------- |
| X99 platform ReBAR support | ❌ **Generally NOT supported** |
| E5-2697v3 CPU ReBAR | ❌ No (Haswell architecture predates ReBAR) |
| Huanan X99-AD4 BIOS ReBAR | ❌ Unlikely / no official support |

- **Resizable BAR requires both CPU and motherboard support**, typically from 2020+ platforms (Intel 10th gen+ / AMD Ryzen 5000+).
- The X99 platform is **too old** to support ReBAR natively. Some modded BIOSes claim partial support, but it is **not reliable or officially supported**.

---

### P100 / M40 Compatibility

| GPU | 4G Decoding Needed | ReBAR Needed | Works on X99? |
|-----|--------------------|--------------|---------------|
| **Tesla P100** | ✅ Recommended | ❌ Not required | ✅ Yes, works well |
| **Tesla M40** | ⚠️ Optional | ❌ Not required | ✅ Yes, works well |

- Both the **P100** and **M40** are **data center / compute GPUs** — they do **not** require ReBAR to function.
- ReBAR is mainly a gaming/consumer GPU performance feature (e.g., RTX 3000+).
- For **CUDA compute, AI inference, or rendering**, these cards will work fine on X99 **without ReBAR**.
- Make sure your **PSU can supply sufficient power** (P100: up to 250W; M40: up to 250W).

---

### ✅ Summary

| Feature | Verdict |
| --------- | --------- |
| 4G Decoding | ⚠️ Likely available in BIOS, but verify |
| Resizable BAR | ❌ Not supported on this platform |
| P100 on X99-AD4 | ✅ Compatible for compute workloads |
| M40 on X99-AD4 | ✅ Compatible for compute workloads |

> **Bottom line:** For ML/AI/compute use with a P100 or M40, this ¥189 combo is a **viable budget platform**. ReBAR is irrelevant for these workloads. Just confirm 4G Decoding is in your BIOS and ensure adequate power delivery.

---

References:

- [Intel Xeon E5-2697 v3 Specs](https://ark.intel.com/content/www/us/en/ark/products/81059/intel-xeon-processor-e5-2697-v3-35m-cache-2-60-ghz.html)
- [NVIDIA Tesla P100 Overview](https://www.nvidia.com/en-us/data-center/tesla-p100/)
- [Resizable BAR Explained – Intel](https://www.intel.com/content/www/us/en/support/articles/000090831/graphics.html)
