---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy USB Install and ISO Copy
translated: false
type: note
---

## Plan — Ventoy + Flash Windows ISO

### ISO Found

```
/home/lzw/Downloads/Win11_25H2_English_x64_v2.iso   (7.9G)
```

### USB Target

```
/dev/sdb  (14.6G USB)  ← currently has old Windows installer
```

### ⚠️ Critical Warning

Installing Ventoy to `/dev/sdb` will **erase everything** on it — the current EFI and WIN11 partitions will be destroyed. Your old USB content will be gone.

### Step-by-Step

| Step | Action | Command |
| --- | --- | --- |
| **1** | Download Ventoy | `wget https://github.com/ventoy/Ventoy/releases/latest/download/ventoy-1.1.05-linux.tar.gz` |
| **2** | Extract | `tar xzf ventoy-*.tar.gz && cd ventoy-*` |
| **3** | Confirm USB is `/dev/sdb` | `lsblk` |
| **4** | Install Ventoy to USB | `sudo ./Ventoy2Disk.sh -i /dev/sdb` |
| **5** | Copy ISO | `cp ~/Downloads/Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/` |
| **6** | Sync & eject | `sync` then unplug |

After step 4, the USB becomes a Ventoy disk. You just copy the ISO file onto it — no extraction, no partition fiddling. Multiple ISOs can coexist.

---

**Confirm you want to proceed?** The current USB data will be wiped.
