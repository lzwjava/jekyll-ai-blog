---
audio: false
generated: true
image: false
lang: en
layout: post
title: JGINYUE B85M-VDH Tesla P100 Test Platform
translated: false
type: note
---

Question: Can the **JGINYUE B85M-VDH** run an NVIDIA Tesla P100 PCIe?

Answer: **Yes, electrically/PCIe-wise it should work**, and this is actually a reasonable cheap test platform for your P100.

* **Motherboard:** B85M-VDH has **1 × PCIe x16 slot**. ([jginyue][1])
* **P100:** Tesla P100 PCIe uses **PCIe 3.0 ×16**, so the interface matches directly. ([NVIDIA][2])
* **CPU:** An i5-4590 / i3-4130 / Xeon E3-1231 v3 is sufficient to boot and enumerate the P100. The P100 does not require a special Xeon motherboard.
* **RAM:** DDR3 1333/1600; this board officially supports up to 16 GB. ([jginyue][1])
* **Power:** This is the important part. P100 PCIe is a **250 W card** and requires an **8-pin auxiliary power connector**. NVIDIA specifies up to 240 W through that auxiliary connector plus 66 W through PCIe. ([NVIDIA][2])
* **Cooling:** P100 PCIe is **passively cooled**, so you need strong airflow across the heatsink. NVIDIA explicitly specifies system airflow for the passive card. ([NVIDIA Images][3])

### For your P100 testing setup

I'd configure it roughly like:

```text
B85M-VDH
├── Xeon E3-1231 v3 / i5-4590
├── 16 GB DDR3
├── Tesla P100 PCIe 12/16 GB
│   └── 8-pin EPS/CPU power
├── SATA SSD
└── 600–750 W PSU
```

One caveat: **don't confuse the P100 PCIe with the P100 SXM2**. You want the PCIe version. The PCIe version is a full-height, dual-slot PCIe card; SXM2 is a completely different module. ([NVIDIA Images][3])

For your particular use—**cheap GPU repair/test bench**—I'd actually consider this B85M-VDH a better choice than the ASUS A68HM-E you were testing earlier, because the platform is Intel + PCIe 3.0 and the B85 board has a straightforward x16 slot.

I can also compare **B85M-VDH vs B150M vs B250M vs X99** specifically as a P100 test bench, including PCI resource/BIOS risk.

[1]: https://jginyue.com.cn/index/Article/show/cat_id/41/id/92?utm_source=chatgpt.com "精粤B85M-VDH主板 - Intel LGA1150 - 精粤JGINYUE官网"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
[3]: https://images.nvidia.com/content/grid/pdf/DA-09018-001_v07.pdf?utm_source=chatgpt.com "Tesla P100

The NVIDIA Tesla P100 GPU Accelerator"