---
audio: false
generated: true
image: false
lang: en
layout: post
title: ISO File Access Methods for Windows
translated: false
type: note
---

Question: How to extract/inspect an ISO file in Windows?

Answer:

## Method 1: Built-in Mount (Windows 10/11) — Easiest
No software needed:

1. **Right-click** the `.iso` file
2. Click **"Mount"**
3. A virtual drive appears in **File Explorer** (e.g., `D:\`)
4. Browse the contents freely
5. When done, right-click the virtual drive → **"Eject"**

---

## Method 2: 7-Zip — Extract to Folder
1. Download & install **7-Zip** from [7-zip.org](https://www.7-zip.org)
2. Right-click the `.iso` file
3. Hover **"7-Zip"** → click **"Extract Here"** or **"Extract to [folder]"**
4. Done — all files are extracted to a normal folder

---

## Method 3: Command Line (PowerShell)
```powershell
# Mount the ISO
Mount-DiskImage -ImagePath "C:\path\to\yourfile.iso"

# Check which drive letter it got
Get-DiskImage -ImagePath "C:\path\to\yourfile.iso" | Get-Volume

# When done, unmount it
Dismount-DiskImage -ImagePath "C:\path\to\yourfile.iso"
```

---

## Which Method to Choose?

| Method | Best For |
|---|---|
| Built-in Mount | Quick peek, no install needed |
| 7-Zip | Permanently extracting files to disk |
| PowerShell | Automation / scripting |

The **built-in mount** is recommended for most users — it's fast, free, and requires no extra software.
