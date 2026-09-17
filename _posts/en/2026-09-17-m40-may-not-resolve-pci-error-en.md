---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 May Not Resolve PCI Error
translated: false
type: note
---

Question: **If I replace the P100 with a Tesla M40, will the PCI resource error disappear?**

Answer: **Much more likely, but not guaranteed.** The M40 is actually a reasonable card to try with the MSI PRO B760M-E, but there is an important catch: **the M40 also has a large BAR requirement**, so the motherboard still needs to allocate a large 64-bit PCIe MMIO region correctly.

### P100 vs M40

|              |    Tesla P100 | Tesla M40 24GB |
| ------------ | ------------: | -------------: |
| Architecture |        Pascal |        Maxwell |
| VRAM         | 12/16 GB HBM2 |    24 GB GDDR5 |
| PCIe         |      Gen3 x16 |       Gen3 x16 |
| Power        |         250 W |          250 W |
| Cooling      |       Passive |        Passive |
| Main concern | Large PCI BAR |  Large PCI BAR |

NVIDIA specifies the M40 as PCIe 3.0 x16, 250 W, passive, with 24 GB VRAM. ([NVIDIA Images][1])

The important part is that **M40 does not automatically mean "small PCI resource requirement."** There are real reports of M40 systems failing because BAR1 could not be assigned, including an M40 24GB on an ASUS Z97 system. ([NVIDIA Developer Forums][2])

So:

```text
A68HM-E + P100
       ↓
PCI resource error
       ↓
old BIOS / PCI MMIO allocation
```

Changing to:

```text
A68HM-E + M40
       ↓
might work
       ↓
but NOT something I'd rely on
```

Whereas:

```text
B760M-E + M40
       ↓
modern UEFI
       ↓
CPU PCIe 4.0 x16
       ↓
M40 PCIe 3.0 x16
       ↓
much better candidate
```

The B760M-E's primary PCIe slot is directly connected to the CPU and supports PCIe 4.0 x16. ([MSI][3])

### One big advantage of M40

If your goal is **cheap CUDA VRAM**, the M40 24GB is interesting.

But if you're choosing between your **P100 and M40**, don't assume M40 is newer/better:

```text
M40 = Maxwell, 2015
P100 = Pascal, 2016
```

The P100 is substantially newer architecturally. NVIDIA's data-center driver documentation still lists both M40 and P100 in the supported Tesla families of the 470 branch. ([NVIDIA Docs][4])

For ML workloads, **P100 is generally the more capable compute architecture**, particularly because Pascal adds features that Maxwell lacks.

### What I would do

If you **already own the M40**:

```text
MSI PRO B760M-E
        +
Tesla M40 24GB
        +
Intel i5-12400/13400
```

is worth trying.

If you **are buying a GPU specifically to put in the B760M-E**, I would **not buy the M40 just to avoid the PCI-resource error**. The motherboard/firmware is the more important variable.

In fact, there's a useful experiment:

```text
Current A68HM-E
       │
       ├── P100 → PCI resource error
       │
       └── M40 → test
```

If **both** produce the same error, you've basically proven that the A68 BIOS/platform is the problem.

Then:

```text
B760M-E
   │
   ├── P100
   └── M40
```

should be the next test.

### One correction from my previous answer

I also want to correct something important: **I would not use the existence of the P100's large BAR as proof that the B760M-E will fail or succeed.** Actual BAR allocation depends on the firmware's PCI resource map, CSM/UEFI configuration, other devices, and BIOS implementation. There are documented cases where even newer boards have Tesla BAR allocation problems. ([NVIDIA Developer Forums][5])

For the B760M-E, MSI explicitly documents **Above 4G Decoding as the mechanism for allowing 64-bit PCIe MMIO above the 4-GB address space**. ([MSI][6])

So if your priority is simply:

> **"I want the cheapest motherboard that boots my Tesla reliably."**

I'd take **B760M-E + M40** seriously, but I'd still prefer **B760M-E + P100** if you already own the P100.

**And make sure the M40 has proper auxiliary power and aggressive airflow** — it's a 250 W passive data-center card. ([NVIDIA Images][1])

References:

* [NVIDIA Tesla M40 datasheet](https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com)
* [MSI PRO B760M-E specifications](https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com)
* [MSI Above 4G Decoding explanation](https://us.msi.com/faq/2726?utm_source=chatgpt.com)

[1]: https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com "Data Sheet: Quadro M6000"
[2]: https://forums.developer.nvidia.com/t/this-pci-i-o-region-assigned-to-your-nvidia-device-is-invalid-above-4g-decoding-already-enabled/121633?utm_source=chatgpt.com "This PCI I/O region assigned to your NVIDIA device is invalid (Above 4G decoding already enabled) - Drivers - Linux, Windows, MacOS - NVIDIA Developer Forums"
[3]: https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com "PRO B760M-E"
[4]: https://docs.nvidia.com/datacenter/tesla/tesla-release-notes-470-103-01/index.html?utm_source=chatgpt.com "Version 470.103.01(Linux)/472.98(Windows) :: NVIDIA Data Center GPU Driver Documentation"
[5]: https://forums.developer.nvidia.com/t/tesla-p40-in-dell-percision-7910-rack/281034?utm_source=chatgpt.com "Tesla P40 in Dell Percision 7910 rack - CUDA Programming and Performance - NVIDIA Developer Forums"
[6]: https://us.msi.com/faq/2726?utm_source=chatgpt.com "MSI USA | MSI USA"
