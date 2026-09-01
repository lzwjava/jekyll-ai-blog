---
audio: false
generated: true
image: false
lang: en
layout: post
title: Don't Use Windows Boot Options for USB
translated: false
type: note
---

Question: What is this screen, and how do I get from here to booting the Debian USB?

Answer: This is **Windows 7's Advanced Boot Options**, not the motherboard BIOS/boot menu.

You're currently seeing options like:

* Repair your computer
* Safe Mode
* Enable low-resolution video
* Debugging Mode
* Disable driver signature enforcement
* **Start Windows Normally**

So **don't select anything here**. Press **Esc** to leave this menu.

### Boot Debian from USB

You need the **BIOS/boot-device menu**, which happens *before* Windows starts.

1. Shut the PC down completely.
2. Plug in your Debian USB.
3. Power it on.
4. Immediately repeatedly press:

```text
F12
```

If F12 doesn't work, try:

```text
F11
F2
Delete
```

You should eventually see something more like:

```text
Boot Menu
------------------
Hard Disk
USB HDD
CD/DVD
Network
```

Select:

```text
USB HDD
```

or the name of your USB stick.

### Important distinction

```text
Power ON
   │
   ▼
BIOS / POST
   │
   ├── F12 → Boot device selection  ← YOU WANT THIS
   │
   ▼
Windows Boot Manager
   │
   └── F8 → Advanced Boot Options  ← YOUR CURRENT SCREEN
```

Your photo shows the **F8/Windows bootloader stage**, so you're already too far into the boot process.

If you tell me **what happens when you press F12 immediately after powering on** (or send a photo), I can walk you through the exact next step.
