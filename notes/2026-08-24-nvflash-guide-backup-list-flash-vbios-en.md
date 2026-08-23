---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NVFlash Guide: Backup, List, Flash VBIOS"
translated: false
type: note
---

**Question:** How do I use NVFlash to back up a ROM, list GPUs, and flash a new VBIOS on an RTX graphics card?

**Answer:**

---

## ⚠️ WARNING — Read First

Flashing the wrong VBIOS **can permanently brick your GPU**. Always back up first. Do not interrupt power during flashing. Verify compatibility before proceeding.

---

## 1. Download NVFlash

The latest stable release is **v5.867** (February 2025), supporting RTX 5000 (Blackwell) through GTX 1000 series. Download only from **TechPowerUp.com** (the trusted official mirror) — malware-laced fakes exist. No installation needed — just extract the `.exe` and run from Command Prompt.

The zip contains both `nvflash.exe` (32-bit) and `nvflash64.exe` (64-bit). Use 64-bit for modern systems.

Extract to `C:\nvflash\` for easy access.

---

## 2. Setup

1. Open **Command Prompt as Administrator** (search `cmd` → right-click → *Run as administrator*)
2. Navigate to the folder:

   ```
   cd C:\nvflash
   ```

---

## 3. Key Commands

### List all GPUs

```
nvflash --list
```

Lists all NVIDIA GPUs in the system with their index number, device ID, SubVendor ID, and BIOS version.

### Show GPU info / BIOS version (no changes)

```
nvflash --version
nvflash -v
```

### Show detailed info for a specific adapter

```
nvflash -i 0
```

*(replace `0` with the index from `--list`)*

---

## 4. Back Up Current VBIOS (Do This First!)

```
nvflash --save backup.rom
```

To save the ROM of a specific GPU (e.g., index 0):

```
nvflash -i0 --save gpu0.rom
```

Name the file clearly — e.g., `RTX3070-GamingX-original.rom` — including the card model. Store copies locally, on a USB drive, and in cloud storage. Also save a copy of the NVFlash version used alongside the ROM file.

Verify the backup by opening it in **GPU-Z** (click *Save BIOS* → compare the saved file to what GPU-Z reads from your card).

---

## 5. Flash a New VBIOS

### Standard flash (same card/vendor)

```
nvflash -6 newbios.rom
```

The `-6` flag allows you to override a PCI Subsystem ID mismatch. If there's a discrepancy, NVFlash will ask for confirmation — press `Y` (or `Z` on non-US keyboards).

### Force flash (skip confirmation)

```
nvflash -f -6 newbios.rom
```

### Flash a specific GPU by index (multi-GPU systems)

```
nvflash --index=0 bios.rom
```

Use `--list` first to find the correct index for each card in a multi-GPU rig.

### If write-protection is blocking the flash

```
nvflash --protectoff newbios.rom
```

This disables write protection temporarily for the current session. Protection is re-enabled after a cold reboot.

---

## 6. Restore Original VBIOS

Restoring uses the same flash command with your backup file:

```
nvflash -6 original.rom
```

This is the standard procedure before returning a card for warranty service.

---

## 7. Post-Flash Verification

After rebooting, GPU-Z should show the new BIOS version string, the system should POST normally, and the GPU driver should load without errors. If the version string is unchanged, the flash did not take — retry. If there is no display output, follow recovery procedures.

---

## 8. Important Notes on RTX 20+ Signed BIOS

Since the Turing (RTX 20) series, every NVIDIA VBIOS is **cryptographically signed** — the card only accepts a signed image. Flashing one vendor's stock BIOS onto another vendor's card with the same board design generally works, with `-6` handling the subsystem ID mismatch.

Modified BIOSes (power table edited, device ID changed) are blocked by signature validation on Blackwell (RTX 50) series.

---

## Quick Command Cheat Sheet

| Task | Command |
| --- | --- |
| List all GPUs | `nvflash --list` |
| Show version/info | `nvflash -v` |
| Backup VBIOS | `nvflash --save backup.rom` |
| Backup specific GPU | `nvflash -i0 --save gpu0.rom` |
| Flash VBIOS | `nvflash -6 newbios.rom` |
| Flash (force) | `nvflash -f -6 newbios.rom` |
| Flash specific GPU | `nvflash --index=0 newbios.rom` |
| Disable write protection | `nvflash --protectoff newbios.rom` |
| Restore backup | `nvflash -6 original.rom` |

---

**References:**

- [GPU BIOS Flash Guide 2026 (nvflash, commands, recovery)](https://www.mvktech.net/gpu-bios-flash-guide/)
- [nvflash Command Reference 2026](https://www.mvktech.net/nvflash-guide/)
- [NVflash: How to Flash a GPU BIOS (myminingrig.com)](https://myminingrig.com/how-to-flash-a-gpu-bios-with-nvflash/)
- [NVIDIA nvFlash v5.867 Overview](https://pcgamingtools.com/nvidia-nvflash-download/)
- [TechPowerUp NVFlash Download (official mirror)](https://www.techpowerup.com/download/nvidia-nvflash/)
- [Minerstat: NVIDIA VBIOS Flashing Guide](https://minerstat.com/help/nvidia-vbios-flashing)
