---
audio: false
generated: true
image: false
lang: en
layout: post
title: Z170 PCI Resource Allocation Problem
translated: false
type: note
---

Question: Why does the MSI Z170A Gaming M5 show **“PCI Insufficient PCI Resources Detected”**?

Answer: This is usually a **PCIe resource-allocation problem**, not necessarily a dead motherboard/GPU.

On a Z170 system, the BIOS/firmware has to allocate **MMIO address space, I/O space, bus numbers, and PCIe BAR regions** to every PCI/PCIe device. If the firmware cannot assign enough address space, you can get:

```text
PCI OUT OF RESOURCES
Insufficient PCI Resources Detected
```

This is especially common when you're trying to boot an older Z170 platform with a **large-VRAM GPU such as Tesla M40/P100** or multiple PCIe devices.

### The important distinction

There are several different resources:

```text
CPU
 │
 ├── PCIe x16 ── GPU
 │                ├── BAR0
 │                ├── BAR1 / framebuffer BAR
 │                └── other BARs
 │
 ├── chipset ── NVMe
 │           ── SATA
 │           ── USB
 │           ── LAN
 │           ── audio
 │           └── PCIe slots
 │
 └── firmware allocates MMIO / I/O / bus numbers
```

A GPU can have **24 GB VRAM** while the CPU does *not* need to map 24 GB of address space directly. But the GPU still exposes PCIe BARs, and depending on the GPU/firmware configuration, those BAR requirements can become difficult for an old BIOS to allocate.

### For your Z170A Gaming M5, I'd check these first

Enter BIOS and look for:

```text
Settings
 └── Advanced
      └── PCI Subsystem Settings
```

Look for:

```text
Above 4G Memory / Crypto Currency mining
Above 4G Decoding
```

If available:

```text
Above 4G Decoding = Enabled
```

Also try:

```text
PCI_E1 Max Link Speed = Gen2
```

or even:

```text
Gen1
```

as a diagnostic.

Don't confuse **link speed** with **resource allocation**: Gen1/Gen2 changes the PCIe negotiation, while Above 4G changes how PCIe MMIO can be allocated.

### Also test with the minimum PCIe configuration

For example:

```text
Z170A Gaming M5
    │
    ├── CPU
    ├── 1 DIMM
    ├── iGPU / motherboard display
    └── M40/P100 in PCI_E1
```

Remove:

* NVMe temporarily
* other PCIe cards
* unnecessary USB devices
* second GPU
* PCIe Wi-Fi/network cards

Then boot.

If the error disappears, add devices back one at a time.

### One particularly interesting Z170 issue

Z170 has only a finite number of CPU PCIe lanes:

```text
CPU
 └── 16 PCIe 3.0 lanes
       ├── x16
       ├── x8 + x8
       └── x8 + x4 + x4   depending on motherboard implementation
```

The chipset provides additional PCIe lanes, but those go through the **DMI link** to the CPU.

So if you're using something unusual like:

```text
M40 24GB
+
NVMe
+
another PCIe card
+
old GPU
```

you're stressing the motherboard firmware's PCIe enumeration/resource allocation much more than a normal Z170 gaming configuration.

### The fastest diagnostic

I'd do this exact sequence:

```text
1. Load Optimized Defaults
2. Disable CSM
3. Enable Above 4G Decoding, if present
4. Disable ReBAR
5. Put M40/P100 in the primary CPU x16 slot
6. Remove NVMe and all other PCIe devices
7. Boot using motherboard/iGPU display if possible
8. Try PCIe Gen2
9. If still failing → try Gen1
10. Test the GPU in another machine
```

If **Gen1/Gen2 makes no difference but removing another PCIe device fixes it**, that's strong evidence for a resource-allocation problem.

If **the same GPU fails on multiple machines with the same PCI resource error**, then I'd start investigating the GPU's PCIe configuration/firmware or hardware rather than the Z170 board.

For your particular case, if you're testing the **M40 24 GB**, I'd pay special attention to **Above 4G Decoding + CSM + BAR allocation**, because the M40 is old enough that modern firmware settings and old NVIDIA firmware behavior can interact badly.

I can also map the **Z170A Gaming M5 BIOS settings one-by-one for an M40/P100 boot configuration** and give you the exact settings to try.
