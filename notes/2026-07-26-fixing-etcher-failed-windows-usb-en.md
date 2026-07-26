---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Etcher Failed Windows USB
translated: false
type: note
---

Question: Etcher is stuck while flashing Windows 11 ISO on Mac. How to recover and create the USB?

Answer:

Since you are flashing:

```text
Win11_25H2_English_x64_v2.iso
```

Etcher hanging is expected behavior sometimes because **Windows ISO is not a proper disk image for Etcher**. It may stay at:

* "Starting..."
* "Validating..."
* "Flash failed"
* "Preparing..."

Do not wait too long. Stop it.

---

## 1. Quit Etcher

Press:

```text
Cmd + Q
```

If it does not close:

```bash
killall balenaEtcher
```

or:

```bash
pkill -f balena
```

---

## 2. Reset the USB

Find your USB:

```bash
diskutil list
```

Example:

```text
/dev/disk2 (external, physical)
```

Unmount:

```bash
diskutil unmountDisk /dev/disk2
```

Erase:

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

Now the USB is clean.

---

## 3. Use the correct Windows USB creation method

For Windows ISO on Mac, use `wimlib`.

Install:

```bash
brew install wimlib
```

Mount ISO:

Double click:

```text
Win11_25H2_English_x64_v2.iso
```

Check:

```bash
ls /Volumes
```

You will see something like:

```text
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

## 4. Copy files

Assume USB is:

```text
/Volumes/WIN11
```

Copy:

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

If you get:

```text
File too large
install.wim
```

remove it:

```bash
rm /Volumes/WIN11/sources/install.wim
```

Then split:

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

---

## 5. Boot Lenovo Xiaoxin

Insert USB.

Power on:

```text
F12
```

Choose:

```text
UEFI USB
```

Windows installer should start.

---

## Why Etcher failed

Etcher expects:

```
disk image
 |
 +-- GPT
 +-- EFI partition
 +-- filesystem
```

Example:

```
Ubuntu.iso
      |
      +-- partition table
      +-- bootloader
```

Windows ISO:

```
Windows.iso
      |
      +-- DVD filesystem
      +-- setup files
      +-- install.wim
```

Different structure.

So for Windows:

```
Mac
 |
 | wimlib
 v
FAT32 GPT USB
 |
 v
Lenovo UEFI boot
 |
 v
Windows Setup
```

is the reliable path.
