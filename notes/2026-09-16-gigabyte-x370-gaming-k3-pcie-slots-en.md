---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gigabyte X370 Gaming K3 PCIe Slots
translated: false
type: note
---

Question: Does the Gigabyte X370 Gaming K3 have two PCIe slots suitable for two cards?

Answer: **Yes.** The **GA-AX370-Gaming K3** has:

* **1 × PCIe x16** — electrically **x16**, PCIe 3.0
* **1 × PCIe x16-length slot** — electrically **x4**, PCIe 2.0
* **3 × PCIe x1** slots ([GIGABYTE][1])

So if by “two PCIe slots” you mean **two full-length slots for GPUs / accelerator cards**, yes:

```text
GPU / card 1 → PCIe x16  (x16)
GPU / card 2 → PCIe x16  (x4)
```

But **it is not x8/x8**. The second slot is only **x4**, and its bandwidth can drop to **x2** if the relevant x1 slots are populated. ([GIGABYTE][1])

If you're asking because you want to put **two GPUs / AI cards** in it, tell me the two card models and I can check whether this board will actually work well for that setup. I can also check the seller's claim that the BIOS supports Ryzen 1–5 generations.

[1]: https://www.gigabyte.com/Motherboard/GA-AX370-Gaming-K3-rev-10/sp?utm_source=chatgpt.com "GA-AX370-Gaming K3 (Rev. 1.0) Motherboard - GIGABYTE Global"
