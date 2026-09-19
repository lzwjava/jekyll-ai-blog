---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best-Value ReBAR X99 Combo
translated: false
type: note
---

**Question:** Is the secondhand Huananzhi X99-BD4 + E5-2680V4 combo a good deal for ReBAR and 4G Decoding support?

**Answer:**

Yes — this is actually an **excellent combination** for your use case, and one of the best-value secondhand picks on the LGA2011-3 platform right now. Here's the full breakdown:

---

**The motherboard: Huananzhi X99-BD4**

As established in the previous answer, the Huananzhi BD4 BIOS natively includes Above 4G Decoding and Resizable BAR support, along with smart fan control, RAM overclocking, Secure Boot, and TPM support — no BIOS modding, no CH341A programmer needed. This is the one Chinese X99 board where everything works out of the box for ReBAR. The seller's description of "华南金牌X99-BD4" (Huananzhi Gold X99-BD4) matches this exact board.

---

**The CPU: E5-2680 V4**

The E5-2680 V4 is a high-end Broadwell-EP processor with 14 physical cores and 28 threads via Hyper-Threading, a base clock of 2.4 GHz boosting up to 3.3 GHz via Turbo Boost, a 35 MB L3 cache, and a TDP of 120 W. It supports up to 4 memory channels of DDR4 (1600/1866/2133/2400 MHz), with a maximum memory bandwidth of 76.8 GB/s, and up to 40 PCIe 3.0 lanes.

For gaming, rendering, multi-instance work, and general desktop use, 14c/28t is still very capable in 2026 — particularly for multi-threaded workloads like Blender, video encoding, or running multiple VMs.

---

**Condition assessment**

The seller describes it as "99新" (99% new), pulled from a personal upgrade, no repairs, no dust, plug-and-play. This is standard Chinese secondhand market language for a board that was used but well-maintained. "有点使用痕迹" (minor cosmetic wear) is honest and expected. The key phrase is "没修过，插上就能用" — not repaired, works as soon as you plug it in. That's the best thing you can hear about a used board.

---

**What to verify before or after buying**

- Confirm it's the **DDR4** version (BD4 = DDR4). If the seller mentions DDR3, that's a different board entirely.
- Check that the BIOS version is recent enough to have the Above 4G Decoding + ReBAR menu items (most BD4 boards shipped with this since ~2022 BIOS revisions).
- After receiving: disable CSM → enable Above 4G Decoding → enable ReBAR → run `ReBarState.exe` to set to 32 (unlimited).

---

**Verdict: Buy it.** The BD4 + 2680V4 is the X99 combo the community consistently recommends for anyone who wants ReBAR to just work. The 2680V4 is also one of the better V4 CPUs (14 cores vs the 12-core 2680V3), so you're getting the faster generation too.

---

**References:**

- [Intel Xeon E5-2680 V4 Official Specs – Intel ARK](https://www.intel.com/content/www/us/en/products/sku/91754/intel-xeon-processor-e52680-v4-35m-cache-2-40-ghz/specifications.html)
- [Guide: Overclock BIOS mods for Chinese X99 MBs (BD4 ReBAR section) – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
