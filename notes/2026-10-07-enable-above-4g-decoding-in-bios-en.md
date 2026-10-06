---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable Above 4G Decoding in BIOS
translated: false
type: note
---

Diagnosis is now definitive. Here's the raw proof from the GPU's PCI config space:

```
BAR0 = 90000000            ← 16MB MMIO (assigned)
BAR1 = 0000000c            ← 64-bit prefetchable, size huge (32GB), UNASSIGNED (address=0)
BAR2 = 00000000            ← upper half of BAR1
BAR3 = 0000000c            ← another 64-bit prefetchable BAR, UNASSIGNED
BAR4 = 00000000            ← upper half of BAR3
BAR5 = 00000000
```

And the root PCIe bridge's 64-bit prefetchable window is **`[disabled]`**. So the Tesla M40 24GB's 32GB memory BAR is being left unassigned because the motherboard isn't reserving MMIO space above 4GB. `pci=realloc` can't fix this — **it must be enabled in the BIOS.**

## 🔧 The fix: enable "Above 4G Decoding" in BIOS

1. Reboot and press **DEL** to enter BIOS setup (MSI Z170A GAMING M3).
2. Press **F7** for Advanced mode.
3. Go to **Settings → Advanced → PCI Subsystem Settings** (or "PCIe/PCI Subsystem Settings").
4. Set **"Above 4G Decoding"** → **Enabled**.
   - On some MSI boards this is called **"Above 4G memory/Crypto Currency mining"** — enable it.
5. **Save & Exit** (F10).

> ⚠️ If you **don't see** that option, your BIOS (A.50, from Feb 2016) is too old — MSI added "Above 4G Decoding" to Z170 boards in later BIOS versions (mining-era updates). In that case we'll need to flash a newer BIOS. Let me know and I'll find the exact latest BIOS file and give you flashing steps.

## After that, I'll re-check remotely

Once you've enabled it and booted back into Debian, tell me and I'll verify the BARs are assigned and run `nvidia-smi`. The driver itself (550.163.01) is already correctly installed and supports this card — only the BAR allocation is blocking it.

---

**Quick summary of where we are:**

| Item | Status |
| --- | --- |
| `lzw` in sudo group | ✅ |
| NVIDIA driver 550.163.01 installed (supports Tesla M40) | ✅ |
| DKMS module built for 6.12 kernel | ✅ |
| GPU detected on PCI bus | ✅ (`10de:17fd`) |
| GPU usable | ❌ — blocked by BIOS not assigning the 32GB BAR |

Go ahead and check the BIOS — does the "Above 4G Decoding" option exist?
