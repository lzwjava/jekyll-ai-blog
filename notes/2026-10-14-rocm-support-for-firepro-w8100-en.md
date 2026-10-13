---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm Support for FirePro W8100
translated: false
type: note
---

**Question:** What ROCm version can run on the AMD FirePro W8100?

---

**Answer:**

The W8100 uses the **Hawaii** GPU (`gfx701`, GCN 2.0) — a different and slightly more "ROCm-friendly" chip than the W7100's Tonga. But the story is still largely bad.

**W8100 vs W7100 — Key Difference**

| Card | GPU | ROCm ID | Architecture |
|---|---|---|---|
| FirePro W7100 | Tonga | `gfx802` | GCN 3.0 |
| FirePro W8100 | Hawaii GL40 | `gfx701` | GCN 2.0 |

**Hawaii ROCm History**

Hawaii chips — such as the AMD Radeon R9 390X and FirePro W9100/W8100 — were listed as enabled in the ROCm software, though full support was never guaranteed.

Experimental support for Hawaii (GFX7) GPUs did not require or take advantage of PCIe Atomics, which was actually an advantage over GFX8 cards that needed PCIe Atomic support from the CPU.

**But then ROCm 2.0 broke it:**

Support for Hawaii (gfx700/1) has been broken since ROCm 2.0, not even unofficially supported.

**Timeline**

| ROCm Version | W8100 / Hawaii status |
|---|---|
| 1.x | ✅ Partial / experimental — actually worked for some workloads |
| 2.0+ | ❌ Broken — Hawaii outgrew the fixed microcode store in the MEC block |
| 3.x → current | ❌ Completely unsupported, no plans to restore |

Hawaii (gfx7) had an early version of MEC (Micro Engine Compute) with a fixed microcode store, while later gfx8 parts could support larger microcode images by executing directly out of VRAM. It was always a challenge to fit even stripped-down ROCm functionality into the fixed microcode store — so it likely just outgrew it.

**Comparison Summary**

| | W7100 (Tonga/gfx802) | W8100 (Hawaii/gfx701) |
|---|---|---|
| ROCm 1.x | ❌ Never worked | ⚠️ Experimental |
| ROCm 2.x+ | ❌ Never worked | ❌ Broken |
| ROCm today | ❌ Unsupported | ❌ Unsupported |
| OpenCL (AMDGPU-PRO) | ✅ Works | ✅ Works |

**Bottom line:** The W8100 is marginally better historically — it at least had brief experimental ROCm 1.x support — but both cards are effectively **dead for ROCm compute in 2026**. If OpenCL is sufficient for your workload (e.g. Blender, some scientific apps), the W8100's wider **512-bit memory bus and 320 GB/s bandwidth** make it noticeably more capable than the W7100 (160 GB/s) for those tasks.

---

**References:**
- [Phoronix Forums – Hawaii GFX7 ROCm broken since 2.0](https://phoronix.com/forums/forum/linux-graphics-x-org-drivers/open-source-amd-linux/1184064-radeon-rocm-3-5-released-with-new-features-but-still-no-navi-support/page9)
- [ROCm GFX8P – GFX7 Hawaii partial/experimental listing](https://copr.fedorainfracloud.org/coprs/cosmicfusion/ROCm-GFX8P)
- [AMD Community – R9 290 / Hawaii ROCm discussion](https://community.amd.com/t5/ai-discussions/r9-290-rocm-support/td-p/709523)
- [TechPowerUp – FirePro W8100 specs](https://www.techpowerup.com/gpudb/2588/firepro-w8100)