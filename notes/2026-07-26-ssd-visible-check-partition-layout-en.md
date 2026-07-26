---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSD Visible, Check Partition Layout
translated: false
type: note
---

Question: `diskpart list disk` shows Disk 0 (476GB) and USB Disk 1 (14GB). Does this confirm VMD/RST?

Answer:

This result is actually useful:

```
Disk ###  Status   Size
------------------------
Disk 0   Online    476 GB
Disk 1   Online     14 GB
```

Conclusions:

✅ The NVMe SSD is visible in Windows PE
✅ The USB installer is visible
✅ The storage controller is not completely hiding the disk

So **this is not the classic "Windows installer cannot see SSD because VMD driver missing" case**.

The VMD theory becomes less likely.

---

The next thing to check is the partition layout.

Run:

```cmd
diskpart

select disk 0

list partition

list volume
```

Send the screenshot.

---

Given your previous logs:

```
Setup Phase: [4]
0xC19001F4
```

and now:

```
Disk 0 visible
```

my suspicion moves toward:

### 1. Old GPT/EFI partition metadata (highest)

Your earlier error:

```
partition is of an unrecognized type
volume is offline
```

strongly points here.

If this is a clean install and you don't need existing data, do:

```cmd
diskpart

select disk 0

clean

convert gpt

exit
```

Then click Refresh in Windows Setup and install.

This will recreate:

```
EFI       FAT32    ~100MB
MSR       16MB
Windows   NTFS
Recovery  ~1GB
```

---

### 2. Check BIOS boot mode

In BIOS:

```
Boot Mode: UEFI
Legacy Boot: Disabled
CSM: Disabled
Secure Boot: temporarily Disabled
```

Windows 11 expects UEFI + GPT.

---

### 3. One more useful check

Run:

```cmd
diskpart

select disk 0

detail disk
```

Look for:

```
Partition Style : GPT
```

or:

```
Dynamic Disk : Yes
```

If it says Dynamic, that explains the previous "unrecognized type" problem.

---

At this point I would **not chase VMD anymore**. Your SSD visibility proves the installer can communicate with the storage. I would check `list partition` and then likely do the GPT clean install.
