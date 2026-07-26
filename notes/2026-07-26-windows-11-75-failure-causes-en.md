---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 75% Failure Causes
translated: false
type: note
---

Question: **If Windows 11 installation reaches 75% and then fails, could Pro vs Home be the reason?**

Answer: **No. If it reaches 75%, Windows edition selection is definitely not the cause.**

At ~75%, Windows Setup has already passed:

```
USB boot
→ WinPE loading
→ SSD detection
→ partition creation
→ install.wim extraction
→ file copy
→ applying Windows image
```

The failure is usually during:

```
Applying image
→ configuring drivers
→ installing devices
→ first reboot preparation
→ Windows OOBE setup
```

For a Lenovo Xiaoxin, the likely causes are:

## 1. Storage driver / Intel VMD-RST issue (still possible)

Even if Setup sees the SSD, Windows may fail later when switching from WinPE drivers to the installed system.

Try:

BIOS:

```
Intel VMD Controller → Disabled
Storage Mode → AHCI
```

Then reinstall.

---

## 2. Bad USB media / ISO corruption

At 75%, Windows is reading and expanding many files. A corrupted ISO or USB flash drive often fails here.

Verify ISO:

```bash
sha256sum Win11_25H2_English_x64_v2.iso
```

Compare with Microsoft's SHA256 if available.

Or recreate USB using Ventoy:

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdX
```

Then just copy:

```
Win11_25H2_English_x64_v2.iso
```

to the USB.

---

## 3. SSD problem

Since you previously saw:

```
Disk 0 512 GB
```

the SSD is detected, but write failures can happen.

From Windows installer:

```
Shift + F10
```

Run:

```cmd
diskpart

select disk 0

clean

create partition primary

format fs=ntfs quick

exit
```

Then try again.

---

## 4. RAM instability

Windows installation is surprisingly sensitive to bad RAM.

If it always fails at approximately the same percentage:

* 70–80% → often storage/USB
* random percentages → often RAM

Run:

```
memtest86+
```

if possible.

---

The useful clue is **the exact error message after 75%**.

Can you take a photo of the failure screen? Especially if it says something like:

* `Windows cannot install required files`
* `0x8007025D`
* `0x80070002`
* `0xC1900101`
* `The installation failed in the SAFE_OS phase`

The error code will narrow it down immediately.
