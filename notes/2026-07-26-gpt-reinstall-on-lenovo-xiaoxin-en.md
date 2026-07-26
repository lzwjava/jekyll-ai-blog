---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT Reinstall on Lenovo Xiaoxin
translated: false
type: note
---

## ✅ Done — Reinstalled with GPT

### What Changed

| Before | After |
|---|---|
| **MBR** partition style | **GPT** partition style |
| Ventoy default Secure Boot | Ventoy default Secure Boot (still enabled) |
| Win10 ISO copied | Win10 ISO copied (5.8G) |

### On Your Lenovo Xiaoxin — Do This

1. **Boot** → press **F2** to enter BIOS setup
2. **Security tab** → **Secure Boot** → **Disabled**
3. **Boot tab** → **Boot Mode** → **UEFI** (not Legacy)
4. **Save & Exit** (F10)
5. Immediately press **F12** for boot menu
6. You should now see **UEFI: <USB name>** in the list
7. Select it → Ventoy menu → `Win10_22H2_English_x64v1.iso` → Enter

If it **still doesn't show up**, try these in BIOS:
- **USB Boot** → **Enabled**
- **XHCI Hand-off** → **Enabled**
- Try a **USB 2.0 port** instead of USB 3.0 (sometimes matters on older Xiaoxin models)