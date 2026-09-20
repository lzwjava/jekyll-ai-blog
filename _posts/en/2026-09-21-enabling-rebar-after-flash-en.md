---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling ReBAR After Flash
translated: false
type: note
---

Flash succeeded 🎉 Now:

## 1. Power off the B75, then boot into BIOS setup

Power on → tap **Del** (or F2) → BIOS setup.

## 2. In BIOS setup, change two settings

1. **Enable "Above 4G Decoding"**
   - Usually under **Advanced → PCI/PnP** or **Chipset** or **Boot**. Look for "Above 4G Decoding" / "Above 4G MMIO" / "Memory Mapped I/O above 4GB" → **Enabled**.

2. **Disable "CSM"**
   - Under **Boot** → "CSM" / "Compatibility Support Module" → **Disabled**.

Save & exit (**F10**).

⚠️ One caveat: if your Ubuntu on the B75 was installed in **legacy/MBR** mode, disabling CSM will stop it booting. After booting Ubuntu you can check with:
```bash
ls /sys/firmware/efi    # exists = UEFI boot (CSM off is fine); "No such file" = legacy/MBR
```
If it's legacy and won't boot, re-enable CSM for now — the flash is already done, so that's safe — and tell me; we can either convert Ubuntu to UEFI or keep CSM on (you'd be limited to a smaller BAR).

## 3. Boot Ubuntu, then set the BAR size

`ReBarState` is on the **MSI machine**, not the B75 — copy it over first (USB stick or `scp`):

```bash
# from this MSI machine to the B75 (adjust user/host):
scp /home/lzw/Downloads/B75/rebar-work/ReBarState  user@b75-ip:~
```

Then on the **B75** (as root):
```bash
sudo ./ReBarState
# type: 32
```
Then **reboot**.

## 4. Verify

```bash
sudo dmesg | grep -i "root bus resource"   # last mem window should end ≥ 0xfffffffff
sudo dmesg | grep -i bar
```
or GPU-Z on Windows if you dual-boot.

---

Tell me:
1. Did you find **Above 4G Decoding** (and where)?
2. Does Ubuntu still boot after disabling CSM?

If you want, I can also build a **Windows `ReBarState.exe`** so you can set the size from Windows instead of Linux.