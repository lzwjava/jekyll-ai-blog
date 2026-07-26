---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix macOS Recovery Server Error
translated: false
type: note
---

Question: **macOS Recovery shows "The recovery server could not be contacted" when reinstalling macOS on MacBook Pro 2017. How to fix?**

Answer:

This error is very common on Intel Macs when using Internet Recovery. It usually means **network / date / Apple server certificate validation**, not a broken SSD.

Try these in order.

---

## 1. Check date/time in Recovery (most common)

Boot into Recovery:

```
Command (⌘) + R
```

Open:

```
Utilities → Terminal
```

Check:

```bash
date
```

If the date is wrong (for example 2020/2010), set it manually.

Example:

```bash
date 072609302026
```

Format:

```
MMDDhhmmyyyy
```

Example above:

```
07/26 09:30 2026
```

Then retry:

```
Reinstall macOS
```

---

## 2. Use Internet Recovery instead of local Recovery

For MacBook Pro 2017:

Power off.

Hold:

```
Option + Command + R
```

Keep holding until globe appears.

This downloads the latest compatible macOS.

Not:

```
Command + R
```

because that may load an old recovery partition.

---

## 3. Try a different network

Recovery is picky.

Avoid:

* company WiFi
* captive portals
* VPN
* filtered networks

Try:

* phone hotspot
* home router 2.4GHz WiFi

---

## 4. If you erased the disk, check GPT/APFS

In Recovery Terminal:

```bash
diskutil list
```

You should see something like:

```
/dev/disk0
   GUID_partition_scheme
   Apple_APFS Container
```

If not:

```bash
diskutil eraseDisk APFS "Macintosh HD" GPT /dev/disk0
```

Then reinstall.

---

## 5. Best method in your case: create macOS USB installer

Since you already have Linux/Ubuntu and can write USBs, this is probably easier.

Download macOS installer from Apple:

Example:

```
Install macOS Monterey.app
```

Create USB:

```bash
sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia \
--volume /Volumes/MyUSB
```

Boot:

```
Option (⌥)
```

Select USB installer.

---

For your situation:

* MacBook Pro 2017
* Ubuntu installed
* Want Windows 10 via Boot Camp

I would do:

```
1. Fix macOS Recovery
        |
        v
2. Install macOS
        |
        v
3. Boot Camp Assistant
        |
        v
4. Windows 10 22H2
```

Do not install Windows directly yet. The Apple firmware + Boot Camp driver path is much easier if macOS is restored first.
