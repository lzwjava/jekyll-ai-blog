---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kirin Chips Are Not Open Source
translated: false
type: note
---

**Question:** Are Huawei's Kirin chips open sourced?

**Answer:** No, the Huawei Kirin chips are **not open source**. They are fully proprietary. Here's a breakdown:

**Ownership & IP**
All Kirin branding, IP, and design authority resides solely with Huawei, through its wholly-owned fabless semiconductor subsidiary HiSilicon.

**Architecture Licensing (not open)**
HiSilicon purchases licenses for CPU designs from ARM Holdings, including various ARM Cortex cores and Mali graphics cores. This means Kirin is built on licensed (but closed) ARM architectures — not open-source RISC-V or similar.

**In-house custom cores (also closed)**
While Huawei still licenses ARM's basic designs, its HiSilicon chip design division has improved on them to build its own custom processor cores in newer chips like the Kirin 9000S. These custom cores are also proprietary and not publicly disclosed.

**Independent IP claim**
The Kirin 710A has the distinction of being the first pure Chinese chip with independent intellectual property (IP) rights — but "independent IP" here means Chinese-owned, not open-sourced.

**In short:** Kirin chips are closed-source, proprietary silicon designed by HiSilicon (Huawei). Neither the chip designs, RTL schematics, nor firmware are publicly released. The only open-source adjacent activity from Huawei is on the *software* side (e.g., parts of HarmonyOS/OpenHarmony), not the chip hardware itself.

---

**References:**
- [What Is HiSilicon Kirin? – Alibaba Electronics](https://electronics.alibaba.com/question/hisilicon-kirin-explained-performance,-ai,-us-restrictions)
- [HiSilicon – EPFL Graph Search](https://graphsearch.epfl.ch/en/concept/39222054)
- [Huawei's New SoC Features Processor Cores Designed In-House – Slashdot](https://mobile.slashdot.org/story/23/09/24/1835200/huaweis-new-soc-features-processor-cores-designed-in-house)
- [Kirin 710A: First Pure Chinese Chip with Independent IP – XDA](https://www.xda-developers.com/huawei-hisilicon-14-nm-kirin-710a-chip-manufactured-shanghai-based-simc/)
