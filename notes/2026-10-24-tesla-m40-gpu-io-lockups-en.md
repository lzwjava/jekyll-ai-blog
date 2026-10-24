---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 GPU I/O Lockups
translated: false
type: note
---

All info collected. Here's the full report for **192.168.1.34 (lzw-MS-7996)**:

## System Overview

| Component | Detail |
|---|---|
| **OS** | Ubuntu 26.04.1 LTS (resolute), kernel 7.0.0-38-generic, up 10d 17h |
| **Board** | MSI **Z170A GAMING M5** (MS-7977) — note the hostname says MS-7996 but DMI reads MS-7977 |
| **CPU** | Intel Core **i5-6600** @ 3.30 GHz — 1 socket, 4 cores / 4 threads, turbo 3.9 GHz, Skylake, VT-x |
| **RAM** | 11 GiB total (4.5 GiB used), **swap 3.7 GiB fully used** ⚠️ |
| **GPU** | **NVIDIA Tesla M40** (12 GB: 11520 MiB) + Intel HD 530 (iGPU) |
| **Disk** | 1 TB WD Blue `WD10EZEX` (SATA) — `/` 915G ext4, 139G used (16%), `/boot/efi` 1G vfat |
| **Network** | `enp3s0` → 192.168.1.34/24 |

## GPU detail (nvidia-smi, driver 580.178.04 / CUDA 13.0)

```
GPU 0:  Tesla M40          Off    41°C    P0    62W / 250W
        4 MiB / 11520 MiB used    0% util    Persistence Off
gnome-shell is the only process on it (1 MiB)
```

## Notes / health flags

- ⚠️ **GPU has I/O lockups**: `nvidia-smi` hangs (processes sit in **D-state** `Dl` — uninterruptible, survive even SIGKILL). A query from 18 minutes ago is still stuck; several accumulated. The GPU responds intermittently (one background run succeeded and returned the table above). Worth rebooting the box or checking the card/driver, especially before relying on it for compute.
- ⚠️ Swap is 100% full (3.7/3.7 GiB).
- 🔄 A `python` process (PID 88699) is pegging 1 core at 99.9% — load avg is exactly 4.00 across 4 cores, so the box is currently busy.
- 🖥️ It's a desktop box: GNOME shell, Firefox, Ghostty running (6 users logged in).
- Memory stick details (DMI) need root; I only got the 11 GiB total.

Want me to dig into anything — e.g. identify that running python process, check the stuck nvidia-smi D-state processes, or run a GPU benchmark?
