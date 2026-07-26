---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Plan for Lenovo USB Issue
translated: false
type: note
---

USB not detected yet — plug it in and I'll proceed.

In the meantime, here's the fix plan:

### Why Lenovo Xiaoxin Doesn't See It

| Cause | Fix |
|---|---|
| **MBR partition style** (Ventoy default) | Reinstall with `-g` flag → **GPT** |
| **Secure Boot** blocking unsigned bootloader | Either disable in BIOS or reinstall Ventoy with `-S` (no Secure Boot) |

### Fix Steps (once USB is plugged in)

```bash
sudo /tmp/ventoy-1.1.17/Ventoy2Disk.sh -I -g /dev/sdb   # Force GPT install
```

Then re-copy the ISO and done.

Also, in your Lenovo BIOS:
- Press **F2** on boot → **Security** tab → **Secure Boot** → **Disabled**
- **Boot** tab → **Boot Mode** → **UEFI** (not Legacy)
- Save & exit → press **F12** → the USB should now appear

Plug the USB in and I'll execute.