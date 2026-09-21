---
audio: false
generated: true
image: false
lang: en
layout: post
title: B450M-A PRO MAX II Native ReBAR
translated: false
type: note
---

Question: **Is the MSI B450M-A PRO MAX II a good choice if the goal is native ReBAR without ReBarUEFI?**

Answer: **Yes, but I would choose it over the MORTAR MAX only if it is significantly cheaper.** The important part is that this is a newer MSI B450 model and MSI's current BIOS supports the normal **Re-Size BAR** configuration. MSI documents the BIOS option as:

```text
Advanced
  └─ PCIe Sub-system Settings
       └─ Re-size BAR Support → Enabled
```

([MSI][1])

The board's official specs confirm it has a CPU-connected **PCIe 3.0 x16** slot and supports Ryzen 1000–5000 series CPUs. ([MSI][2])

### For your specific goal

I'd rank these two **by practicality**, not as an overall motherboard ranking:

|                    | B450M MORTAR MAX | B450M-A PRO MAX II |
| ------------------ | ---------------- | ------------------ |
| Native ReBAR       | ✅                | ✅                  |
| ReBarUEFI          | **Not needed**   | **Not needed**     |
| AM4                | ✅                | ✅                  |
| PCIe GPU slot      | Gen 3 x16        | Gen 3 x16          |
| M.2                | ✅                | ✅                  |
| RAM slots          | 4                | **2**              |
| LAN                | 1GbE             | **2.5GbE**         |
| VRM / board class  | Better           | More basic         |
| Used-market appeal | Better           | Cheaper/basic      |

One interesting point: the **A PRO MAX II has 2.5GbE**, whereas the older MORTAR MAX is generally a more substantial board in terms of expansion/VRM/features.

### The one thing I'd verify

The seller says:

> `支持AM4锐龙1-5代`

That's broadly consistent with MSI's official specification. ([MSI][2])

But **don't interpret that sentence as proof that the exact used board currently has the right BIOS**.

Ask:

```text
请拍一下 BIOS 版本号，以及
Advanced → PCIe Sub-system Settings
里面 Above 4G Decoding / Re-Size BAR Support 的页面。
```

You want:

```text
Above 4G Decoding       [Enabled]
Re-Size BAR Support     [Enabled]
```

MSI explicitly documents those ReBAR settings, and Intel likewise recommends UEFI mode with CSM disabled plus Above 4G Decoding and Re-Size BAR enabled. ([MSI][1])

**So yes: this B450M-A PRO MAX II is a legitimate candidate for your “no ReBarUEFI” build.** If you give me the **price of this one and the MORTAR MAX**, I can tell you which makes more sense purely from the hardware/price difference.

[1]: https://www.msi.com/Landing/msi-click-bios-intel-amd-motherboard?utm_source=chatgpt.com "MSI Click BIOS - One-click optimization for Intel / AMD motherboards, effortlessly and efficiently"
[2]: https://www.msi.com/Motherboard/B450M-A-PRO-MAX-II/Specification?utm_source=chatgpt.com "B450M-A PRO MAX II | Motherboard | MSI Global"