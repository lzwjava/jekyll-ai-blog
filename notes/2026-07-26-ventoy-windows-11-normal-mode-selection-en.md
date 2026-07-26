---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy Windows 11 Normal Mode Selection
translated: false
type: note
---

Question: **In Ventoy, after selecting the Windows 11 ISO, which option should I choose: Normal Mode, WIMBOOT Mode, or File Checksum?**

Answer:

For a normal Windows 11 installation USB, choose:

```
Boot in normal mode
```

This is the default and recommended option.

### Ventoy menu explanation

#### 1. Boot in normal mode ✅ (choose this)

Flow:

```
UEFI BIOS
    ↓
Ventoy
    ↓
Windows 11 ISO
    ↓
Windows Setup
```

Ventoy maps the ISO as a virtual DVD drive. Windows installer reads:

```
boot.wim
install.wim
```

normally.

Use this for:

* Lenovo Xiaoxin
* Windows 11 clean install
* Most UEFI PCs

---

#### 2. Boot in WIMBOOT mode

Do **not** choose this first.

WIMBOOT mode is a compatibility fallback. It extracts/boots using Windows WIM files differently.

Use only if:

* Normal mode fails
* Windows Setup cannot find files
* Some old firmware has ISO loading issues

For modern UEFI laptops, normal mode is better.

---

#### 3. File checksum

This is only a verification tool.

It calculates something like:

```
SHA256:
xxxxxxxxxxxxxxxx
```

to check whether the ISO file is corrupted.

You use it before installation if you suspect:

* interrupted download
* bad ISO copy
* modified ISO

It does not boot Windows.

---

For your Lenovo Xiaoxin:

Select:

```
Ventoy
 └── Win11_25H2_English_x64_v2.iso
       └── Boot in normal mode  ← choose this
```

Then Windows Setup should appear.

If it reaches the disk selection screen and you see:

```
Drive 0 512GB
```

then the SSD is already detected. The remaining issue is usually partition/delete/install, not USB creation.
