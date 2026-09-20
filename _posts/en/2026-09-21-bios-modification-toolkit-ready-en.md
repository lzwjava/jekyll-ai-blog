---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Modification Toolkit Ready
translated: false
type: note
---

Done. Everything is unzipped and staged in one folder:

**`/home/lzw/Downloads/B75/rebar-work/`** now contains:

| File | Use |
| --- | --- |
| `UEFITool-0.28.0` | **Main GUI** — "Insert after" + "Replace body" |
| `UEFITool-NE-A75` | GUI — view/verify/extract only |
| `uefiextract`, `uefifind` | CLI dump / search |
| `UEFIPatch` + `patches.txt` | Apply the 4 Sandy/Ivy patches |
| `ReBarDxe.ffs` | Driver to insert |
| `AmiBoardInfoMod.efi` | DSDT-patched module to replace |
| `ReBarState` | BAR size config tool |
| `B75V101_original.bin` | Your backup BIOS |

All binaries are executable and their dependencies resolve (both GUI tools, verified).

Start Step 1 with:

```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFITool-0.28.0
```

Then follow the README (`README-NEXT-STEPS.md`): insert `ReBarDxe.ffs` after **CRBSMI**, replace the **AmiBoardInfo** PE32 with `AmiBoardInfoMod.efi`, save, run `./UEFIPatch b75_modded.bin patches.txt`, and flash the resulting `.patched` file.