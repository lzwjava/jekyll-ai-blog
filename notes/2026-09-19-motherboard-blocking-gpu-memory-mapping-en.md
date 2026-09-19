---
audio: false
generated: true
image: false
lang: en
layout: post
title: Motherboard Blocking GPU Memory Mapping
translated: false
type: note
---

Important discovery: the machine we just diagnosed **is** that board. The DMI data reads:

```
bios_vendor  : American Megatrends Inc.
bios_version : 4.6.5
bios_date    : 12/09/2016
board_name   : SY-B85N FS        <-- the SOYO SY-B85N
```

And the kernel log gives us the exact reason the P100 won't work:

```
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
pci 0000:00:01.0: bridge window [mem size 0x402000000 64bit pref]: can't assign; no space
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: failed to assign
pci_bus 0000:00: Some PCI device resources are unassigned, try booting with pci=realloc
```

`0x400000000` = **16 GB**. The P100's BAR1 is a 16 GB *64-bit prefetchable* BAR. The BIOS never created a 64-bit MMIO window above 4 GB, so the kernel has nowhere to put it. Only BAR0 (16 MB) got assigned — hence `BAR1 is 0M @ 0x0` and the driver probe failure loop.

## Answer to your question

**Resizable BAR: not possible on this board. Full stop.**
Resizable BAR requires chipset/firmware support that arrived with Intel 400-series / 10th-gen (~2020). Haswell + B85 (2014) predates it by six years. There is no BIOS option, and no cross-flash or mod can add it, because the silicon path doesn't exist. (Note: the P100 *GPU* side supports it, since it's Pascal — the *platform* is the blocker.)

**Above 4G Decoding: that's the only thing that matters here** — and it's what you need to look for.

### 1. Check the BIOS (Del key at boot)

AMI BIOS 4.6.5 on a B85 board — the option, *if present*, is usually under one of:

```
Advanced  → PCI Subsystem Settings  → Above 4G Decoding        (most likely place)
Chipset   → PCH-IO Configuration    → Above 4G Decoding
Chipset   → System Agent (SA) Config → Above 4G Decoding
Advanced  → PCI Express Configuration
```

Also make sure **CSM is Disabled** and the system boots pure UEFI (it already does here — `/sys/firmware/efi` exists). Above 4G Decoding is a UEFI feature and is ignored in legacy mode.

**Be prepared for it to be absent.** B85-era AMI BIOSes very often do not ship this option at all. If it's there, enable it, save, reboot, and you're done. If it's *not* there, you cannot unhide it — there'd be nothing to unhide, because the firmware code path for >4 GB MMIO allocation was never compiled in. (You can verify: dump the BIOS and run `strings bios.bin | grep -i "above 4g"`. No hit = the setting object doesn't exist in the firmware.)

### 2. Free thing to try first — kernel-side realloc

The kernel itself suggested this, so test it before buying anything:

```bash
sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pci=realloc pci=nocrs"/' /etc/default/grub
sudo update-grub && sudo reboot
```

Then check whether BAR1 got an address:

```bash
lspci -vv -s 01:00.0 | grep -i region      # want Region 1 with a real address
journalctl -b -k | grep -i "BAR 1"          # should no longer say "failed to assign"
```

**Set expectations low:** `pci=realloc` can only distribute space the ACPI host bridge declares to the OS. If the BIOS never declares a 64-bit window (which is exactly what "no Above 4G Decoding" means), the 16 GB request still can't fit under 4 GB and it will keep failing. `pci=nocrs` sometimes makes the kernel probe harder. It's ~5 minutes to test and costs nothing.

### 3. If the BIOS has no Above 4G Decoding

Then the board simply cannot host this card. Your realistic paths:

- **Different platform.** X99/C612 workstation boards, or a newer consumer board where the vendor shipped Above 4G Decoding (many B450/B550/Z390/Z490 boards, ASRock H110 Pro BTC+, etc.). Nearly all Haswell/B85 boards lack it.
- **Drop the P100 from this build.** Keep the Intel iGPU for display and use the box as a plain desktop/NAS.

### 4. Reality check on the P100 in this build anyway

Even with BAR1 assigned, this combination has serious problems:

| Issue | Detail |
| --- | --- |
| **Cooling** | P100 is a *passive* Tesla card designed for 1U/2U server airflow. In an open desktop it will overheat and throttle/shutdown; it needs a shroud + high-static-pressure fan. |
| **Power connector** | The Tesla P100 PCIe uses an **8-pin CPU/EPS connector**, *not* a PCIe 8-pin. Using a PCIe cable on it is a no-boot/damage risk. 250 W TDP. |
| **Host RAM** | You have **3.2–4 GB**. A 16 GB CUDA card with 4 GB of host RAM is not a usable compute host. |
| **No display out** | Tesla cards have no video outputs (fine here, iGPU handles display). |
| **PCIe** | i5-4460 gives PCIe 3.0 x16 — acceptable, but the whole package is mismatched. |

## Bottom line

- **Resizable BAR:** impossible on B85 — don't waste time.
- **Above 4G Decoding:** look under `Advanced → PCI Subsystem Settings` in the AMI BIOS. If it exists, enable it → the 16 GB BAR1 will map and the driver loop stops. If it doesn't exist, the board cannot do it, and `pci=realloc`/`pci=nocrs` is your only (long-shot) free attempt.
- **Also, regardless of the GPU:** the machine's slowness is dominated by that 7200 RPM HDD + 4 GB RAM + the NVIDIA retry storm. Disabling `nvidia-persistenced` stops the CPU churn immediately, and the P100 being unusable just means you should blacklist `nvidia` and move on.

Want me to go ahead and (a) apply the `pci=realloc`/`pci=nocrs` boot-parameter test, and (b) disable the `nvidia-persistenced` retry loop on that host? I'd need your sudo password for the GRUB/systemd changes.
