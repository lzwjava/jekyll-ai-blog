---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safe Graphics Won't Help Disk Errors
translated: false
type: note
---

Question: **Will choosing “Ubuntu (safe graphics)” help with this installation problem?**

Answer: **Probably not for the errors shown in your screenshot.**

“Ubuntu (safe graphics)” mainly changes the **GPU/display driver initialization**. It adds parameters like:

```bash
nomodeset
```

which disables advanced GPU acceleration during boot.

It helps when you have problems like:

* black screen after Ubuntu logo
* frozen graphical installer
* NVIDIA/AMD GPU driver crash
* display resolution problems

It **does not fix**:

```text
GPT PMBR size mismatch
backup GPT table is corrupt
EXT4-fs: Could not load journal inode
```

Those are **disk partition/filesystem problems**, not graphics problems.

---

However, because you are installing Ubuntu and the screen is hanging, trying safe graphics is reasonable:

1. Boot menu:

```
Try or Install Ubuntu
Ubuntu (safe graphics)
```

2. If safe graphics reaches the desktop/installer, then your GPU driver was the problem.

3. If you still see:

```
EXT4-fs (sda4): Could not load journal inode
```

then the disk/partition is the problem.

---

Given your screenshot, I suspect:

```
USB installer -> OK
GPU -> probably OK
Target disk (/dev/sda) -> suspicious
```

I would check after entering the live Ubuntu desktop:

```bash
lsblk
```

Find the target disk, then:

```bash
sudo smartctl -a /dev/sda
```

(if `smartctl` exists)

and:

```bash
sudo fdisk -l /dev/sda
```

The GPT mismatch often happens because an old Ubuntu install or cloned image was left on that disk. If you don't need old data, a fresh erase during installation is the cleanest fix.
