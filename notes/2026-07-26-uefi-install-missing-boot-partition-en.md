---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFI Install Missing Boot Partition
translated: false
type: note
---

Question: Install failed and rebooted back to the partition screen — Disk 0 now shows MSR + 476.9GB Primary (no EFI System Partition), and there's a separate Disk 1 with a leftover 200MB System + 14.5GB "WIN11" partition — what's wrong?

Answer: Two things stand out here that explain the failure:

**1. Disk 0 is missing its EFI System Partition.**
A proper UEFI/GPT Windows layout needs 4 partitions: **EFI System Partition (FAT32, ~100–260MB)**, MSR (16MB), Primary (Windows), and Recovery. Your Disk 0 only has **MSR + Primary** — no ESP. That pattern (MSR + Primary, no ESP) is what Setup creates when it thinks it's doing a **Legacy/MBR-style install**, but you already ran `convert gpt` in diskpart. So now you have a GPT disk with an MBR-style partition layout — the firmware can't find a bootloader after the first reboot, which is exactly why it fails after restart.

→ **Fix: check BIOS boot mode.**
Reboot into BIOS (`F2` or `Novo button` on Xiaoxin), find **Boot Mode / UEFI/Legacy Boot**, and make sure it's set to **UEFI only** (disable CSM/Legacy/Compatibility Support Module). If it's currently on Legacy or "Both", that's the root cause.

**2. Disk 1 is a second, tiny (14.7GB) drive with a half-finished Windows install on it.**
That "200MB System + 14.5GB Primary: WIN11" is leftover from install attempt(s) landing on the wrong disk — 14.5GB is **too small for Windows 11** (needs 20GB+ minimum, realistically 64GB+). This is likely your Xiaoxin's eMMC/cache storage, not the main SSD. Ignore/don't touch it as install target — your real target is Disk 0 (the 476GB one).

**Steps to redo cleanly:**

1. Enter BIOS → set **UEFI boot mode**, disable CSM/Legacy → save & reboot back into Setup.
2. On Disk 0: select **Partition 1 (MSR)** → Delete. Select **Partition 2 (476.9GB Primary)** → Delete. Now Disk 0 = fully unallocated.
3. Select the unallocated space on Disk 0 → **Next** (let Setup auto-create all 4 partitions this time — you should now see EFI System Partition appear).
4. Do NOT select Disk 1 at all.

If BIOS was already set to UEFI-only and this still happens, tell me and we'll check if Secure Boot or a fast-boot setting is interfering instead.
