---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Ubuntu Boot Errors: Are They Serious?"
translated: false
type: note
---

Question: **What is happening in this Ubuntu installation/boot screen, and are these errors serious?**

Answer: **There are several different messages here. Most are warnings, but two are worth paying attention to.**

### 1. GPT/PMBR mismatch

You have:

```text
GPT PMBR size mismatch (12732371 != 30719999) will be corrected by write.
The backup GPT table is not on the end of the device.
The backup GPT table is corrupt, but the primary appears OK, so that will be used.
```

This means the USB/disk's **GPT partition metadata doesn't match the actual disk size**.

For example:

```text
GPT thinks disk ≈ 12.7 GB
actual disk ≈ 30.7 GB
```

This commonly happens when:

* an image was written to a USB drive of a different size
* a disk was cloned
* the disk size changed
* the GPT backup header wasn't moved to the physical end of the disk

The important line is:

```text
the primary appears OK, so that will be used.
```

So **this alone doesn't mean the USB is dead**. The installer can often repair it automatically.

---

### 2. More concerning: EXT4 journal error

You have:

```text
EXT4-fs (sda4): Could not load journal inode
```

This means Linux tried to mount `/dev/sda4` as an ext4 filesystem and **couldn't load its journal**.

If `/dev/sda4` is the partition you're trying to install Ubuntu onto, this can indicate:

* corrupted filesystem
* interrupted previous installation
* damaged filesystem metadata
* potentially a failing disk

If you're installing fresh and **don't need anything on that disk**, the simplest solution is usually to completely recreate the partition/filesystem rather than trying to preserve the old ext4 filesystem.

---

### 3. This is probably why you're seeing the long pause

At the bottom:

```text
Get:1 file:/cdrom ...
Get:2 file:/cdrom ...
Get:3 file:/cdrom ...
Get:4 file:/cdrom ...
Get:5 file:/cdrom ...
```

This is actually Ubuntu's package system reading packages from the **installation USB/live CD**:

```text
file:/cdrom
```

So it's not necessarily downloading from the Internet.

The earlier:

```text
A connection to the bus can't be made
```

and

```text
fuse: device /dev/fuse not found
```

are generally **not the reason to panic** in this situation.

---

## What I would do

If this is your **old/test machine and you don't need the data on `/dev/sda`**, I would stop trying to preserve the existing filesystem.

Boot the Ubuntu installer and choose:

**Erase disk and install Ubuntu**

That will recreate the partition table/filesystems cleanly.

If you specifically want to diagnose the disk first, from a live terminal:

```bash
lsblk -f
sudo fdisk -l
sudo smartctl -a /dev/sda
```

and for the ext4 partition:

```bash
sudo e2fsck -f /dev/sda4
```

**Do not run `e2fsck` on a mounted filesystem.**

### The key distinction

| Message                                    | Meaning                              | Serious?                       |
| ------------------------------------------ | ------------------------------------ | ------------------------------ |
| GPT PMBR mismatch                          | GPT metadata doesn't match disk size | Usually fixable                |
| Backup GPT not at end                      | GPT needs relocation/repair          | Usually fixable                |
| Backup GPT corrupt, primary OK             | Backup partition table damaged       | Repairable if primary is valid |
| `EXT4-fs ... Could not load journal inode` | ext4 filesystem problem              | **Worth fixing**               |
| `file:/cdrom` package messages             | Installer reading USB media          | Normal                         |
| `/dev/fuse not found`                      | FUSE unavailable in this environment | Usually irrelevant             |

**If the progress bar has been sitting there for ~30 minutes with no change, I would not assume it is normal.** Given the GPT + ext4 errors together, I'd first verify whether the USB and target disk are healthy rather than waiting indefinitely.
