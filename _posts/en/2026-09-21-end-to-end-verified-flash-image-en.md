---
audio: false
generated: true
image: false
lang: en
layout: post
title: End-to-End Verified Flash Image
translated: false
type: note
---

Everything verified end-to-end. Your **final flash-ready image** is ready:

**`/home/lzw/Downloads/B75/rebar-work/b75_modded.bin.patched`**

## Final verification (all in the `.patched` file)

| Check | Result |
| --- | --- |
| ReBarDxe inserted (GUID `A8EE1777…`, DXE driver) | ✅ module #183 |
| AmiBoardInfo DSDT patched (PE32 = `AmiBoardInfoMod.efi`) | ✅ md5 `3fe6c7c2…` |
| PciBus `<16GB` → `<64GB` BAR limit removed | ✅ |
| PciHostBridge 16GB → 64GB MMIO | ✅ |
| PciHostBridge 4GB `PciRootBridgeIo.Mem` limit removed | ✅ ×2 |

## What's left (on the physical machine)

1. **Flash** — boot a FreeDOS USB with your `fpt.exe` + `fparts.txt`, then:
   ```
   fpt -f b75_modded.bin.patched
   ```
   ⚠️ Keep `B75V101_original.bin` safe — don't power off during flash.

2. **BIOS setup** — enable **Above 4G Decoding**, disable **CSM**.

3. **Set BAR size** (as root, on this Linux box):
   ```bash
   cd /home/lzw/Downloads/B75/rebar-work
   sudo ./ReBarState    # type 32 (unlimited), then reboot
   ```

4. **Verify**:
   ```bash
   sudo dmesg | grep -i "root bus resource"   # last mem window should end ≥ 0xfffffffff
   sudo dmesg | grep -i bar
   ```
   or GPU-Z on Windows.

If it won't POST after setting a BAR size: **clear CMOS** (pull the battery if needed) — that disables ReBAR.

Good luck! Want me to prep a FreeDOS USB image layout (folder structure + the flash command in a `flash.bat`), or build a Windows `ReBarState.exe` too?