---
audio: false
generated: true
image: false
lang: en
layout: post
title: Create Windows USB on Mac
translated: false
type: note
---

Question: How to create a Windows installation USB on a Mac for installing Windows on Lenovo Xiaoxin?

Answer:

Since you only have a **MacBook** available, you can prepare the Windows USB using macOS tools. The easiest method is **not Media Creation Tool** (that is Windows-only), but download the ISO and write it to USB.

## Method 1 (recommended): Use `diskutil` + `wimlib` on macOS

### 1. Download Windows ISO

Download the official ISO:

* Windows 11 ISO:
  [Download Windows 11 Disk Image (ISO)](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)

* Windows 10 ISO:
  [Download Windows 10 Disc Image (ISO)](https://www.microsoft.com/software-download/windows10ISO?utm_source=chatgpt.com)

Choose:

* Windows 11 x64 ISO
* English or Chinese version depending on your preference

---

### 2. Prepare USB drive

Plug in your USB (16GB recommended).

Find the disk:

```bash
diskutil list
```

Example:

```
/dev/disk2 (external, physical)
```

Unmount it:

```bash
diskutil unmountDisk /dev/disk2
```

---

### 3. Install `wimlib`

Windows ISO contains a file:

```
sources/install.wim
```

which is often larger than 4GB.

FAT32 cannot store files >4GB, so we need to split it.

Install:

```bash
brew install wimlib
```

If you don't have Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### 4. Format USB as FAT32 GPT

Replace `disk2` with your USB:

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

Now mount the USB.

---

### 5. Mount Windows ISO

Double click the ISO.

macOS will mount it, for example:

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

### 6. Copy Windows files

Copy everything:

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

If it fails at:

```
install.wim too large
```

remove it:

```bash
rm /Volumes/WIN11/sources/install.wim
```

Then split it:

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

You will get:

```
install.swm
install2.swm
...
```

Windows installer understands this.

---

### 7. Eject USB

```bash
diskutil eject /dev/disk2
```

Now the USB is ready.

---

## Install on Lenovo Xiaoxin

1. Insert USB into Lenovo
2. Power on
3. Press:

```
F12
```

(or sometimes Fn+F12)

4. Select:

```
UEFI USB Device
```

5. Windows installer starts.

---

## Lenovo Xiaoxin BIOS settings

If USB does not boot:

Enter BIOS:

```
F2
```

Check:

```
Boot Mode:
UEFI

Secure Boot:
Disable
```

Then try again.

---

## Alternative easier GUI method

You can use:

* [balenaEtcher official website](https://etcher.balena.io?utm_source=chatgpt.com)

Steps:

1. Download ISO
2. Open Etcher
3. Select ISO
4. Select USB
5. Flash

However, for modern Windows 10/11 installation USB, the `wimlib` method is more reliable because it handles the 4GB `install.wim` issue.

For a Lenovo Xiaoxin (UEFI laptop), I would use **GPT + FAT32 + wimlib split**, which matches Microsoft's UEFI installation path.
