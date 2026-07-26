---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 on MacBook Pro 2017
translated: false
type: note
---

Question: Installing Windows 11 directly on the MacBook Pro 2017 itself (via Boot Camp) — how, given no TPM 2.0?

Answer: Doable, but needs a bypass since your 2017 MacBook Pro has no TPM 2.0 chip and its CPU (7th-gen Intel) isn't on Microsoft's supported list either. Here's the practical path:

**1. Check free space** — you'll want 64GB+ partition minimum, ideally 100GB+.

**2. Use Boot Camp Assistant to partition (don't let it create the USB):**

- Open Boot Camp Assistant (Spotlight → "Boot Camp Assistant")
- If it lets you proceed with just partitioning (uncheck "Download Windows support software" / "Create install disk" if it complains about the Windows 11 ISO), do that to carve out the Windows partition.
- If Boot Camp Assistant flat-out refuses your Windows 11 ISO, skip it entirely and manually partition instead: `Disk Utility` → partition your drive, leave the new volume as **MS-DOS (FAT)**, then let Setup reformat it as NTFS later.

**3. Create the bootable USB using balenaEtcher** (from your earlier question) since Boot Camp Assistant's own USB creation tool may reject an unsupported ISO.

**4. Boot from the USB:** Hold `Option (⌥)` at startup → select the EFI USB drive.

**5. At Windows Setup, the moment you hit "This PC doesn't currently meet Windows 11 requirements":**

```
Shift + Fn + F10
```

(MacBook keyboards need `Fn` since F10 alone is a media key). This opens Command Prompt. Then:

```cmd
regedit
```

Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\Setup`, create a key named `LabConfig`, and inside it add these DWORD (32-bit) values, all set to `1`:

```
BypassTPMCheck
BypassSecureBootCheck
BypassRAMCheck
BypassCPUCheck
BypassStorageCheck
```

Close regedit, close cmd, click **Back** then **Next** again in Setup — it'll proceed past the compatibility block.

**6. Install onto the Boot Camp partition** you created, let it finish normally.

**7. After Windows boots, install Apple's Boot Camp drivers** (WiFi, trackpad, audio, GPU) — download via Boot Camp Support Software separately since Boot Camp Assistant's auto-download may also gate on OS version; get the driver pack from a working Mac or search "Boot Camp 6 support software download" if Assistant won't do it.

Caveat worth flagging honestly: Microsoft has tightened bypass enforcement over time, and future Windows Updates on an unsupported config can occasionally break or get blocked — this is a known tradeoff, not a guaranteed-forever setup.

References:

- [Run Windows 11 on MacBook Without TPM - Intel Macs guide](https://www.positioniseverything.net/run-windows-11-on-macbook-without-tpm-step-by-step-guide-for-intel-macs/)
- [Windows 11 24H2 on MacBook without TPM - Mac Observer](https://www.macobserver.com/tips/how-to/install-windows-11-24h2-on-macs-without-tpm/)
