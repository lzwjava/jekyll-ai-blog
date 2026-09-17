---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing PCI Resource Allocation Error
translated: false
type: note
---

Question: Your MSI Click BIOS reports **“PCI OUT OF RESOURCES CONDITION — Insufficient PCI Resources detected.”**

Answer: This is a **PCI/PCIe address-resource allocation problem during POST**, not a storage or RAM error.

The BIOS is telling you that it cannot allocate enough PCI resource space (typically MMIO/I/O address ranges) for all detected PCI/PCIe devices, so it has disabled some devices.

### First: get the machine to boot

From this screen:

1. Press **F10** / go to **Save & Exit**.
2. Choose **Boot Device** and select your OS disk, or choose **Discard Changes and Exit** if you haven't changed BIOS settings.
3. If Windows/Linux boots, the machine is usable, but one or more PCI devices may be missing.

### Then fix the underlying allocation

Go into BIOS and look under:

**Advanced → PCI Subsystem Settings**

Look for:

```text
Above 4G Decoding
```

If present, set:

```text
Above 4G Decoding = Enabled
```

This is particularly important if you have a modern/high-memory GPU or multiple PCIe cards. It allows PCIe MMIO resources to be mapped above the 4-GB physical address boundary.

Also check for:

```text
Re-Size BAR Support
```

If you're troubleshooting an older motherboard/GPU combination, temporarily set:

```text
Re-Size BAR = Disabled
```

Then test booting again.

### If it still happens

Physically reduce the PCIe device count.

For example, temporarily remove:

```text
PCIe NIC
PCIe NVMe adapter
PCIe USB card
sound card
capture card
second GPU
other PCI/PCIe expansion cards
```

Leave only:

```text
GPU
boot/storage devices
```

Boot successfully, then add cards back one at a time.

### Why this happens

PCIe devices don't just consume electrical lanes. During firmware initialization they request address regions such as:

```text
BAR0 ── MMIO
BAR1 ── MMIO
BAR2 ── I/O
...
```

A GPU can request very large MMIO regions. The firmware has to construct something roughly like:

```text
CPU physical address space
│
├── RAM
├── PCI MMIO
│   ├── GPU BARs
│   ├── NVMe BARs
│   ├── NIC BARs
│   └── other PCIe BARs
│
└── other firmware-reserved regions
```

If the firmware cannot find enough suitable address space, you get exactly the error in your photo.

### If you recently changed hardware

The most useful clue is **what changed immediately before this appeared**.

If you tell me your:

```text
CPU:
Motherboard model:
BIOS version:
GPU(s):
PCIe cards:
NVMe drives:
```

I can narrow this down to the specific BIOS setting/resource conflict rather than having you randomly disable devices.
