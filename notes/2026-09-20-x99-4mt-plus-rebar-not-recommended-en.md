---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99-4MT Plus ReBAR Not Recommended
translated: false
type: note
---

**Question:** Is the 华南 (Huananzhi) X99-4MT Plus + E5-2673 V3 combo good for ReBAR and Above 4G Decoding?

**Answer:**

Two separate issues here — the board and the CPU. Let's break them down.

---

**The motherboard: Huananzhi X99-4MT Plus**

The "4MT" suffix means this is a **DDR3** variant of the Huananzhi X99 micro-ATX lineup, not the BD4 (DDR4). This is a critical distinction — the BD4 is the one confirmed to have native Above 4G Decoding and ReBAR support in its BIOS. The 4MT/4MF/4MD series boards are budget DDR3 boards that share a simpler, more stripped-down BIOS.

There is no specific community documentation confirming that the X99-4MT Plus supports Above 4G Decoding or ReBAR natively. Given the pattern across the Chinese X99 DDR3 boards (精粤 D3, Machinist D3, etc.), native support is very unlikely. BIOS modding may be possible but is uncharted territory for this specific model — it does not have the well-documented BIOS swap path that the BD4 benefits from.

**Verdict on the board for ReBAR: ⚠️ Not recommended if ReBAR is a priority.**

---

**The CPU: E5-2673 V3**

The 2673 V3 is a Haswell-EP Xeon with 12 cores / 24 threads, 2.4 GHz base / 3.1 GHz turbo (some sources indicate up to 3.6 GHz turbo in single-core boost), 30 MB L3 cache, and a 105 W TDP. It was originally an Azure cloud CPU (Microsoft OEM), not a retail part — which is why it's so cheap on the secondhand market. It is fully functional on LGA2011-3 consumer boards and widely used.

Compared to the 2680 V4 from the previous combo, the 2673 V3 is:

| | E5-2673 V3 | E5-2680 V4 |
| --- | --- | --- |
| Architecture | Haswell (V3) | Broadwell (V4) |
| Cores / Threads | 12c / 24t | 14c / 28t |
| Base / Turbo | 2.4 / 3.1 GHz | 2.4 / 3.3 GHz |
| Cache | 30 MB | 35 MB |
| Memory | DDR4 | DDR4 |
| TDP | 105 W | 120 W |
| IPC | Lower (Haswell) | Higher (Broadwell) |

The 2673 V3 is a solid CPU for the price, but the 2680 V4 is meaningfully better — more cores, newer architecture with better IPC, and slightly higher turbo. If you're choosing between the two, the BD4 + 2680 V4 combo from the previous recommendation is the stronger pick on every axis.

---

**Overall verdict**

The X99-4MT Plus + 2673 V3 is a **decent general-purpose budget build**, but if ReBAR and Above 4G Decoding are requirements, this combo falls short. The DDR3 board is the weaker link — not confirmed for ReBAR support, and the community path (Huananzhi BD4 BIOS swap) may not be compatible with DDR3 boards. You'd be taking on significant uncertainty.

**The Huananzhi X99 BD4 + E5-2680 V4 combo discussed earlier remains the clear recommendation** if native ReBAR matters to you.

---

**References:**

- [Guide: Overclock BIOS mods for Chinese X99 MBs – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [E5-2673 V3 Specs – OpenBenchmarking](https://openbenchmarking.org/s/Intel+Xeon+E5-2673+v3)
