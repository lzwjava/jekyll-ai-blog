---
audio: false
generated: true
image: false
lang: en
layout: post
title: B75 ReBAR BIOS Patch Steps
translated: false
type: note
---

Done. I took your `B75V101.bin`, analyzed it, ran UEFIPatch, and prepared everything that can be done headlessly. Here's the status and your exact next steps.

## What I found in your B75 (Ivy Bridge) BIOS

- **UEFIPatch matched 4 Sandy/Ivy patches** (verified in the decompressed modules):
  - Replace 16 GB MMIO → full 64 GB (PciHostBridge)
  - Remove `<16 GB` BAR limit (PciBus)
  - Remove 4 GB `PciRootBridgeIo.Mem` limit (PciHostBridge, ×2)
- **Your DSDT has the hard-coded 16 GB MMIO limit** (`M2LN = 0x0000000400000000`) — the exact "Gigabyte B75M-D3H" pattern from the wiki. Since patch #1 was applied, **the DSDT patch is required** or Windows will fail with 4G decoding on.
- **I already patched the DSDT**: decompiled → modified → recompiled with `iasl` (0 errors) → rebuilt via `AmiBoardInfoTool` → produced `AmiBoardInfoMod.efi`.
- Insertion target confirmed: the driver goes into the inner DXE volume (`8C8CE578-...`), **after the last module "CRBSMI" (#182)**.

## Everything is staged in `/home/lzw/Downloads/B75/rebar-work/`

`B75V101_original.bin` (backup), `ReBarDxe.ffs`, `ReBarState`, `AmiBoardInfoMod.efi`, `UEFIPatch` + `patches.txt`, plus a full `README-NEXT-STEPS.md`.

## What YOU do next (2 GUI clicks, 1 command, then flash)

**1. UEFITool 0.28.0 (non-NE) GUI** — open `B75V101_original.bin`:
- Search header-only GUID `3C1DE39F-D207-408A-AACC-731CFB7F1DD7` (PciBus) → jump to the DXE volume → right-click **CRBSMI** (last module) → **Insert after** → `ReBarDxe.ffs`
- Search header-only GUID `9F3A0016-AE55-4288-829D-D22FD344C347` (AmiBoardInfo) → open Compressed section → PE32 image section → **Replace body** → `AmiBoardInfoMod.efi`
- Save as `b75_modded.bin`

**2. Patch it (already tested, will print "Image patched" with 4 patches):**
```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFIPatch b75_modded.bin patches.txt
```
→ produces **`b75_modded.bin.patched`** ← flash this one.

**3. Flash** from FreeDOS USB with your vendor's `fpt.exe` (`fpt -f b75_modded.bin.patched`, same as their `1.BAT`). ⚠️ Risky — keep the original.

**4. In BIOS:** enable **Above 4G Decoding**, disable **CSM**.

**5. Set BAR size (as root):**
```bash
sudo ./ReBarState    # type 32 = unlimited
```

**6. Verify:** `sudo dmesg | grep -i "root bus resource"` (last mem entry should end ≥ `0xfffffffff`) or GPU-Z on Windows.

Want me to also build a **Windows ReBarState.exe**, or help you make the FreeDOS boot USB layout for `fpt`?