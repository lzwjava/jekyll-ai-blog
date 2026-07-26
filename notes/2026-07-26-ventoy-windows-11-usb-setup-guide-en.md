---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy Windows 11 USB Setup Guide
translated: false
type: note
---

## ✅ Done! Ventoy v1.1.17 + Windows 11 ISO — Complete

### Final USB Layout

| Partition | Size | Filesystem | Label | Content |
| --- | --- | --- | --- | --- |
| `/dev/sdb1` | 14.6G | exFAT | **Ventoy** | `Win11_25H2_English_x64_v2.iso` (7.9G) |
| `/dev/sdb2` | 32M | vfat | **VTOYEFI** | Ventoy EFI bootloader |

### How to Use

1. **Plug USB** into your Lenovo Xiaoxin
2. **Boot** → press F2/F12 (or whatever enters boot menu on your model)
3. Select **UEFI: <USB name>** (not legacy/CSM)
4. Ventoy menu appears → select `Win11_25H2_English_x64_v2.iso`
5. Windows installer starts

### If SSD Not Detected (common Lenovo Xiaoxin issue)

Windows 11 installer may not see the NVMe SSD — this is the **Intel VMD/RST driver** problem. You'll need to:

1. Download the Intel RST F6 driver from [Intel's site](https://www.intel.com/content/www/us/en/download/19512/)
2. Extract to a **second USB**
3. At disk selection screen → **Load Driver** → browse to the extracted folder
4. SSD appears → proceed with installation

### Bonus: Multi-ISO

Ventoy supports multiple ISOs. You can copy Linux ISOs, rescue disks, etc. alongside Windows:

```bash
sudo cp ~/Downloads/ubuntu-24.04-desktop.iso /media/$USER/Ventoy/
```

All ISOs show up in the Ventoy boot menu.
