---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Install on Lenovo Xiaoxin
translated: false
type: note
---

Question: How to install Windows on a Lenovo Xiaoxin laptop?

Answer:

For a Lenovo Xiaoxin (小新) laptop, the usual way is to create a Windows USB installer and boot from it. The process is the same as most modern Lenovo laptops.

## 1. Prepare a Windows installation USB

You need:

* USB flash drive: **8GB+** (16GB recommended)
* Another working computer
* Windows 11/10 ISO or Microsoft Media Creation Tool

Official download:

* [Download Windows 11](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)
* [Download Windows 10](https://www.microsoft.com/software-download/windows10?utm_source=chatgpt.com)

On another PC:

### Option A: Microsoft Media Creation Tool

1. Plug in USB drive
2. Run Media Creation Tool
3. Select:

   ```
   Create installation media
   → USB flash drive
   → Select your USB
   ```

4. Wait until it finishes.

### Option B: Rufus + ISO

Download Rufus:

[Rufus USB installer tool](https://rufus.ie?utm_source=chatgpt.com)

Settings:

```
Device: your USB
Boot selection: Windows ISO

Partition scheme:
GPT

Target system:
UEFI

File system:
NTFS
```

Click Start.

---

## 2. Enter Lenovo Xiaoxin boot menu

Power off the laptop.

Common Lenovo keys:

* **F12** → Boot menu
* **Fn + F12** → sometimes needed
* **F2** → BIOS setup
* **Novo button** → Lenovo recovery/boot menu

For Xiaoxin, the Novo button is often:

* a small pin hole near the power button
* press with a paper clip when powered off

Menu:

```
Novo Button Menu

Normal Startup
BIOS Setup
Boot Menu
System Recovery
```

Choose:

```
Boot Menu
→ USB HDD
```

---

## 3. Install Windows

Windows installer starts.

Choose:

```
Language
Keyboard
Install Now
```

When asked for product key:

If the laptop originally had Windows:

```
I don't have a product key
```

Windows usually activates automatically later because the key is stored in firmware (OEM).

---

## 4. Disk partition

For a clean install:

At:

```
Where do you want to install Windows?
```

You will see:

```
Drive 0 Partition 1
Drive 0 Partition 2
...
```

If you want a full reinstall:

Delete all partitions:

```
Delete → Drive 0
```

Then:

```
Drive 0 Unallocated Space
→ Next
```

Windows creates:

```
EFI System Partition
MSR
Windows Partition
Recovery Partition
```

For dual boot, do not delete existing partitions.

---

## 5. After Windows boots

Install Lenovo drivers:

[Lenovo Support Drivers](https://pcsupport.lenovo.com?utm_source=chatgpt.com)

Install:

* Chipset driver
* Intel/AMD graphics driver
* WiFi/Bluetooth driver
* Touchpad driver
* Lenovo Vantage

You can also run:

```powershell
winget upgrade --all
```

---

## Common Xiaoxin issues

### USB not detected

Enter BIOS:

```
F2
```

Check:

```
Boot Mode:
UEFI

USB Boot:
Enabled
```

Some models have:

```
Secure Boot → Disable temporarily
```

---

### SSD not visible during installation

Recent Lenovo laptops often use Intel VMD/RST.

Symptom:

```
No drives found
```

Fix:

BIOS:

```
Configuration
→ Intel VMD Controller
→ Disable
```

or load Intel storage driver during installation.

---

### Chinese Windows → English Windows

You can install English Windows directly. After installation:

```
Settings
→ Time & Language
→ Language
→ Add English
```

---

For most Lenovo Xiaoxin models (Air/Pro/14/15/16), the fastest path is:

```
Create Windows 11 GPT USB
        ↓
Press Novo button
        ↓
Boot USB
        ↓
Delete old partitions
        ↓
Install Windows
        ↓
Install Lenovo drivers
```

If you tell me the exact model (for example **Xiaoxin Pro 14 2022 / 2023 / 2024, Intel or AMD**), I can give the exact BIOS keys and driver steps.
