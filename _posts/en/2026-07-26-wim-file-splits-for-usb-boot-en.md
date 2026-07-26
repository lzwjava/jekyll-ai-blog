---
audio: false
generated: true
image: false
lang: en
layout: post
title: WIM File Splits for USB Boot
translated: false
type: note
---

## Analysis Complete — Here's the Full Picture

### ✅ What We Found

| Item | Status |
|---|---|
| **ISO file** | ✅ Exists at `/Users/lzwjava/Downloads/Win11_25H2_English_x64_v2.iso` — **7.9 GB** |
| **ISO contents** | ✅ Standard Windows 11 DVD layout — `boot/`, `efi/`, `sources/`, `setup.exe` |
| **`install.wim`** | ⚠️ **7.1 GB** — exceeds FAT32's **4 GB file size limit** |
| **USB drive** (`/dev/disk13`) | ✅ **15.7 GB** — detected, but **no partition table, no filesystem** ("Content: None") |
| **`wimlib`** | ✅ Already installed at `/opt/homebrew/bin/wimlib-imagex` |

### 🔍 Root Cause of Etcher's Error

The USB drive (`/dev/disk13`) is completely raw — **no MBR, no GPT, no filesystem**. When Etcher inspects the Windows ISO, it sees:

- **ISO format** (ISO9660/UDF) — **not a hybrid disk image** with a partition table
- Windows ISOs are **DVD images**, not raw disk images like Ubuntu/Raspberry Pi ISOs
- Etcher expects `GPT/MBR → partition → filesystem` inside the image

So Etcher says *"missing partition table"* — correct, but the real issue is that Etcher is the wrong tool for this job.

### 🚨 The Real Problem

Even if you format the USB, `install.wim` is **7.1 GB** — FAT32 caps at 4 GB per file. You **must** split it into `.swm` files.

### ✅ Recommended Action: `wimlib` Method

The steps from your answer are correct. Since everything is already in place:

1. **Format USB** as FAT32 (GPT)
2. **Copy all ISO files** except `install.wim`
3. **Split `install.wim`** into `install.swm`, `install2.swm`, `install3.swm`
4. **Eject** both drives

---

**Shall I execute the full setup now?** I'll:

1. `diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13` — format the USB
2. `cp -av` to copy files
3. `rm /Volumes/WIN11/sources/install.wim`
4. `wimlib-imagex split` into 3800 MB chunks

The USB will then boot perfectly on your **Lenovo Xiaoxin UEFI laptop**.
