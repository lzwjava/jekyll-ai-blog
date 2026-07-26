---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Unrecognized Partition in Windows Setup
translated: false
type: note
---

**Question: Windows 11 Setup says "partition is of an unrecognized type" / "selected volume is offline" — what should I do?**

This is usually because the target SSD has an old partition layout, RAID metadata, dynamic disk state, or leftover OEM/Linux partitions. If you **do not need any data on this disk**, the cleanest fix is to wipe and recreate the Windows partition.

### Method 1 (recommended for a fresh Windows install)

⚠️ This deletes everything on the target disk.

At the Windows Setup screen:

1. Press:

```
Shift + F10
```

2. Open diskpart:

```cmd
diskpart
```

3. Find your disk:

```cmd
list disk
```

Example:

```
Disk 0   1000 GB
Disk 1    512 GB
```

Identify your Lenovo SSD.

4. Select it:

```cmd
select disk 1
```

Verify:

```cmd
detail disk
```

Make sure it is the correct SSD.

5. Wipe partition information:

```cmd
clean
```

6. Create GPT partition:

```cmd
convert gpt
exit
```

Close command prompt.

7. Back in Windows Setup:

* Click **Refresh**
* Select the unallocated space
* Click **Next**

Windows will automatically create:

```
EFI System Partition
MSR Partition
Windows Partition
Recovery Partition
```

---

### If `clean` fails because disk is offline

Run:

```cmd
diskpart

list disk
select disk 1

attributes disk
```

If you see:

```
Current Read-only State: Yes
```

then:

```cmd
attributes disk clear readonly
online disk
```

Try again:

```cmd
clean
```

---

### If the disk is not detected correctly

Check BIOS first.

For Lenovo Xiaoxin:

Enter BIOS:

```
F2
```

Look for:

```
Storage Controller Mode
```

Possible options:

```
RAID
AHCI
```

For a simple Windows install:

```
AHCI
```

is easier.

However, do **not** randomly switch RAID/AHCI if the existing Windows installation matters. For a new installation, AHCI is usually fine.

---

### If you have important data on the disk

Do **not** run:

```cmd
clean
```

Instead:

```cmd
diskpart

list disk
select disk X
detail disk
```

Check whether it contains your files.

You can boot a Linux live USB and inspect:

```bash
lsblk
sudo fdisk -l
```

---

For your case (Lenovo Xiaoxin installing Windows fresh), I would do:

```
Shift + F10
↓
diskpart
↓
list disk
↓
select SSD
↓
clean
↓
convert gpt
↓
install Windows 11 Pro
```

This is the fastest and most reliable path.
