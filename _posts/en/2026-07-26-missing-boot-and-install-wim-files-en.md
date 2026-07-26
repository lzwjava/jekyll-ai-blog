---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing Boot and Install WIM Files
translated: false
type: note
---

Question: USB does not contain `boot.wim` and `install.wim` — what does it mean?

Answer:

This is a **very important clue**.

A normal Windows 11 installation USB must have:

```
\sources\boot.wim
\sources\install.wim
```

or:

```
\sources\boot.wim
\sources\install.swm
\sources\install2.swm
```

`boot.wim` is required because it contains Windows PE (the installer environment).

`install.wim` / `install.swm` contains the actual Windows image.

If both are missing, your USB is **not a valid Windows installation media**.

---

Given your previous steps on Mac:

* FAT32 format
* manually copying ISO files
* splitting WIM because FAT32 has 4GB limit

The likely mistake is:

You copied files but forgot the `sources` directory contents, or the split WIM operation did not create the `.swm` files correctly.

---

Check USB structure:

```cmd
dir D:\
```

You should see something like:

```
boot
efi
sources
support
setup.exe
```

Then:

```cmd
dir D:\sources
```

Expected:

```
boot.wim
install.swm
install2.swm
...
```

---

## Fix: recreate USB from Mac

Mount ISO:

```bash
hdiutil attach Win11_25H2_English_x64_v2.iso
```

Assume:

ISO:

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

USB:

```
/Volumes/WIN11
```

Copy everything except install.wim:

```bash
rsync -avh \
--exclude=sources/install.wim \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/ \
/Volumes/WIN11/
```

Install wimlib:

```bash
brew install wimlib
```

Split:

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

After this:

```bash
ls /Volumes/WIN11/sources/
```

should show:

```
boot.wim
install.swm
install2.swm
```

---

Then eject:

```bash
diskutil eject /Volumes/WIN11
```

Boot Lenovo from USB again.

---

Your current failure:

```
0xC19001F4
```

makes much more sense now. Setup starts because `boot.wim` was probably loaded somehow, but the installation image/settings stage is broken.

First verify:

```cmd
dir D:\sources\boot.wim
```

because if `boot.wim` is also missing, the USB creation is definitely wrong.
