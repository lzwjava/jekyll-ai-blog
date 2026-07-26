---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wimlib SWM Windows 11 USB Safe
translated: false
type: note
---

Question: **Is it safe to flash Windows 11 USB using the wimlib split `.swm` method on Mac?**

Answer: **Yes, it is safe.** This is actually one of the cleanest ways to create a Windows 11 installation USB from macOS.

The important point: you are **not modifying Windows itself**. You are only changing the USB layout:

Original ISO:

```
sources/
 └── install.wim  (7.1GB)
```

FAT32 limitation:

```
max single file size = 4GB
```

So wimlib converts:

```
install.wim
      |
      v
install.swm
install2.swm
```

Example:

```
sources/
 ├── boot.wim
 ├── install.swm
 └── install2.swm
```

Windows Setup understands this format natively.

During installation:

```
USB
 |
 |  read install.swm chunks
 |
 v
Windows Setup
 |
 v
expand image
 |
 v
C:\Windows
```

No performance difference. No activation issue. No driver difference.

---

For Lenovo Xiaoxin, this is actually preferable because:

1. **UEFI boot compatibility**

You create:

```
GPT partition table
+
FAT32 filesystem
+
EFI boot files
```

which matches modern Lenovo firmware.

2. **Avoids NTFS boot hacks**

Some tools create:

```
NTFS USB
+
UEFI:NTFS loader
```

Rufus can do this, but some laptops have firmware quirks. FAT32 is the most universal.

3. **Works with Microsoft's own installer**

Microsoft itself supports split WIM files (`.swm`) for deployment scenarios.

---

Before reinstalling, I would check one thing:

Enter Lenovo BIOS:

Usually:

```
Power off
↓
Press F2 repeatedly
↓
BIOS Setup
```

Look for:

```
Configuration
    Intel VMD Controller
        Enabled
```

Change:

```
Intel VMD Controller = Disabled
```

or:

```
SATA Mode
    AHCI
```

Save:

```
F10
```

Then boot USB:

```
F12
→ UEFI USB
```

---

Your error:

```
0xC19001F4
```

is more suspicious for storage/controller/upgrade-state issues than the USB creation method.

The diagnostic logic:

| Test                                  | Result                           | Meaning               |
| ------------------------------------- | -------------------------------- | --------------------- |
| New FAT32 + wimlib USB                | install works                    | old USB/image problem |
| New USB still fails                   | BIOS/storage issue               |                       |
| Disable VMD fixes it                  | Intel RST driver issue           |                       |
| Windows 10 works but Windows 11 fails | Win11 compatibility/driver issue |                       |

So yes, proceed with the wimlib flash. It is a good next step. I would **not use Etcher for this ISO**.
