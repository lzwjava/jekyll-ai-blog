---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Repair and Disk Partition Issues
translated: false
type: note
---

Question: Does Windows Setup's "Repair your computer" option help with the disk/partition issue?

Answer: Yes — it's actually a cleaner path to the same diskpart tools you've been using via `Shift+F10`, plus a few automated repair options:

**Repair your computer → Troubleshoot → Advanced options** gives you:

- **Startup Repair** — auto-scans for boot config issues (BCD, boot sector). Won't fix a missing ESP/wrong partition table, but worth trying after your next successful install if boot fails again.
- **Command Prompt** — same as `Shift+F10`, gives you diskpart access. No functional difference, just a menu path instead of a shortcut.
- **System Restore / System Image Recovery** — irrelevant here, no OS installed yet.
- **UEFI Firmware Settings** — this one's useful: jumps straight into BIOS setup without needing to catch the boot key at power-on. Use this instead of hunting for F2/Novo button timing.

**For your specific situation** (missing ESP after clean/convert gpt), Repair your PC won't auto-fix it — it's for repairing an *existing broken install*, not creating partitions from scratch. Your fastest path is still:

1. Boot the Windows 11 USB installer (not "Repair")
2. `Shift+F10` → diskpart → `clean` → `convert gpt` → exit
3. Refresh → select unallocated space → Next
4. **Check the partition list Setup creates before clicking Next again** — confirm you see EFI System Partition, MSR, Primary, and Recovery all four listed. If ESP is missing again, something is actively stopping Setup from creating it (worth checking Secure Boot state at that point via UEFI Firmware Settings).

So: use "Repair your PC → UEFI Firmware Settings" as a shortcut into BIOS, but do the actual disk work from the main Setup installer, not from Repair.
