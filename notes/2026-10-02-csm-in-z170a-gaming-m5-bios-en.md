---
audio: false
generated: true
image: false
lang: en
layout: post
title: CSM in Z170A Gaming M5 BIOS
translated: false
type: note
---

Question: What is **CSM** in the Z170A Gaming M5 BIOS?

Answer: **CSM = Compatibility Support Module**. It is a UEFI firmware component that lets a modern UEFI motherboard behave like an old legacy BIOS.

Think of it as:

```text
UEFI BIOS
   │
   ├── CSM Disabled
   │      └── pure UEFI boot
   │
   └── CSM Enabled
          └── UEFI + legacy BIOS compatibility
```

For your **M40 / PCI resource problem**, CSM matters because it can change how the firmware initializes PCIe devices and allocates resources.

### On MSI Z170A Gaming M5

You'll generally find it around:

```text
Settings
  └── Advanced
       └── Windows OS Configuration
            └── Windows 10 WHQL Support
```

Depending on BIOS version, CSM may appear as:

```text
Boot
 └── Boot Mode Select
```

or indirectly through **Windows 10 WHQL Support**.

Typical combinations are:

```text
Windows 10 WHQL Support = Enabled
    → UEFI-oriented configuration
    → CSM effectively disabled

Windows 10 WHQL Support = Disabled
    → Legacy/UEFI compatibility available
    → CSM can be used
```

### For your M40 experiment

I'd test **CSM disabled first**:

```text
CSM             = Disabled
Above 4G Decode = Enabled
PCI_E1          = your M40
PCIe Speed      = Gen2
```

Then boot.

If that doesn't work, test the opposite:

```text
CSM             = Enabled
Above 4G Decode = Enabled
PCI_E1          = M40
PCIe Speed      = Gen2
```

The key point is that **CSM isn't a PCIe resource setting itself**. It changes the firmware's boot/device initialization environment. The setting I'd consider more directly relevant to your **“Insufficient PCI Resources”** error is **Above 4G Decoding**.

If you tell me your **exact M5 BIOS version**, I can map the actual MSI BIOS menu path and tell you exactly what to set.