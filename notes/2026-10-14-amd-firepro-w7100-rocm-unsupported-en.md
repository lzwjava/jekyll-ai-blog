---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD FirePro W7100 ROCm Unsupported
translated: false
type: note
---

**Question:** What ROCm version can run on the AMD FirePro W7100?

---

**Answer:**

**Short answer: None officially.** The W7100 is effectively **unsupported by all ROCm versions**.

**Why — the GPU ID issue**

The W7100 uses the **Tonga** chip, identified as **`gfx802`** in ROCm. This is a critical distinction:

| GPU | ROCm ID | ROCm Support |
|---|---|---|
| Tonga (FirePro W7100) | `gfx802` | ❌ Never officially supported |
| Fiji / Polaris (RX 480, RX 580…) | `gfx803` | ✅ Until ~ROCm 3.7, then broken; fully dropped at ROCm 4.0+ |

With the exception of Tonga (`gfx802`), all AMD GCN GPUs since 2015 were supported by ROCm. Tonga support was explicitly excluded.

Because many ROCm projects rely on HCC (the compiler), and HCC did not compile for `gfx802` by default, support for Tonga effectively never worked across the stack.

**Timeline summary**

| ROCm Version | W7100 / Tonga status |
|---|---|
| 1.x – 2.x | Partially detectable, but not functional for HIP/HCC compute |
| 3.x | Still unrecognized / broken |
| 4.0+ | gfx803 (Fiji) also dropped; gfx802 was never there |
| 5.x → current | No GCN support at all |

ROCm 5.7.1 was the last working version even for gfx803 (Polaris), and ROCm 6+ fully dropped it — showing an "Unsupported HSA device" error at runtime. The W7100's `gfx802` never even reached that level.

**What does work instead?**

- ✅ **OpenCL** — works via the **AMDGPU-PRO closed-source driver** (not ROCm)
- ROCm identifies the card as `Tonga PRO GL [FirePro W7100]` via `clinfo`, but OpenCL shows as v1.2 (with possible v2.1 capability) — this runs through the closed-source stack, not ROCm's open compute stack.
- ❌ **HIP / ROCm compute** — not usable on this card in any version

**Bottom line:** If you're buying this card for ROCm-based AI/ML (PyTorch, TensorFlow via ROCm), it **will not work**. It's better suited for OpenCL workloads, CAD/visualization, or multi-display use.

---

**References:**
- [GitHub – Does ROCm support Tonga? #509](https://github.com/RadeonOpenCompute/ROCm/issues/509)
- [GitHub – gfx802 segfaults with ROCm 2.7 #880](https://github.com/ROCm/ROCm/issues/880)
- [Debian AI List – Dropping gfx803 support](https://lists.debian.org/debian-ai/2024/09/msg00030.html)
- [Phoronix – AMD GCN3/Fiji Support Retired from GCC](https://www.phoronix.com/news/AMD-GCN3-Fiji-GCC-Removal)