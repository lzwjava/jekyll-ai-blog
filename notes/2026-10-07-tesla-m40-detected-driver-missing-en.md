---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 detected, driver missing
translated: false
type: note
---

## Result: NVIDIA Tesla M40 GPU — **the hardware EXISTS**, but no driver is installed.

### ✅ Hardware present (in `lspci`)
```
01:00.0 3D controller: NVIDIA Corporation GM200GL [Tesla M40] (rev a1)
```
The Tesla M40 (GM200/Maxwell, 12GB GDDR5, compute-only card) is physically installed in the PCIe x16 slot (`01:00.0`, behind the CPU-attached PCIe bridge at `00:01.0`).

### ❌ But the software stack is completely missing

| Check | Result |
|---|---|
| `nvidia-smi` | Not installed |
| NVIDIA kernel modules (`nvidia`, `nvidia_modeset`) | Not loaded |
| NVIDIA packages (`dpkg -l \| grep nvidia`) | None |
| `/dev/nvidia*` device nodes | None |

So the card is **detected by the system but not usable** — no driver means no CUDA, no compute.

> 📌 Side note: in my earlier hardware scan the M40 didn't appear (grep only caught the iGPU), but the full `lspci` dump above is authoritative — the card is there.

### Two things worth knowing before we can make it work
1. **`lzw` is not in sudoers** — installing the NVIDIA driver needs root. Either `adduser lzw sudo` + reboot (needs physical/admin access, or root password), or I can prepare the commands for you to run as root.
2. **Driver choice**: M40 is Maxwell, so on Debian 13 (trixie, kernel 6.12) it'll need either the `nvidia-driver` package or the legacy `nvidia-legacy-470xx-driver` — plus the card needs its 8-pin power connector (250W TDP) and likely active cooling since it's passively cooled/needs airflow.

Want me to:
- **(a)** prepare the full driver install command sequence (run as root now, or after you add lzw to sudo), or
- **(b)** reboot/check the GPU post-driver once you've enabled sudo?
