---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing ASUS A68HM-E Tesla P100
translated: false
type: note
---

Question: **ASUS A68HM-E + NVIDIA Tesla P100 is showing “PCI OUT OF RESOURCES.”**

Answer: **Yes — the Tesla P100 is very likely the reason.** The key detail is that the P100 is a compute accelerator with a **very large PCIe BAR requirement**.

NVIDIA's P100 PCIe specification says:

```text
BAR0 = 16 MB
BAR1 = 16 GB   <-- Compute mode
BAR3 = 32 MB
```

So the P100 can request roughly a **16-GB PCIe MMIO address window** in compute mode. ([NVIDIA Images][1])

Your **A68HM-E is an old AMD FM2+ motherboard**, and its BIOS/resource allocation is much older than the P100. ASUS still provides the original A68HM-E manual/BIOS support here. ([ASUS Global][2])

### What I would try

Enter BIOS → **Advanced** and look for PCI/PCIe settings.

The most important setting is:

```text
Above 4G Decoding
        ↓
      Enabled
```

If your A68HM-E BIOS **does not have Above 4G Decoding**, that's significant. Modern firmware uses this mechanism to put 64-bit PCIe MMIO resources above the 4-GB address space. ([ASUS Download Center][3])

Then:

```text
CSM              → Disabled   (if available)
UEFI Boot        → Enabled
Above 4G Decoding → Enabled
```

Save and reboot.

### But there is an important catch

The **A68HM-E may simply be too old to properly allocate the P100's BAR requirements**.

The P100 isn't an ordinary GeForce card:

```text
Tesla P100
    │
    ├── PCIe Gen3 x16
    ├── 12/16 GB HBM2
    ├── 250 W
    └── BAR1 = 16 GB in Compute mode
```

NVIDIA specifies the PCIe P100 as a **250-W, PCIe Gen3 accelerator**, designed for server/HPC systems. ([NVIDIA][4])

So this combination:

```text
AMD A68 / 2014-era consumer motherboard
              +
Tesla P100 / 2016-era data-center GPU
```

is exactly the sort of combination where firmware PCI-resource allocation can become the limiting factor.

### One thing I'd check immediately

If you can get into Windows/Linux despite the warning, run:

```bash
lspci -vv
```

and find the P100:

```bash
lspci -vv | grep -A30 -i nvidia
```

The important part is the `Memory at ...` / `size=` BAR information.

If Linux says something like:

```text
BAR 1: no space
BAR 1: failed to assign
```

then we've confirmed this is a **firmware PCI BAR allocation problem**, rather than a defective P100.

### Also check power

The P100 PCIe is rated at **250 W**. ([NVIDIA][4])

If you're using the common passive P100, make sure you have:

```text
proper PCIe auxiliary power
+
a PSU capable of supplying the card
+
substantial airflow across the passive heatsink
```

The power issue would normally cause a different failure, though — **the specific BIOS message in your photo points first to PCI resource allocation**.

If you send me **a photo of the A68HM-E BIOS → Advanced menu**, I can tell you exactly which settings to change.

[1]: https://images.nvidia.com/content/pdf/tesla/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
[2]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"
[3]: https://dlcdnets.asus.com/pub/ASUS/server/RS720-E10/Manual/E18516_RS720-E10-RS12_UM_WEB.pdf?utm_source=chatgpt.com "Possible: [Use Automatic Settings]"
[4]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-p100/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P100"
