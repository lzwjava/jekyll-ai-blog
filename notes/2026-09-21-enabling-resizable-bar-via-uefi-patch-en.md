---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling Resizable BAR via UEFI Patch
translated: false
type: note
---

This project enables **Resizable BAR** on motherboards/BIOS that don't officially support it. Here's a step-by-step usage guide:

## Overview

The tool has 3 main components:

1. **ReBarDxe** — A UEFI DXE driver injected into your BIOS firmware
2. **ReBarState** — A Windows/Linux utility to configure the BAR size at runtime
3. **UEFIPatch** — Patches to fix BIOS limitations (BAR size limits, MMIO space issues, etc.)

---

## Step 1: Add the DXE Driver to Your BIOS

You need to insert `ReBarDxe` into your motherboard's UEFI firmware image using tools like **UEFITool** or **AMI CBFS** (see the [wiki guide](https://github.com/xCuri0/ReBarUEFI/wiki/Adding-FFS-module) for details).

If you want to build from source:

```bash
# Clone EDK2 first, then inside it:
git clone https://github.com/xCuri0/ReBarUEFI.git
cd ReBarUEFI/ReBarDxe
python buildffs.py
```

## Step 2: Apply UEFI Patches (Optional but Recommended)

Most BIOS firmware has artificial limitations. Use **UEFIPatch** (v0.28.0+) with the patches in `UEFIPatch/patches.txt` to fix:

| Patch | Purpose |
| ------- | --------- |
| `<4GB BAR size limit removal` | Sandy/Ivy Bridge |
| `<16GB / <64GB BAR size limit removal` | Various chipsets |
| `Prevent 64-bit BAR downgrade` | Haswell/Broadwell |
| `Increase MMIO space` | Skylake/KBL/CFL, Haswell/Broadwell, Sandy/Ivy Bridge |
| `NVRAM whitelist unlock` | Fix `GetLastError: 5` in ReBarState |
| `USB 3 fix` | Fix USB ports with Above 4G Decoding (Ivy/Haswell/Broadwell) |

Apply like:

```bash
UEFIPatch your_bios.rom UEFIPatch/patches.txt
```

> **Note**: The `X79 Above 4G Decoding fix` patch (in `UEFIPatch/patch.txt` as commented out) may also be relevant for X79 platforms.

## Step 3: Flash the Modified BIOS

Flash the patched BIOS to your motherboard using your vendor's flashing tool or a hardware programmer.

## Step 4: Configure via ReBarState

After booting with the modified firmware:

- **Enable Above 4G Decoding** in BIOS
- **Disable CSM** (Compatibility Support Module)
- Boot into Windows/Linux and run **ReBarState**

### Windows

Download from [Releases](https://github.com/xCuri0/ReBarUEFI/releases). Run as Administrator:

```
ReBarState.exe
```

### Linux

Build with CMake:

```bash
cd ReBarState
mkdir build && cd build
cmake ..
make
sudo ./ReBarState
```

### Selecting BAR Size

- **32** = Unlimited (recommended if stable)
- Smaller values (2, 4, 8, 16 GB) if 32 doesn't work

> ⚠️ **If the system won't boot**: Clear CMOS. The Resizable BAR setting will be disabled.

---

## Additional Context

The tool also provides a helper script in `tools/`:

- **`uuidconv.py`** — Converts UUIDs to C struct format (e.g., for GUIDs used in the driver)

For the full details, refer to the [project wiki](https://github.com/xCuri0/ReBarUEFI/wiki).
