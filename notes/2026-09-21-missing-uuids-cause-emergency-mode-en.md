---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing UUIDs Cause Emergency Mode
translated: false
type: note
---

Question: Why is this Linux machine stuck in emergency mode?

Answer: The screen shows **two filesystem UUIDs referenced by the boot configuration that no longer exist**:

```text
Warning: /dev/disk/by-uuid/2B6A-70B5 does not exist
Warning: /dev/disk/by-uuid/bba45be2-f8c5-4745-8438-f62d853a3198 does not exist
```

This almost certainly means `/etc/fstab` contains entries for disks/partitions that Linux cannot currently find.

### What to do

Press **Enter** to get the maintenance shell, then run:

```bash
lsblk -f
blkid
cat /etc/fstab
```

The important comparison is:

```text
/etc/fstab          <-- UUIDs Linux expects
blkid / lsblk -f    <-- UUIDs that actually exist
```

You'll probably find something like:

```fstab
UUID=2B6A-70B5    /some/mount    ...
UUID=bba45be2-...  /another/mount ...
```

but those UUIDs aren't present in `blkid`.

### If these are just old/missing disks

Back up `fstab`:

```bash
cp /etc/fstab /etc/fstab.bak
```

Then edit it:

```bash
nano /etc/fstab
```

Comment out the stale lines by putting `#` at the beginning:

```fstab
# UUID=2B6A-70B5 ...
# UUID=bba45be2-...
```

Then test:

```bash
mount -a
```

If that returns without errors:

```bash
reboot
```

### If you *expect* those disks to exist

Don't delete the `fstab` entries yet. Check:

```bash
lsblk -o NAME,SIZE,FSTYPE,UUID,MOUNTPOINTS
```

If the physical disk is missing entirely, it could be:

* an unplugged external drive
* a failed/unrecognized drive
* a changed BIOS/VM disk configuration
* a partition that was recreated, giving it a new UUID

If the disk exists but has a **different UUID**, update `/etc/fstab` to the new UUID instead.

**The key point:** this isn't primarily a kernel failure—the boot process is refusing to continue because required filesystems specified in `/etc/fstab` cannot be found.

If you paste the output of these three commands:

```bash
lsblk -f
blkid
cat /etc/fstab
```

I can tell you **exactly which `fstab` lines to change**.
