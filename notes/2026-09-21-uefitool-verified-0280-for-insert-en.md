---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFITool Verified, 0.28.0 for Insert
translated: false
type: note
---

Downloaded and verified. It's now at `/tmp/uefitool/ueefitool` (UEFITool NE A75, Linux x64, ~4.8 MB) and it launches fine (GUI opened; Qt libs all resolve).

⚠️ **Important:** UEFITool **NE** (A75) does **not** support inserting new modules — the "Insert after" feature doesn't exist in the NE branch. For the ReBarDxe insertion step you still need the **non-NE UEFITool 0.28.0**, which I already downloaded earlier at:

- `/tmp/ueefitool/UEFITool.zip` → contains `UEFITool` (0.28.0, non-NE)

So your tooling is now complete:

| Tool | Purpose | Location |
| --- | --- | --- |
| **UEFITool 0.28.0 (non-NE)** | Insert `ReBarDxe.ffs` + replace DSDT PE32 | `/tmp/ueefitool/UEFITool.zip` |
| UEFITool NE A75 | View/verify, extract (no insert) | `/tmp/ueefitool/ueefitool` |
| UEFIExtract NE A75 | CLI dump (already used) | `/tmp/ueefitool/ueefiextract` |
| UEFIFind NE A75 | CLI search | `/tmp/ueefitool/ueefifind` |
| UEFIPatch 0.28.0 | Apply the 4 Sandy/Ivy patches | `/home/lzw/Downloads/B75/rebar-work/UEFIPatch` |

Unzip the 0.28.0 one and use **that** for Step 1 in the guide:

```bash
cd /tmp/ueefitool && unzip -o UEFITool.zip && ./UEFITool
```

Want me to unzip it now, or copy both tools into your `~/Downloads/B75/rebar-work/` folder so everything is in one place?