---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 Install Fails on Lenovo Xiaoxin
translated: false
type: note
---

Question: Summary of the whole troubleshooting session so far.

Answer:

**Setup:** Lenovo Xiaoxin, previously Linux Mint, installing Windows 11 fresh. Disk 0 = 476GB UMIS NVMe (main SSD), Disk 1 = small ~14GB drive (ignore, unrelated).

**What we fixed:**
1. Original error — "partition unrecognized type / volume offline" — caused by leftover Linux Mint partition signatures (LVM/RAID) on Disk 0.
2. Fixed via `diskpart`: `clean` → `convert gpt` on Disk 0 (confirmed correct disk each time via `detail disk`).
3. Confirmed BIOS is UEFI-only (no Legacy/CSM toggle needed on this model).
4. Selected Disk 0 unallocated space correctly in Setup, clicked Next — partition selection itself is no longer the problem.

**Current blocker:**
Install now fails during the "Installing Windows" progress phase with a generic "Windows 11 installation has failed" dialog. Log analysis (`setupact.log` / `setuperr.log`) shows:
- Early errors (`0x80070490`, `0x80072EE7`, `0x80070002`) = harmless, just no internet in WinPE — ignore these.
- Real fatal chain: `CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4` — Setup receives a "launch recovery environment" request and self-aborts.
- This happened **twice in a row at the same point**, ruling out accidental keypress as sole cause.

**Not yet tried (next steps):**
1. Re-download Windows 11 ISO fresh from Microsoft.
2. Re-flash a **different** USB stick with Rufus (GPT + UEFI target) — current USB media is now the top suspect.
3. Run the install completely hands-off (no keyboard/trackpad touch) from progress bar to OOBE.
4. If it fails identically a third time with fresh ISO + fresh USB + no touching → likely hardware issue (RAM or NVMe controller), not media/software — would need memory test (`Windows Memory Diagnostic` or MemTest86) and NVMe health check (`nvme-cli` or manufacturer tool) at that point.

**Not needed:** extending/manually creating partitions — Setup's auto-partitioning of unallocated space is correct and not the issue.
