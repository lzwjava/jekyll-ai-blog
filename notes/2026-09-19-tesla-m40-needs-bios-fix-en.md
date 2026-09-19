---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 Needs BIOS Fix
translated: false
type: note
---

I have a complete diagnosis. Before I install, I need the sudo password (it's not passwordless).

## What I found

**The GPU:** Tesla M40 12 GB (`10de:17fd`, GM200, VBIOS 84.00.56.00.02) — installed today at 17:15. The earlier boot logs in `kern.log` are from a *different* card (a Fermi `GF100` 2 GB) that was previously in the box.

**The driver:** `nvidia-driver-580` (580.178.04) is confirmed correct:
- NVIDIA's official 580.178.04 README lists `Tesla M40` and `Tesla M40 24GB`
- 590/595/610 are Turing+ only (590 is literally a transitional alias → 595)
- `ubuntu-drivers devices` independently recommends `nvidia-driver-580` for `v000010DEd000017FD`

**A blocker you should know about** — the M40 currently **cannot be initialized**, and installing the driver alone will not fix it:

```
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
pci 0000:01:00.0: BAR 3 [mem size 0x02000000 64bit pref]: can't assign; no space
nouveau 0000:01:00.0: bar: one-time init failed, -12
```

The M40 requires a **16 GiB 64-bit prefetchable BAR** (normal for datacenter GPUs). Your BIOS only provides a 16 MB 32-bit window, and the root port reports `Prefetchable memory behind bridge: [disabled] [64-bit]`. Result: `nvidia-smi` would report "No devices were found" even with 580 installed.

Fixing that requires enabling **Above 4G Decoding** in BIOS (MSI B150M PRO-VH, BIOS 1.80, dated 07/2016). I couldn't confirm from MSI's site whether 1.80 exposes that option — you may need a BIOS update, since MSI added it to some boards only in later revisions.

## Plan once you give me the password

1. `apt update`
2. Install `build-essential dkms linux-headers-$(uname -r)` (DKMS isn't installed yet)
3. Install `nvidia-driver-580`
4. Blacklist `nouveau` (currently bound to the card)
5. `update-initramfs -u`, then reboot
6. Verify with `nvidia-smi`

Secure Boot is disabled, so no MOK enrollment is needed. The M40 has no display outputs, so your desktop will stay on the Intel HD 530 and rebooting is safe.

**How would you like to proceed?**

- Send me the sudo password (or enable `NOPASSWD` for `lzw`), and I'll run all of it, or
- Give me the go-ahead and reboot yourself for step 5.

Also worth deciding: your board has a **passive** M40 (designed for server airflow) — make sure it has forced airflow, and note ECC is on by default (that's why nouveau sees 11520 MiB of the 12288 MiB).