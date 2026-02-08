---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Restore Windows 10 on Lenovo Xiaoxin
translated: false
type: note
---

If you've installed Ubuntu on your Lenovo Xiaoxin and want to get Windows 10 back, here are your main options:

**Option 1: Dual Boot (Keep Both)**
If you want both Windows 10 and Ubuntu on your machine, you can use your bootloader to switch between them. When you restart your computer, you should see a boot menu (usually GRUB) that lets you choose which OS to load. This is the easiest if you want to keep both systems.

**Option 2: Reinstall Windows 10 (Erase Ubuntu)**
If you want Windows 10 back as your only OS, you'll need to:
1. Back up any important files from Ubuntu first
2. Create a Windows 10 installation USB drive on another computer using the Windows Media Creation Tool (downloadable from Microsoft)
3. Boot from that USB drive and reinstall Windows 10, which will overwrite Ubuntu
4. During installation, you can format the drive to completely remove Ubuntu partitions

**Option 3: Use Your Original Recovery Partition**
Lenovo laptops often come with a recovery partition or recovery media. Check if you have:
- Lenovo Vantage app (if Windows is still accessible)
- Original recovery DVDs or USB that came with your laptop
- A hidden recovery partition on the drive

If you have these, you might be able to restore Windows 10 to factory settings without needing an installation disk.

**What you'll need:**
- Windows 10 installation media or recovery media
- Another computer to create the installation USB
- Time for the installation process

Which option sounds most suitable for what you want to do?