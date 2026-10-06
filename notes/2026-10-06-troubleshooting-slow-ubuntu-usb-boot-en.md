---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting Slow Ubuntu USB Boot
translated: false
type: note
---

Question: **Why is my Ubuntu USB booting slowly / showing all these errors?**

Answer: The screenshot shows **two separate problems**, and the main one is your USB/live Ubuntu environment.

### 1. Your Windows NTFS disk was not cleanly shut down

You have:

```text
The disk contains an unclean file system (0, 0).
Metadata kept in Windows cache, refused to mount.
Falling back to read-only mount because the NTFS partition is in an unsafe state.
Please resume and shutdown Windows fully (no hibernation or fast restarting).
```

This means Ubuntu detected an NTFS partition that Windows left in a **hibernated / fast-startup / unclean state**.

If that is your Windows SSD/HDD, boot Windows once and do:

```powershell
shutdown /s /t 0
```

Then boot the Ubuntu USB again.

Also disable Windows Fast Startup if necessary.

---

### 2. More importantly: your Ubuntu live USB's persistence partition has an error

This line is significant:

```text
EXT4-fs (sdb4): Could not load journal inode
mount: mounting /dev/disk/by-label/writable on /log-persistence failed: Invalid argument
```

Your USB is apparently `/dev/sdb`, and:

```text
/dev/sdb4
```

is the Ubuntu live USB's **writable/persistence partition**.

Ubuntu tried to mount it at:

```text
/log-persistence
```

but the ext4 filesystem's journal could not be loaded.

That usually means **filesystem corruption** or a damaged/incorrectly-created persistence partition.

So if you created this Ubuntu USB with persistence, this is likely the real problem.

---

### 3. Why is it sitting at `Get: ... file:/cdrom ...`?

At the bottom:

```text
Ign:1 file:/cdrom resolute InRelease
Get:2 file:/cdrom resolute Release
Get:3 file:/cdrom resolute Release.gpg
Get:4 file:/cdrom resolute/restricted amd64 Packages
Get:5 file:/cdrom resolute/main amd64 Packages
```

This is actually **normal for a live Ubuntu system**.

`file:/cdrom` means:

> "Use the Ubuntu installation ISO mounted from the USB as an APT package source."

It's not downloading those packages from the Internet. It's reading the package metadata **from the USB**.

If your USB is slow or having I/O problems, this can be extremely slow.

---

### The interesting clue

You previously said:

> the Ubuntu USB progress bar runs for half an hour

Combined with this screenshot, I'd strongly suspect the **USB drive / USB filesystem**, rather than your motherboard or SSD.

You have:

```text
/dev/sdb4
EXT4 journal error
```

and the system is also reading:

```text
file:/cdrom
```

So the boot environment may be spending a long time doing USB I/O/recovery.

### What I would do

If you don't need anything stored on this USB:

```text
1. Re-create the Ubuntu USB
2. Use a different USB flash drive if possible
3. Don't enable persistence initially
4. Boot it
5. Check whether Ubuntu becomes normal/fast
```

Then inside Ubuntu:

```bash
lsblk -f
sudo dmesg | grep -Ei 'usb|sdb|error|ext4|I/O'
```

The second command is particularly useful. If you see things like:

```text
I/O error
Buffer I/O error
reset SuperSpeed USB device
blk_update_request
EXT4-fs error
```

then we can determine whether the **USB stick itself is failing** or whether the persistence filesystem was simply created incorrectly.

**I would not blame your SSD yet.** The screenshot points much more strongly at `/dev/sdb4` / the Ubuntu USB environment.
