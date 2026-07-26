---
audio: false
generated: true
image: false
lang: en
layout: post
title: Delete All Disk 0 Partitions
translated: false
type: note
---

Question: Should I also delete Disk 0 Partition 0 (the remaining small partition)?

Answer: Yes — delete it too, assuming you want a clean single-OS Windows install on Disk 0.

That "Partition 0" is almost certainly the **EFI System Partition (ESP)** that Mint's GRUB was using, or possibly a small Linux boot/reserved partition. If you leave it:

- Windows *can* technically reuse an existing ESP if it's FAT32 and correctly formatted, but it often still gets flagged because GRUB's boot entries and Windows' expected ESP layout don't match cleanly.
- Simpler and more reliable: delete every partition on Disk 0, leave it 100% unallocated, then let Setup auto-create fresh Recovery + EFI + MSR + Windows partitions in one shot.

Steps:

1. Select **Disk 0 Partition 0**, click **Delete Partition**, confirm.
2. Repeat for any other remaining partition on Disk 0 until it's all unallocated.
3. Select the unallocated space → **Next** (don't manually create partitions).

Don't touch **Disk 1** unless you're also wiping that drive — leave it as-is if it's a second drive you want to keep data on or dual-boot from later.

References:

- [UEFI/GPT-based hard drive partitions - Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions)
