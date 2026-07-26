---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing GPT Disk Layout for Windows 11
translated: false
type: note
---

Question: Analyze `diskpart list partition` — is the disk layout causing Windows 11 install failure?

Answer:

This screenshot is very useful. Your SSD layout is:

```
Disk 0 (476 GB GPT)

Partition 1   Reserved   16 MB
Partition 2   Primary    476 GB
```

This is **not a normal Windows 11 UEFI layout**.

A correct clean Windows 11 GPT disk normally becomes:

```
Partition 1   EFI System      ~100 MB   FAT32
Partition 2   Microsoft MSR    16 MB
Partition 3   Windows          NTFS
Partition 4   Recovery         ~500 MB-1GB
```

Your disk currently has:

```
MSR 16 MB
+
one huge primary partition
```

Missing:

* EFI System Partition (ESP) ❌
* Recovery partition ❌

This explains the installation failure much better than VMD.

---

## Fix

Since you are doing a clean install, wipe the disk.

In the same command prompt:

```cmd
diskpart

select disk 0

clean

convert gpt

exit
```

Then close CMD.

In Windows Setup:

1. Click **Refresh**
2. Select the **Unallocated Space**
3. Click **Next**

Do **not** manually create partitions.

Windows Setup will automatically create:

```
EFI
MSR
Windows
Recovery
```

---

## Why this happened

Most likely the previous partition was created by:

* old Linux install
* previous Windows clone
* Lenovo recovery modification
* manual partitioning

The installer tried to upgrade/install into an existing GPT layout without a valid EFI boot partition, then failed later with:

```
0xC19001F4
```

---

At this point:

* USB ✅ confirmed good
* SSD detected ✅
* VMD ❌ less likely
* Disk layout ❌ likely root cause

I would do the `clean + convert gpt` now. This is the highest-probability fix.
