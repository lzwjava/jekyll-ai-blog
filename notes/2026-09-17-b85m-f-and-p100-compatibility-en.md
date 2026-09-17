---
audio: false
generated: true
image: false
lang: en
layout: post
title: B85M-F and P100 Compatibility
translated: false
type: note
---

Question: Can the **ASUS B85M-F + i3-4170** run an NVIDIA Tesla P100 PCIe?

Answer: **Yes, very likely.** In fact, this is a reasonable cheap test platform for a P100.

* **CPU socket:** LGA1150; i3-4170 is compatible.
* **GPU slot:** B85M-F has **1 × PCIe x16 slot**, electrically x16. ASUS documents it as PCIe 3.0/2.0 x16 depending on platform/CPU. ([ASUS Download Center][1])
* **P100 interface:** Tesla P100 PCIe is **PCIe Gen3 x16**, so the interface matches. ([NVIDIA][2])
* **UEFI:** B85M-F uses an ASUS UEFI BIOS, while the P100's VBIOS supports UEFI. ([ASUS Download Center][3])
* **Power:** This is the important part. P100 PCIe is a **250 W passive card** and requires an **8-pin auxiliary power connector**. ([NVIDIA][2])
* **Cooling:** P100 is **passively cooled**, so don't run it bare on an open bench without strong airflow across the heatsink. NVIDIA explicitly specifies system airflow for thermal operation. ([NVIDIA Images][4])

### Compared with your ASUS A68HM-E problem

I'd actually prefer this **B85M-F + i3-4170** over the A68HM-E for your P100 testing.

Your previous `PCI OUT OF RESOURCES CONDITION` problem is the kind of BIOS/PCI resource-allocation issue where a newer Intel platform with a proper UEFI implementation is a better test candidate.

The B85M-F is also cheap:

> **55 RMB board + 12 RMB CPU = 67 RMB**

That's a pretty good P100 test platform.

### One caveat

The **P100 is not a display GPU**. If you connect a monitor to the motherboard's VGA/DVI, you'll use the i3-4170's Intel iGPU for display, while Linux/Windows can use the P100 as the CUDA device.

I'd configure it roughly:

```text
B85M-F
├── i3-4170
├── 8–16 GB DDR3
├── Intel iGPU → monitor
└── PCIe x16 → Tesla P100
                     └── 8-pin power
```

For your specific use—**P100 CUDA/LLM experimentation and GPU repair/testing**—I'd say **buyable at ¥67 if you can test it before taking it**. The bigger risk is not PCIe compatibility; it's the **250 W PSU + 8-pin power + airflow**.

Also, update the B85M-F to its latest BIOS (**2604**) if the seller can do it; ASUS lists 2604 as the latest BIOS for this board. ([ASUS Global][5])

References:

* [ASUS B85M-F manual](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?model=b85mf&utm_source=chatgpt.com)
* [NVIDIA Tesla P100 PCIe specifications](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com)
* [ASUS B85M-F BIOS support](https://www.asus.com/supportonly/b85m-f/helpdesk_bios/?utm_source=chatgpt.com)

[1]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?model=b85mf&utm_source=chatgpt.com "B85M-F
Motherboard"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "SPECIFICATIONS"
[3]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?utm_source=chatgpt.com "B85M-F specifications summary"
[4]: https://images.nvidia.com/content/grid/pdf/DA-09018-001_v10.pdf?utm_source=chatgpt.com "Tesla P100

The NVIDIA Tesla P100 GPU Accelerator"
[5]: https://www.asus.com/supportonly/b85m-f/helpdesk_bios/?utm_source=chatgpt.com "B85M-F - Support"