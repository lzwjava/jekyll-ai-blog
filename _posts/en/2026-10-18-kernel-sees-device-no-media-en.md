---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel Sees Device, No Media
translated: false
type: note
---

The kernel *does* see the device — but the flash controller reports **no media**. Here's what happened, from `dmesg`:

## What the log shows

The stick enumerated **three times with three different identities** in ~40 seconds, then dropped media:

```
1-4.3: idVendor=... General UDisk      → [sdb] 7864320 blocks (4 GB), sdb1
       → sdb: detected capacity change from 7864320 to 0   ← capacity vanished
       → USB disconnect

1-4.3: idVendor=346d, idProduct=5678  Product: "Disk 2.0"
       VendorCo ProductCode → [sdb] 30720000 blocks (15 GB), sdb1 sdb2
       FAT-fs: Volume was not properly unmounted...
       → USB disconnect  (+ lost async page writes, device offline errors)

1-4.3 / then 1-4.1: idVendor=ffff, idProduct=1201
       NAND USB2DISK 0.00
       sd 8:0:0:0: [sdb] Media removed, stopped polling   ← this is the current state
```

That's why `lsblk` shows `sdb 0B`, `/sys/block/sdb/size` is `0`, and `fdisk` says **`No medium found`**:
- `/dev/sdb` exists (USB device enumerated OK)
- but the controller reports "media removed", so there's no capacity and no `/dev/sdb1`.

## Diagnosis

1. **Most likely: the drive itself is failing or is a fake-capacity stick.** Evidence:
   - It reports *different* vendor/product/capacity each replug (`4 GB` → `16 GB` → `ffff:1201` with no serial).
   - `ffff:1201`, `bcdDevice=0.00`, `Mfr=0, Product=0` = bogus USB descriptors (typical of counterfeit/dead controllers).
   - It disconnects itself ~8 seconds after each connect.
   - Previous sessions wrote to it while it was disappearing → `device offline error ... lost async page write`.

2. **Possible contributor: it's on a hub.** `1-4.3` = hub port 3 (you have Genesys `05e3:0610`, Terminus `1a40:0101` hubs + a Realtek NIC on the bus). Cheap sticks are sensitive to hub power.

## What to try

```bash
# 1. Plug it straight into a rear motherboard USB port (no hub, no front-panel),
#    ideally USB 2.0, then watch live:
sudo dmesg -w

# 2. Compare after replugging:
lsblk -o NAME,SIZE,TRAN
sudo fdisk -l /dev/sdb
```

- If it still says `Media removed` / `ffff:1201` / capacity 0 on a direct port → **the drive is dead**, data recovery only via a professional tool (and it likely never had the capacity it advertised).
- If it comes back with real capacity, unmount cleanly before unplugging:
  ```bash
  sudo fsck.vfat -a /dev/sdb1   # it was "not properly unmounted"
  sudo umount /dev/sdb1
  ```
- Cross-check on another machine — if it also shows `ffff:1201` / no medium there, it definitively confirms the stick, not your PC.

Also worth noting: writes were lost on this disk earlier (`lost async page write` on sdb1 and sdb2), so treat any data on it as suspect.