---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Windows 10 on MacBook Pro 2017
translated: false
type: note
---

Question: **For a MacBook Pro 2017, how do I install Windows 10 from `/home/lzw/Downloads/Win10_22H2_English_x64v1.iso`?**

Answer:

For **MacBook Pro 2017 (Intel)**, the best method is **Boot Camp Assistant**, not manually creating a USB. Apple officially supports Windows 10 installation through Boot Camp on Intel Macs. ([Apple Support][1])

Your ISO:

```
/home/lzw/Downloads/Win10_22H2_English_x64v1.iso
```

is a Linux path. If this file is currently on your Ubuntu system, first copy it to the Mac.

Example:

```bash
scp Win10_22H2_English_x64v1.iso user@mac:/Users/user/Downloads/
```

Then on macOS:

## 1. Check ISO

Open Terminal:

```bash
ls -lh ~/Downloads/Win10_22H2_English_x64v1.iso
```

You should see a file around 5-6 GB.

## 2. Open Boot Camp Assistant

macOS:

```
Applications
 └── Utilities
      └── Boot Camp Assistant
```

Run:

```text
Continue
```

Select:

```
ISO Image:
~/Downloads/Win10_22H2_English_x64v1.iso
```

Boot Camp will:

1. Create BOOTCAMP partition
2. Download Apple Windows drivers
3. Start Windows installer

([Apple Support][1])

## 3. Partition size

For a 2017 MacBook Pro:

Minimum:

```
Windows: 64 GB
```

Recommended:

```
Windows: 100-150 GB
```

because Windows updates consume space.

## 4. Windows installer

When Windows setup appears:

Choose:

```
BOOTCAMP
```

partition.

Click:

```
Format
```

then:

```
Next
```

Do **not** delete EFI/APFS partitions.

## 5. Install Boot Camp drivers

After first Windows boot:

Run:

```
D:\BootCamp\Setup.exe
```

or wait for the automatic installer.

This installs:

* WiFi
* Trackpad
* Keyboard
* AMD/NVIDIA graphics
* Thunderbolt
* Apple keyboard shortcuts

([Apple Support][1])

---

### If your MacBook Pro 2017 currently only has Ubuntu

Since you mentioned before that your MacBook Pro 2017 is running Ubuntu and the Linux kernel experiment broke boot, you have two choices:

### Option A (recommended): reinstall macOS first

Boot:

```
Command + R
```

Internet Recovery:

```
Disk Utility
→ erase SSD as APFS
→ reinstall macOS
```

Then use Boot Camp.

### Option B: install Windows directly

Possible, but harder:

* create GPT/UEFI Windows USB
* manually install Apple Boot Camp drivers
* fix keyboard/trackpad/WiFi

For a 2017 MacBook Pro, Boot Camp is much smoother. ([Apple Support][1])

---

Your flow should be:

```
Ubuntu
  |
  | copy ISO
  v
macOS Recovery
  |
  v
macOS
  |
  v
Boot Camp Assistant
  |
  v
Windows 10 22H2
```

This is also a good diagnostic: if Windows 10 installs successfully, your Mac hardware (SSD/RAM/UEFI) is likely fine.

[1]: https://support.apple.com/en-ke/guide/bootcamp-assistant/-bcmp173b3bf2/mac?utm_source=chatgpt.com "Install Windows on your newer Mac using Boot Camp - Apple Support (KE)"
