---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Kernel Panic After pci=realloc
translated: false
type: note
---

The machine is **not coming back** — 100% ping loss and "Host is down" after ~7 minutes. The `pci=realloc` change (or the reboot itself) has left it unbootable/off, so this now needs physical access to recover.

## What happened (summary)

| Step | Result |
|---|---|
| Added `lzw` to sudo | ✅ |
| Installed `nvidia-driver` 550.163.01 (DKMS built for 6.12 kernel) | ✅ |
| Loaded modules | ✅ (`nvidia`, `nvidia_uvm`) |
| `nvidia-smi` | ❌ "No devices were found" |
| Root cause | GPU's large BARs (BAR1–5) unallocated → `NVRM: This PCI I/O region ... is invalid` |
| Fix attempt | Added `pci=realloc` to GRUB + reboot |
| Result | ❌ Host now unreachable |

## What you need to do at the machine

**1. Check it's powered on** — look for fans/LEDs/screen. If off, press the power button.

**2. Recover from a boot hang** (most likely):
- Interrupt GRUB: during the 5s GRUB screen, or press/repeat **Shift** (or **Esc**) at startup to get the menu.
- Highlight the Debian entry → press **`e`** to edit.
- Find the line starting with `linux` and **delete `pci=realloc`**.
- Press **Ctrl+X** (or F10) to boot.

**3. Once it's back up**, tell me and I'll revert the GRUB change remotely so a normal reboot works again.

## The proper fix (BIOS — needs you at the machine anyway)

`pci=realloc` was the "software workaround." The real fix for a 24GB Tesla M40's large BAR is in the BIOS:

- Enter BIOS (DEL key at startup) on the **MSI Z170A GAMING M3**
- **Settings → Advanced → PCI Subsystem Settings → "Above 4G Decoding" → Enabled**
- Save & exit.

With "Above 4G Decoding" enabled, the board will properly assign the M40's BARs and `nvidia-smi` should detect it.

---

**Do you have access to the machine right now?** If so, try step 1–2 and let me know what the screen shows — I'll guide you from there. If the screen shows a GRUB menu or an error, tell me the exact text.
