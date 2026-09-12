---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix GPU Initialization Failure Guide
translated: false
type: note
---

Question: **How to fix the GPU initialization failure shown in the screenshot?**

Answer:

The **TSC warning is not the problem**. The actual failure is:

```text
PCI chip ID 0x00001006 (DID=1287) is an unrecognized GPU
Possibly you need a newer MODS package.

There are no active devices to test.
Error 220: Gpu.Initialize pci device not found
Error Code = 00000220
```

`DID=1287` is significant: **PCI device ID `1287` corresponds to NVIDIA GK208B / GeForce GT 730** when paired with NVIDIA vendor ID `10de`. ([blog.jklug.work][1])

So I would debug this in this order:

### 1. Check what Linux actually sees

At the shell, run:

```bash
lspci -nn | grep -Ei 'vga|3d|display|nvidia'
```

Then:

```bash
lspci -nn -s 01:00.0
```

Replace `01:00.0` with the actual GPU PCI address.

You want something like:

```text
01:00.0 VGA compatible controller [0300]:
NVIDIA Corporation GK208B [GeForce GT 730] [10de:1287]
```

The important part is:

```text
[10de:1287]
```

`10de` = NVIDIA, `1287` = GK208B/GT 730. ([blog.jklug.work][1])

### 2. If Linux reports `10de:1287`

Then **your GPU is visible to PCIe**, and this is almost certainly a **MODS compatibility/version problem**, not a dead GPU.

The screen itself is telling you this:

```text
Possibly you need a newer MODS package.
```

Get a MODS build that explicitly supports the GPU generation you're testing.

Also check:

```bash
lspci -nnk -s 01:00.0
```

and:

```bash
dmesg | grep -Ei 'nvrm|nouveau|pci|vfio|gpu'
```

If `nouveau`, `nvidia`, or `vfio-pci` has already claimed the device, that can also interfere with MODS.

For example:

```bash
lspci -nnk -s 01:00.0
```

If you see:

```text
Kernel driver in use: nouveau
```

or:

```text
Kernel driver in use: nvidia
```

you need to account for that before running MODS.

### 3. If Linux reports `1006:1287`

That's much more interesting.

`1006` is **not NVIDIA's vendor ID**; NVIDIA is `10de`. The PCI ID database identifies `1006` as Reply Group, not NVIDIA. ([GitHub][2])

In that case, don't touch the TSC setting yet. We need to determine why the PCI vendor ID is being presented incorrectly.

Run:

```bash
lspci -nn
```

and:

```bash
lspci -xxxx -s <GPU_BDF>
```

Also:

```bash
cat /sys/bus/pci/devices/<GPU_BDF>/vendor
cat /sys/bus/pci/devices/<GPU_BDF>/device
```

For a normal GT 730 those should effectively be:

```text
0x10de
0x1287
```

### 4. Ignore the TSC warning for now

This:

```text
NURM: Warning - TSC is unstable on this CPU!
```

is a separate Linux clocksource issue. Linux has explicit `tsc=` kernel parameters for handling unstable TSCs, but changing them won't make a missing PCI GPU appear. ([Kernel.org][3])

So **don't start with `tsc=reliable` or BIOS clock settings**.

---

### My strongest guess

Given:

```text
DID=1287
/home/GT610
MODS
Error 220
```

I'd first assume **an old MODS build that doesn't recognize the installed NVIDIA GPU**, especially if this is a custom TinyLinux/MODS boot environment.

Run these three commands and paste the output:

```bash
lspci -nn | grep -Ei 'vga|3d|display|nvidia'

lspci -nnk | grep -A4 -Ei 'vga|3d|display|nvidia'

dmesg | grep -Ei 'nvrm|nouveau|vfio|pci' | tail -100
```

With those, I can tell you whether this is **MODS version mismatch, wrong PCI ID, driver ownership, VFIO passthrough, or actual PCIe/GPU hardware failure**.

References:

* [PCI/GPU identification example for NVIDIA 10de:1287](https://blog.jklug.work/posts/proxmox/?utm_source=chatgpt.com)
* [Linux kernel TSC parameters](https://kernel.org/doc/html/next/admin-guide/kernel-parameters.html?utm_source=chatgpt.com)
* [PCI vendor ID database](https://github.com/evanphx/ulysses/blob/master/src/pci_db.hpp?utm_source=chatgpt.com)

[1]: https://blog.jklug.work/posts/proxmox/?utm_source=chatgpt.com "Proxmox Hypervisor - GPU and Disk Passthrough · blog.jklug.work"
[2]: https://github.com/evanphx/ulysses/blob/master/src/pci_db.hpp?utm_source=chatgpt.com "ulysses/src/pci_db.hpp at master · evanphx/ulysses · GitHub"
[3]: https://kernel.org/doc/html/next/admin-guide/kernel-parameters.html?utm_source=chatgpt.com "The kernel’s command-line parameters — The Linux Kernel documentation"
