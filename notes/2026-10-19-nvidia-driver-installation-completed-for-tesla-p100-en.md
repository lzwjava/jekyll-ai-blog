---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NVIDIA Driver Installation Completed for Tesla P100"
translated: false
type: note
---

Done. The NVIDIA driver is installed and the Tesla P100 is now active.

## Summary

**GPU detected:** `NVIDIA Tesla P100 PCIe 16GB` (GP100, Pascal)

**Installation steps performed:**

1. Identified OS (Ubuntu 26.04 LTS) and confirmed no NVIDIA driver present.
2. Used `ubuntu-drivers devices` → recommended driver `nvidia-driver-580`.
3. Installed `nvidia-driver-580` (version **580.178.04**, CUDA 13.0) via apt.
4. Found `nouveau` (open-source driver) had claimed the P100 and blocked the NVIDIA module, so I added `/etc/modprobe.d/blacklist-nouveau.conf`, ran `update-initramfs -u`, then unbound nouveau and loaded the NVIDIA stack.

**Current status — working:**

```
NVIDIA-SMI 580.178.04   Driver Version: 580.178.04   CUDA Version: 13.0
Tesla P100-PCIE-16GB | 00000000:01:00.0 | 0MiB / 16384MiB | 0%
```

- P100 bound to the `nvidia` driver
- Device nodes present (`/dev/nvidia0`, `/dev/nvidiactl`, etc.)
- `nvidia-persistenced` service active (recommended for Tesla cards)
- Nouveau blacklist persisted; boot services (`nvidia-powerd`, suspend/resume) enabled

**Note:** The old `nouveau` module is still resident in this running kernel session, though it no longer owns the P100. A reboot will give a fully clean state and confirm persistent auto-loading. Since display is driven by the Intel `i915` GPU, rebooting is optional — the P100 is already usable now.

You can verify with `nvidia-smi` or, once you add the CUDA toolkit, `nvidia-smi -q` / `nvcc --version`.

Would you like me to also install the CUDA toolkit for compute workloads?
