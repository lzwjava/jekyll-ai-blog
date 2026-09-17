---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar Three PCIe Slots
translated: false
type: note
---

Question: Does the MSI MAG B760M Mortar have two PCIe slots?

Answer: **Yes — actually it has 3 PCIe slots**:

| Slot       | Physical size | PCIe generation | Lanes  | Source       |
| ---------- | ------------- | --------------- | ------ | ------------ |
| **PCI_E1** | x16           | **PCIe 5.0**    | x16    | CPU          |
| **PCI_E2** | x1            | **PCIe 3.0**    | x1     | B760 chipset |
| **PCI_E3** | x16           | **PCIe 4.0**    | **x4** | B760 chipset |

MSI officially lists it as **2 × PCIe x16 + 1 × PCIe x1**. ([MSI][1])

So physically, you can do something like:

```text
CPU
 │
 ├── PCI_E1 ───────── x16 physical / PCIe 5.0
 │      └── GPU
 │
 ├── PCI_E2 ───────── x1 physical / PCIe 3.0
 │      └── NIC / USB card / etc.
 │
 └── PCI_E3 ───────── x16 physical / PCIe 4.0 x4 electrical
        └── second GPU / accelerator / HBA / etc.
```

**Important distinction:** the second long slot looks like x16, but electrically it is only **x4**. So if you're asking because you want to put **two GPUs / two AI accelerators** in it, the second device gets PCIe 4.0 ×4 bandwidth, not ×16. ([storage-asset.msi.com][2])

If you tell me what you want to put in the **second PCIe slot** (GPU, NIC, NVMe adapter, capture card, etc.), I can check the lane/bandwidth implications for that specific setup.

[1]: https://www.msi.com/Motherboard/MAG-B760M-MORTAR/Specification?utm_source=chatgpt.com "MAG B760M MORTAR"
[2]: https://storage-asset.msi.com/datasheet/mb/in/MAG-B760M-MORTAR.pdf?utm_source=chatgpt.com "MAG B760M MORTAR"
