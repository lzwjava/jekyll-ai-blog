---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Valid, Fix BIOS VMD
translated: false
type: note
---

## Analysis Complete

Good news — **your USB is already correctly made**. Here's what I found:

### ✅ USB is Valid (`/dev/disk12` — 15.7 GB)

| Required File | Status | Size |
| --- | --- | --- |
| `sources/boot.wim` | ✅ **Present** | 586 MB |
| `sources/install.wim` | ❌ Missing (expected — >4GB) | 7.1 GB original |
| `sources/install.swm` | ✅ **Present** | 3.2 GB (part 1) |
| `sources/install2.swm` | ✅ **Present** | 3.7 GB (part 2) |
| `sources/install3.swm` | ✅ **Present** | 79 MB (part 3) |
| `boot/`, `efi/`, `setup.exe` | ✅ **All present** | |

Everything is in order. `boot.wim` is there. The `install.wim` was correctly split into 3 `.swm` files that Windows Setup handles natively.

### 🎯 The Real Problem (Not the USB)

Since the USB is fine, **re-flashing it won't fix the `0xC19001F4` error**. The issue is almost certainly on the **Lenovo Xiaoxin BIOS side**:

> **Intel VMD Controller** or **Intel RST** is enabled in BIOS

When VMD is on:

1. Windows PE can see the NVMe (Setup starts copying files)
2. After first reboot, Windows tries to boot from NVMe using in-box `stornvme.sys`
3. That driver can't talk through the VMD controller → drive disappears
4. Windows triggers recovery → Setup sees this → aborts with `0xC19001F4`

### Step 1 — Fix BIOS First (2 minutes)

Before anything else, reboot the Xiaoxin → press **`F2`** → look for:

| Setting to find | Change to |
| --- | --- |
| **Intel VMD Controller** | **Disabled** |
| **Intel RST / Optane** | **AHCI** |
| **SATA Mode** | **AHCI** (not RST/Optane) |

Save & exit. Then try the install again with the **same USB** — it should work.

Want to try that first before we rebuild the ISO?
