---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Etcher Windows ISO Missing Partition Table
translated: false
type: note
---

Question: Why does balenaEtcher say “missing partition table” when flashing `Win11_25H2_English_x64_v2.iso` on Mac, and what should you do?

Answer:

This happens because **Windows ISO files are not hybrid boot images**.

Etcher is designed mainly for images like:

* Ubuntu ISO
* Debian ISO
* Raspberry Pi images

Those contain a partition table inside the image:

```
ISO
 |
 +-- GPT/MBR partition table
 |
 +-- EFI partition
 |
 +-- filesystem
```

Windows ISO is different:

```
Windows ISO
 |
 +-- boot files
 +-- sources/install.wim
 +-- setup.exe
```

It is an installation DVD image, not a raw disk image.

So Etcher sees:

```
No partition table found
```

and warns you.

---

## Can you continue and flash anyway?

You can click:

```
Continue
```

but for Windows installation USB, it is **not the recommended path**.

The result may be:

* USB appears in BIOS but does not boot
* Lenovo Xiaoxin says:

```
No bootable device
```

* UEFI cannot find Windows installer

---

## Better method on Mac: use `wimlib` (recommended)

For Windows 11 25H2 ISO:

```
Win11_25H2_English_x64_v2.iso
```

do this:

### 1. Install tools

```bash
brew install wimlib
```

---

### 2. Format USB

Find USB:

```bash
diskutil list
```

Example:

```
/dev/disk2
```

Erase:

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

---

### 3. Mount ISO

Double click:

```
Win11_25H2_English_x64_v2.iso
```

Example:

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

### 4. Copy files

Copy everything except `install.wim`:

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

Remove large file:

```bash
rm /Volumes/WIN11/sources/install.wim
```

---

### 5. Split install.wim

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

Result:

```
install.swm
install2.swm
install3.swm
```

---

Now USB structure:

```
USB
 |
 +-- EFI
 |
 +-- boot
 |
 +-- setup.exe
 |
 +-- sources
       |
       +-- install.swm
       +-- install2.swm
```

This is exactly what Windows Setup expects.

---

## Another easier GUI option

Use:

[Rufus official website](https://rufus.ie/?utm_source=chatgpt.com)

but Rufus only runs on Windows.

If you have access to your Ubuntu/MacBook running Windows VM, Rufus is probably the easiest.

---

For your setup:

```
MacBook Pro 2017
        |
        | create USB
        v
Lenovo Xiaoxin UEFI laptop
        |
        v
Windows 11 25H2
```

I would **not use Etcher for this ISO**. Use the `wimlib` method. It is the same approach Microsoft uses for UEFI Windows installation media.
