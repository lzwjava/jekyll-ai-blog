---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PCIe Slot Differences: x16 vs x1"
translated: false
type: note
---

Question: What is the difference between PCIEX_1 and PCIEX16?

Answer:

These labels appear on motherboards and refer to PCIe (PCI Express) slots, but they differ in **lane count** and **intended use**:

| Feature | PCIEX16 | PCIEX1 |
| --- | --- | --- |
| Lane count | 16 lanes | 1 lane |
| Bandwidth (PCIe 4.0) | ~32 GB/s | ~2 GB/s |
| Physical slot size | Long | Short |
| Primary use | Discrete GPU | Sound cards, Wi-Fi cards, capture cards, etc. |
| Backward compatible | Yes (can accept x1 cards) | Yes (but only x1 throughput) |

**Key points:**

- **PCIEX16** is the full-bandwidth slot designed for graphics cards. It has 16 data lanes for maximum throughput.
- **PCIEX1** (sometimes labeled PCIEX_1) has only 1 data lane, offering much lower bandwidth. It's used for expansion cards that don't need high speed — like network adapters, USB expansion cards, or audio cards.
- A card physically fits in any slot that is long enough, but it will only run at the speed of the slot's actual lane count.
- On many motherboards, a second "x16 physical" slot may actually run at x4 or x1 electrically — always check your motherboard manual for the actual wired lanes.

References:

- [PCIe Lanes Explained – What Are They and How Many Do You Need?](https://www.cgdirector.com/pcie-lanes-explained/)
- [PCI Express – Wikipedia](https://en.wikipedia.org/wiki/PCI_Express)
