---
audio: false
generated: true
image: false
lang: en
layout: post
title: B760M-E for a Single P100
translated: false
type: note
---

Question: **Will the MSI PRO B760M-E work well with the NVIDIA Tesla P100?**

Answer: **Yes. I would choose the B760M-E over the old A68HM-E for this P100 build.** The important part is that the B760M-E gives the P100 a modern CPU-connected **PCIe 4.0 x16 slot** and has a much newer UEFI/PCIe platform. MSI specifies the main slot as PCIe 4.0 x16 directly from the CPU. ([MSI][1])

### [MSI PRO B760M-E](https://www.newegg.com/msi-motherboards-intel/p/1JW-001M-00GY8?item=9SIC3DRKN71786&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$100.88*

### For your P100, I'd configure it like this

```text
CPU:       Intel 12th/13th/14th gen
GPU:       Tesla P100 PCIe
Slot:      CPU PCIe x16
PCIe Gen:  Gen3 initially
CSM:       Disabled
UEFI:      Enabled
```

The P100 is a **PCIe Gen3 x16** device, so running it in the B760's Gen4 x16 slot is backward-compatible; you can also explicitly force Gen3 if you encounter POST/resource issues.

### One correction to my previous answer

I would **not blindly enable Above 4G Decoding** for the P100.

MSI has an old but explicit Tesla/GRID FAQ saying that for its Tesla/GRID configurations, **Above 4G Decoding should be disabled** because it can prevent normal display. ([MSI Canada][2])

So for a **Tesla P100 specifically**, I'd start with:

```text
Above 4G Decoding = Disabled
```

If the B760M-E still reports PCI resource exhaustion, then we can experiment with it rather than assuming it should be enabled.

### The B760M-E's limitation

The board is quite barebones:

```text
B760M-E
├── 1 × PCIe 4.0 x16   ← P100
├── 1 × PCIe 3.0 x1
├── 1 × M.2
└── 4 × SATA
```

MSI confirms there is only **one x16 slot** and one x1 slot. ([MSI][1])

For **one P100**, that's perfectly fine.

If you're planning something like:

```text
P100 × 2
P100 × 4
P100 + 10GbE NIC
P100 + multiple NVMe adapters
```

then I would **not** use the B760M-E. You'd want a board with substantially more physical PCIe slots and better lane topology.

### DDR4 vs DDR5

There are actually two versions:

**B760M-E DDR5**

```text
2 × DDR5
max 128 GB
```

([MSI][1])

**B760M-E DDR4**

```text
2 × DDR4
max 64 GB
```

([MSI][3])

For a P100 compute box, **I'd get the DDR5 version if you're buying RAM anyway**. But if you already have 32/64 GB DDR4, the DDR4 version is perfectly reasonable.

### One important thing: CPU

Don't put an expensive i9 in this board just because the socket supports it. For a single P100 compute machine, something like:

```text
i5-12400
i5-13400
i5-13500
```

is much more sensible.

The GPU will do the actual CUDA work; you mainly need the CPU for feeding it, storage/network I/O, compilation, and orchestration.

**So: B760M-E + i5 + P100 = sensible cheap compute box.**

And compared with your current A68HM-E, the architectural difference is substantial:

```text
A68HM-E
   ↓
old FM2+ platform
   ↓
PCI resource allocation problem
   ↓
P100 ❌

B760M-E
   ↓
modern LGA1700 / B760 UEFI
   ↓
CPU PCIe 4.0 x16
   ↓
P100 PCIe Gen3 x16
   ↓
P100 ✅
```

I'd be comfortable trying the **B760M-E** for a **single P100**. ([MSI][1])

If you tell me **which CPU and RAM you currently have**, I can give you the cheapest exact CPU + motherboard + RAM combination without buying unnecessary parts.

References:

* [MSI PRO B760M-E specifications](https://www.msi.com/Motherboard/PRO-B760M-E/Specification) ([MSI][1])
* [MSI: Tesla/GRID and Above 4G Decoding](https://ca.msi.com/faq/2736) ([MSI Canada][2])

[1]: https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com "PRO B760M-E"
[2]: https://ca.msi.com/faq/2736?utm_source=chatgpt.com "MSI Canada | MSI Canada"
[3]: https://www.msi.com/Motherboard/PRO-B760M-E-DDR4/Specification?utm_source=chatgpt.com "PRO B760M-E DDR4"
