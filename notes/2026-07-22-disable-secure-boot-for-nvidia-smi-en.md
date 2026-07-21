---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Secure Boot for nvidia-smi
translated: false
type: note
---

Agent can't run `reboot` — you'll need to do it from your terminal directly.

On the workstation, run:

```bash
sudo reboot
```

Then during POST (black screen, right after power-on), **tap DEL repeatedly** to enter BIOS.

Inside BIOS:
1. **Settings** → **Security** → **Secure Boot** → **Disabled**
2. **F10** → **Yes** to Save & Exit

Reboot once more, then `nvidia-smi` should work.