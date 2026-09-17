---
audio: false
generated: true
image: false
lang: en
layout: post
title: SOYO B85N Run Tesla P100?
translated: false
type: note
---

Question: Can the **SOYO SY-B85N + i5-4460 + 4GB DDR3** run a Tesla P100?

Answer: **Yes, this is also a good candidate.** The basic platform is compatible with a PCIe Tesla P100.

```text
SOYO SY-B85N
├── i5-4460
├── DDR3 4GB
└── PCIe x16
      └── Tesla P100
```

Key points:

| Component                    | Compatibility                         |
| ---------------------------- | ------------------------------------- |
| i5-4460                      | ✅ LGA1150                             |
| DDR3                         | ✅                                     |
| Tesla P100 PCIe              | ✅ PCIe x16                            |
| UEFI/PCI resource allocation | ⚠️ Need to test                       |
| P100 display output          | ❌ P100 is compute/passive             |
| Power                        | ⚠️ P100 needs ~250W + auxiliary power |
| Cooling                      | ⚠️ Must provide strong airflow        |

### Compared with the ASUS B85M-F

For your specific **P100 testing**, I'd put them roughly like this:

**ASUS B85M-F + i3-4170**

* More established ASUS BIOS
* 8–16 GB DDR3 possible
* Cheap: ~¥67 based on the listing
* **My preference for troubleshooting PCIe/BIOS issues**

**SOYO SY-B85N + i5-4460 + 4GB**

* More CPU performance
* Comes with RAM
* B85 + Haswell is exactly the right generation
* 4 GB is enough for basic P100 detection/testing, but I'd eventually use 8–16 GB
* **Also perfectly reasonable**

The important thing is that **i5 vs i3 doesn't matter much for whether the P100 works**. The critical things are:

```text
PCIe x16 slot
       ↓
BIOS can enumerate P100
       ↓
Enough PCIe MMIO resources
       ↓
PSU provides P100 power
       ↓
Good airflow
       ↓
nvidia-smi / CUDA sees P100
```

Since you're specifically trying to get around the **`PCI OUT OF RESOURCES CONDITION`** you've been seeing on the A68HM-E, I'd favor the **ASUS B85M-F** if the prices are similar, mainly because ASUS's BIOS/UEFI is a safer variable to eliminate.

If the SOYO is **significantly cheaper and you can test it with your P100 in Guangzhou**, though, it's worth trying.
