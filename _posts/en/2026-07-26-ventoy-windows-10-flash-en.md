---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ventoy Windows 10 Flash
translated: false
type: note
---

## ✅ Done — Windows 10 Flashed via Ventoy

### What Happened

| Step | Action | Time |
|---|---|---|
| 1 | Unmounted old FAT32 partition | Instant |
| 2 | Installed **Ventoy v1.1.17** to `/dev/sdb` (wiped + repartitioned) | ~15s |
| 3 | **Copied** `Win10_22H2_English_x64v1.iso` (5.8G) to Ventoy partition | ~2 min |
| 4 | Synced, unmounted, powered off | Instant |

### Final USB Layout

| Partition | Size | Filesystem | Label | Content |
|---|---|---|---|---|
| `/dev/sdb1` | 14.6G | **exFAT** | `Ventoy` | `Win10_22H2_English_x64v1.iso` (5.8G) |
| `/dev/sdb2` | 32M | **vfat** | `VTOYEFI` | Ventoy EFI bootloader |

### USB Now Has 2 ISOs

Since you previously copied the Windows 11 ISO... wait — that was on the **old** USB before it got repartitioned to `DISK_IMG`. This is a fresh Ventoy install with only:

- **Windows 10 22H2** (5.8G) ← just added

If you want Windows 11 on here too:

```bash
sudo mount /dev/sdb1 /mnt
sudo cp ~/Downloads/Win11_25H2_English_x64_v2.iso /mnt/
sync; sudo umount /mnt
```

Both ISOs will show up in the Ventoy boot menu at startup. **Safe to unplug.**