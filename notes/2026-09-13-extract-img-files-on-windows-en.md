---
audio: false
generated: true
image: false
lang: en
layout: post
title: Extract .img Files on Windows
translated: false
type: note
---

Question: How to extract/inspect an `.img` file in Windows?

Answer:

`.img` files are similar to ISO but more varied — they can be raw disk images, Raspberry Pi images, or Android images. Here's how to handle them:

---

## Method 1: 7-Zip — Simplest Way
Works for many `.img` files:
1. Right-click the `.img` file
2. Hover **"7-Zip"** → **"Extract Here"**
3. ✅ Done — if the format is supported

> ⚠️ 7-Zip may **not** work on raw disk images (e.g., Raspberry Pi `.img`)

---

## Method 2: OSFMount — Best for Raw Disk Images
Mounts `.img` as a virtual drive, just like ISO mounting:
1. Download **OSFMount** from [osforensics.com](https://www.osforensics.com/tools/mount-disk-images.html)
2. Open OSFMount → **"Mount New"**
3. Select your `.img` file
4. Choose the **partition** inside the image
5. A drive letter appears in File Explorer — browse freely

---

## Method 3: PowerShell (Windows 10/11)
Works if the `.img` is a standard disk image:
```powershell
# Same as ISO mounting
Mount-DiskImage -ImagePath "C:\path\to\yourfile.img"

# Unmount when done
Dismount-DiskImage -ImagePath "C:\path\to\yourfile.img"
```

---

## Method 4: WSL (Windows Subsystem for Linux)
Great for Linux-based `.img` files (e.g., Raspberry Pi):
```bash
# In WSL terminal
sudo mkdir /mnt/imgfile
sudo mount -o loop yourfile.img /mnt/imgfile
ls /mnt/imgfile
```

---

## Which Tool to Use?

| `.img` Type | Best Tool |
|---|---|
| General archive | 7-Zip |
| Raw disk / Raspberry Pi | OSFMount or WSL |
| Windows disk image | PowerShell `Mount-DiskImage` |
| Android system image | Android SDK tools |

For **Raspberry Pi** or **Linux** `.img` files, **OSFMount** is the most user-friendly option on Windows.
