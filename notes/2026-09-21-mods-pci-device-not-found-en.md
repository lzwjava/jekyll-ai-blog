---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS PCI device not found
translated: false
type: note
---

**Question:** Why is MODS (GPU diagnostic tool) showing a "PCI device not found" error?

**Answer:**

The screen shows a MODS GPU test (`gputest.js`) failing with **Error Code `0x220` — PCI device not found**. Here's why:

**Root Cause**

The key error is:

```
ERROR: SBIOS assigned incorrect BAR1 – offset 0x0, size 0x0
```

The BIOS/UEFI failed to properly assign a **Base Address Register (BAR)** to the GPU. BAR1 has size `0x0`, meaning the system couldn't map the GPU into PCI address space — so MODS simply cannot find the GPU device on the PCI bus.

**Likely Causes**

1. **No discrete GPU installed** — This system (Intel i5-4460, Haswell) may only have integrated graphics. MODS is looking for an NVIDIA GPU that doesn't exist.
2. **GPU physically unseated** — If a GPU card was installed, it may have a poor PCIe slot connection.
3. **Above 4G Decoding disabled in BIOS** — Required for some GPUs to get proper BAR allocation.
4. **BIOS bug or outdated firmware** — SBIOS date is `12/09/2016`, which is very old.
5. **PCIe slot or card failure** — The GPU may be dead or the slot damaged.

**What to Check**

- Confirm a discrete NVIDIA GPU is actually installed
- Reseat the GPU in the PCIe slot
- Enable **Above 4G Decoding** in BIOS settings
- Update BIOS firmware if possible
- Test the GPU in another machine or slot

**References:**

- [NVIDIA MODS Documentation](https://developer.nvidia.com/mods)
- [PCI BAR (Base Address Register) Explained](https://wiki.osdev.org/PCI#Base_Address_Registers)
- [PCIe BAR allocation issues on Linux](https://www.kernel.org/doc/html/latest/PCI/pci-error-recovery.html)
