---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS lacks Above 4G Decoding
translated: false
type: note
---

I've hit the limit of what I can determine remotely. Here's the full picture.

## What happened to your reboot

The reboot was **refused, and the machine never went down** (`uptime` showed `up 1:23`). GNOME registers a *block*-mode inhibitor:

```
gnome-session-s  shutdown  user session inhibited   ← block
gsd-power        handle-lid-switch                  ← block
gsd-media-keys   handle-power-key...                ← block
```

`systemctl reboot` respects that. My reconnect loop then spun until it timed out — that's the "Command aborted" you saw. Nothing broke.

## Steps 1–4 are done and verified

| Step | Status |
| --- | --- |
| 1. `apt update` | ✅ |
| 2. `build-essential dkms linux-headers-$(uname -r)` | ✅ dkms installed, headers already present |
| 3. `nvidia-driver-580` (580.178.04) | ✅ all 5 modules built + installed: `nvidia/580.178.04, 7.0.0-31-generic, x86_64: installed` |
| 4. blacklist nouveau | ✅ `/etc/modprobe.d/blacklist-nouveau.conf` + initramfs rebuilt |

The driver itself is fine — it loads and initializes nvlink. But:

```
NVRM: BAR1 is 0M @ 0x0 (PCI:0000:01:00.0)
nvidia 0000:01:00.0: probe with driver nvidia failed with error -1
```

## The real blocker: your BIOS has no 64-bit MMIO window

The M40 requests `BAR 1 [mem size 0x400000000 64bit pref]` = **16 GiB**, which is normal for Tesla cards. Your root port reports:

```
Prefetchable memory behind bridge: [disabled] [64-bit]
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
```

So **no driver can work** — nouveau failed the same way earlier (`bar: one-time init failed, -12`). This is fixed by enabling **Above 4G Decoding** in BIOS.

## What I found about your BIOS (with a correction)

- Board: MSI B150M PRO-VH (MS-7996), BIOS **1.80, 2016-07-27**
- Newer BIOSes exist: up to **3.A0, 2018-07-12** (`download.msi.com/bos_exe/mb/7996v3A.zip`)
- **Correction:** I first searched the BIOS image for "Above 4G" and found nothing — but that was a *false* negative. The known strings "Secure Boot" and "SATA Configuration" were missing too, meaning the AMI setup strings are compressed. I decompressed 314 LZMA streams and still couldn't reach them (Tiano-compressed), so **I could not determine whether the option exists.**

One soft signal: the release notes for both 1.80 and 3.A0 mention only PCIe/USB compatibility and microcode — neither mentions Above 4G. So a BIOS update may well not help.

## What you need to do

1. Reboot and press **Del** at the MSI logo.
2. Look for **Above 4G Decoding** / **Above 4G Memory** / **Crypto Currency mining** — usually under `Settings → Advanced → PCI Subsystem Settings`.
3. **If found:** enable, save & exit. Then I'll verify:

   ```
   nvidia-smi
   ```

4. **If absent:** the M40 physically cannot work in this board, and you'd need a motherboard with Above-4G decoding.

Since you have to visit BIOS anyway, that's the natural moment to reboot. If you'd rather I force one from here now, I can run `sudo systemctl reboot -i` (ignores the GNOME inhibitor) — but it will kill your logged-in GNOME session, and won't change the outcome.

Two side notes: `nvidia-persistenced` will fail harmlessly on each boot until the GPU initializes, and your old Fermi card worked purely because it had a ~128 MB BAR1 that fit *below* 4 GB — the same reason a Pascal/GeForce card would work without any BIOS change. Also, the M40 is passive, so it needs real airflow, and ECC is on by default (hence the 11520 MiB of 12288 MiB).
