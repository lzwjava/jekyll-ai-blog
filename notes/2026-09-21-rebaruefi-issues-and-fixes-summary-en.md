---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI Issues and Fixes Summary
translated: false
type: note
---

**Question:** Summary of the ReBarUEFI Common Issues and Fixes wiki page.

**Answer:**

Here's a structured summary of the page covering known issues and their fixes for [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI) — a project that enables Resizable BAR on unsupported UEFI systems.

---

### Current Known Issues (No Fix)
- Many **Haswell** systems lack the 4G decoding option, making full-size ReBarUEFI impossible.
- **LGA1151** has display output issues on some boards (workaround: connect monitor to iGPU).
- **ASRock Z170 K4/D3**: Intel SATA controller stops working when 4G decoding is enabled.
- **32GB BAR** doesn't work on Sandy/Ivy Bridge even under 32GB RAM, though a workaround exists in the linked issue.

---

### GPU-Specific Fixes

| Issue | Fix |
|---|---|
| NVIDIA RTX 30 series ReBAR not working | Update VBIOS via NVIDIA's official guide |
| AMD GPU — blank screen when CSM disabled | Restore original VBIOS (or apply GOP update) |
| AMD unsupported GPU — enable ReBAR | Use Radeon-ID drivers or apply a `.reg` file |
| RX 5600 XT won't resume from sleep | Set BAR size to **1GB** or lower |
| Intel Arc GPU won't work | Set Primary Graphics Adapter to **PCI Express** |
| Driver shows ReBAR disabled (GPU-Z shows working) | Reinstall GPU driver (DDU usually not needed) |

---

### Boot / POST Issues

| Issue | Fix |
|---|---|
| Windows won't boot after disabling CSM | Convert MBR disk to UEFI GPT |
| LGA1151 won't POST with 4GB+ BAR | Connect monitor to iGPU |
| No video output before OS loads | Disable **Above 4G Decoding Patch** option |
| No POST / overclocking broken | Redo guide using **MMTool** instead of UEFITool (UEFITool corrupts some firmwares) |
| Can't boot Windows / GPU error in Device Manager | Follow the **DSDT Patching** guide |
| HEDT system won't boot with ≥16GB VRAM or multi-GPU | Increase `MMIOH Size` / `MMIO High Granularity Size` in BIOS |

---

### Software / NVRAM Issues

| Issue | Fix |
|---|---|
| `ReBarState` says "Failed to write UEFI variable" | Run as Administrator; apply `NvramSmi` or `NvramSmiDxe` patches via UEFIPatch |
| Games crash after enabling ReBAR | Increase **pagefile size** |
| Stutters on Ryzen | Known firmware bug; try setting `Above 4GB MMIO Limit` to `512GB` |
| Stutters on HEDT after enabling 4G decoding | Set `MMIOH Base` to `256GB` or higher |

---

### Common Questions

- **BAR size needed**: You only need a BAR size that fits all your VRAM — e.g., 8GB is enough for 8GB VRAM.
- **Without 4G Decoding**: You're likely limited to 1GB BAR. Reducing the TOLUD option may allow up to 2GB. Linux users can use DSDT patching for full ReBAR without 4G decoding.
- **Memory Remap ≠ 4G Decoding**: Leave Memory Remap at its default setting.
- **GPU-Z reporting**: GPU-Z often reports 4G decode and CSM values incorrectly, so it cannot be fully trusted.

---

References:
- [ReBarUEFI Common Issues and Fixes Wiki](https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-(and-fixes))
