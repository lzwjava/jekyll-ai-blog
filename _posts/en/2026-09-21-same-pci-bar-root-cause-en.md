---
audio: false
generated: true
image: false
lang: en
layout: post
title: Same PCI BAR Root Cause
translated: false
type: note
---

**Question:** Is the PCI error shown in the photo the same root cause as described in the blog post about M40 and PCI resource errors?

**Answer:**

Yes, they are essentially the **same root cause** — but with a slightly different context:

| | Your Photo (MODS error) | Blog Post (M40/P100 article) |
|---|---|---|
| **Error** | `BAR1 offset 0x0, size 0x0` / PCI device not found | PCI resource / BAR allocation failure |
| **Root Cause** | BIOS cannot assign BAR to GPU | BIOS cannot assign large 64-bit PCIe MMIO region |
| **Platform** | Old Lenovo, i5-4460, SBIOS 2016 | A68HM-E (old) vs B760M-E (newer) |
| **GPU** | No/undetected GPU | Tesla P100 / M40 |

Both failures trace back to the **same fundamental problem:**

> The motherboard BIOS/UEFI **fails to properly allocate PCI BAR (Base Address Register)** for the GPU — resulting in `BAR1 = size 0x0` and the GPU becoming invisible on the PCI bus.

The blog article discusses exactly this: even switching from a P100 to an M40 may **not** resolve the error, because the M40 also has a large BAR requirement — the real fix is the **motherboard/firmware**, specifically enabling **Above 4G Decoding** in a modern UEFI BIOS.

Your system (SBIOS date `12/09/2016`) is an even older platform, making it very likely the same BIOS limitation — the system simply cannot allocate the large 64-bit MMIO window a data-center GPU needs.

**References:**
- [M40 May Not Resolve PCI Error — lzwjava.com](https://lzwjava.com/m40-may-not-resolve-pci-error-en)
- [MSI Above 4G Decoding FAQ](https://us.msi.com/faq/2726)
- [NVIDIA Developer Forums — BAR allocation issues](https://forums.developer.nvidia.com/t/this-pci-i-o-region-assigned-to-your-nvidia-device-is-invalid-above-4g-decoding-already-enabled/121633)
