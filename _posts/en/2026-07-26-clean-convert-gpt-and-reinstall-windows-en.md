---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Convert GPT and Reinstall Windows
translated: false
type: note
---

Question: Now in command prompt (via Repair your PC) — what next?

Answer: Run diskpart and redo the clean/convert, same as before:

```cmd
diskpart
list disk
```

Confirm which disk is your main SSD (the ~476GB one).

```cmd
select disk 0
detail disk
```

Check it says **Partition Style: MBR** or **GPT**, and confirms it's the right disk (not the small 14GB Disk 1).

```cmd
clean
convert gpt
exit
```

Close the command prompt window, go back to the main Repair/Setup menu, and boot into the **Windows 11 installer USB** again (not Repair — you need the actual Setup flow to select install location). From there:

1. Get to "Select location to install Windows 11"
2. Click **Refresh**
3. Select the now-unallocated Disk 0
4. Click **Next** — let it auto-create partitions

Then immediately check the partition list before hitting Next again — confirm **EFI System Partition** shows up alongside MSR/Primary/Recovery. That's the thing that was missing last time and caused the boot failure.
