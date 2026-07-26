---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo Xiaoxin 14 SSD detection fix
translated: false
type: note
---

Question: **Does Lenovo Xiaoxin 14 have the Intel VMD/RST SSD detection issue during Windows 11 installation?**

Answer:

Yes, **Lenovo Xiaoxin 14 (小新 14)** is one of the models where this can happen, especially newer Intel CPU versions (12th/13th/14th gen). Your USB preparation is probably fine — the next thing to check is the **storage controller mode**.

Typical flow:

1. Boot USB in UEFI mode:

```
EFI/BOOT/BOOTX64.EFI
```

is correct ✅

2. Start Windows 11 installer.

3. At the disk selection page:

### Case A — SSD appears

```
Drive 0 Unallocated Space
```

Then continue normally.

### Case B — "We couldn't find any drives"

or only USB disk appears:

This is usually Intel VMD/RST.

You need Intel storage driver:

```
Intel Rapid Storage Technology (Intel RST)
F6 Driver
```

Extract it, put on another USB:

Example:

```
USB/
 └── f6vmdflpy-x64/
      ├── iaStorVD.inf
      ├── iaStorAC.inf
      └── drivers...
```

Windows setup:

```
Where do you want to install Windows?
        ↓
Load driver
        ↓
Browse USB
        ↓
Select iaStorVD.inf
```

Then SSD should appear.

---

For Lenovo Xiaoxin 14, also check BIOS:

Enter BIOS:

```
Power off
Press F2 repeatedly
```

Look for:

```
Configuration
  └── Storage Controller Mode
```

Possible options:

```
[AHCI]
[RAID / RST]
```

If available:

```
RAID/RST → AHCI
```

is easier because Windows has native NVMe driver.

However, some Lenovo consumer BIOS hides this option. Then F6 driver is the correct solution.

---

You can also verify before installing:

At Windows setup press:

```
Shift + F10
```

Then:

```cmd
diskpart

list disk
```

If you see:

```
Disk 0  512 GB
```

or

```
Disk 0  1 TB
```

SSD is detected.

If only:

```
Disk 1  USB
```

then it is definitely VMD/RST.

---

For your specific case:

* USB EFI: ✅ OK
* FAT32 + split install.wim: ✅ OK
* Lenovo Xiaoxin 14: likely VMD/RST issue if SSD missing
* No need to recreate USB

The next diagnostic step is simply: **boot the USB and tell me what appears at the "Where do you want to install Windows?" screen.**