---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCI Resource Fix Location Explained
translated: false
type: note
---

Yes — this repo does contain the fix, but it's important to be precise about **where** it lives. The fix for "PCI Insufficient PCI Resources Detected" on a Z170 is **not** in the `ReBarDxe` driver; it's in the binary firmware patches under `UEFIPatch/`.

## Where the fix is

`/mnt/data/ReBarUEFI/UEFIPatch/patches.txt`

This file contains pattern-based patches applied to the AMI Aptio V firmware modules (`PciHostBridge` and `PciBus`) that directly remove the artificial MMIO/BAR limits which produce that exact POST error.

## Which patches target your Z170 (Skylake) case

From `patches.txt`:

| Patch | Module (GUID) | What it fixes |
|---|---|---|
| `Replace 64GB MMIO region with complete use of 512GB physical address space (Skylake/Kaby Lake/Coffee Lake)` | PciHostBridge `8D6756B9-...` | Expands the MMIO aperture from the stock 16–32GB (or 64GB) window up to the full 39-bit / 512GB range |
| `Remove <64GB BAR size limit (Skylake/Kaby Lake/Coffee Lake)` | PciBus `3C1DE39F-...` | Removes the firmware's 64GB BAR cap |
| `Don't downgrade 64-bit BARs to 32-bit` | PciBus `3C1DE39F-...` | Stops the firmware from forcing large 64-bit BARs down into the tiny 32-bit/4GB window — the most common direct cause of "Insufficient PCI Resources" |
| `Remove 4GB limit for PciRootBridgeIo.Mem` | PciHostBridge `8D6756B9-...` | Removes the 4GB decode limit on the root bridge memory window |
| `Remove 4GB limit for CpuIo2` | Runtime `CBC59C4A-...` | Removes the 4GB CPU I/O limit |

The README's "Working patches" section confirms the Skylake-specific one:

> Increase MMIO space from 16-32GB to full usage of 512GB/39-bit range (Skylake/Kaby Lake/Coffee Lake)

## How this maps to your error

The AMI "Insufficient PCI Resources Detected" message is what `PciBus`/`PciHostBridge` report when BAR allocation fails (the `NotifyPhase(EfiPciHostBridgeAllocateResources)` path returns `EFI_OUT_OF_RESOURCES` — you can see that exact return value documented in `ReBarDxe/include/PciHostBridgeResourceAllocation.h`). With an M40/P100 exposing a multi-GB BAR1, the stock Z170 firmware:

1. caps the MMIO region (16–32GB or 64GB), and/or
2. downgrades the 64-bit BAR to 32-bit, and/or
3. caps BAR size at <64GB,

…so allocation runs out and you get the error. The patches above lift exactly those three limits.

## The important caveat

- `ReBarDxe/ReBar.c` is **only the ReBAR enabler** — it hooks `PreprocessController` and programs the ReBAR capability. It does **not** fix resource allocation by itself, and in fact it can *make* the problem worse if you request a BAR size the unpatched firmware can't allocate.
- The patches are GUID + byte-pattern based. They apply cleanly only if MSI used stock AMI Aptio V modules with matching byte patterns. You apply them with UEFIPatch and must confirm the patterns matched (and that pad files weren't changed, per the README).
- The MMIO expansion only takes effect with **Above 4G Decoding enabled** (the option may be hidden on your board — see the README/wiki reference to "Enabling hidden 4G decoding").
- **CSM must be off**, and some boards also need the **DSDT patch** (the Skylake MMIO patch comment doesn't flag it, but the Sandy/Ivy and Haswell/Broadwell equivalents do — worth verifying on your board).

## Verdict

**Yes**, `UEFIPatch/patches.txt` contains the fix for this exact class of Z170 PCI resource-allocation failure — specifically the Skylake "512GB MMIO space" patch plus the `<64GB BAR limit removal` and "don't downgrade 64-bit BARs" patches. The `ReBarDxe` module itself is only the ReBAR part, not the resource fix.