---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFITool Modding Guide
translated: false
type: note
---

Open **`UEFITool-0.28.0`** (the non-NE one).

NE-A75 does **not** have "Insert after" — that feature is missing in the NE branch, and inserting `ReBarDxe.ffs` is exactly what you need to do first.

Run:

```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFITool-0.28.0
```

Then in the GUI:

1. `File → Open image file…` → `B75V101_original.bin`
2. `File → Search…` → **Header only** → **GUID** → `3C1DE39F-D207-408A-AACC-731CFB7F1DD7` → double-click the result
3. In the tree, scroll to the bottom of that volume → last module **CRBSMI** → right-click → **Insert after…** → `ReBarDxe.ffs`
4. Then search GUID `9F3A0016-AE55-4288-829D-D22FD344C347` (AmiBoardInfo) → open **Compressed section → PE32 image section** → right-click the PE32 section → **Replace body…** → `AmiBoardInfoMod.efi`
5. `File → Save image file…` → `b75_modded.bin`

Keep NE-A75 around only for viewing/verifying later (e.g. checking pad files).